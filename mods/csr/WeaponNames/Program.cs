using SoulsFormats;
using System.Text;

Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
var names = new Dictionary<string, string> {
    ["Saw Cleaver"] = "Yharnam Can Opener",
    ["Hunter Axe"] = "Eviction Notice",
    ["Threaded Cane"] = "Gentleman’s Disagreement",
};
var replacements = new Dictionary<string, string>();
foreach (var (oldName, newName) in names)
    foreach (var prefix in new[] { "", "Uncanny ", "Lost " })
        for (var level = 0; level <= 10; level++) {
            var suffix = level == 0 ? "" : $" +{level}";
            replacements.Add(prefix + oldName + suffix, prefix + newName + suffix);
        }

byte[] Rename(byte[] bytes) {
    var fmg = FMG.Read(bytes);
    var found = new HashSet<string>();
    foreach (var entry in fmg.Entries)
        if (entry.Text != null && replacements.TryGetValue(entry.Text, out var renamed)) {
            if (!found.Add(entry.Text)) throw new InvalidDataException("Duplicate weapon name.");
            entry.Text = renamed;
        }
    if (found.Count != replacements.Count)
        throw new InvalidDataException($"Expected 99 weapon names; found {found.Count}.");
    var result = fmg.Write();
    var readback = FMG.Read(result);
    if (!readback.Entries.Select(e => (e.ID, e.Text)).SequenceEqual(fmg.Entries.Select(e => (e.ID, e.Text))))
        throw new InvalidDataException("FMG readback changed entries.");
    return result;
}

if (args.SequenceEqual(new[] { "--self-test" })) {
    var fixture = new FMG { Entries = new(), Long = true };
    fixture.Entries.AddRange(replacements.Keys.Select((name, i) => new FMG.Entry(i, name)));
    fixture.Entries.Add(new FMG.Entry(1000, "Threaded Cane +99"));
    fixture.Entries.Add(new FMG.Entry(1001, "A story about the Saw Cleaver."));
    fixture.Entries.Add(new FMG.Entry(1002, null));
    var original = fixture.Entries.Select(e => (e.ID, e.Text)).ToArray();
    var result = FMG.Read(Rename(fixture.Write()));
    foreach (var (entry, before) in result.Entries.Zip(original))
        if (entry.ID != before.ID || entry.Text != (before.Text != null && replacements.TryGetValue(before.Text, out var value) ? value : before.Text))
            throw new Exception("Rename changed an unexpected entry.");
    fixture.Entries.RemoveAt(0);
    try { Rename(fixture.Write()); } catch (InvalidDataException) {
        Console.WriteLine("PASS: 99 variants, Unicode, untouched lore/nulls, missing-name refusal.");
        return;
    }
    throw new Exception("Missing weapon was accepted.");
}
if (args.Length != 2) throw new ArgumentException("Usage: WeaponNames SOURCE OUTPUT | --self-test");
if (File.Exists(args[1])) throw new IOException("Output already exists; refusing to overwrite it.");
var originalBytes = File.ReadAllBytes(args[0]);
var binder = BND4.Read(originalBytes);
var weaponFile = binder.Files.Single(f => f.ID == 11 && f.Name.EndsWith("武器名.fmg"));
weaponFile.Bytes = Rename(weaponFile.Bytes);
var output = binder.Write();
var checkedBinder = BND4.Read(output);
if (checkedBinder.Compression != binder.Compression || checkedBinder.Files.Count != binder.Files.Count)
    throw new InvalidDataException("Binder structure changed.");
foreach (var (expected, actual) in binder.Files.Zip(checkedBinder.Files))
    if (expected.ID != actual.ID || expected.Name != actual.Name || expected.Flags != actual.Flags || !expected.Bytes.SequenceEqual(actual.Bytes))
        throw new InvalidDataException("Binder readback changed a file.");
if (!originalBytes.SequenceEqual(File.ReadAllBytes(args[0]))) throw new IOException("Source changed during build.");
Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(args[1]))!);
using (var stream = new FileStream(args[1], FileMode.CreateNew, FileAccess.Write)) stream.Write(output);
Console.WriteLine($"Verified 99 weapon renames: {args[1]}");
