# -*- coding: utf-8 -*-
"""
build_showcase.py
C:\\Users\\PC\\Downloads\\발표 프로젝트 의 모든 자료를 스캔·변환하여
GitHub Pages 정적 사이트(site/) 및 GitHub Releases 대용량 자산(release_assets/)을 생성한다.
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
import docx

SRC_ROOT = r"C:\Users\PC\Downloads\발표 프로젝트"
PRJ_ROOT = r"c:\DMDG_Jobs\DMDG_PRJ\dmdg-student-showcase"
SITE_DIR = os.path.join(PRJ_ROOT, "site")
RELEASE_DIR = os.path.join(PRJ_ROOT, "release_assets")

GITHUB_OWNER = "freefluxkr"
GITHUB_REPO = "dmdg-student-showcase"
RELEASE_TAG = "v1.0-assets"
RELEASE_BASE = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download/{RELEASE_TAG}"

# Pages Git에 직접 포함할 단일 파일 최대 크기 (35MB 초과 파일은 GitHub Releases로 분리)
PAGES_MAX_BYTES = 35 * 1024 * 1024

TAB1_DIR = os.path.join(SRC_ROOT, "데이터 분석 1차 프로젝트 최종 자료(발표 자료  및  시연영상_피드백 포함)")
TAB2_DIR = os.path.join(SRC_ROOT, "미니 프로젝트 발표자료 제출 폴더 (11.5까지)")
TAB3_DIR = os.path.join(SRC_ROOT, "최종 기획안")


def safe_slug(name: str) -> str:
    h = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    ascii_part = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    if len(ascii_part) > 48:
        ascii_part = ascii_part[:48]
    return f"{ascii_part}_{h}" if ascii_part else f"file_{h}"


def ensure_clean_dir(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def esc(s) -> str:
    return html.escape(str(s))


def convert_pptx_to_html(pptx_path: str, out_html_path: str, title: str):
    """PPTX의 슬라이드 텍스트, 노트, 내장 이미지를 추출해 16:9 오로라 슬라이드 뷰어 HTML 생성."""
    os.makedirs(os.path.dirname(out_html_path), exist_ok=True)
    media_dir = os.path.join(os.path.dirname(out_html_path), os.path.splitext(os.path.basename(out_html_path))[0] + "_media")
    os.makedirs(media_dir, exist_ok=True)
    media_rel_prefix = os.path.basename(media_dir)

    slides_html = []
    with zipfile.ZipFile(pptx_path, "r") as z:
        # extract all media
        media_map = {}
        for m in z.namelist():
            if m.startswith("ppt/media/") and not m.endswith("/"):
                fn = os.path.basename(m)
                with open(os.path.join(media_dir, fn), "wb") as f:
                    f.write(z.read(m))
                media_map[m] = f"{media_rel_prefix}/{fn}"

        slide_files = sorted(
            [n for n in z.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", n)],
            key=lambda x: int(re.search(r"slide(\d+)\.xml", x).group(1))
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

            # Check rels for images & notes
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
                # 이미지가 많으면 그리드, 1개면 풀폭
                if len(imgs) == 1:
                    img_html = f'<div class="slide-img-wrap"><img src="{esc(imgs[0])}" alt="Slide {snum}" loading="lazy"></div>'
                else:
                    img_html = '<div class="slide-img-grid">' + "".join(
                        f'<img src="{esc(im)}" alt="Slide {snum}" loading="lazy">' for im in imgs[:6]
                    ) + "</div>"

            text_html = ""
            if paragraphs:
                text_html = '<div class="slide-text-box">' + "".join(f"<p>{esc(p)}</p>" for p in paragraphs) + "</div>"

            note_html = ""
            if note_text:
                note_html = f'<div class="slide-note"><strong>발표자 노트:</strong> {esc(note_text)}</div>'

            slides_html.append(f"""
            <article class="slide-card">
              <div class="slide-badge">SLIDE {snum:02d} / {len(slide_files):02d}</div>
              {img_html}
              {text_html}
              {note_html}
            </article>""")

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


def convert_docx_to_html(docx_path: str, out_html_path: str, title: str):
    os.makedirs(os.path.dirname(out_html_path), exist_ok=True)
    d = docx.Document(docx_path)
    blocks = []
    for p in d.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        sname = (p.style.name or "").lower()
        if "heading 1" in sname or "title" in sname:
            blocks.append(f"<h2>{esc(t)}</h2>")
        elif "heading" in sname:
            blocks.append(f"<h3>{esc(t)}</h3>")
        else:
            blocks.append(f"<p>{esc(t)}</p>")
    for tbl in d.tables:
        rows_html = []
        for idx, r in enumerate(tbl.rows):
            tag = "th" if idx == 0 else "td"
            cells = "".join(f"<{tag}>{esc(c.text.strip())}</{tag}>" for c in r.cells)
            rows_html.append(f"<tr>{cells}</tr>")
        blocks.append(f'<div class="tbl-wrap"><table>{"".join(rows_html)}</table></div>')

    doc_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} - 문서 뷰어</title>
<style>
  body {{ margin:0; padding:24px; background:#0b1936; color:#e2e8f0; font-family:'Pretendard', -apple-system, sans-serif; line-height:1.65; }}
  .doc-container {{ max-width:860px; margin:0 auto; background:rgba(15,26,52,0.78); border:1px solid rgba(255,255,255,0.18); border-radius:18px; padding:28px 32px; box-shadow:0 16px 36px rgba(0,0,0,0.4); }}
  h1 {{ margin:0 0 18px; font-size:20px; color:#38bdf8; border-bottom:1px solid rgba(56,189,248,0.3); padding-bottom:10px; }}
  h2 {{ margin:22px 0 10px; font-size:17px; color:#34d399; }}
  h3 {{ margin:16px 0 8px; font-size:15px; color:#a78bfa; }}
  p {{ margin:7px 0; font-size:14px; color:#e2e8f0; }}
  .tbl-wrap {{ overflow-x:auto; margin:14px 0; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th, td {{ border:1px solid rgba(148,163,184,0.25); padding:8px 10px; text-align:left; }}
  th {{ background:rgba(56,189,248,0.16); color:#bae6fd; }}
</style>
</head>
<body>
  <div class="doc-container">
    <h1>📄 {esc(title)}</h1>
    {''.join(blocks)}
  </div>
</body>
</html>"""
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(doc_html)


def convert_ipynb_to_html(ipynb_path: str, out_html_path: str, title: str):
    os.makedirs(os.path.dirname(out_html_path), exist_ok=True)
    with open(ipynb_path, "r", encoding="utf-8", errors="replace") as f:
        nb = json.load(f)
    cells_html = []
    for idx, cell in enumerate(nb.get("cells", []), 1):
        ctype = cell.get("cell_type", "code")
        src = "".join(cell.get("source", []))
        if not src.strip():
            continue
        if ctype == "markdown":
            cells_html.append(f'<div class="cell-md"><div class="cell-tag">MD [{idx}]</div><pre class="md-pre">{esc(src)}</pre></div>')
        else:
            outs_html = []
            for out in cell.get("outputs", []):
                if "text" in out:
                    txt = "".join(out["text"])[:2500]
                    outs_html.append(f'<pre class="out-txt">{esc(txt)}</pre>')
                elif "data" in out:
                    d = out["data"]
                    if "image/png" in d:
                        b64 = "".join(d["image/png"]).replace("\n", "")
                        outs_html.append(f'<img class="out-img" src="data:image/png;base64,{b64}" alt="output">')
                    elif "text/plain" in d:
                        txt = "".join(d["text/plain"])[:1800]
                        outs_html.append(f'<pre class="out-txt">{esc(txt)}</pre>')
            cells_html.append(
                f'<div class="cell-code"><div class="cell-tag">In [{cell.get("execution_count") or idx}]</div>'
                f'<pre class="code-pre">{esc(src)}</pre>{"".join(outs_html)}</div>'
            )

    doc_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} - Notebook 뷰어</title>
<style>
  body {{ margin:0; padding:20px; background:#0b1936; color:#e2e8f0; font-family:'Pretendard', sans-serif; }}
  .nb-wrap {{ max-width:960px; margin:0 auto; display:flex; flex-direction:column; gap:12px; }}
  .nb-head {{ padding:14px 18px; border-radius:14px; background:rgba(15,26,52,0.8); border:1px solid rgba(167,139,250,0.4); }}
  .nb-head h1 {{ margin:0; font-size:16px; color:#c4b5fd; }}
  .cell-md, .cell-code {{ background:rgba(15,26,52,0.72); border:1px solid rgba(255,255,255,0.14); border-radius:12px; padding:12px 14px; }}
  .cell-tag {{ font-size:11px; font-weight:800; color:#34d399; margin-bottom:6px; }}
  pre {{ margin:0; white-space:pre-wrap; word-break:break-word; font-family:Consolas, monospace; font-size:12.5px; line-height:1.48; }}
  .md-pre {{ font-family:'Pretendard', sans-serif; color:#f1f5f9; font-size:13.5px; }}
  .code-pre {{ background:#020617; padding:10px 12px; border-radius:8px; color:#93c5fd; border-left:3px solid #38bdf8; }}
  .out-txt {{ margin-top:8px; background:rgba(2,6,23,0.65); padding:8px 10px; border-radius:8px; color:#cbd5e1; font-size:12px; }}
  .out-img {{ margin-top:8px; max-width:100%; border-radius:8px; background:#fff; padding:4px; }}
</style>
</head>
<body>
  <div class="nb-wrap">
    <div class="nb-head"><h1>📓 {esc(title)} (총 {len(cells_html)} 셀)</h1></div>
    {''.join(cells_html)}
  </div>
</body>
</html>"""
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(doc_html)


def convert_text_to_html(txt_path: str, out_html_path: str, title: str):
    os.makedirs(os.path.dirname(out_html_path), exist_ok=True)
    content = open(txt_path, "r", encoding="utf-8", errors="replace").read()
    doc_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{esc(title)}</title>
<style>
  body {{ margin:0; padding:22px; background:#0b1936; color:#e2e8f0; font-family:'Pretendard', sans-serif; }}
  .box {{ max-width:860px; margin:0 auto; background:rgba(15,26,52,0.78); border:1px solid rgba(255,255,255,0.18); border-radius:16px; padding:22px 26px; }}
  h1 {{ margin:0 0 14px; font-size:16px; color:#38bdf8; border-bottom:1px solid rgba(56,189,248,0.25); padding-bottom:8px; }}
  pre {{ margin:0; white-space:pre-wrap; word-break:break-word; font-family:'Pretendard', Consolas, monospace; font-size:13.5px; line-height:1.65; color:#f1f5f9; }}
</style>
</head>
<body><div class="box"><h1>📝 {esc(title)}</h1><pre>{esc(content)}</pre></div></body></html>"""
    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(doc_html)


def parse_url_file(path: str) -> str:
    txt = open(path, "r", encoding="utf-8", errors="replace").read()
    m = re.search(r"https?://[^\s\)\]>\"']+", txt)
    return m.group(0) if m else ""


def register_file(src_path: str, rel_subpath: str, tab_id: str, proj_id: str, role: str):
    """
    파일을 Pages(<=35MB) 또는 Releases(>35MB or .csv)에 배치하고 메타데이터 반환.
    필요 시 웹 뷰어용 previewUrl 생성.
    """
    fname = os.path.basename(src_path)
    ext = os.path.splitext(fname)[1].lower().lstrip(".")
    sz = os.path.getsize(src_path)
    slug_name = safe_slug(f"{tab_id}_{proj_id}_{fname}")
    ext_suffix = f".{ext}" if ext else ""
    if not slug_name.endswith(ext_suffix):
        slug_name += ext_suffix

    # 저장 위치 결정: CSV 전부 또는 35MB 초과는 GitHub Releases, 나머지는 GitHub Pages
    is_release = (ext == "csv") or (sz > PAGES_MAX_BYTES)
    if is_release:
        rel_dest = os.path.join(RELEASE_DIR, slug_name)
        shutil.copy2(src_path, rel_dest)
        download_url = f"{RELEASE_BASE}/{slug_name}"
        raw_view_url = download_url
        hosted_on = "releases"
    else:
        rel_path = f"assets/files/{tab_id}/{proj_id}/{slug_name}"
        dest = os.path.join(SITE_DIR, rel_path.replace("/", os.sep))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src_path, dest)
        download_url = f"./{rel_path}"
        raw_view_url = download_url
        hosted_on = "pages"

    # 미리보기 URL 생성
    preview_url = None
    external_url = None

    if ext in ("pdf", "html", "png", "jpg", "jpeg", "mp4", "m4a"):
        preview_url = raw_view_url
    elif ext == "pptx":
        p_rel = f"assets/previews/{tab_id}/{proj_id}/{slug_name}.html"
        p_dest = os.path.join(SITE_DIR, p_rel.replace("/", os.sep))
        convert_pptx_to_html(src_path, p_dest, fname)
        preview_url = f"./{p_rel}"
    elif ext == "docx":
        p_rel = f"assets/previews/{tab_id}/{proj_id}/{slug_name}.html"
        p_dest = os.path.join(SITE_DIR, p_rel.replace("/", os.sep))
        convert_docx_to_html(src_path, p_dest, fname)
        preview_url = f"./{p_rel}"
    elif ext == "ipynb":
        p_rel = f"assets/previews/{tab_id}/{proj_id}/{slug_name}.html"
        p_dest = os.path.join(SITE_DIR, p_rel.replace("/", os.sep))
        convert_ipynb_to_html(src_path, p_dest, fname)
        preview_url = f"./{p_rel}"
    elif ext in ("txt", "md", "url"):
        p_rel = f"assets/previews/{tab_id}/{proj_id}/{slug_name}.html"
        p_dest = os.path.join(SITE_DIR, p_rel.replace("/", os.sep))
        convert_text_to_html(src_path, p_dest, fname)
        preview_url = f"./{p_rel}"
        ext_u = parse_url_file(src_path)
        if ext_u:
            external_url = ext_u

    if ext == "html":
        # html 리다이렉트 파일(스마트민원케어_GitHub.html) 체크
        txt_head = open(src_path, "r", encoding="utf-8", errors="replace").read(1000)
        if 'http-equiv="refresh"' in txt_head:
            u = parse_url_file(src_path)
            if u:
                external_url = u

    return {
        "name": fname,
        "relPath": rel_subpath.replace("\\", "/"),
        "ext": ext,
        "sizeBytes": sz,
        "role": role,
        "hostedOn": hosted_on,
        "previewUrl": preview_url,
        "downloadUrl": download_url,
        "externalUrl": external_url,
    }


def make_bundle_zip(proj_files_src: list[str], zip_name: str) -> tuple[str, int]:
    """프로젝트 내 경량/전체 파일을 ZIP으로 묶어 Release(또는 Pages)에 저장. (CSV 대용량 19종은 별도 ZIP)"""
    z_path = os.path.join(RELEASE_DIR, zip_name)
    with zipfile.ZipFile(z_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp, arcname in proj_files_src:
            zf.write(fp, arcname=arcname)
    return f"{RELEASE_BASE}/{zip_name}", os.path.getsize(z_path)


def build_all():
    ensure_clean_dir(SITE_DIR)
    ensure_clean_dir(RELEASE_DIR)
    os.makedirs(os.path.join(SITE_DIR, "data"), exist_ok=True)

    # ── TAB 1: 데이터 분석 1차 프로젝트 ──────────────────────────────────────────
    t1_configs = [
        {
            "id": "s1_gu",
            "title": "AI 기반 항만 선박 식별 및 자동 Entity Matching",
            "authors": ["구명회"],
            "grade": "A+",
            "score": 94,
            "summary": "후보 검색 → 랭킹 판별 → 신뢰도(Gap≥0.2) 기반 자동/수동 분기(84.81% 자동연결, 99.80% 정확도)를 구현한 1차 최우수 프로젝트",
            "folder": os.path.join(TAB1_DIR, "데이터_분석_1차_프로젝트_최종자료_구명회"),
            "feedbacks": [
                os.path.join(TAB1_DIR, "데이터_분석_1차_프로젝트_최종자료_구명회_피드백.pdf"),
                os.path.join(TAB1_DIR, "데이터_분석_1차_프로젝트_구명회_피드백.pdf"),
            ],
            "extra_raw": [os.path.join(TAB1_DIR, "데이터_분석_1차_프로젝트_최종자료_구명회_피드백.txt"), os.path.join(TAB1_DIR, "데이터_분석_1차_프로젝트_구명회_피드백.txt")],
        },
        {
            "id": "s1_card_fds",
            "title": "CARD-FDS-N (카드 이상거래 탐지 및 알림 서비스)",
            "authors": ["오주원", "김지선", "신상아", "이인애"],
            "grade": "A-",
            "score": 89,
            "summary": "시니어 특화 금융 안전망. Data Leakage 차단, SMOTENC, Soft Voting 앙상블(PR-AUC 0.80) 및 FastAPI·Streamlit·TTS 실시간 경고 구현",
            "folder": os.path.join(TAB1_DIR, "1차 프로젝트_오주원, 김지선, 신상아, 이인애"),
            "feedbacks": [os.path.join(TAB1_DIR, "CARD-FDS-N 프로젝트_오주원, 김지선, 신상아, 이인애_피드백.pdf")],
            "extra_raw": [os.path.join(TAB1_DIR, "CARD-FDS-N 프로젝트_오주원, 김지선, 신상아, 이인애_피드백.txt")],
        },
        {
            "id": "s1_minwon",
            "title": "스마트 민원케어 (민원 조기경보 및 인력 지원 대시보드)",
            "authors": ["백선병", "남유진", "김윤준", "김제형"],
            "grade": "B+",
            "score": 84,
            "summary": "기상 데이터와 민원 데이터를 연계해 1~14일 단기 민원 폭증을 조기 경보하고 부서별 현황을 시각화한 대시보드",
            "folder": os.path.join(TAB1_DIR, "1차 프로젝트_백선병, 남유진, 김윤준, 김제형"),
            "feedbacks": [os.path.join(TAB1_DIR, "1차 프로젝트_백선병, 남유진, 김윤준, 김제형_피드백.pdf")],
            "extra_raw": [os.path.join(TAB1_DIR, "1차 프로젝트_백선병, 남유진, 김윤준, 김제형_피드백.txt")],
        },
        {
            "id": "s1_logipredict",
            "title": "스마트 물류센터 AI 예지보전 관제 시스템 (LogiPredict AI)",
            "authors": ["방호원"],
            "grade": "B",
            "score": 78,
            "summary": "1D-CNN Autoencoder와 CBM 상태기반정비 시나리오를 인터랙티브 웹 관제 대시보드(HTML)로 구현한 물류 설비 예지보전 시스템",
            "folder": os.path.join(TAB1_DIR, "1차 프로젝트_방호원"),
            "feedbacks": [os.path.join(TAB1_DIR, "물류 설비_방호원_피드백.pdf")],
            "extra_raw": [os.path.join(TAB1_DIR, "물류 설비_방호원_피드백.txt")],
        },
        {
            "id": "s1_unmanned",
            "title": "무인점포 입지 선정 및 AI 보안 전략 보고서",
            "authors": ["정호연"],
            "grade": "C+",
            "score": 68,
            "summary": "전국 소상공인 상가(상권)정보 19개 지역 데이터와 치안 통계를 결합해 무인점포 최적 입지를 분석한 보고서 및 노트북",
            "folder": os.path.join(TAB1_DIR, "1차_프로젝트_최종자료_정호연"),
            "feedbacks": [os.path.join(TAB1_DIR, "무인점포 입지 선정 및 AI 보안 전략 보고서 정호연_피드백.pdf")],
            "extra_raw": [os.path.join(TAB1_DIR, "무인점포 입지 선정 및 AI 보안 전략 보고서 정호연_피드백.txt")],
        },
        {
            "id": "s1_midterm",
            "title": "Card-FDS-N 중간점검 코드·파이프라인 & 오디오 브리핑",
            "authors": ["오주원", "김지선", "신상아", "이인애"],
            "grade": "A",
            "score": 92,
            "summary": "중간점검 제출 노트북 3종, 슬라이드 기획안, 파이프라인 장표, 분석 차트, AI 오디오 브리핑(.m4a) 및 기준 기술 감사 피드백 패키지",
            "folders": [
                os.path.join(TAB1_DIR, "중간점검제출파일_Updated"),
                os.path.join(TAB1_DIR, "중간점검제출파일_Updated_오주원김지선신상아이인애 피드백"),
            ],
            "feedbacks": [os.path.join(TAB1_DIR, "중간점검제출파일_Updated_오주원김지선신상아이인애 피드백", "피드백.pdf")],
            "extra_raw": [os.path.join(TAB1_DIR, "10월 23일 오후 14시 발표 배점.txt")],
        },
    ]

    # ── TAB 2: 미니 프로젝트 발표자료 ───────────────────────────────────────────
    t2_configs = [
        {
            "id": "m_namyujin",
            "title": "axiMini · 2일 경량 AI-EDR (엔드포인트 탐지 및 대응)",
            "authors": ["남유진"],
            "grade": "A+",
            "score": 95,
            "summary": "EMBER2024 72만 PE 시간순 분할·8.5σ 드리프트 검출, 36ms 고속 추출(비트 동일성), 하드닝 Docker 샌드박스 & TreeSHAP SOC 구현",
            "folder": os.path.join(TAB2_DIR, "미니프로젝트_남유진"),
            "feedbacks": [os.path.join(TAB2_DIR, "미니프로젝트_남유진", "발표자료_남유진_피드백.pdf")],
        },
        {
            "id": "m_kimjisun",
            "title": "진동·센서 스트림 기반 예지보전(PdM) 관제 시스템",
            "authors": ["김지선"],
            "grade": "A",
            "score": 91,
            "summary": "CWRU·NASA IMS·C-MAPSS(RMSE 27% 감축) 검증 및 Kafka→TimescaleDB→FastAPI→Streamlit 실시간 파이프라인 구축",
            "folder": os.path.join(TAB2_DIR, "미니프로젝트_김지선"),
            "feedbacks": [os.path.join(TAB2_DIR, "미니프로젝트_김지선", "미니프로젝트_김지선_피드백.pdf")],
        },
        {
            "id": "m_kimyunjun1",
            "title": "업로드 파일 악성코드 사전 선별 시스템 (1차 제출본)",
            "authors": ["김윤준"],
            "grade": "A",
            "score": 90,
            "summary": "정상 전송률(2%/5%) 비용 기준 정립 및 로그 우도비 결합층으로 미탐 38% 감축(29→18건), AWS Docker 4컨테이너 격리 서빙",
            "folder": os.path.join(TAB2_DIR, "미니_프로젝트_김윤준"),
            "feedbacks": [os.path.join(TAB2_DIR, "미니_프로젝트_김윤준", "악성코드 사전 선별 시스템_피드백.pdf")],
        },
        {
            "id": "m_kimyunjun2",
            "title": "업로드 파일 악성코드 사전 선별 시스템 (malware-mini 정리본 v2)",
            "authors": ["김윤준"],
            "grade": "A",
            "score": 90,
            "summary": "불필요한 평문 계정 파일 정리 및 EC2 배포 링크·데모 영상을 영문 체계로 패키징한 최종 정리 제출본",
            "folder": os.path.join(TAB2_DIR, "미니_프로젝트_김윤준 (2)"),
            "feedbacks": [os.path.join(TAB2_DIR, "미니_프로젝트_김윤준 (2)", "악성코드 사전 선별 시스템_피드백.pdf")],
        },
        {
            "id": "m_gumyeonghoe",
            "title": "LightGBM · YARA-X · 로지스틱 회귀 기반 PE 정적 분석 대시보드",
            "authors": ["구명회"],
            "grade": "A-",
            "score": 88,
            "summary": "EMBER2024 528피처 LightGBM + ReversingLabs YARA-X 14규칙 + L2 로지스틱 결합 모델 및 Streamlit 5탭 XAI 대시보드",
            "folder": os.path.join(TAB2_DIR, "미니프로젝트_구명회"),
            "feedbacks": [os.path.join(TAB2_DIR, "미니프로젝트_구명회", "미니프로젝트_피드백.pdf")],
        },
        {
            "id": "m_shinsanga",
            "title": "NASA IMS 기반 베어링 예지보전(PdM) 시스템",
            "authors": ["신상아"],
            "grade": "B+",
            "score": 85,
            "summary": "NASA IMS 진동(RMS·Kurtosis·FFT/STFT) 분석, RF 결함 분류(97.35%), 실측 MAD×5 경보 + 조건부 FFT 워터폴(Render·Streamlit Cloud 배포)",
            "folder": os.path.join(TAB2_DIR, "미니프로젝트_신상아"),
            "feedbacks": [os.path.join(TAB2_DIR, "미니프로젝트_신상아", "베어링예지보전_신상아_피드백.pdf")],
        },
        {
            "id": "m_leeinae",
            "title": "Windows PE 다중 엔진(ClamAV·YARA·LightGBM) 악성코드 탐지",
            "authors": ["이인애"],
            "grade": "B+",
            "score": 83,
            "summary": "BODMAS 134,435건 LightGBM(99.69%) + ClamAV + YARA Forge 10규칙 ThreadPool 병렬 스캔 및 후기 융합 아키텍처 구현",
            "folder": os.path.join(TAB2_DIR, "미니프로젝트_이인애"),
            "feedbacks": [os.path.join(TAB2_DIR, "미니프로젝트_이인애", "미니프로젝트ppt_피드백.pdf")],
        },
        {
            "id": "m_ohjuwon",
            "title": "안전감지자동화 119 호출서비스 (실시간 위기감지 & HITL)",
            "authors": ["오주원"],
            "grade": "B",
            "score": 79,
            "summary": "Edge PII Shield(원본 영상/음성 차단) → Kafka/LightGBM 5초 슬라이딩 윈도우 핫패스 → 10초 HITL 관제 유예 게이트 설계",
            "folder": os.path.join(TAB2_DIR, "미니프로젝트_오주원"),
            "feedbacks": [os.path.join(TAB2_DIR, "미니프로젝트_오주원", "안전감지자동화 119 호출서비스_수정_피드백.pdf")],
        },
    ]

    # ── TAB 3: 최종 프로젝트 기획안 ───────────────────────────────────────────
    t3_configs = [
        {
            "id": "p_mirimakum",
            "title": "AI 기반 업로드 파일 악성코드 사전 탐지·차단 시스템 (미리막음)",
            "authors": ["김윤준", "구명회", "이인애", "남유진", "백선병"],
            "grade": "A+",
            "score": 95,
            "summary": "PE·MS Office·HWP/HWPX 다형식 정적 추출과 선택적 CAPEv2(정상 2~5%) 동적 분석을 결합한 B2B MSP 보안 솔루션 기획서(35p)",
            "files": [os.path.join(TAB3_DIR, "미리막음_김윤준_구명회_이인애_남유진_백선병.pdf")],
            "feedbacks": [os.path.join(TAB3_DIR, "미리막음_김윤준_구명회_이인애_남유진_백선병_피드백.pdf")],
        },
        {
            "id": "p_baek",
            "title": "다변량 IoT 센서 스트림 기반 회전설비 사전감지 고장예측(PdM) 시스템",
            "authors": ["백선병 (협약: 쓰리뷰)"],
            "grade": "A-",
            "score": 88,
            "summary": "첨도·파고율 도메인 특성공학(기여도 40.2%)과 Random Forest 0.0569ms 초저지연 추론·SQLite·하이브리드 관제 대시보드 구축 기획서",
            "files": [os.path.join(TAB3_DIR, "회전설비_사전감지_고장예측_시스템_구축_기획서_백선병.pdf")],
            "feedbacks": [os.path.join(TAB3_DIR, "회전설비_사전감지_고장예측_시스템_구축_기획서_백선병_피드백.pdf")],
        },
        {
            "id": "p_baemin",
            "title": "배차의 민족 · 자동 화물 기사 매칭 플랫폼 개발 기획서",
            "authors": ["오주원", "신상아", "김지선", "방호원"],
            "grade": "A-",
            "score": 87,
            "summary": "KTDB 실데이터 기반 PostGIS/OSRM·Extreme Point 3D 적재·LightGBM·헝가리안 전역 배차 및 FSM/SHA-256 감사 로그 플랫폼 기획서",
            "files": [os.path.join(TAB3_DIR, "배차의 민족_오주원_신상아, 김지선, 방호원.pdf")],
            "feedbacks": [os.path.join(TAB3_DIR, "배차의 민족_오주원_신상아, 김지선, 방호원_피드백.pdf")],
        },
        {
            "id": "p_kimjehyung",
            "title": "화물 기사 자동 배정 플랫폼 기획서 (Automated Driver Dispatch)",
            "authors": ["김제형"],
            "grade": "B+",
            "score": 84,
            "summary": "운송사 10곳 직접 인터뷰 기반 소형 운송사 전용 SaaS, 도로교통법 제49조 정차 안전 UX 및 84개 자동 테스트를 완료한 실행형 기획서",
            "files": [os.path.join(TAB3_DIR, "Freight_Dispatch_Proposal_화물배차기획서_김제형.docx")],
            "feedbacks": [os.path.join(TAB3_DIR, "Freight_Dispatch_Proposal_화물배차기획서_김제형_피드백.pdf")],
        },
    ]

    def process_tab(tab_id: str, tab_label: str, source_folder: str, configs: list, extra_common=None):
        projects_out = []
        for cfg in configs:
            pid = cfg["id"]
            fb_set = {os.path.abspath(p) for p in cfg["feedbacks"]}
            raw_sources = []  # (abs_path, rel_path_in_proj, role)

            if "folder" in cfg:
                base_f = cfg["folder"]
                for dp, _, fns in os.walk(base_f):
                    for fn in sorted(fns):
                        fp = os.path.join(dp, fn)
                        if os.path.abspath(fp) in fb_set:
                            continue
                        rel = os.path.relpath(fp, base_f)
                        ext = os.path.splitext(fn)[1].lower()
                        role = "video" if ext == ".mp4" else ("audio" if ext == ".m4a" else ("dataset" if ext == ".csv" else "presentation"))
                        raw_sources.append((fp, rel, role))
            elif "folders" in cfg:
                for bf in cfg["folders"]:
                    bname = os.path.basename(bf)
                    for dp, _, fns in os.walk(bf):
                        for fn in sorted(fns):
                            fp = os.path.join(dp, fn)
                            if os.path.abspath(fp) in fb_set:
                                continue
                            rel = os.path.join(bname, os.path.relpath(fp, bf))
                            ext = os.path.splitext(fn)[1].lower()
                            role = "video" if ext == ".mp4" else ("audio" if ext == ".m4a" else "presentation")
                            raw_sources.append((fp, rel, role))
            elif "files" in cfg:
                for fp in cfg["files"]:
                    raw_sources.append((fp, os.path.basename(fp), "presentation"))

            for ex in cfg.get("extra_raw", []):
                if os.path.exists(ex):
                    raw_sources.append((ex, os.path.basename(ex), "raw_extra"))

            presentations = []
            videos = []
            audios = []
            datasets = []
            all_files = []
            zip_inputs = []

            for fp, rel, role in raw_sources:
                meta = register_file(fp, rel, tab_id, pid, role)
                all_files.append(meta)
                if role == "video":
                    videos.append(meta)
                elif role == "audio":
                    audios.append(meta)
                elif role == "dataset":
                    datasets.append(meta)
                elif role == "presentation":
                    presentations.append(meta)
                # CSV 19종(1.38GB)은 개별 다운로드 + 별도 CSV 통합 ZIP, 일반 산출물은 프로젝트 ZIP에 묶음
                if meta["ext"] != "csv":
                    zip_inputs.append((fp, rel))

            # 피드백 PDF 전용 처리 (4페이지 *_피드백.pdf만)
            feedbacks_out = []
            for fbp in cfg["feedbacks"]:
                fmeta = register_file(fbp, os.path.basename(fbp), tab_id, pid, "feedback")
                feedbacks_out.append(fmeta)
                all_files.append(fmeta)
                zip_inputs.append((fbp, os.path.basename(fbp)))

            # 프로젝트 전체 ZIP 생성 (Releases 호스팅)
            zip_url, zip_sz = make_bundle_zip(zip_inputs, f"bundle_{tab_id}_{pid}.zip")

            # 시연 영상 판정 (없으면 반드시 '미제공')
            demo_video = {
                "available": len(videos) > 0,
                "statusText": "제공" if len(videos) > 0 else "미제공",
                "files": videos,
            }

            projects_out.append({
                "id": pid,
                "title": cfg["title"],
                "authors": cfg["authors"],
                "grade": cfg["grade"],
                "score": cfg["score"],
                "summary": cfg["summary"],
                "presentations": presentations,
                "demoVideo": demo_video,
                "audios": audios,
                "datasets": datasets,
                "feedbacks": feedbacks_out,
                "allFiles": all_files,
                "bundleZipUrl": zip_url,
                "bundleZipBytes": zip_sz,
            })

        res = {
            "id": tab_id,
            "label": tab_label,
            "sourceFolder": source_folder,
            "projects": projects_out,
        }
        if extra_common:
            res["commonResources"] = extra_common
        return res

    # Tab 1 공통 배점 기준 파일 등록
    rubric_path = os.path.join(TAB1_DIR, "10월 23일 오후 14시 발표 배점.txt")
    rubric_meta = register_file(rubric_path, "10월 23일 오후 14시 발표 배점.txt", "stage1", "common", "rubric")
    rubric_text = open(rubric_path, "r", encoding="utf-8", errors="replace").read()

    tab1 = process_tab(
        "stage1",
        "데이터 분석 1차 프로젝트",
        "데이터 분석 1차 프로젝트 최종 자료(발표 자료  및  시연영상_피드백 포함)",
        t1_configs,
        extra_common=[{**rubric_meta, "content": rubric_text}]
    )
    tab2 = process_tab(
        "mini",
        "미니 프로젝트 발표자료",
        "미니 프로젝트 발표자료 제출 폴더 (11.5까지)",
        t2_configs,
    )
    tab3 = process_tab(
        "final",
        "최종 프로젝트 기획안",
        "최종 기획안",
        t3_configs,
    )

    tabs = [tab1, tab2, tab3]
    total_projects = sum(len(t["projects"]) for t in tabs)
    total_files = sum(len(p["allFiles"]) for t in tabs for p in t["projects"]) + 1  # +rubric
    video_yes = sum(1 for t in tabs for p in t["projects"] if p["demoVideo"]["available"])
    video_no = total_projects - video_yes
    total_feedbacks = sum(len(p["feedbacks"]) for t in tabs for p in t["projects"])

    manifest = {
        "siteTitle": "심화 : 심층 데이터 분석을 통한 개인 맞춤형 예측 자동화 서비스 솔루션 개발과정의 단계별 프로젝트들 발표자료 서비스",
        "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "repoUrl": f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}",
        "pagesUrl": f"https://{GITHUB_OWNER}.github.io/{GITHUB_REPO}/",
        "releaseTag": RELEASE_TAG,
        "stats": {
            "totalProjects": total_projects,
            "totalFiles": total_files,
            "videosAvailable": video_yes,
            "videosMissing": video_no,
            "totalFeedbackPdfs": total_feedbacks,
        },
        "tabs": tabs,
    }

    manifest_path = os.path.join(SITE_DIR, "data", "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 용량 요약 출력
    site_bytes = sum(os.path.getsize(os.path.join(dp, fn)) for dp, _, fns in os.walk(SITE_DIR) for fn in fns)
    rel_bytes = sum(os.path.getsize(os.path.join(dp, fn)) for dp, _, fns in os.walk(RELEASE_DIR) for fn in fns)
    rel_count = sum(len(fns) for _, _, fns in os.walk(RELEASE_DIR))
    print(f"✅ Build complete!")
    print(f"   Projects: {total_projects} | Files: {total_files} | Videos: {video_yes} yes / {video_no} 미제공 | Feedback PDFs: {total_feedbacks}")
    print(f"   site/ (GitHub Pages): {site_bytes/(1024*1024):.2f} MB")
    print(f"   release_assets/ ({rel_count} files for GitHub Releases): {rel_bytes/(1024*1024):.2f} MB")


if __name__ == "__main__":
    build_all()
