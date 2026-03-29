"""
fix_border_order.py
Post-process a .docx file to fix w:pBdr child element order.
OOXML schema requires: top → left → bottom → right
docx-js library outputs: top → bottom → left → right

Usage: python3 fix_border_order.py <input.docx> [output.docx]
If output is omitted, overwrites input.
"""
import zipfile, shutil, sys, os, re

CORRECT_ORDER = ["top", "left", "bottom", "right", "between", "bar"]

def fix_pbdr_order(xml_bytes):
    """Reorder w:pBdr children to match OOXML schema order."""
    xml = xml_bytes.decode("utf-8")

    def reorder_pbdr(m):
        pbdr_inner = m.group(1)
        # Extract all child elements with their full tags
        elements = re.findall(r'<w:(top|bottom|left|right|between|bar)[^/]*/>', pbdr_inner)
        # Build ordered output
        found = {}
        for tag in elements:
            pat = r'(<w:' + tag + r'[^/]*/>)'
            hit = re.search(pat, pbdr_inner)
            if hit:
                found[tag] = hit.group(1)
        ordered = [found[t] for t in CORRECT_ORDER if t in found]
        return "<w:pBdr>" + "".join(ordered) + "</w:pBdr>"

    # Match <w:pBdr>...</w:pBdr> blocks (non-greedy, no nesting expected)
    fixed = re.sub(r"<w:pBdr>(.*?)</w:pBdr>", reorder_pbdr, xml, flags=re.DOTALL)
    return fixed.encode("utf-8")

def process(input_path, output_path=None):
    if output_path is None:
        output_path = input_path

    tmp = input_path + ".tmp"
    with zipfile.ZipFile(input_path, "r") as zin:
        with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = fix_pbdr_order(data)
                zout.writestr(item, data)

    if output_path == input_path:
        os.replace(tmp, input_path)
    else:
        shutil.move(tmp, output_path)
    print(f"Fixed: {output_path}")

if __name__ == "__main__":
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    process(inp, out)
