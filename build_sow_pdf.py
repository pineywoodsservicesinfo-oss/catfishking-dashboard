#!/usr/bin/env python3
"""Convert SOW markdown to a styled board-ready PDF."""
import sys
import re
from pathlib import Path
import markdown
from weasyprint import HTML, CSS

SRC = Path("/home/testydiagram/catfishking/SOW_Catfish_King_FINAL.md")
DST = Path("/home/testydiagram/catfishking/SOW_Catfish_King_FINAL.pdf")

# Read source
md_text = SRC.read_text(encoding="utf-8")

# Convert markdown to HTML
md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"])
body_html = md.convert(md_text)

# Extract title for cover banner
title_match = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
title = title_match.group(1) if title_match else "Statement of Work"

CSS_STYLES = """
@page {
  size: Letter;
  margin: 0.7in 0.8in;
  @top-right {
    content: "SOW v3.1 · Catfish King · 2026";
    font-family: -apple-system, sans-serif;
    font-size: 8pt;
    color: #a0aec0;
  }
  @bottom-center {
    content: "Page " counter(page) " of " counter(pages);
    font-family: -apple-system, sans-serif;
    font-size: 8pt;
    color: #a0aec0;
  }
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #1a202c;
  line-height: 1.55;
  font-size: 10pt;
  background: white;
}
h1 {
  font-size: 22pt;
  color: #c05621;
  font-weight: 800;
  margin: 0 0 4px 0;
  border-bottom: 3px solid #c05621;
  padding-bottom: 8px;
}
h2 {
  font-size: 13pt;
  color: #2d3748;
  margin: 18px 0 6px 0;
  font-weight: 700;
  border-left: 4px solid #c05621;
  padding-left: 8px;
  page-break-after: avoid;
}
h3 {
  font-size: 11pt;
  color: #2d3748;
  margin: 12px 0 4px 0;
  font-weight: 600;
  page-break-after: avoid;
}
h4 {
  font-size: 10pt;
  color: #4a5568;
  margin: 10px 0 4px 0;
  font-weight: 600;
}
p { margin: 6px 0; }
ul, ol { margin: 6px 0 6px 24px; }
li { margin: 3px 0; }
strong { color: #2d3748; }
em { color: #4a5568; }
code {
  font-family: "SF Mono", Monaco, Consolas, monospace;
  background: #f7fafc;
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 9pt;
  color: #c05621;
}
pre {
  background: #2d3748;
  color: #e2e8f0;
  padding: 10px 12px;
  border-radius: 4px;
  font-size: 9pt;
  margin: 8px 0;
  white-space: pre-wrap;
}
pre code { background: transparent; color: inherit; padding: 0; }
table {
  width: 100%;
  border-collapse: collapse;
  margin: 8px 0 12px 0;
  font-size: 9pt;
  page-break-inside: avoid;
}
th, td {
  padding: 5px 8px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: top;
}
th {
  background: #2d3748;
  color: white;
  font-weight: 600;
}
tr:nth-child(even) td { background: #f7fafc; }
blockquote {
  border-left: 4px solid #c05621;
  background: #fff5f0;
  padding: 8px 12px;
  margin: 8px 0;
  font-style: italic;
  color: #4a5568;
}
hr {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 16px 0;
}
.cover-meta {
  font-size: 9pt;
  color: #718096;
  margin: 6px 0 16px 0;
}
.cover-meta strong { color: #2d3748; }
"""

HTML_DOC = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>{CSS_STYLES}</style>
</head>
<body>
<div class="cover-meta"><strong>Document:</strong> Statement of Work v3.1 · <strong>Effective:</strong> July 6, 2026 · <strong>Status:</strong> Ready for execution</div>
{body_html}
</body>
</html>"""

# Write temp HTML then render
tmp_html = Path("/tmp/sow_render.html")
tmp_html.write_text(HTML_DOC, encoding="utf-8")
HTML(string=HTML_DOC).write_pdf(DST)

print(f"✓ Generated: {DST}")
print(f"  Size: {DST.stat().st_size:,} bytes")
print(f"  Pages: see PDF metadata")
