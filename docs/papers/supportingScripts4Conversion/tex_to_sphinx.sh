#!/usr/bin/env bash
# =============================================================================
# tex_to_sphinx.sh
# Convert a LaTeX paper (elsarticle or similar) to Sphinx-ready Markdown
#
# Usage:
#   bash tex_to_sphinx.sh paper.tex bibliography.bib
#
# Output:
#   paper.md  (ready to drop into docs/papers/)
#
# Requirements:
#   - pandoc       (brew install pandoc  /  apt install pandoc)
#   - python3      (standard on Mac/Linux)
# =============================================================================

set -e  # exit on any error

# ---------- arguments --------------------------------------------------------
TEX_FILE="$1"
BIB_FILE="$2"

if [[ -z "$TEX_FILE" || -z "$BIB_FILE" ]]; then
    echo "Usage: bash tex_to_sphinx.sh <paper.tex> <bibliography.bib>"
    exit 1
fi

if [[ ! -f "$TEX_FILE" ]]; then
    echo "Error: cannot find $TEX_FILE"
    exit 1
fi

if [[ ! -f "$BIB_FILE" ]]; then
    echo "Error: cannot find $BIB_FILE"
    exit 1
fi

# Derive output filename from input (replace .tex with .md)
BASENAME="${TEX_FILE%.tex}"
RAW_MD="${BASENAME}_raw.md"
OUT_MD="${BASENAME}.md"

echo "Input:  $TEX_FILE"
echo "Bib:    $BIB_FILE"
echo "Output: $OUT_MD"
echo ""

# ---------- step 1: pandoc conversion ----------------------------------------
# Key flags:
#   --from=latex               read LaTeX
#   --to=markdown+tex_math_dollars  keep $...$ and $$...$$ math (MyST understands these)
#   --wrap=none                don't hard-wrap lines (cleaner diffs in git)
#   --bibliography             point to your .bib file
#   NO --citeproc              keep citations as [@key] for sphinxcontrib-bibtex
#                              (--citeproc would expand them into inline text)

echo "Step 1: running pandoc..."
pandoc "$TEX_FILE" \
    --from=latex \
    --to=markdown+tex_math_dollars \
    --wrap=none \
    --bibliography="$BIB_FILE" \
    -o "$RAW_MD"

echo "        done -> $RAW_MD"
echo ""

# ---------- step 2: python cleanup -------------------------------------------
echo "Step 2: cleaning up for Sphinx/MyST..."

python3 << PYEOF
import re, sys

with open("$RAW_MD", "r") as f:
    text = f.read()

# -- 2a. Strip YAML frontmatter block (--- ... ---) ---------------------------
text = re.sub(r'^---\n.*?^---\n', '', text, flags=re.DOTALL | re.MULTILINE)

# -- 2b. Remove elsarticle-specific div blocks --------------------------------
#    pandoc converts \begin{graphicalabstract}, \begin{highlights},
#    \begin{frontmatter}, \begin{keyword} into ::: divs — useless in Sphinx
for env in ['frontmatter', 'graphicalabstract', 'highlights', 'keyword']:
    text = re.sub(
        r':::\s*' + env + r'\n.*?:::\n?',
        '',
        text,
        flags=re.DOTALL
    )
# Catch any leftover bare ::: lines
text = re.sub(r'^:::\s*\w*\s*$', '', text, flags=re.MULTILINE)

# -- 2c. Fix pandoc figure cross-reference noise ------------------------------
#    LaTeX \ref{fig:label} becomes [N](#fig:label){reference-type="ref" reference="fig:label"}
#    Simplify to just the label so you can fix them manually or use MyST targets
text = re.sub(
    r'\[(\d+)\]\(#([\w:]+)\)\{reference-type="ref"\s+reference="[\w:]+"\}',
    r'\\ref{\2}',
    text
)
# Also clean any remaining {reference-type...} attributes
text = re.sub(r'\{reference-type="[^"]+"\s+reference="[^"]+"\}', '', text)

# -- 2d. Remove HTML comment artifacts from pandoc ----------------------------
#    e.g.  $\sim$`<!-- -->`{=html}0.5 m  →  $\sim$0.5 m
text = re.sub(r'`<!-- -->`\{=html\}', '', text)

# -- 2e. Clean up image width attributes pandoc can't translate ---------------
#    ![caption](file.png){width="\\textwidth"}  →  ![caption](file.png)
text = re.sub(r'\{width="\\\\textwidth"\}', '', text)

# -- 2f. Tidy whitespace ------------------------------------------------------
text = re.sub(r'  +', ' ', text)       # multiple spaces → single
text = re.sub(r'\n{3,}', '\n\n', text) # 3+ blank lines → 2

# -- 2g. Prepend a note about figures -----------------------------------------
figure_note = """\
<!--
NOTE FOR SPHINX:
  - Copy your figures folder into docs/papers/figures/
  - Replace image paths like ./Figures_v2/Fig01.png
    with the relative path:   figures/Fig01.png
  - Figure cross-references show as \\ref{fig:label} — replace with
    a MyST figure target:
        ```{figure} figures/Fig01.png
        :name: fig-map
        Caption text here.
        ```
    and reference it in text as {numref}\`fig-map\`
-->

"""
text = figure_note + text.lstrip()

with open("$OUT_MD", "w") as f:
    f.write(text)

# Report
sections = re.findall(r'^#+ .+', text, re.MULTILINE)
print(f"  Sections/headings: {len(sections)}")
for s in sections:
    print(f"    {s}")
remaining_refs = re.findall(r'\\\\ref\{', text)
print(f"  Figure refs still to fix manually: {len(remaining_refs)}")
print(f"  Output size: {len(text)} chars")
PYEOF

echo ""
echo "Step 3: removing temporary raw file..."
rm "$RAW_MD"

echo ""
echo "Done!  ->  $OUT_MD"
echo ""
echo "Next steps:"
echo "  1. Copy $OUT_MD to docs/papers/"
echo "  2. Copy your figures folder to docs/papers/figures/"
echo "  3. Fix image paths and figure cross-references (see note at top of file)"
echo "  4. Add the filename (without .md) to docs/papers/index.rst"
