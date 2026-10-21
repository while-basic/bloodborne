"""Add a CSR text label while preserving every original GFX tag byte-for-byte."""
import argparse
import copy
import struct
import subprocess
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

LABEL = "CSR · Celaya Solutions"
CHARACTER = 65000


def tags(data):
    if len(data) < 14 or data[:4] != b"GFX\x0b" or struct.unpack_from("<I", data, 4)[0] != len(data):
        raise ValueError("Expected an uncompressed Bloodborne GFX v11 file.")
    offset = 8 + (5 + (data[8] >> 3) * 4 + 7) // 8 + 4
    result = []
    while offset < len(data):
        start = offset
        if offset + 2 > len(data):
            raise ValueError("Truncated tag header.")
        header, = struct.unpack_from("<H", data, offset)
        offset += 2
        size = header & 63
        if size == 63:
            if offset + 4 > len(data):
                raise ValueError("Truncated long tag header.")
            size, = struct.unpack_from("<I", data, offset)
            offset += 4
        end = offset + size
        if end > len(data):
            raise ValueError("Tag exceeds file size.")
        result.append((header >> 6, start, offset, end))
        offset = end
    if not result or result[-1][0] != 0:
        raise ValueError("Missing final End tag.")
    return result


def brand(source, output, ffdec):
    if output.exists():
        raise FileExistsError(output)
    original = source.read_bytes()
    original_tags = tags(original)
    command = ["java", "-Djava.awt.headless=true", "-jar", str(ffdec)]
    with tempfile.TemporaryDirectory() as folder:
        xml = Path(folder) / "menu.xml"
        encoded = Path(folder) / "encoded.gfx"
        subprocess.run(command + ["-swf2xml", str(source), str(xml)], check=True)
        tree = ET.parse(xml)
        root = tree.getroot()
        if root.find("displayRect").get("Xmax") != "38400" or root.find("displayRect").get("Ymax") != "21600":
            raise ValueError("Expected the 1920 by 1080 loading screen.")
        if any(str(CHARACTER) in node.attrib.values() for node in root.iter()):
            raise ValueError("Reserved label character is already in use.")
        timeline = root.find("tags")
        template = next(node for node in root.iter("item") if node.get("type") == "DefineEditTextTag")
        text = copy.deepcopy(template)
        text.attrib.update(characterID=str(CHARACTER), fontHeight="520", align="1", leading="0",
                           multiline="false", wordWrap="false", noSelect="true", variableName="",
                           initialText='<p align="right"><font size="26" color="#a0a08c">' + LABEL + '</font></p>')
        text.find("bounds").attrib.update(Xmin="0", Ymin="0", Xmax="11200", Ymax="1000", nbits="15")
        text.find("textColor").attrib.update(red="160", green="160", blue="140", alpha="255")
        placement = copy.deepcopy(next(node for node in timeline
                                       if node.get("type") == "PlaceObject2Tag" and node.get("placeFlagMove") == "false"))
        depth = max(int(node.get(key, "0")) for node in timeline for key in ("depth", "clipDepth")) + 1
        placement.attrib.update(characterId=str(CHARACTER), depth=str(depth), placeFlagHasName="false",
                               placeFlagHasColorTransform="false", placeFlagHasClipDepth="false",
                               placeFlagHasClipActions="false", placeFlagHasRatio="false")
        for child in list(placement):
            placement.remove(child)
        ET.SubElement(placement, "matrix", type="MATRIX", hasRotate="false", hasScale="false",
                      nRotateBits="0", nScaleBits="0", nTranslateBits="17", translateX="25920", translateY="20160")
        first_frame = next(i for i, node in enumerate(timeline) if node.get("type") == "ShowFrameTag")
        timeline.insert(first_frame, text)
        timeline.insert(first_frame + 1, placement)
        tree.write(xml, encoding="utf-8", xml_declaration=True)
        subprocess.run(command + ["-xml2swf", str(xml), str(encoded)], check=True)
        candidate = encoded.read_bytes()
        additions = []
        for kind, start, body, end in tags(candidate):
            if kind == 37 and struct.unpack_from("<H", candidate, body)[0] == CHARACTER:
                additions.append(candidate[start:end])
            if kind == 26 and candidate[body] & 2 and struct.unpack_from("<H", candidate, body + 3)[0] == CHARACTER:
                additions.append(candidate[start:end])
        if len(additions) != 2:
            raise ValueError("Expected exactly one text tag and one placement.")
        insertion = next(start for kind, start, _, _ in original_tags if kind == 1)
        # FFDec normalizes some existing shapes; take only its two new tags.
        result = bytearray(original[:insertion] + b"".join(additions) + original[insertion:])
        struct.pack_into("<I", result, 4, len(result))
        readback = tags(result)
        untouched = [bytes(result[start:end]) for _, start, _, end in readback
                     if not insertion <= start < insertion + sum(map(len, additions))]
        if untouched != [original[start:end] for _, start, _, end in original_tags]:
            raise ValueError("An original menu tag changed.")
        encoded.write_bytes(result)
        subprocess.run(command + ["-swf2xml", str(encoded), str(xml)], check=True)
        verified = ET.parse(xml).getroot()
        labels = [n for n in verified.iter("item") if n.get("type") == "DefineEditTextTag" and n.get("characterID") == str(CHARACTER)]
        if len(labels) != 1 or labels[0].get("initialText") != text.get("initialText"):
            raise ValueError("Branding failed readback.")
        if source.read_bytes() != original:
            raise ValueError("Source changed during build.")
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as stream:
            stream.write(result)
    print(f"Verified CSR label; all {len(original_tags)} original tags preserved: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("ffdec", type=Path)
    args = parser.parse_args()
    brand(args.source, args.output, args.ffdec)
