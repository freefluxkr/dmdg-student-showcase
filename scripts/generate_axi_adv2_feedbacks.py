# -*- coding: utf-8 -*-
"""
Generate & verify 5 4-page A4 practitioner audit PDFs:
  - Updated Track 7: axi2_final_01_SafePredict3D_신상아_피드백.pdf
  - New Track 8: axi2_imp_01..04 (4 teams improvement plans)
Also syncs clean copies to backups/pdf_originals_20261125/showcase_generated_feedbacks.
"""
import os
import sys
import shutil
import pymupdf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SHOWCASE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
OUT_DIR = os.path.join(SHOWCASE_ROOT, "generated_feedbacks")
HTML_TMP_DIR = os.path.join(OUT_DIR, "_html_tmp")
BACKUP_FB_DIR = r"c:\DMDG_Jobs\backups\pdf_originals_20261125\showcase_generated_feedbacks"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(HTML_TMP_DIR, exist_ok=True)

sys.path.insert(0, SCRIPT_DIR)

from feedback_gen.pdf_builder import render_pdf
from feedback_gen.renderer import render_4page_report
from feedback_gen.data_axi_adv2_final import AXI_ADV2_FINAL_PLANS
from feedback_gen.data_axi_adv2_improved import AXI_ADV2_IMPROVED_PLANS


def main():
    plans = [AXI_ADV2_FINAL_PLANS[0]] + AXI_ADV2_IMPROVED_PLANS
    print(f"Generating {len(plans)} 4-page A4 practitioner feedback PDFs...", flush=True)
    failures = []
    for idx, plan in enumerate(plans, 1):
        pdf_path = os.path.join(OUT_DIR, plan["out_pdf"])
        html_path = os.path.join(HTML_TMP_DIR, f"{plan['out_pdf']}.html")
        html_str = render_4page_report(plan)
        n_pages = render_pdf(html_str, html_path, pdf_path)

        doc = pymupdf.open(pdf_path)
        p4_txt = doc[3].get_text("text") if len(doc) >= 4 else ""
        has_footer_p4 = "Page 4 of 4" in p4_txt
        doc.close()

        sz_kb = os.path.getsize(pdf_path) / 1024
        status = "OK" if (n_pages == 4 and has_footer_p4) else f"WARN({n_pages}p,p4={has_footer_p4})"
        print(f"[{idx}/{len(plans)}] {status} | {n_pages}p | {sz_kb:5.1f} KB | {plan['out_pdf']}", flush=True)
        if n_pages != 4 or not has_footer_p4:
            failures.append((plan["out_pdf"], n_pages, has_footer_p4))
        elif os.path.isdir(BACKUP_FB_DIR):
            shutil.copy2(pdf_path, os.path.join(BACKUP_FB_DIR, plan["out_pdf"]))

    if failures:
        print(f"ERROR: Page verification failed: {failures}", file=sys.stderr)
        sys.exit(1)
    print("ALL 5 PRACTITIONER AUDIT PDFs VERIFIED == 4 PAGES & BACKED UP!")


if __name__ == "__main__":
    main()
