#!/bin/bash
# install_cbd_tools.sh — Communicate by Design
# Run this once to set up the CBD build tools on your Mac.
# Usage: bash ~/Library/Mobile\ Documents/com~apple~CloudDocs/Communicate\ by\ Design/_Operations/Build/install_cbd_tools.sh

set -e

CBD_ROOT="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Communicate by Design"
SCRIPT="$CBD_ROOT/_Operations/Build/export_docx_to_pdf.py"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Communicate by Design — Tool Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Install docx2pdf
echo "→ Installing docx2pdf..."
pip3 install docx2pdf --quiet 2>/dev/null || pip3 install docx2pdf --user --quiet
echo "  ✓ docx2pdf installed"
echo ""

# 2. Create a short alias command: cbd-pdf
# Writes a tiny wrapper script to /usr/local/bin/cbd-pdf
echo "→ Installing cbd-pdf command..."
cat > /tmp/cbd-pdf-wrapper.sh << 'WRAPPER'
#!/bin/bash
CBD_SCRIPT="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Communicate by Design/_Operations/Build/export_docx_to_pdf.py"
python3 "$CBD_SCRIPT" "$@"
WRAPPER

chmod +x /tmp/cbd-pdf-wrapper.sh

# Try /usr/local/bin first, fall back to ~/bin
if [ -w "/usr/local/bin" ]; then
    cp /tmp/cbd-pdf-wrapper.sh /usr/local/bin/cbd-pdf
    echo "  ✓ Installed to /usr/local/bin/cbd-pdf"
else
    mkdir -p "$HOME/bin"
    cp /tmp/cbd-pdf-wrapper.sh "$HOME/bin/cbd-pdf"
    echo "  ✓ Installed to ~/bin/cbd-pdf"
    # Add ~/bin to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
        echo ""
        echo "  ⚠️  Add this line to your ~/.zshrc or ~/.bash_profile:"
        echo '     export PATH="$HOME/bin:$PATH"'
        echo "  Then run: source ~/.zshrc"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Done! You can now run:"
echo ""
echo "  cbd-pdf --product-line poetry"
echo "  cbd-pdf --product-line nonfiction"
echo "  cbd-pdf --product-line fiction"
echo "  cbd-pdf path/to/Unit_COMPLETE.docx"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
