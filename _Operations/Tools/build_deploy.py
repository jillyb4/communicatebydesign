#!/usr/bin/env python3
"""
Build the hosted copy of the Symbol Card Sheet Generator.

The tool itself is the single source of truth. This generates a deploy folder
from it rather than keeping a second copy, so the two cannot drift.

    python3 _Operations/Tools/build_deploy.py

Output: _Operations/Tools/deploy/  (gitignored — regenerate, never edit)
    index.html            the tool + the meta iOS needs for a Home Screen app
    manifest.webmanifest  } from deploy_assets/, tracked in git
    icon-*.png            }

Then host that folder. Add to Home Screen gives a full-screen app, which is
what Guided Access needs to lock onto.
"""
import shutil
from pathlib import Path

HERE   = Path(__file__).resolve().parent
SRC    = HERE / "cbd-pecs-sheet-generator.html"
ASSETS = HERE / "deploy_assets"
OUT    = HERE / "deploy"

HEAD = """<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Symbol Cards">
<meta name="theme-color" content="#1B1F3B">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
"""

def main() -> None:
    html = SRC.read_text()

    if '<link rel="manifest"' in html:
        raise SystemExit("source already carries deploy meta — did someone edit the wrong file?")
    html = html.replace("<title>", HEAD + "<title>", 1)

    # A hosted copy has no symbol cache beside it. Left pointing at the relative
    # path it 404s on every lookup before falling through to ARASAAC, which is
    # slow and fills the console with noise.
    html = html.replace(
        "const LOCAL_CACHE = '../Symbols/symbol_cache/';",
        "const LOCAL_CACHE = null;   // hosted copy: no cache folder beside it")
    html = html.replace(
        """function probeLocal(term) {
  return new Promise(resolve => {
    const url = LOCAL_CACHE + 'arasaac_' + slug(term) + '.png';""",
        """function probeLocal(term) {
  return new Promise(resolve => {
    if (!LOCAL_CACHE) return resolve(null);
    const url = LOCAL_CACHE + 'arasaac_' + slug(term) + '.png';""")

    if "LOCAL_CACHE = null" not in html or "if (!LOCAL_CACHE)" not in html:
        raise SystemExit("cache-disable patch did not apply — the source has changed shape")

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(html)
    for f in sorted(ASSETS.iterdir()):
        if f.is_file():
            shutil.copy2(f, OUT / f.name)

    print(f"built {OUT}")
    for f in sorted(OUT.iterdir()):
        print(f"  {f.name:24s} {f.stat().st_size:>7,} bytes")

if __name__ == "__main__":
    main()
