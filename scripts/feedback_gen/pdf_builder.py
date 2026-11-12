# -*- coding: utf-8 -*-
import os
import subprocess
import html
import pymupdf

CHROME_BIN = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_BIN = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BROWSER = CHROME_BIN if os.path.exists(CHROME_BIN) else EDGE_BIN

CSS_TEMPLATE = """
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');

@page {
  size: A4 portrait;
  margin: 0;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Malgun Gothic', sans-serif;
  color: #1e293b;
  background: #ffffff;
  font-size: 8.6pt;
  line-height: 1.48;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page {
  width: 210mm;
  height: 296.5mm;
  padding: 12mm 14.5mm 15mm 14.5mm;
  position: relative;
  page-break-after: always;
  background: #ffffff;
  overflow: hidden;
}

.page:last-child {
  page-break-after: auto;
}

/* Header Banner */
.hero-banner {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 65%, #0f2942 100%);
  color: #ffffff;
  border-radius: 10px;
  padding: 15px 20px 14px 20px;
  margin-bottom: 12px;
  border-bottom: 3px solid #3b82f6;
}

.hero-tag {
  display: inline-block;
  font-size: 7pt;
  font-weight: 700;
  letter-spacing: 0.9px;
  color: #93c5fd;
  background: rgba(59, 130, 246, 0.18);
  border: 1px solid rgba(96, 165, 250, 0.4);
  padding: 2px 8px;
  border-radius: 12px;
  margin-bottom: 7px;
  text-transform: uppercase;
}

.hero-title {
  font-size: 16.5pt;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.4px;
  line-height: 1.25;
  margin-bottom: 4px;
}

.hero-subtitle {
  font-size: 8.8pt;
  color: #cbd5e1;
  font-weight: 400;
  margin-bottom: 10px;
}

.hero-meta-grid {
  display: grid;
  grid-template-columns: 1.15fr 1.25fr 0.85fr 1.1fr;
  gap: 10px;
  padding-top: 9px;
  border-top: 1px solid rgba(255, 255, 255, 0.14);
}

.meta-label {
  font-size: 6.8pt;
  color: #94a3b8;
  margin-bottom: 2px;
}

.meta-value {
  font-size: 8pt;
  font-weight: 600;
  color: #f8fafc;
  line-height: 1.3;
}

/* Score Row */
.score-row {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: 12px;
  margin-bottom: 14px;
}

.score-card-dark {
  background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%);
  border-radius: 10px;
  padding: 12px 10px;
  text-align: center;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.grade-pill {
  display: inline-block;
  font-size: 7.5pt;
  font-weight: 800;
  padding: 2px 10px;
  border-radius: 12px;
  margin-bottom: 4px;
  letter-spacing: 0.4px;
}

.grade-aplus { background: #059669; color: #ffffff; }
.grade-a { background: #10b981; color: #ffffff; }
.grade-aminus { background: #0ea5e9; color: #ffffff; }
.grade-bplus { background: #3b82f6; color: #ffffff; }
.grade-b { background: #f59e0b; color: #ffffff; }
.grade-cplus { background: #ef4444; color: #ffffff; }

.score-number {
  font-size: 29pt;
  font-weight: 900;
  line-height: 1.05;
  color: #38bdf8;
  margin: 2px 0;
}

.score-denom {
  font-size: 7pt;
  color: #94a3b8;
  letter-spacing: 0.7px;
  font-weight: 600;
}

.score-breakdown {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 9px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.sb-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 3.5px 0;
  border-bottom: 1px dashed #e2e8f0;
  font-size: 8.2pt;
}

.sb-row:last-child {
  border-bottom: none;
}

.sb-label {
  color: #334155;
  font-weight: 500;
}

.sb-val {
  color: #0f172a;
  font-weight: 800;
}

/* Section Title */
.sec-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-left: 4px solid #3b82f6;
  padding-left: 9px;
  margin-top: 2px;
  margin-bottom: 10px;
}

.sec-title {
  font-size: 11.5pt;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.2px;
}

.sec-badge {
  font-size: 7.4pt;
  font-weight: 700;
  color: #1d4ed8;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  padding: 2px 9px;
  border-radius: 12px;
}

/* Callout Boxes */
.callout {
  border-radius: 7px;
  padding: 9px 12px;
  margin-bottom: 9px;
}

.callout-green {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-left: 4px solid #22c55e;
}

.callout-red {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-left: 4px solid #ef4444;
}

.callout-amber {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-left: 4px solid #f59e0b;
}

.callout-indigo {
  background: #f5f3ff;
  border: 1px solid #ddd6fe;
  border-left: 4px solid #6366f1;
}

.callout-slate {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #475569;
}

.callout-title {
  font-size: 8.8pt;
  font-weight: 800;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.callout-green .callout-title { color: #15803d; }
.callout-red .callout-title { color: #b91c1c; }
.callout-amber .callout-title { color: #b45309; }
.callout-indigo .callout-title { color: #4338ca; }
.callout-slate .callout-title { color: #1e293b; }

.callout-body {
  font-size: 8.1pt;
  color: #334155;
  line-height: 1.48;
}

/* Tables */
table.audit-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 6px;
  margin-bottom: 10px;
  font-size: 7.9pt;
}

table.audit-table th {
  background: #f1f5f9;
  color: #334155;
  font-weight: 700;
  text-align: left;
  padding: 6px 8px;
  border-top: 1px solid #cbd5e1;
  border-bottom: 1.5px solid #94a3b8;
}

table.audit-table td {
  padding: 5.5px 8px;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: middle;
  color: #1e293b;
  line-height: 1.4;
}

table.audit-table tr:nth-child(even) td {
  background: #fafbfc;
}

.status-pill {
  display: inline-block;
  font-size: 7pt;
  font-weight: 700;
  padding: 1.5px 7px;
  border-radius: 10px;
  white-space: nowrap;
}

.pill-green { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
.pill-red { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
.pill-blue { background: #dbeafe; color: #1d4ed8; border: 1px solid #93c5fd; }
.pill-amber { background: #fef3c7; color: #b45309; border: 1px solid #fcd34d; }
.pill-slate { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }

/* Detail Cards (Page 2 / 3) */
.item-block {
  margin-bottom: 11px;
}

.item-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.item-title {
  font-size: 9.6pt;
  font-weight: 800;
  color: #0f172a;
}

.item-sub {
  font-size: 8pt;
  color: #475569;
  margin-bottom: 7px;
}

.card-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 9px 12px;
  margin-bottom: 8px;
}

.card-box-tint {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 9px 12px;
  margin-bottom: 8px;
}

.bullet-list {
  padding-left: 14px;
  margin: 0;
}

.bullet-list li {
  margin-bottom: 3.5px;
  font-size: 8pt;
  color: #334155;
  line-height: 1.45;
}

.bullet-list li strong {
  color: #0f172a;
}

.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

/* Code / Solution Box */
.code-card {
  margin-bottom: 9px;
}

.code-label {
  font-size: 8.6pt;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 4px;
}

pre.fix-code {
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 6px;
  padding: 8px 11px;
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 7.4pt;
  line-height: 1.42;
  white-space: pre-wrap;
  word-break: break-word;
  border-left: 3px solid #38bdf8;
}

/* Strategy 2x2 Grid (Page 4) */
.strategy-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 9px;
  margin-bottom: 11px;
}

.strategy-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 9px 11px;
}

.strategy-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
  gap: 6px;
}

.strategy-title {
  font-size: 8.8pt;
  font-weight: 800;
  color: #0f172a;
}

.strategy-body {
  font-size: 7.8pt;
  color: #475569;
  line-height: 1.44;
}

/* Critic Card (Marcus Vance / Victor Choi) */
.critic-intro {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #1e293b;
  border-radius: 6px;
  padding: 7px 11px;
  font-size: 8.2pt;
  font-style: italic;
  color: #334155;
  margin-bottom: 9px;
}

.critic-point {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 9px 12px;
  margin-bottom: 9px;
}

.critic-point-title {
  font-size: 9pt;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Action Plan Box */
.action-card {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-left: 4px solid #0284c7;
  border-radius: 7px;
  padding: 8px 11px;
  margin-bottom: 8px;
}

.action-title {
  font-size: 8.7pt;
  font-weight: 800;
  color: #0369a1;
  margin-bottom: 3px;
}

.action-desc {
  font-size: 8pt;
  color: #1e293b;
  line-height: 1.45;
}

/* Certification Footer Box */
.cert-box {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 9px 14px;
  text-align: center;
  margin-top: 8px;
}

.cert-org {
  font-size: 9pt;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 3px;
}

.cert-desc {
  font-size: 7.5pt;
  color: #64748b;
  line-height: 1.4;
}

/* Page Footer */
.page-footer {
  position: absolute;
  bottom: 8mm;
  left: 14.5mm;
  right: 14.5mm;
  border-top: 1px solid #e2e8f0;
  padding-top: 5px;
  display: flex;
  justify-content: space-between;
  font-size: 7.2pt;
  color: #94a3b8;
}
"""

def grade_pill_class(grade_str: str) -> str:
    g = grade_str.upper()
    if "A+" in g: return "grade-aplus"
    if "(A)" in g or g == "A": return "grade-a"
    if "A-" in g: return "grade-aminus"
    if "B+" in g: return "grade-bplus"
    if "(B)" in g or g == "B": return "grade-b"
    return "grade-cplus"

def esc(s) -> str:
    return html.escape(str(s))

def render_pdf(html_str: str, html_path: str, pdf_path: str) -> int:
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_str)

    cmd = [
        BROWSER,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--virtual-time-budget=5000",
        f"--print-to-pdf={pdf_path}",
        html_path,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    doc = pymupdf.open(pdf_path)
    n_pages = len(doc)
    doc.close()
    return n_pages
