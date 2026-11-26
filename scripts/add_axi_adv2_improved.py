# -*- coding: utf-8 -*-
"""
add_axi_adv2_improved.py
1) Updates Track 7 SafePredict 3D (axi2_f_01) with the rewritten practitioner audit PDF,
   grade ("B"), score (76), summary, and exact sizeBytes.
2) Incrementally adds Track 8 (8. 삼성AXI 심화2 최종프로젝트 (개선 · 4팀)) right below Track 7
   in site/assets/, release_assets/, and site/data/manifest.json. Idempotent.
"""
import os
import re
import json
import shutil
import zipfile
import hashlib
from datetime import datetime

PRJ_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE_DIR = os.path.join(PRJ_ROOT, "site")
RELEASE_DIR = os.path.join(PRJ_ROOT, "release_assets")
FB_DIR = os.path.join(PRJ_ROOT, "generated_feedbacks")
DL_DIR = r"C:\Users\PC\Downloads"

GITHUB_OWNER = "freefluxkr"
GITHUB_REPO = "dmdg-student-showcase"
RELEASE_TAG = "v1.0-assets"
RELEASE_BASE = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{RELEASE_TAG}"

TAB_ID = "axi_adv2_improved"
TRACK_ID = "samsung_axi_adv2_improved"
TRACK_LABEL = "8. 삼성AXI 심화2 최종프로젝트 (개선 · 4팀)"


def safe_slug(name: str) -> str:
    h = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    ascii_part = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    if len(ascii_part) > 48:
        ascii_part = ascii_part[:48]
    return f"{ascii_part}_{h}" if ascii_part else f"file_{h}"


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

    return {
        "name": fname,
        "relPath": rel_subpath.replace("\\", "/"),
        "ext": ext,
        "sizeBytes": sz,
        "role": role,
        "hostedOn": "pages",
        "previewUrl": download_url,
        "downloadUrl": download_url,
        "externalUrl": None,
    }


def update_track7_safepredict(manifest: dict) -> None:
    new_fb_src = os.path.join(FB_DIR, "axi2_final_01_SafePredict3D_신상아_피드백.pdf")
    assert os.path.exists(new_fb_src), f"Missing rewritten feedback PDF: {new_fb_src}"
    new_sz = os.path.getsize(new_fb_src)

    updated = False
    for tab in manifest.get("tabs", []):
        if tab.get("id") != "axi_adv2_final":
            continue
        for proj in tab.get("projects", []):
            if proj.get("id") != "axi2_f_01":
                continue
            proj["grade"] = "B"
            proj["score"] = 76
            proj["summary"] = (
                "1인 E2E 3D 관제 프로토타입(Three.js·Docker 2컨테이너·pytest 34건)을 완주했으나, "
                "물리합성 MLP를 CV와 16표본만 비교한 순환 검증·CTRV 미비교·직진 +21.7% 열화·FPR/노이즈/가중치 영속화 미검증 보완 필요"
            )
            for flist_key in ("feedbacks", "allFiles"):
                for item in proj.get(flist_key, []):
                    if item.get("role") == "feedback":
                        item["sizeBytes"] = new_sz
                        rel = item["downloadUrl"].lstrip("./").replace("/", os.sep)
                        dest = os.path.join(SITE_DIR, rel)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        shutil.copy2(new_fb_src, dest)
                        updated = True
    assert updated, "Failed to locate axi2_f_01 feedback entry in manifest.json"


def main():
    projects_spec = [
        {
            "id": "axi2_i_01",
            "title": "SafePredict-3D 피드백 개선안 (랙 배치 외부화 · 타깃 현장 재정의)",
            "authors": ["신상아"],
            "grade": "B",
            "score": 74,
            "summary": (
                "SCENARIO_RACKS/VIEW의 layouts/*.json 외부화 및 동적 GridHelper 설계는 합리적이나, "
                "저예산 중소 현장 타깃에 고가 RTLS+LiDAR를 전제한 단가 모순과 랙 충돌/NLOS 배제·v1 코어 결함 미조치 보완 필요"
            ),
            "docs": [
                (os.path.join(DL_DIR, "SafePredict-3D_개선안_신상아.pdf"), "SafePredict-3D_개선안_신상아.pdf"),
            ],
            "feedback": os.path.join(FB_DIR, "axi2_imp_01_SafePredict3D_개선안_신상아_피드백.pdf"),
        },
        {
            "id": "axi2_i_02",
            "title": "예지보전 시스템 아키텍처 개선안 (AS-IS vs TO-BE · 폐쇄망 Qwen3)",
            "authors": ["김지선"],
            "grade": "B+",
            "score": 84,
            "summary": (
                "가상 PLC+DAQ 단일 스트림과 폐쇄망 Qwen3(32B/8B)+Kafka 비동기 워커 전환 방향은 우수하나, "
                "이종 데이터셋(진동 vs C-MAPSS) 단일 스트림 전제 오류·로컬 CPU LLM 실측 부재·문서 오탈자 교정 필요"
            ),
            "docs": [
                (os.path.join(DL_DIR, "예지보전_시스템_개선안_ASIS_TOBE_김지선.pdf"), "예지보전_시스템_개선안_ASIS_TOBE_김지선.pdf"),
            ],
            "feedback": os.path.join(FB_DIR, "axi2_imp_02_SmartFactory_PdM_개선안_김지선_피드백.pdf"),
        },
        {
            "id": "axi2_i_03",
            "title": "팀 미리막음: 기업 첨부파일 검사 인프라 개선안 (CAPE 병렬·캐시·RDS)",
            "authors": ["미리막음", "구명회", "김윤준", "남유진", "백선병", "이인애"],
            "grade": "A-",
            "score": 89,
            "summary": (
                "CAPE 제출/회수 디커플링·정적 캐시 연결·RDS Multi-AZ·DoD까지 실무 수준으로 정확히 진단했으나, "
                "오전 피크(3~5x) 슬롯 과소산정(133슬롯)과 AWS Bare Metal KVM TCO·실측 겹침/복구 로그 검증 보완 필요"
            ),
            "docs": [
                (os.path.join(DL_DIR, "팀 미리막음_피드백반영_개선안_구명회,김윤준,남유진,백선병,이인애.pdf"), "팀 미리막음_피드백반영_개선안_구명회,김윤준,남유진,백선병,이인애.pdf"),
            ],
            "feedback": os.path.join(FB_DIR, "axi2_imp_03_미리막음_개선안_피드백.pdf"),
        },
        {
            "id": "axi2_i_04",
            "title": "배차의 민족 최종 발표 개선안 (Phase 0~8 아키텍처 & 10테이블 ERD)",
            "authors": ["배차의 민족", "오주원", "방호원", "김지선", "신상아"],
            "grade": "B+",
            "score": 80,
            "summary": (
                "Phase 0~8 구조도와 실제 backend/models 기반 10테이블 ERD 공개는 투명하나, "
                "본문 2-1~2-5절이 추가 학습 계획 수준에 머물러 있고 DB 물리 FK 미제약(논리적 FK)·토큰 만료 부재·실측 지표 누락 보완 필요"
            ),
            "docs": [
                (os.path.join(DL_DIR, "최종 개선안_배차의 민족_오주원, 방호원, 김지선, 신상아.pdf"), "최종 개선안_배차의 민족_오주원, 방호원, 김지선, 신상아.pdf"),
            ],
            "feedback": os.path.join(FB_DIR, "axi2_imp_04_배차의민족_개선안_피드백.pdf"),
        },
    ]

    for sub in ("files", "previews"):
        target_dir = os.path.join(SITE_DIR, "assets", sub, TAB_ID)
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

    projects_out = []
    for spec in projects_spec:
        pid = spec["id"]
        presentations = []
        all_files = []
        zip_inputs = []

        for src_fp, rel in spec["docs"]:
            meta = register_pages_doc(src_fp, rel, pid, "presentation")
            presentations.append(meta)
            all_files.append(meta)
            zip_inputs.append((src_fp, rel))

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
                "available": False,
                "statusText": "미제공",
                "files": [],
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

    # 1) Update Track 7 SafePredict 3D practitioner audit
    update_track7_safepredict(manifest)

    # 2) Remove prior Track 8 / Tab 15 if re-running, then insert right after Track 7
    manifest["tracks"] = [t for t in manifest.get("tracks", []) if t.get("id") != TRACK_ID]
    manifest["tabs"] = [tb for tb in manifest.get("tabs", []) if tb.get("id") != TAB_ID]

    new_track = {
        "id": TRACK_ID,
        "label": TRACK_LABEL,
        "shortLabel": "AXI 심화2 개선",
        "heroTitle": "삼성AXI 심화2 최종프로젝트 (개선 · 4팀)",
        "subtitle": "최종 발표 피드백 반영 개선안 4팀 — SafePredict 3D(신상아) · 예지보전 AS-IS/TO-BE(김지선) · 미리막음(인프라 개선) · 배차의 민족(아키텍처·ERD 보완)",
        "tabIds": [TAB_ID],
    }
    new_tab = {
        "id": TAB_ID,
        "label": "최종 개선안 · 실무 피드백 (4팀)",
        "tabBadge": "AXI 심화2 개선",
        "trackId": TRACK_ID,
        "trackLabel": TRACK_LABEL,
        "sourceFolder": "Downloads/최종 개선안 4팀",
        "projects": projects_out,
    }

    t7_idx = next((i for i, t in enumerate(manifest["tracks"]) if t.get("id") == "samsung_axi_adv2_final"), len(manifest["tracks"]) - 1)
    manifest["tracks"].insert(t7_idx + 1, new_track)

    tab7_idx = next((i for i, tb in enumerate(manifest["tabs"]) if tb.get("id") == "axi_adv2_final"), len(manifest["tabs"]) - 1)
    manifest["tabs"].insert(tab7_idx + 1, new_tab)

    manifest["defaultTrackId"] = "samsung_axi_adv2_final"
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
