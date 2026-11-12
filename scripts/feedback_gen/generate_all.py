# -*- coding: utf-8 -*-
"""
Batch-generate all 46 expansion 4-page A4 Technical Audit PDF reports into:
  ../generated_feedbacks/<out_pdf>
Verifies page count == 4 for every single generated PDF.
"""
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SHOWCASE_SCRIPTS = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SHOWCASE_ROOT = os.path.abspath(os.path.join(SHOWCASE_SCRIPTS, ".."))
OUT_DIR = os.path.join(SHOWCASE_ROOT, "generated_feedbacks")
HTML_TMP_DIR = os.path.join(OUT_DIR, "_html_tmp")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(HTML_TMP_DIR, exist_ok=True)

sys.path.insert(0, SHOWCASE_SCRIPTS)

from feedback_gen.pdf_builder import render_pdf
from feedback_gen.renderer import render_4page_report
from feedback_gen.data_adv import ADV_PLANS
from feedback_gen.data_axi_kdt import AXI_KDT_PLANS
from feedback_gen.data_lg import LG_PLANS


def main():
    all_plans = ADV_PLANS + AXI_KDT_PLANS + LG_PLANS
    print(f"Generating {len(all_plans)} 4-page A4 feedback PDFs into {OUT_DIR} ...", flush=True)
    failures = []
    for idx, plan in enumerate(all_plans, 1):
        pdf_path = os.path.join(OUT_DIR, plan["out_pdf"])
        html_path = os.path.join(HTML_TMP_DIR, f"{plan['out_pdf']}.html")
        html_str = render_4page_report(plan)
        n_pages = render_pdf(html_str, html_path, pdf_path)
        sz_kb = os.path.getsize(pdf_path) / 1024
        status = "OK" if n_pages == 4 else f"WARN({n_pages}p)"
        print(f"[{idx:02d}/{len(all_plans)}] {status} | {n_pages}p | {sz_kb:5.1f} KB | {plan['out_pdf']}", flush=True)
        if n_pages != 4:
            failures.append((plan["out_pdf"], n_pages))

    if failures:
        print(f"ERROR: Some PDFs did not match 4 pages: {failures}", file=sys.stderr)
        sys.exit(1)
    print(f"ALL {len(all_plans)} FEEDBACK PDFs GENERATED & VERIFIED == 4 PAGES!")


if __name__ == "__main__":
    main()

