# -*- coding: utf-8 -*-
"""
Rebuilds all 6 remaining Shin Sang-ah-involved practitioner audit PDFs, verifies
every single PDF == 4 pages with Page 1..4 of 4 and cert footer, updates
site/assets/files/... and site/data/manifest.json, syncs clean backups, and
exports ALL 9 Shin Sang-ah practitioner audit PDFs into C:/Users/PC/Downloads/피드백/.
"""
import os
import sys
import json
import shutil
from datetime import datetime
import pymupdf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SHOWCASE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SITE_DIR = os.path.join(SHOWCASE_ROOT, "site")
OUT_DIR = os.path.join(SHOWCASE_ROOT, "generated_feedbacks")
HTML_TMP_DIR = os.path.join(OUT_DIR, "_html_tmp")
BACKUP_FB_DIR = r"c:\DMDG_Jobs\backups\pdf_originals_20261125\showcase_generated_feedbacks"
EXPORT_DIR = r"C:\Users\PC\Downloads\피드백"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(HTML_TMP_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

sys.path.insert(0, SCRIPT_DIR)

from feedback_gen.pdf_builder import render_pdf
from feedback_gen.renderer import render_4page_report
from feedback_gen.data_adv import ADV_PLANS
from feedback_gen.data_axi_adv2_final import AXI_ADV2_FINAL_PLANS
from feedback_gen.data_shinsanga_legacy import SHINSANGA_LEGACY_PLANS


MANIFEST_OVERRIDES = {
    "adv2_p02": {
        "grade": "C+",
        "score": 66,
        "summary": (
            "시의성 있는 주제이나 수집 불가 민간·개인정보(은행계좌·고용보험·카드결제) 의존, "
            "'~일 것이다' 추측성 가설, 원인/결과 혼재 및 D-2/D-4 세분화·정량 KPI 부재로 전면 수정 필요"
        ),
        "pdf": "adv2_02_신상아_유학생증가세분석_피드백.pdf",
    },
    "s1_midterm": {
        "grade": "B",
        "score": 74,
        "summary": (
            "고도화버전 노트북의 누수 차단·Val PR-AUC 0.8073은 양호하나, 제출 노트북 3종 중 2종 런타임 크래시·"
            "SMOTENC PR-AUC 하락(0.7503→0.7426) 오독·시간순 분할 및 Velocity 피처 부재 보완 필요"
        ),
        "pdf": "s1_midterm_Card-FDS-N_중간점검_피드백.pdf",
    },
    "s1_card_fds": {
        "grade": "B",
        "score": 77,
        "summary": (
            "PR-AUC·누수 차단·FastAPI 서빙 기본기는 갖췄으나, 비현실적 합성데이터(3.68%)·무작위 분할·"
            "고령자 알람피로 유발 '주의 TTS'·Velocity 피처/룰엔진 부재·`pr_auc_score` 오기 보완 필요"
        ),
        "pdf": "s1_card_fds_CARD-FDS-N_피드백.pdf",
    },
    "m_shinsanga": {
        "grade": "B",
        "score": 73,
        "summary": (
            "실패 수치 투명 보고와 Render/Streamlit 배포는 긍정적이나, BiLSTM(57.50h > 기준 38.21h)·교차 RUL(R² -191) 전면 실패·"
            "동일 베어링 회고적 97.35% 한계·수명 97.3% 시점 지연경보 보완 필요"
        ),
        "pdf": "mini_신상아_베어링예지보전_피드백.pdf",
    },
    "p_baemin": {
        "grade": "B",
        "score": 75,
        "summary": (
            "KTDB 실데이터 기반 문제 정의는 탄탄하나 21일 일정에 15종+ 과잉 스코프·"
            "`(기획 전용: Redis, Celery)` 문서 자기모순·6.1절 정량 KPI 0건·PM 1인 AI 병목 해소 필요"
        ),
        "pdf": "final_배차의민족_기획서_피드백.pdf",
    },
    "axi2_f_04": {
        "grade": "B+",
        "score": 82,
        "summary": (
            "Clean Architecture 기반 172항목 QA 및 GPS 6,000건 무유실·Mock 한계 투명 고지는 우수하나, "
            "매칭 P95(0.0309s)가 라운드당 화물 1건 측정치인 점·주문생성 P95 3.075s 병목·pickup_km 59.2% 가상 ML 편중·물리 FK 미제약 보완 필요"
        ),
        "pdf": "axi2_final_04_배차의민족_화물매칭_피드백.pdf",
    },
}

EXPORT_MAP = [
    ("adv2_02_신상아_유학생증가세분석_피드백.pdf", "01_심화2기_0차기획안_유학생증가세분석_신상아_실무피드백.pdf"),
    ("s1_midterm_Card-FDS-N_중간점검_피드백.pdf", "02_심화2기_1차중간점검_Card-FDS-N_오주원_김지선_신상아_이인애_실무피드백.pdf"),
    ("s1_card_fds_CARD-FDS-N_피드백.pdf", "03_심화2기_1차프로젝트_CARD-FDS-N_오주원_김지선_신상아_이인애_실무피드백.pdf"),
    ("mini_신상아_베어링예지보전_피드백.pdf", "04_심화2기_미니프로젝트_베어링예지보전_신상아_실무피드백.pdf"),
    ("final_배차의민족_기획서_피드백.pdf", "05_심화2기_2차최종기획안_배차의민족_오주원_신상아_김지선_방호원_실무피드백.pdf"),
    ("axi2_final_01_SafePredict3D_신상아_피드백.pdf", "06_삼성AXI심화2_최종_SafePredict3D_신상아_실무피드백.pdf"),
    ("axi2_final_04_배차의민족_화물매칭_피드백.pdf", "07_삼성AXI심화2_최종_배차의민족_오주원_방호원_김지선_신상아_실무피드백.pdf"),
    ("axi2_imp_01_SafePredict3D_개선안_신상아_피드백.pdf", "08_삼성AXI심화2_개선안_SafePredict3D_신상아_실무피드백.pdf"),
    ("axi2_imp_04_배차의민족_개선안_피드백.pdf", "09_삼성AXI심화2_개선안_배차의민족_오주원_방호원_김지선_신상아_실무피드백.pdf"),
]


def verify_4page_pdf(pdf_path: str) -> tuple[int, list[str], bool]:
    doc = pymupdf.open(pdf_path)
    n_pages = len(doc)
    flags = []
    for i, page in enumerate(doc, 1):
        txt = page.get_text("text")
        flags.append(f"P{i}:{'OK' if f'Page {i} of 4' in txt else 'MISSING'}")
    p4_txt = doc[3].get_text("text") if n_pages >= 4 else ""
    cert = "응원합니다" in p4_txt
    doc.close()
    return n_pages, flags, cert


def main():
    adv2_02_plan = next(p for p in ADV_PLANS if p["out_pdf"] == "adv2_02_신상아_유학생증가세분석_피드백.pdf")
    axi2_04_plan = next(p for p in AXI_ADV2_FINAL_PLANS if p["out_pdf"] == "axi2_final_04_배차의민족_화물매칭_피드백.pdf")
    plans_to_build = [adv2_02_plan, axi2_04_plan] + SHINSANGA_LEGACY_PLANS

    print(f"Rebuilding {len(plans_to_build)} Shin Sang-ah practitioner audit PDFs...", flush=True)
    failures = []
    for idx, plan in enumerate(plans_to_build, 1):
        pdf_path = os.path.join(OUT_DIR, plan["out_pdf"])
        html_path = os.path.join(HTML_TMP_DIR, f"{plan['out_pdf']}.html")
        html_str = render_4page_report(plan)
        render_pdf(html_str, html_path, pdf_path)
        n_pages, flags, cert = verify_4page_pdf(pdf_path)
        sz_kb = os.path.getsize(pdf_path) / 1024
        ok = (n_pages == 4 and all(f.endswith(":OK") for f in flags) and cert)
        print(f"[{idx}/{len(plans_to_build)}] {'OK' if ok else 'FAIL'} | {n_pages}p | {' '.join(flags)} | cert={cert} | {sz_kb:5.1f} KB | {plan['out_pdf']}", flush=True)
        if not ok:
            failures.append((plan["out_pdf"], n_pages, flags, cert))
        elif os.path.isdir(BACKUP_FB_DIR):
            shutil.copy2(pdf_path, os.path.join(BACKUP_FB_DIR, plan["out_pdf"]))

    if failures:
        print("ERROR: Page verification failed:", failures, file=sys.stderr)
        sys.exit(1)

    manifest_path = os.path.join(SITE_DIR, "data", "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    updated_pids = []
    updated_rel_paths = []
    for tab in manifest.get("tabs", []):
        for proj in tab.get("projects", []):
            pid = proj.get("id")
            if pid not in MANIFEST_OVERRIDES:
                continue
            ov = MANIFEST_OVERRIDES[pid]
            src_pdf = os.path.join(OUT_DIR, ov["pdf"])
            assert os.path.exists(src_pdf), f"Missing generated PDF: {src_pdf}"
            new_sz = os.path.getsize(src_pdf)

            proj["grade"] = ov["grade"]
            proj["score"] = ov["score"]
            proj["summary"] = ov["summary"]

            fb_updated = False
            for flist_key in ("feedbacks", "allFiles"):
                for item in proj.get(flist_key, []):
                    if item.get("role") == "feedback":
                        item["sizeBytes"] = new_sz
                        rel = item["downloadUrl"].lstrip("./")
                        dest = os.path.join(SITE_DIR, rel.replace("/", os.sep))
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        shutil.copy2(src_pdf, dest)
                        if rel not in updated_rel_paths:
                            updated_rel_paths.append(rel)
                        fb_updated = True
            assert fb_updated, f"No feedback entry found for {pid}"
            updated_pids.append(pid)

    assert sorted(updated_pids) == sorted(MANIFEST_OVERRIDES.keys()), f"Mismatch: {updated_pids}"
    manifest["generatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\nUpdated manifest.json for {len(updated_pids)} projects: {updated_pids}")
    for rel in updated_rel_paths:
        print("  site file updated:", rel)

    print(f"\nExporting all {len(EXPORT_MAP)} Shin Sang-ah audit PDFs to {EXPORT_DIR} ...")
    for src_name, dst_name in EXPORT_MAP:
        src_fp = os.path.join(OUT_DIR, src_name)
        dst_fp = os.path.join(EXPORT_DIR, dst_name)
        assert os.path.exists(src_fp), f"Missing source for export: {src_fp}"
        shutil.copy2(src_fp, dst_fp)
        n_pages, flags, cert = verify_4page_pdf(dst_fp)
        assert n_pages == 4 and cert, f"Export verify failed: {dst_name}"
        print(f"  EXPORTED ({n_pages}p, {os.path.getsize(dst_fp)/1024:5.1f} KB): {dst_name}")

    print("\nALL 6 REBUILDS + 9 DOWNLOAD EXPORTS COMPLETED & VERIFIED!")


if __name__ == "__main__":
    main()
