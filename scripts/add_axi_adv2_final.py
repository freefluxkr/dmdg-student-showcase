# -*- coding: utf-8 -*-
"""
add_axi_adv2_final.py
Incrementally adds Track 7 (7. 삼성AXI 심화2 최종프로젝트, 4 teams) into
site/assets/, release_assets/, and site/data/manifest.json WITHOUT wiping
existing 64 projects or 34 _cf_videos files. Idempotent.
"""
import os
import re
import json
import html
import shutil
import zipfile
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime

PRJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_DIR = os.path.join(PRJ_ROOT, "site")
RELEASE_DIR = os.path.join(PRJ_ROOT, "release_assets")
CF_DIR = os.path.join(PRJ_ROOT, "_cf_videos")
FB_DIR = os.path.join(PRJ_ROOT, "generated_feedbacks")
SRC_ROOT = r"C:\Users\PC\Desktop\팀별 최종 발표 자료(11.26까지제출) (1)"

GITHUB_OWNER = "freefluxkr"
GITHUB_REPO = "dmdg-student-showcase"
RELEASE_TAG = "v1.0-assets"
RELEASE_BASE = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{RELEASE_TAG}"
CF_MEDIA_BASE = "https://dmdg-showcase-media.pages.dev"

TAB_ID = "axi_adv2_final"
TRACK_ID = "samsung_axi_adv2_final"
TRACK_LABEL = "7. 삼성AXI 심화2 최종프로젝트 (최신 · 4팀)"


def safe_slug(name: str) -> str:
    h = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    ascii_part = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    if len(ascii_part) > 48:
        ascii_part = ascii_part[:48]
    return f"{ascii_part}_{h}" if ascii_part else f"file_{h}"


def esc(s) -> str:
    return html.escape(str(s))


def convert_pptx_to_html(pptx_path: str, out_html_path: str, title: str):
    """PPTX의 슬라이드 텍스트, 노트, 내장 이미지를 추출해 16:9 오로라 슬라이드 뷰어 HTML 생성."""
    os.makedirs(os.path.dirname(out_html_path), exist_ok=True)
    media_dir = os.path.join(
        os.path.dirname(out_html_path),
        os.path.splitext(os.path.basename(out_html_path))[0] + "_media",
    )
    os.makedirs(media_dir, exist_ok=True)
    media_rel_prefix = os.path.basename(media_dir)

    slides_html = []
    with zipfile.ZipFile(pptx_path, "r") as z:
        media_map = {}
        for m in z.namelist():
            if m.startswith("ppt/media/") and not m.endswith("/"):
                fn = os.path.basename(m)
                if os.path.splitext(fn)[1].lower() in (".mp4", ".mov", ".avi", ".mkv", ".wmv", ".bin", ".media"):
                    continue
                with open(os.path.join(media_dir, fn), "wb") as f:
                    f.write(z.read(m))
                media_map[m] = f"{media_rel_prefix}/{fn}"

        slide_files = sorted(
            [n for n in z.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", n)],
            key=lambda x: int(re.search(r"slide(\d+)\.xml", x).group(1)),
        )

        for sf in slide_files:
            snum = int(re.search(r"slide(\d+)\.xml", sf).group(1))
            root = ET.fromstring(z.read(sf))
            paragraphs = []
            for p_el in root.iter():
                if p_el.tag.endswith("}p"):
                    runs = [t.text for t in p_el.iter() if t.tag.endswith("}t") and t.text]
                    line = "".join(runs).strip()
                    if line:
                        paragraphs.append(line)

            rels_path = f"ppt/slides/_rels/slide{snum}.xml.rels"
            imgs = []
            note_text = ""
            if rels_path in z.namelist():
                rels_root = ET.fromstring(z.read(rels_path))
                for rel in rels_root:
                    target = rel.attrib.get("Target", "")
                    rtype = rel.attrib.get("Type", "")
                    if "image" in rtype:
                        norm = os.path.normpath(os.path.join("ppt/slides", target)).replace("\\", "/")
                        if norm in media_map:
                            imgs.append(media_map[norm])
                    elif "notesSlide" in rtype:
                        norm = os.path.normpath(os.path.join("ppt/slides", target)).replace("\\", "/")
                        if norm in z.namelist():
                            nroot = ET.fromstring(z.read(norm))
                            nts = [t.text for t in nroot.iter() if t.tag.endswith("}t") and t.text]
                            note_text = " ".join(nts).strip()

            img_html = ""
            if imgs:
                if len(imgs) == 1:
                    img_html = f'<div class="slide-img-wrap"><img src="{esc(imgs[0])}" alt="Slide {snum}" loading="lazy"></div>'
                else:
                    img_html = (
                        '<div class="slide-img-grid">'
                        + "".join(f'<img src="{esc(im)}" alt="Slide {snum}" loading="lazy">' for im in imgs[:6])
                        + "</div>"
                    )

            text_html = ""
            if paragraphs:
                text_html = '<div class="slide-text-box">' + "".join(f"<p>{esc(p)}</p>" for p in paragraphs) + "</div>"

            note_html = ""
            if note_text:
                note_html = f'<div class="slide-note"><strong>발표자 노트:</strong> {esc(note_text)}</div>'

            slides_html.append(
                f"""
            <article class="slide-card">
              <div class="slide-badge">SLIDE {snum:02d} / {len(slide_files):02d}</div>
              {img_html}
              {text_html}
              {note_html}
            </article>"""
            )

    doc_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} - 웹 슬라이드 뷰어</title>
<style>
  body {{ margin:0; padding:18px; background:#0b1936; color:#f8fafc; font-family:'Pretendard', -apple-system, sans-serif; line-height:1.55; }}
  .top-bar {{ max-width:980px; margin:0 auto 16px; padding:12px 18px; border-radius:14px; background:rgba(15,26,52,0.75); border:1px solid rgba(56,189,248,0.35); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; }}
  .top-bar h1 {{ margin:0; font-size:15px; font-weight:800; color:#38bdf8; }}
  .top-bar span {{ font-size:12px; color:#94a3b8; }}
  .slides-wrap {{ max-width:980px; margin:0 auto; display:flex; flex-direction:column; gap:18px; }}
  .slide-card {{ background:rgba(15,26,52,0.72); border:1px solid rgba(255,255,255,0.18); border-radius:16px; padding:16px; box-shadow:0 12px 28px rgba(0,0,0,0.35); }}
  .slide-badge {{ display:inline-block; font-size:11px; font-weight:800; color:#34d399; background:rgba(52,211,153,0.15); border:1px solid rgba(52,211,153,0.4); padding:2px 10px; border-radius:999px; margin-bottom:10px; }}
  .slide-img-wrap img {{ width:100%; border-radius:10px; border:1px solid rgba(255,255,255,0.12); display:block; margin-bottom:10px; }}
  .slide-img-grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; margin-bottom:10px; }}
  .slide-img-grid img {{ width:100%; border-radius:8px; border:1px solid rgba(255,255,255,0.12); }}
  .slide-text-box p {{ margin:4px 0; font-size:13.5px; color:#e2e8f0; }}
  .slide-text-box p:first-child {{ font-size:15.5px; font-weight:800; color:#ffffff; margin-bottom:6px; }}
  .slide-note {{ margin-top:10px; padding:10px 12px; border-radius:10px; background:rgba(56,189,248,0.1); border-left:3px solid #38bdf8; font-size:12.5px; color:#cbd5e1; }}
</style>
</head>
<body>
  <div class="top-bar">
    <h1>📊 {esc(title)}</h1>
    <span>총 {len(slide_files)} 슬라이드 · 웹 슬라이드 뷰어</span>
  </div>
  <div class="slides-wrap">
    {''.join(slides_html)}
  </div>
</body>
</html>"""
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(doc_html)


def make_bundle_zip(proj_files_src: list[tuple[str, str]], zip_name: str) -> tuple[str, int]:
    os.makedirs(RELEASE_DIR, exist_ok=True)
    z_path = os.path.join(RELEASE_DIR, zip_name)
    seen = set()
    with zipfile.ZipFile(z_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp, arcname in proj_files_src:
            key = arcname.replace("\\", "/")
            if key in seen:
                base, ext = os.path.splitext(key)
                idx = 2
                while f"{base}_{idx}{ext}" in seen:
                    idx += 1
                key = f"{base}_{idx}{ext}"
            seen.add(key)
            zf.write(fp, arcname=key)
    return f"{RELEASE_BASE}/{zip_name}", os.path.getsize(z_path)


def register_pages_doc(src_path: str, rel_subpath: str, pid: str, role: str) -> dict:
    assert os.path.exists(src_path), f"Missing file: {src_path}"
    fname = os.path.basename(src_path)
    ext = os.path.splitext(fname)[1].lower().lstrip(".")
    sz = os.path.getsize(src_path)
    slug_name = safe_slug(f"{TAB_ID}_{pid}_{fname}")
    ext_suffix = f".{ext}" if ext else ""
    if not slug_name.endswith(ext_suffix):
        slug_name += ext_suffix

    rel_path = f"assets/files/{TAB_ID}/{pid}/{slug_name}"
    dest = os.path.join(SITE_DIR, rel_path.replace("/", os.sep))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src_path, dest)
    download_url = f"./{rel_path}"

    if ext == "pptx":
        p_rel = f"assets/previews/{TAB_ID}/{pid}/{slug_name}.html"
        p_dest = os.path.join(SITE_DIR, p_rel.replace("/", os.sep))
        convert_pptx_to_html(src_path, p_dest, fname)
        preview_url = f"./{p_rel}"
    else:
        preview_url = download_url

    return {
        "name": fname,
        "relPath": rel_subpath.replace("\\", "/"),
        "ext": ext,
        "sizeBytes": sz,
        "role": role,
        "hostedOn": "pages",
        "previewUrl": preview_url,
        "downloadUrl": download_url,
        "externalUrl": None,
    }


def register_cf_video(cf_filename: str, rel_subpath: str) -> tuple[dict, str]:
    cf_path = os.path.join(CF_DIR, cf_filename)
    assert os.path.exists(cf_path), f"Missing transcoded video: {cf_path}"
    sz = os.path.getsize(cf_path)
    assert sz < 24_000_000, f"Video exceeds 24MB margin: {cf_path} ({sz} bytes)"
    url = f"{CF_MEDIA_BASE}/{cf_filename}"
    meta = {
        "name": os.path.basename(rel_subpath),
        "relPath": rel_subpath.replace("\\", "/"),
        "ext": "mp4",
        "sizeBytes": sz,
        "role": "video",
        "hostedOn": "cloudflare_pages",
        "previewUrl": url,
        "downloadUrl": url,
        "externalUrl": None,
    }
    return meta, cf_path


def main():
    projects_spec = [
        {
            "id": "axi2_f_01",
            "title": "SafePredict 3D: 월드모델 기반 산업현장 충돌위험 예측 및 3D 안전관제 PoC",
            "authors": ["신상아"],
            "grade": "B",
            "score": 76,
            "summary": "1인 E2E 3D 관제 프로토타입(Three.js·Docker 2컨테이너·pytest 34건)을 완주했으나, 물리합성 MLP를 CV와 16표본만 비교한 순환 검증·CTRV 미비교·직진 +21.7% 열화·FPR/노이즈/가중치 영속화 미검증 보완 필요",
            "docs": [
                (os.path.join(SRC_ROOT, r"Safepredict-3D_신상아\SafePredict_3D_발표자료_신상아.pdf"), "SafePredict_3D_발표자료_신상아.pdf"),
            ],
            "video": ("axi_adv2_final_axi2_f_01_safepredict3d_demo.mp4", "충돌위험예측_시연영상.mp4"),
            "feedback": os.path.join(FB_DIR, "axi2_final_01_SafePredict3D_신상아_피드백.pdf"),
        },
        {
            "id": "axi2_f_02",
            "title": "Smart Factory PdM: 진동·센서 스트림 기반 예지보전 관제 시스템",
            "authors": ["김지선"],
            "grade": "A+",
            "score": 94,
            "summary": "ISA-95 Level 2 비침습 연동 기반 Kafka 3.7→FastAPI→TimescaleDB 실시간 스트림(100대 동시 10,196건 무오차 적재), CWRU(1.00)·IMS(74시간 전 조기경보)·C-MAPSS RUL(RMSE 12.51) 및 +5 히스테리시스·Gemini SOP 에이전트 통합 관제탑",
            "docs": [
                (os.path.join(SRC_ROOT, r"Smart_factory_FDM_김지선\PdM_관제시스템.pptx"), "PdM_관제시스템.pptx"),
            ],
            "video": ("axi_adv2_final_axi2_f_02_smartfactory_pdm_demo.mp4", "smart_factory_fdm_시연영상.mp4"),
            "feedback": os.path.join(FB_DIR, "axi2_final_02_SmartFactory_PdM_김지선_피드백.pdf"),
        },
        {
            "id": "axi2_f_03",
            "title": "[AXI] 미리막음: AI 기반 업로드 파일 악성코드 사전 탐지·차단 시스템",
            "authors": ["미리막음", "김윤준", "구명회", "남유진", "백선병", "이인애"],
            "grade": "A+",
            "score": 95,
            "summary": "스피디 기업 연계 B2B MSP 보안 솔루션. AWS(S3/SQS/EC2) 6단계 정적 선별(정상 2~5% 통제·정상문서 30,902건 오차단 0건)과 인바운드 0 아웃바운드 전용 CAPEv2 Win10 격리 샌드박스를 결합해 E2E 실증을 완결한 악성코드 탐지 시스템",
            "docs": [
                (os.path.join(SRC_ROOT, r"[AXI] 미리막음_김윤준_구명회_남유진_백선병_이인애\발표자료 제출본.pdf"), "발표자료 제출본.pdf"),
                (os.path.join(SRC_ROOT, r"[AXI] 미리막음_김윤준_구명회_남유진_백선병_이인애\발표자료 제출본.html"), "발표자료 제출본.html"),
                (os.path.join(SRC_ROOT, r"[AXI] 미리막음_김윤준_구명회_남유진_백선병_이인애\프로젝트_기획서_제출.pdf"), "프로젝트_기획서_제출.pdf"),
            ],
            "video": ("axi_adv2_final_axi2_f_03_mirimakum_demo.mp4", "악성코드탐지_시연영상_v00.mp4"),
            "feedback": os.path.join(FB_DIR, "axi2_final_03_미리막음_악성코드탐지_피드백.pdf"),
        },
        {
            "id": "axi2_f_04",
            "title": "배차의 민족: 알고리즘 기반 자동 화물 기사 매칭 & AI 실시간 관제 플랫폼",
            "authors": ["배차의 민족", "오주원", "방호원", "김지선", "신상아"],
            "grade": "B+",
            "score": 82,
            "summary": "Clean Architecture 기반 172항목 QA 및 GPS 6,000건 무유실·Mock 한계 투명 고지는 우수하나, 매칭 P95(0.0309s)가 라운드당 화물 1건 측정치인 점·주문생성 P95 3.075s 병목·pickup_km 59.2% 가상 ML 편중·물리 FK 미제약 보완 필요",
            "docs": [
                (os.path.join(SRC_ROOT, r"배차의 민족_오주원, 방호원, 김지선, 신상아\PDF_배차의민족_오주원, 방호원, 김지선, 신상아.pdf"), "PDF_배차의민족_오주원, 방호원, 김지선, 신상아.pdf"),
            ],
            "video": ("axi_adv2_final_axi2_f_04_baemin_demo.mp4", "영상_배차의 민족_오주원, 방호원, 김지선, 신상아.mp4"),
            "feedback": os.path.join(FB_DIR, "axi2_final_04_배차의민족_화물매칭_피드백.pdf"),
        },
    ]

    # Clean previous incremental assets for TAB_ID if re-running
    for sub in ("files", "previews"):
        target_dir = os.path.join(SITE_DIR, "assets", sub, TAB_ID)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

    projects_out = []
    for spec in projects_spec:
        pid = spec["id"]
        presentations = []
        videos = []
        all_files = []
        zip_inputs = []

        for src_fp, rel in spec["docs"]:
            meta = register_pages_doc(src_fp, rel, pid, "presentation")
            presentations.append(meta)
            all_files.append(meta)
            zip_inputs.append((src_fp, rel))

        cf_name, vid_rel = spec["video"]
        vmeta, v_fp = register_cf_video(cf_name, vid_rel)
        videos.append(vmeta)
        all_files.append(vmeta)
        zip_inputs.append((v_fp, vid_rel))

        fmeta = register_pages_doc(spec["feedback"], os.path.basename(spec["feedback"]), pid, "feedback")
        feedbacks_out = [fmeta]
        all_files.append(fmeta)
        zip_inputs.append((spec["feedback"], os.path.basename(spec["feedback"])))

        zip_url, zip_sz = make_bundle_zip(zip_inputs, f"bundle_{TAB_ID}_{pid}.zip")

        projects_out.append({
            "id": pid,
            "title": spec["title"],
            "authors": spec["authors"],
            "grade": spec["grade"],
            "score": spec["score"],
            "summary": spec["summary"],
            "presentations": presentations,
            "demoVideo": {
                "available": True,
                "statusText": "제공",
                "files": videos,
            },
            "audios": [],
            "datasets": [],
            "feedbacks": feedbacks_out,
            "allFiles": all_files,
            "bundleZipUrl": zip_url,
            "bundleZipBytes": zip_sz,
        })

    manifest_path = os.path.join(SITE_DIR, "data", "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Remove prior track/tab if re-running
    manifest["tracks"] = [t for t in manifest.get("tracks", []) if t.get("id") != TRACK_ID]
    manifest["tabs"] = [tb for tb in manifest.get("tabs", []) if tb.get("id") != TAB_ID]

    for tr in manifest["tracks"]:
        if tr.get("id") == "adv_cohort_2":
            tr["label"] = "6. AI·데이터 심화 2기 (26건)"

    manifest["tracks"].append({
        "id": TRACK_ID,
        "label": TRACK_LABEL,
        "shortLabel": "AXI 심화2 최종",
        "heroTitle": "삼성AXI 심화2 최종프로젝트 쇼케이스",
        "subtitle": "SafePredict 3D(월드모델 충돌예측) · Smart Factory PdM(실시간 예지보전) · 미리막음(AI 악성코드 탐지) · 배차의 민족(화물 자동매칭) 최종 4팀",
        "tabIds": [TAB_ID],
    })

    manifest["tabs"].append({
        "id": TAB_ID,
        "label": "최종 발표 · 시연영상 (4팀)",
        "tabBadge": "AXI 심화2 최종",
        "trackId": TRACK_ID,
        "trackLabel": TRACK_LABEL,
        "sourceFolder": "팀별 최종 발표 자료(11.26까지제출)",
        "projects": projects_out,
    })

    manifest["defaultTrackId"] = TRACK_ID
    manifest["generatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    tabs = manifest["tabs"]
    total_projects = sum(len(t["projects"]) for t in tabs)
    total_common_files = sum(len(t.get("commonResources") or []) for t in tabs)
    total_files = sum(len(p["allFiles"]) for t in tabs for p in t["projects"]) + total_common_files
    video_yes = sum(1 for t in tabs for p in t["projects"] if p["demoVideo"]["available"])
    video_no = total_projects - video_yes
    total_feedbacks = sum(len(p["feedbacks"]) for t in tabs for p in t["projects"])

    manifest["stats"] = {
        "totalTracks": len(manifest["tracks"]),
        "totalTabs": len(tabs),
        "totalProjects": total_projects,
        "totalFiles": total_files,
        "videosAvailable": video_yes,
        "videosMissing": video_no,
        "totalFeedbackPdfs": total_feedbacks,
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("UPDATED MANIFEST STATS:", manifest["stats"])
    for p in projects_out:
        print(f" - {p['id']} | {p['title']} | files={len(p['allFiles'])} | zip={p['bundleZipBytes']/1048576:.2f} MB")


if __name__ == "__main__":
    main()
