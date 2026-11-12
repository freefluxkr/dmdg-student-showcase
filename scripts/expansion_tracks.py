# -*- coding: utf-8 -*-
"""
expansion_tracks.py
LG Uplus Why Not 1기·2기, [KDT] 해커톤 1·2기, 삼성 AXI 6개월 과정, AI·데이터 심화 1기,
그리고 AI·데이터 심화 2기 프로젝트 분석 기획안(0차) 구성을 정의한다.
"""
import os
from feedback_gen import data_adv, data_axi_kdt, data_lg

SRC_2026 = r"C:\Users\PC\Downloads\20261112"
PRJ_ROOT = r"c:\DMDG_Jobs\DMDG_PRJ\dmdg-student-showcase"
FB_DIR = os.path.join(PRJ_ROOT, "generated_feedbacks")
TRANSCODED_DIR = os.path.join(PRJ_ROOT, "transcoded_videos")
EXTRACTED_DIR = os.path.join(PRJ_ROOT, "extracted_sources")


def _must_exist(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required source file missing: {path}")
    return path


def _fb_path(entry: dict) -> str:
    return _must_exist(os.path.join(FB_DIR, os.path.basename(entry["out_pdf"])))


def _grade_short(grade_label: str) -> str:
    # "EXCELLENT (A+)" -> "A+", "GREAT (A-)" -> "A-"
    if "(" in grade_label and ")" in grade_label:
        return grade_label.split("(")[-1].split(")")[0].strip()
    return grade_label.strip()


def _split_authors(authors_str: str) -> list[str]:
    if "·" in authors_str:
        # e.g. "1조 우티달 (박종현·권정인·신새봄·권정인)" or "방호원 (심화 2기)"
        if "(" in authors_str:
            prefix, rest = authors_str.split("(", 1)
            prefix = prefix.strip()
            inner = rest.rsplit(")", 1)[0].strip()
            if "·" in inner:
                members = [m.strip() for m in inner.split("·") if m.strip()]
                return [prefix] + members if prefix else members
            return [prefix] if prefix else [inner]
        return [p.strip() for p in authors_str.split("·") if p.strip()]
    if "(" in authors_str:
        return [authors_str.split("(")[0].strip()]
    return [authors_str.strip()]


def _lg_summary(entry: dict) -> str:
    return f"{entry['subtitle']} — {entry['strength_title']}"


def _collect_lg1_weekly_reports() -> dict[int, list[str]]:
    """LG1 3차 팀별 업무현황 47개 파일을 팀(1~5)으로 정확히 분류."""
    base = os.path.join(EXTRACTED_DIR, "3차 PRJ (최종)", "팀별 업무현황")
    teams: dict[int, list[str]] = {1: [], 2: [], 3: [], 4: [], 5: []}
    matched_count = 0
    for dp, _, fns in os.walk(base):
        for fn in sorted(fns):
            fp = os.path.join(dp, fn)
            low = fn.lower()
            if "1_aicc" in low or "1팀_aicc" in low or "aicc1" in low:
                teams[1].append(fp)
            elif "자율주행" in low:
                teams[2].append(fp)
            elif "4팀" in low:
                teams[4].append(fp)
            elif "5조" in low or "5팀" in low or fn.startswith("일일업무현황_24"):
                teams[5].append(fp)
            elif "3조" in low or "iptv 채널 추천" in low:
                teams[3].append(fp)
            else:
                raise ValueError(f"Unclassified LG1 weekly report file: {fp}")
            matched_count += 1
    if matched_count != 47:
        raise AssertionError(f"Expected 47 weekly reports, got {matched_count}")
    for t in teams.values():
        t.sort()
    return teams


def _build_card(
    pid: str,
    fb_entry: dict,
    files: list[tuple[str, str, str]],
    authors: list[str] | None = None,
    summary: str | None = None,
    extra_note: str | None = None,
) -> dict:
    checked_files = [(_must_exist(fp), rel, role) for fp, rel, role in files]
    fb_pdf = _fb_path(fb_entry)
    return {
        "id": pid,
        "title": fb_entry["title"],
        "authors": authors if authors is not None else _split_authors(fb_entry["authors"]),
        "grade": _grade_short(fb_entry["grade_label"]),
        "score": int(fb_entry["score"]),
        "summary": summary or _lg_summary(fb_entry),
        "extraNote": extra_note,
        "explicitFiles": checked_files,
        "feedbacks": [fb_pdf],
        "isExpansion": True,
    }


def _make_lg1_tabs(register_file_fn) -> tuple[list[dict], list[dict]]:
    lg = data_lg.LG_PLANS  # 0..4 stage1, 5..9 stage2, 10..14 stage3
    ex1 = os.path.join(EXTRACTED_DIR, "1차 PRJ", "1차 서비스 기획 발표자료")
    ex2_base = os.path.join(EXTRACTED_DIR, "2차 PRJ")
    ex2_design = os.path.join(ex2_base, "1 기본 설계")
    ex2_demo = os.path.join(ex2_base, "3 발표자료 및 데모영상")
    ex3_final = os.path.join(EXTRACTED_DIR, "3차 PRJ 최종 발표 자료")
    raw_lg1 = os.path.join(SRC_2026, "LG Uplus Why Not 1기")

    # ── Stage 1 Common Datafiles ──
    df_dir = os.path.join(raw_lg1, "1차 PRJ", "1차 서비스 기획 및 설계_datafiles")
    s1_common = []
    for dp, _, fns in os.walk(df_dir):
        for fn in sorted(fns):
            if fn.startswith("~$"):
                continue
            fp = os.path.join(dp, fn)
            rel = os.path.relpath(fp, df_dir)
            ext = os.path.splitext(fn)[1].lower()
            role = "dataset" if ext in (".csv", ".zip") else "presentation"
            meta = register_file_fn(fp, f"공통_1차_datafiles/{rel}", "lg1_stage1", "common", role, is_expansion=True)
            meta["groupLabel"] = "1차 서비스 기획 및 설계 공통 Datafiles"
            s1_common.append(meta)

    # ── Stage 1 Projects (Teams 1..5) ──
    s1_teams = [
        _build_card(
            "lg1_s1_t1", lg[0],
            authors=["1조 우티달", "정연진", "박종현", "신새봄", "권정인", "이중찬"],
            files=[
                (os.path.join(ex1, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "[KDT] 아이디어 기획서_우티달.pdf"), "1조_우티달/[KDT] 아이디어 기획서_우티달.pdf", "presentation"),
                (os.path.join(ex1, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "MBC_8월_5주(1).pdf"), "1조_우티달/MBC_8월_5주(1).pdf", "presentation"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage1_team1.mp4"), "1조_우티달/1차발표_우티달_web720p.mp4", "video"),
            ],
        ),
        _build_card(
            "lg1_s1_t2", lg[1],
            authors=["2조 TEAM Allll", "이현행", "신종현", "김다란솔", "임기빈", "박준현", "정인엽"],
            files=[
                (os.path.join(ex1, "2_고객상담이력_이현행_신종현_김다란솔_임기빈_박준현_정인엽", "고객 상담 이력 자동 분석 서비스 기획서(최종본)_TEAM Allll.pdf"), "2조_AICC/고객 상담 이력 자동 분석 서비스 기획서(최종본)_TEAM Allll.pdf", "presentation"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage1_team2.mp4"), "2조_AICC/1차발표_TEAMAllll_web720p.mp4", "video"),
            ],
        ),
        _build_card(
            "lg1_s1_t3", lg[2],
            authors=["3조 자율주행", "한은선", "김준희", "박장원", "김나현", "김승엽", "김동혁"],
            files=[
                (os.path.join(ex1, "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁", "계획보고서.pdf"), "3조_자율주행/계획보고서.pdf", "presentation"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage1_team3.mp4"), "3조_자율주행/1차발표_자율주행_web720p.mp4", "video"),
            ],
        ),
        _build_card(
            "lg1_s1_t4", lg[3],
            authors=["4조(5조) 한번에쇼핑", "전서영", "박시원", "임세연", "이지선", "이상민"],
            files=[
                (os.path.join(ex1, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "Project_1차_IPTV_채널-홈쇼핑_연계_추천_서비스_5조.pdf"), "4조_한번에쇼핑/Project_1차_IPTV_채널-홈쇼핑_연계_추천_서비스_5조.pdf", "presentation"),
                (os.path.join(ex1, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "1차-프로젝트.pptx"), "4조_한번에쇼핑/1차-프로젝트.pptx", "presentation"),
                (os.path.join(ex1, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "LG U+ 사용자 이용 행태 분석 5조", "nts.txt"), "4조_한번에쇼핑/nts.txt", "raw_extra"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage1_team4.mp4"), "4조_한번에쇼핑/1차발표_한번에쇼핑_web720p.mp4", "video"),
                (os.path.join(ex1, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "VideoEditor_20240822_043534.mp4"), "4조_한번에쇼핑/VideoEditor_20240822_043534.mp4", "video"),
            ],
        ),
        _build_card(
            "lg1_s1_t5", lg[4],
            authors=["5조 DATA로", "곽현철", "양현우", "조진형", "서정임", "김승훈"],
            files=[
                (os.path.join(ex1, "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈", "프로젝트 기획서(모바일 TV 이용 로그 데이터 기반 콘텐츠 추천 서비스 개발)_240823.pdf"), "5조_DATA로/프로젝트 기획서(모바일 TV 이용 로그 데이터 기반 콘텐츠 추천 서비스 개발)_240823.pdf", "presentation"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage1_team5.mp4"), "5조_DATA로/1차발표_DATA로_web720p.mp4", "video"),
            ],
        ),
    ]

    # ── Stage 2 Common (Photos + Sample Groupware Video) ──
    s2_common = []
    photo_dir = os.path.join(raw_lg1, "2차 PRJ", "2 발표사진")
    for fn in sorted(os.listdir(photo_dir)):
        if fn.lower().endswith((".jpg", ".jpeg", ".png")):
            meta = register_file_fn(os.path.join(photo_dir, fn), f"2차_발표사진/{fn}", "lg1_stage2", "common", "photo", is_expansion=True)
            meta["groupLabel"] = "2차 PRJ 현장 발표 사진"
            s2_common.append(meta)
    sample_vid = _must_exist(os.path.join(TRANSCODED_DIR, "lg1_stage2_sample_groupware.mp4"))
    s_meta = register_file_fn(sample_vid, "인트라넷_기반_그룹웨어_개발_시연_web720p.mp4", "lg1_stage2", "common", "video", is_expansion=True)
    s_meta["groupLabel"] = "2차 PRJ 시연 동영상 샘플 (인트라넷 그룹웨어)"
    s2_common.append(s_meta)

    # ── Stage 2 Projects (Teams 1..5) ──
    s2_teams = [
        _build_card(
            "lg1_s2_t1", lg[5],
            authors=["1조 우티달", "정연진", "박종현", "신새봄", "권정인", "이중찬"],
            files=[
                (os.path.join(raw_lg1, "2차 PRJ", "1 기본 설계", "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬.pdf"), "1_기본설계_우티달.pdf", "presentation"),
                (os.path.join(ex2_demo, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "2차 프로젝트.pdf"), "2차_프로젝트_발표자료.pdf", "presentation"),
                (os.path.join(ex2_demo, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "1. 크롤링 영상.mp4"), "1._크롤링_영상.mp4", "video"),
                (os.path.join(ex2_demo, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "2. API 영상.mp4"), "2._API_영상.mp4", "video"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage2_team1_talk.mp4"), "2차_현장발표_1팀_우티달_web720p.mp4", "video"),
            ],
        ),
        _build_card(
            "lg1_s2_t2", lg[6],
            authors=["2조 TEAM Allll", "이현행", "신종현", "김다란솔", "임기빈", "박준현", "정인엽"],
            files=[
                (os.path.join(raw_lg1, "2차 PRJ", "1 기본 설계", "2_고객상담이력_이현행_신종현_김다란솔_임기빈_박준현_정인엽.pdf"), "1_기본설계_AICC.pdf", "presentation"),
                (os.path.join(ex2_demo, "2_고객상담이력_이현행_신종현_김다란솔_임기빈_박준현_정인엽", "LG_U+_why_not_SW_camp_AICC조_발표자료.pdf"), "LG_U+_why_not_SW_camp_AICC조_발표자료.pdf", "presentation"),
                (os.path.join(ex2_demo, "2_고객상담이력_이현행_신종현_김다란솔_임기빈_박준현_정인엽", "LG_U+_why_not_SW_camp_AICC조_시연영상.mp4"), "LG_U+_why_not_SW_camp_AICC조_시연영상.mp4", "video"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage2_team2_talk.mp4"), "2차_현장발표_2팀_AICC_web720p.mp4", "video"),
            ],
        ),
        _build_card(
            "lg1_s2_t3", lg[7],
            authors=["3조(2조) D오디", "한은선", "김준희", "박장원", "김나현", "김승엽", "김동혁"],
            files=[
                (os.path.join(raw_lg1, "2차 PRJ", "1 기본 설계", "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁.pdf"), "1_기본설계_자율주행.pdf", "presentation"),
                (os.path.join(ex2_demo, "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁", "2차_최종_2조_D오디", "2차_최종본_2초_자율주행_D오디.pdf"), "2차_최종본_자율주행_D오디.pdf", "presentation"),
                (os.path.join(ex2_demo, "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁", "2차_최종_2조_D오디", "2차_최종본_PPT_2조_자율주행_D오디.pptx"), "2차_최종본_PPT_D오디.pptx", "presentation"),
                (os.path.join(ex2_demo, "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁", "2차_최종_2조_D오디", "2차_최종본_기획서_2조_자율주행_D오디.hwp"), "2차_최종본_기획서_D오디.hwp", "presentation"),
                (os.path.join(TRANSCODED_DIR, "lg2_team3_dodi_demo.mp4"), "2차_시연영상_자율주행_D오디_web720p.mp4", "video"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage2_team3_talk.mp4"), "2차_현장발표_3조_자율주행_web720p.mp4", "video"),
            ],
        ),
        _build_card(
            "lg1_s2_t4", lg[8],
            authors=["4조(5조) 한번에쇼핑", "전서영", "박시원", "임세연", "이지선", "이상민"],
            files=[
                (os.path.join(ex2_design, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "5조 데이터 파이프라인.png"), "5조_데이터_파이프라인.png", "presentation"),
                (os.path.join(ex2_design, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "[KDT] 5조 프로젝트-인프라 아키텍처 최종.drawio.png"), "5조_인프라_아키텍처.png", "presentation"),
                (os.path.join(ex2_demo, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "5조 IPTV 채널 홈쇼핑 연계 추천 서비스 최종본.pdf"), "5조_IPTV_홈쇼핑_최종본.pdf", "presentation"),
                (os.path.join(ex2_demo, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "5조 IPTV 채널 홈쇼핑 연계 추천 서비스.pdf"), "5조_IPTV_홈쇼핑_발표본.pdf", "presentation"),
                (os.path.join(ex2_demo, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "5조 IPTV 홈쇼핑 시연영상.mp4"), "5조_IPTV_홈쇼핑_시연영상.mp4", "video"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage2_team4_talk.mp4"), "2차_현장발표_5조_홈쇼핑_web720p.mp4", "video"),
            ],
        ),
        _build_card(
            "lg1_s2_t5", lg[9],
            authors=["5조(4조) DATA로", "곽현철", "양현우", "조진형", "서정임", "김승훈"],
            files=[
                (os.path.join(raw_lg1, "2차 PRJ", "1 기본 설계", "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈.pdf"), "1_기본설계_DATA로.pdf", "presentation"),
                (os.path.join(ex2_demo, "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈", "DATA로_2차프로젝트_241030", "1. 발표자료", "DATA로_모바일TV 이용자 로그데이터 기반 콘텐츠 추천시스템_2차프로젝트_241030.pdf"), "DATA로_2차발표.pdf", "presentation"),
                (os.path.join(ex2_demo, "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈", "DATA로_2차프로젝트_241030", "1. 발표자료", "DATA로_모바일TV 이용자 로그데이터 기반 콘텐츠 추천시스템_2차프로젝트_241030.pptx"), "DATA로_2차발표.pptx", "presentation"),
                (os.path.join(ex2_demo, "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈", "DATA로_2차프로젝트_241030", "2. 시연영상", "시연영상_241030.mp4"), "DATA로_2차_시연영상.mp4", "video"),
                (os.path.join(TRANSCODED_DIR, "lg1_stage2_team5_talk.mp4"), "2차_현장발표_DATA로_web720p.mp4", "video"),
            ],
        ),
    ]

    # ── Stage 3 Common Workbooks & Reference Papers ──
    s3_dir = os.path.join(raw_lg1, "3차 PRJ (최종)")
    s3_common = []
    for fn in ["LG Uplus 3차 최종 프로젝트 내용 및 진행상황.xlsx", "팀_일일업무현황_예시.xlsx", "팀_통합_스케줄.xlsx", "향후 일정.xlsx"]:
        fp = _must_exist(os.path.join(s3_dir, fn))
        meta = register_file_fn(fp, f"3차_운영관리/{fn}", "lg1_stage3", "common", "presentation", is_expansion=True)
        meta["groupLabel"] = "3차 PRJ 통합 진행상황·일정 엑셀"
        s3_common.append(meta)
    ref_dir = os.path.join(s3_dir, "제공 내용")
    for fn in sorted(os.listdir(ref_dir)):
        fp = os.path.join(ref_dir, fn)
        meta = register_file_fn(fp, f"3차_제공자료/{fn}", "lg1_stage3", "common", "presentation", is_expansion=True)
        meta["groupLabel"] = "3차 PRJ 참조 논문·채용 링크"
        s3_common.append(meta)

    weekly = _collect_lg1_weekly_reports()
    s3_specs = [
        ("lg1_s3_t1", lg[11], ["1팀 TEAM ALLL", "박준현", "김다란솔", "이현행", "임기빈", "신종현", "정인엽"], os.path.join(ex3_final, "1팀-20250414T050723Z-001", "1팀", "1팀_발표자료_최종.pdf"), 1),
        ("lg1_s3_t2", lg[12], ["2팀 자율주행", "김승엽", "한은선", "김준희", "박장원", "김나현", "김동혁"], os.path.join(ex3_final, "2팀-20250414T050739Z-001", "2팀", "2팀_발표자료_최종.pdf"), 2),
        ("lg1_s3_t3", lg[10], ["3팀 우티달", "박종현", "권정인", "신새봄", "이중찬", "정연진"], os.path.join(ex3_final, "3팀-20250414T050742Z-001", "3팀", "3팀_발표자료_최종.pdf"), 3),
        ("lg1_s3_t4", lg[13], ["4팀 DATA로", "김승훈", "곽현철", "조진형", "양현우", "서정임"], os.path.join(ex3_final, "4팀-20250414T050743Z-001", "4팀", "4팀_발표자료_최종.pdf"), 4),
        ("lg1_s3_t5", lg[14], ["5팀 배할머니네 손주들", "박시원", "전서영", "이지선", "이상민", "임세연"], os.path.join(ex3_final, "5팀-20250414T050745Z-001", "5팀", "5팀_발표자료_최종.pdf"), 5),
    ]
    s3_teams = []
    for pid, fb_e, authors, fpdf, tno in s3_specs:
        files = [(fpdf, os.path.basename(fpdf), "presentation")]
        for wp in weekly[tno]:
            files.append((wp, f"일일업무현황/{os.path.basename(wp)}", "presentation"))
        s3_teams.append(_build_card(pid, fb_e, authors=authors, files=files))

    tabs_spec = [
        {"id": "lg1_stage1", "label": "1차 · 서비스 기획·설계", "tabBadge": "1차 기획", "sourceFolder": "LG Uplus Why Not 1기/1차 PRJ", "projects": s1_teams, "commonResources": s1_common, "trackId": "lg_whynot_1", "trackLabel": "1. LG Uplus Why Not 1기"},
        {"id": "lg1_stage2", "label": "2차 · 기본설계·시연영상", "tabBadge": "2차 시연", "sourceFolder": "LG Uplus Why Not 1기/2차 PRJ", "projects": s2_teams, "commonResources": s2_common, "trackId": "lg_whynot_1", "trackLabel": "1. LG Uplus Why Not 1기"},
        {"id": "lg1_stage3", "label": "3차 최종 · 팀별 업무현황", "tabBadge": "3차 최종", "sourceFolder": "LG Uplus Why Not 1기/3차 PRJ (최종)", "projects": s3_teams, "commonResources": s3_common, "trackId": "lg_whynot_1", "trackLabel": "1. LG Uplus Why Not 1기"},
    ]
    return [], tabs_spec


def _make_lg2_tabs() -> list[dict]:
    lg = data_lg.LG_PLANS  # 15..19 mid, 20..24 final
    raw_lg2 = os.path.join(SRC_2026, "LG Uplus Why Not 2기")

    mid_teams = [
        _build_card(
            "lg2_m_t1", lg[15],
            authors=["1조 우티달", "정연진", "박종현", "신새봄", "권정인", "이중찬"],
            files=[
                (os.path.join(raw_lg2, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "[KDT] 아이디어 기획서_우티달.pdf"), "[KDT] 아이디어 기획서_우티달.pdf", "presentation"),
                (os.path.join(raw_lg2, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "MBC_8월_5주(1).pdf"), "MBC_8월_5주(1).pdf", "presentation"),
                (os.path.join(raw_lg2, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "2차 프로젝트.pdf"), "2차 프로젝트.pdf", "presentation"),
                (os.path.join(raw_lg2, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "1. 크롤링 영상.mp4"), "1. 크롤링 영상.mp4", "video"),
                (os.path.join(raw_lg2, "1_IPTV 채널 추천_정연진_박종현_신새봄_권정인_이중찬", "2. API 영상.mp4"), "2. API 영상.mp4", "video"),
            ],
        ),
        _build_card(
            "lg2_m_t2", lg[16],
            authors=["2조 TEAM Allll", "이현행", "신종현", "김다란솔", "임기빈", "박준현", "정인엽"],
            files=[
                (os.path.join(raw_lg2, "2_고객상담이력_이현행_신종현_김다란솔_임기빈_박준현_정인엽", "고객 상담 이력 자동 분석 서비스 기획서(최종본)_TEAM Allll.pdf"), "고객 상담 이력 자동 분석 서비스 기획서.pdf", "presentation"),
                (os.path.join(raw_lg2, "2_고객상담이력_이현행_신종현_김다란솔_임기빈_박준현_정인엽", "LG_U+_why_not_SW_camp_AICC조_발표자료.pdf"), "AICC조_발표자료.pdf", "presentation"),
                (os.path.join(raw_lg2, "2_고객상담이력_이현행_신종현_김다란솔_임기빈_박준현_정인엽", "LG_U+_why_not_SW_camp_AICC조_시연영상.mp4"), "AICC조_시연영상.mp4", "video"),
            ],
        ),
        _build_card(
            "lg2_m_t3", lg[17],
            authors=["3조(2조) D오디", "한은선", "김준희", "박장원", "김나현", "김승엽", "김동혁"],
            files=[
                (os.path.join(raw_lg2, "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁", "계획보고서.pdf"), "계획보고서.pdf", "presentation"),
                (os.path.join(raw_lg2, "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁 (1)", "2차_최종본_2초_자율주행_D오디.pdf"), "2차_최종본_자율주행_D오디.pdf", "presentation"),
                (os.path.join(raw_lg2, "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁 (1)", "2차_최종본_PPT_2조_자율주행_D오디.pptx"), "2차_최종본_PPT_D오디.pptx", "presentation"),
                (os.path.join(raw_lg2, "3_자율주행_한은선_김준희_박장원_김나현_김승엽_김동혁 (1)", "2차_최종본_기획서_2조_자율주행_D오디.hwp"), "2차_최종본_기획서_D오디.hwp", "presentation"),
                (os.path.join(TRANSCODED_DIR, "lg2_team3_dodi_demo.mp4"), "2차_최종본_2조_자율주행_D오디_web720p.mp4", "video"),
            ],
        ),
        _build_card(
            "lg2_m_t4", lg[18],
            authors=["4조(5조) 한눈에쇼핑", "전서영", "박시원", "임세연", "이지선", "이상민"],
            files=[
                (os.path.join(raw_lg2, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "Project_1차_IPTV_채널-홈쇼핑_연계_추천_서비스_5조.pdf"), "Project_1차_홈쇼핑_5조.pdf", "presentation"),
                (os.path.join(raw_lg2, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "1차-프로젝트.pptx"), "1차-프로젝트.pptx", "presentation"),
                (os.path.join(raw_lg2, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "LG U+ 사용자 이용 행태 분석 5조", "nts.txt"), "nts.txt", "raw_extra"),
                (os.path.join(raw_lg2, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민 (1)", "5조 IPTV 채널 홈쇼핑 연계 추천 서비스 최종본.pdf"), "5조_홈쇼핑_최종본.pdf", "presentation"),
                (os.path.join(raw_lg2, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민 (1)", "5조 IPTV 채널 홈쇼핑 연계 추천 서비스.pdf"), "5조_홈쇼핑_발표본.pdf", "presentation"),
                (os.path.join(raw_lg2, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민", "VideoEditor_20240822_043534.mp4"), "1차_홈쇼핑_시연영상.mp4", "video"),
                (os.path.join(raw_lg2, "4_TV이용행태_전서영_박시원_임세연_이지선_이상민 (1)", "5조 IPTV 홈쇼핑 시연영상.mp4"), "5조_IPTV_홈쇼핑_시연영상.mp4", "video"),
            ],
        ),
        _build_card(
            "lg2_m_t5", lg[19],
            authors=["5조(4조) DATA로", "곽현철", "양현우", "조진형", "서정임", "김승훈"],
            files=[
                (os.path.join(raw_lg2, "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈 (1)", "프로젝트 기획서(모바일 TV 이용 로그 데이터 기반 콘텐츠 추천 서비스 개발)_240823.pdf"), "프로젝트_기획서_DATA로.pdf", "presentation"),
                (os.path.join(raw_lg2, "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈 (1)", "1. 발표자료", "DATA로_모바일TV 이용자 로그데이터 기반 콘텐츠 추천시스템_2차프로젝트_241030.pdf"), "DATA로_2차발표.pdf", "presentation"),
                (os.path.join(raw_lg2, "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈 (1)", "1. 발표자료", "DATA로_모바일TV 이용자 로그데이터 기반 콘텐츠 추천시스템_2차프로젝트_241030.pptx"), "DATA로_2차발표.pptx", "presentation"),
                (os.path.join(raw_lg2, "5_TV이용행태_곽현철_양현우_조진형_서정임_김승훈 (1)", "2. 시연영상", "시연영상_241030.mp4"), "시연영상_241030.mp4", "video"),
            ],
        ),
    ]

    final_teams = [
        _build_card("lg2_f_t1", lg[20], authors=["1팀 TEAM ALLL", "박준현", "김다란솔", "이현행", "임기빈", "신종현", "정인엽"], files=[(os.path.join(raw_lg2, "1팀-20250414T050723Z-001", "1팀_발표자료_최종.pdf"), "1팀_발표자료_최종.pdf", "presentation")]),
        _build_card("lg2_f_t2", lg[21], authors=["2팀 자율주행", "김승엽", "한은선", "김준희", "박장원", "김나현", "김동혁"], files=[(os.path.join(raw_lg2, "2팀-20250414T050739Z-001", "2팀_발표자료_최종.pdf"), "2팀_발표자료_최종.pdf", "presentation")]),
        _build_card("lg2_f_t3", lg[22], authors=["3팀 우티달", "박종현", "권정인", "신새봄", "이중찬", "정연진"], files=[(os.path.join(raw_lg2, "3팀-20250414T050742Z-001", "3팀_발표자료_최종.pdf"), "3팀_발표자료_최종.pdf", "presentation")]),
        _build_card("lg2_f_t4", lg[23], authors=["4팀 DATA로", "김승훈", "곽현철", "조진형", "양현우", "서정임"], files=[(os.path.join(raw_lg2, "4팀-20250414T050743Z-001", "4팀_발표자료_최종.pdf"), "4팀_발표자료_최종.pdf", "presentation")]),
        _build_card("lg2_f_t5", lg[24], authors=["5팀 배할머니네 손주들", "박시원", "전서영", "이지선", "이상민", "임세연"], files=[(os.path.join(raw_lg2, "5팀-20250414T050745Z-001", "5팀_발표자료_최종.pdf"), "5팀_발표자료_최종.pdf", "presentation")]),
    ]

    return [
        {"id": "lg2_mid", "label": "1·2차 기획·시연", "tabBadge": "2기 · 1·2차", "sourceFolder": "LG Uplus Why Not 2기", "projects": mid_teams, "trackId": "lg_whynot_2", "trackLabel": "2. LG Uplus Why Not 2기"},
        {"id": "lg2_final", "label": "3차 최종 발표", "tabBadge": "2기 · 최종", "sourceFolder": "LG Uplus Why Not 2기/최종발표", "projects": final_teams, "trackId": "lg_whynot_2", "trackLabel": "2. LG Uplus Why Not 2기"},
    ]


def _make_kdt_tabs() -> list[dict]:
    ak = data_axi_kdt.AXI_KDT_PLANS  # 4..8 KDT 2기, 9..10 KDT 1기
    d2 = os.path.join(SRC_2026, "[KDT] 해커톤 2기")
    d1 = os.path.join(SRC_2026, "KDT_해커톤 공모전 1기")

    kdt2 = [
        _build_card("kdt2_01", ak[4], authors=["우티달 참조자료 (2기)"], files=[(os.path.join(d2, "MBC_8월_5주(1).pdf"), "MBC_8월_5주(1).pdf", "presentation")]),
        _build_card("kdt2_02", ak[5], authors=["테스트웍스 KVQA (2기)"], files=[(os.path.join(d2, "[KDT] 시각장애인을 위한 한국어 기반 시각적 질의응답 데이터셋.pdf"), "[KDT] 시각장애인을 위한 한국어 기반 시각적 질의응답 데이터셋.pdf", "presentation")]),
        _build_card("kdt2_03", ak[6], authors=["우티달 (2기)", "박종현", "권정인", "신새봄", "이중찬", "정연진"], files=[(os.path.join(d2, "[KDT] 아이디어 기획서_우티달.pdf"), "[KDT] 아이디어 기획서_우티달.pdf", "presentation")]),
        _build_card("kdt2_04", ak[7], authors=["테스트웍스 SideGuide (2기)"], files=[(os.path.join(d2, "[KDT] 이동취약계층을 위한 대규모 인도보행 데이터셋.pdf"), "[KDT] 이동취약계층을 위한 대규모 인도보행 데이터셋.pdf", "presentation")]),
        _build_card("kdt2_05", ak[8], authors=["권정인 (2기)"], files=[(os.path.join(d2, "[KDT] 해커톤_아이디어_권정인_수정본.pdf"), "[KDT] 해커톤_아이디어_권정인_수정본.pdf", "presentation")]),
    ]
    kdt1 = [
        _build_card("kdt1_01", ak[9], authors=["우티달 (1기)", "박종현", "권정인", "신새봄", "이중찬", "정연진"], files=[(os.path.join(d1, "[KDT] 아이디어 기획서_우티달.pdf"), "[KDT] 아이디어 기획서_우티달.pdf", "presentation")]),
        _build_card("kdt1_02", ak[10], authors=["권정인 (1기)"], files=[(os.path.join(d1, "[KDT] 해커톤_아이디어_권정인_수정본.pdf"), "[KDT] 해커톤_아이디어_권정인_수정본.pdf", "presentation")]),
    ]
    return [
        {"id": "kdt_g2", "label": "[KDT] 해커톤 2기 (5건)", "tabBadge": "KDT 2기", "sourceFolder": "[KDT] 해커톤 2기", "projects": kdt2, "trackId": "kdt_hackathon", "trackLabel": "3. [KDT] 해커톤"},
        {"id": "kdt_g1", "label": "해커톤 공모전 1기 (2건)", "tabBadge": "KDT 1기", "sourceFolder": "KDT_해커톤 공모전 1기", "projects": kdt1, "trackId": "kdt_hackathon", "trackLabel": "3. [KDT] 해커톤"},
    ]


def _make_axi_tabs() -> list[dict]:
    ak = data_axi_kdt.AXI_KDT_PLANS  # 0..3 AXI
    d_axi = os.path.join(SRC_2026, "삼성AXI 6개월 최종 발표 자료")
    axi_projects = [
        _build_card("axi_01", ak[0], authors=["팀 oneplus3 (ADA)", "김효중", "김나연", "어창선", "한정현"], files=[(os.path.join(d_axi, "ADA_김효중 김나연 어창선 한정현.pdf"), "ADA_김효중 김나연 어창선 한정현.pdf", "presentation")]),
        _build_card("axi_02", ak[1], authors=["팀 GYEOL", "김명선", "송병갑"], files=[(os.path.join(d_axi, "GYEOL_김명선 송병갑.pdf"), "GYEOL_김명선 송병갑.pdf", "presentation")]),
        _build_card("axi_03", ak[2], authors=["Team Heartbeats", "이현표", "이새봄", "송지현", "현다은"], files=[(os.path.join(d_axi, "Heartbeats_이현표 이새봄 송지현 현다은.pdf"), "Heartbeats_이현표 이새봄 송지현 현다은.pdf", "presentation")]),
        _build_card("axi_04", ak[3], authors=["팀 강씨네", "강초롱", "강홍지"], files=[(os.path.join(d_axi, "강씨네_강초롱 강홍지.pdf"), "강씨네_강초롱 강홍지.pdf", "presentation")]),
    ]
    return [
        {"id": "axi_final", "label": "최종 발표 자료 (4팀)", "tabBadge": "삼성 AXI", "sourceFolder": "삼성AXI 6개월 최종 발표 자료", "projects": axi_projects, "trackId": "samsung_axi", "trackLabel": "4. 삼성 AXI 6개월 과정"},
    ]


def _make_adv_plan_tabs() -> tuple[list[dict], list[dict]]:
    adv = data_adv.ADV_PLANS  # 0..7 심화 2기, 8..9 심화 1기
    d_adv = os.path.join(SRC_2026, "심화 2 프로젝트 분석 기획안")

    adv2_specs = [
        ("adv2_p01", adv[0], ["방호원"], "1002_대중교통_방호원.pdf", "1002_대중교통_방호원.txt"),
        ("adv2_p02", adv[1], ["신상아"], "261002_유학생증가세분석_신상아.pdf", "261002_유학생증가세분석_신상아.txt"),
        ("adv2_p03", adv[2], ["오주원"], "나라별 외국인 소비 패턴 및 1인당 소비 금액_프로젝트 로드맵_오주원.pdf", "나라별 외국인 소비 패턴 및 1인당 소비 금액_프로젝트 로드맵_오주원.txt"),
        ("adv2_p04", adv[3], ["남유진"], "남유진_빅데이터_활용_프로젝트.pdf", "남유진_빅데이터_활용_프로젝트.txt"),
        ("adv2_p05", adv[4], ["김지선"], "넷플릭스_K드라마_수익성_분석_김지선.pdf", "넷플릭스_K드라마_수익성_분석_김지선.txt"),
        ("adv2_p06", adv[5], ["백선병"], "대한민국 외국인 증가에 따른 현상에 대한 데이터 분석_백선병.pdf", "대한민국 외국인 증가에 따른 현상에 대한 데이터 분석_백선병.txt"),
        ("adv2_p07", adv[6], ["정호연"], "대한민국_외국인_증가와_K팝_정호연20261002.pdf", "대한민국_외국인_증가와_K팝_정호연20261002.txt"),
        ("adv2_p08", adv[7], ["조진훈"], "미쉐린셰프_한식가치_규제이슈_조진훈.pdf", "미쉐린셰프_한식가치_규제이슈_조진훈.txt"),
    ]
    adv2_projects = [
        _build_card(
            pid, fb_e, authors=authors,
            files=[
                (os.path.join(d_adv, pdf_fn), pdf_fn, "presentation"),
                (os.path.join(d_adv, txt_fn), txt_fn, "raw_extra"),
            ],
        )
        for pid, fb_e, authors, pdf_fn, txt_fn in adv2_specs
    ]

    adv1_projects = [
        _build_card("adv1_p01", adv[8], authors=["김종훈"], files=[(os.path.join(d_adv, "프로젝트 기획안 - 김종훈.pdf"), "프로젝트 기획안 - 김종훈.pdf", "presentation")]),
        _build_card("adv1_p02", adv[9], authors=["조유정"], files=[(os.path.join(d_adv, "프로젝트 기획안 - 조유정.pdf"), "프로젝트 기획안 - 조유정.pdf", "presentation")]),
    ]

    adv1_tabs = [
        {"id": "adv1_plan", "label": "프로젝트 분석 기획안 (2명)", "tabBadge": "심화 1기", "sourceFolder": "심화 1기 개인 분석 기획안", "projects": adv1_projects, "trackId": "adv_cohort_1", "trackLabel": "5. AI·데이터 심화 1기"},
    ]
    adv2_analysis_tabs = [
        {"id": "adv2_analysis", "label": "0차 · 프로젝트 분석 기획안 (8명)", "tabBadge": "0차 기획안", "sourceFolder": "심화 2 프로젝트 분석 기획안", "projects": adv2_projects, "trackId": "adv_cohort_2", "trackLabel": "6. AI·데이터 심화 2기"},
    ]
    return adv1_tabs, adv2_analysis_tabs


def get_tracks_metadata() -> list[dict]:
    return [
        {
            "id": "lg_whynot_1",
            "label": "1. LG Uplus Why Not 1기 (2024.08~12 · 15건)",
            "shortLabel": "LG U+ 1기",
            "heroTitle": "LG Uplus Why Not SW Camp 1기 프로젝트 아카이브",
            "subtitle": "1차 서비스 기획·공통 데이터(Datafiles) → 2차 구현·현장 시연영상·발표사진 → 3차 최종 발표 및 팀별 일일업무현황",
            "tabIds": ["lg1_stage1", "lg1_stage2", "lg1_stage3"],
        },
        {
            "id": "lg_whynot_2",
            "label": "2. LG Uplus Why Not 2기 (2024.10~2025 · 10건)",
            "shortLabel": "LG U+ 2기",
            "heroTitle": "LG Uplus Why Not SW Camp 2기 프로젝트 아카이브",
            "subtitle": "2기 독립 기수 아카이브 · 1·2차 기획/시연 및 3차 최종 발표 10건 (1기와 별도 기수 유지)",
            "tabIds": ["lg2_mid", "lg2_final"],
        },
        {
            "id": "kdt_hackathon",
            "label": "3. [KDT] 해커톤 1·2기 (7건)",
            "shortLabel": "KDT 해커톤",
            "heroTitle": "[KDT] AI·데이터 해커톤 1·2기 아카이브",
            "subtitle": "KDT 해커톤 2기 데이터셋·아이디어 5건 & KDT 해커톤 공모전 1기 2건",
            "tabIds": ["kdt_g2", "kdt_g1"],
        },
        {
            "id": "samsung_axi",
            "label": "4. 삼성 AXI 6개월 과정 (4팀)",
            "shortLabel": "삼성 AXI",
            "heroTitle": "삼성 AXI 6개월 과정 최종 프로젝트 쇼케이스",
            "subtitle": "에이전트 자동화·폐쇄망 제조 AI·임상급 정서케어·건설 산재예측 최우수 최종 발표 4팀",
            "tabIds": ["axi_final"],
        },
        {
            "id": "adv_cohort_1",
            "label": "5. AI·데이터 심화 1기 (2명)",
            "shortLabel": "심화 1기",
            "heroTitle": "AI·데이터 심화 1기 개인 분석 기획안",
            "subtitle": "도심 바람길·미세먼지 공간기후 연구(김종훈) 및 태양 활동·우주방사선 천체데이터 분석(조유정)",
            "tabIds": ["adv1_plan"],
        },
        {
            "id": "adv_cohort_2",
            "label": "6. AI·데이터 심화 2기 (최신 · 26건)",
            "shortLabel": "심화 2기",
            "heroTitle": "AI·데이터 심화 2기 단계별 프로젝트 발표 쇼케이스",
            "subtitle": "0차 프로젝트 분석 기획안(8명) → 1차 프로젝트(6팀) → 미니 프로젝트(8건) → 2차 최종 기획안(4건)",
            "tabIds": ["adv2_analysis", "stage1", "mini", "final"],
        },
    ]


def build_expansion_raw_tabs(register_file_fn) -> tuple[list[dict], list[dict], list[dict]]:
    """
    Returns (pre_adv2_tabs, adv2_prefix_tabs, tracks_meta)
    """
    _, lg1_tabs = _make_lg1_tabs(register_file_fn)
    lg2_tabs = _make_lg2_tabs()
    kdt_tabs = _make_kdt_tabs()
    axi_tabs = _make_axi_tabs()
    adv1_tabs, adv2_analysis_tabs = _make_adv_plan_tabs()
    pre_adv2_tabs = lg1_tabs + lg2_tabs + kdt_tabs + axi_tabs + adv1_tabs
    return pre_adv2_tabs, adv2_analysis_tabs, get_tracks_metadata()
