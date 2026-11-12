# -*- coding: utf-8 -*-
"""
Shared 4-page A4 Technical Review & Audit Report Renderer for Showcase Expansion.
"""
from .pdf_builder import esc, grade_pill_class


def render_4page_report(p: dict) -> str:
    grade_cls = grade_pill_class(p["grade_label"])
    footer_left = p.get("footer_left") or f"DMDG Technical Review & Quality Audit Report — {p['authors']}"
    cert_title = p.get("cert_title", "DMDG (당목담글) 교육사업본부 & AI 연구소 기술인증위원회")
    review_org = p.get("review_org", "DMDG 기술심사위원회<br>(Sherlock & Craig)")
    course_label = p.get("course_label", "TECHNICAL REVIEW & QUALITY AUDIT REPORT")

    sb_html = ""
    for lbl, val in p["sub_scores"]:
        sb_html += (
            f'<div class="sb-item">'
            f'<span class="sb-label">{esc(lbl)}</span>'
            f'<div class="sb-bar-wrap"><div class="sb-bar-fill" style="width:{val}%;"></div></div>'
            f'<span class="sb-val">{val}</span>'
            f'</div>'
        )

    files_rows = "".join(
        f'<tr><td style="font-weight:700;word-break:break-all;">{esc(fn)}</td>'
        f'<td>{esc(tp)}</td>'
        f'<td><span class="status-pill {"pill-green" if "양호" in st or "완벽" in st or "우수" in st else "pill-amber" if "보완" in st or "개선" in st else "pill-red"}">{esc(st)}</span></td>'
        f'<td>{esc(sm)}</td></tr>'
        for fn, tp, st, sm in p["files_table"]
    )

    tech_html = ""
    for tb in p["tech_blocks"]:
        tech_html += (
            f'<div class="item-card">'
            f'<div class="item-heading"><span class="item-title">{esc(tb["heading"])}</span>'
            f'<span class="status-pill {tb["badge_cls"]}">{esc(tb["badge"])}</span></div>'
        )
        if "table" in tb:
            headers, rows = tb["table"]
            th = "".join(f"<th>{esc(h)}</th>" for h in headers)
            trs = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in rows)
            tech_html += f'<table class="audit-table" style="margin-bottom:4px;"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'
        if "bullets" in tb:
            lis = "".join(f"<li>{b}</li>" for b in tb["bullets"])
            tech_html += f'<ul class="audit-list">{lis}</ul>'
        tech_html += "</div>"

    fix_rows = "".join(
        f'<tr><td style="font-weight:700;">{esc(cat)}</td><td>{esc(iss)}</td><td style="color:#0f172a;">{esc(sol)}</td></tr>'
        for cat, iss, sol in p["fix_table"]
    )

    code_blocks = "".join(
        f'<div class="code-title">{esc(ct)}</div><div class="code-box">{esc(cb)}</div>'
        for ct, cb in p["fixes_code"]
    )

    strat_html = "".join(
        f'<div class="strat-card"><div class="strat-top"><span class="strat-title">{esc(st)}</span>'
        f'<span class="status-pill {sc}">{esc(sb)}</span></div>'
        f'<div class="strat-body">{esc(sbd)}</div></div>'
        for st, sb, sc, sbd in p["strategies"]
    )

    chk_rows = "".join(
        f'<tr><td><strong>{esc(cat)}</strong></td><td><strong>{esc(it)}</strong></td><td>{esc(dt)}</td>'
        f'<td><span class="status-pill {pc}">{esc(st)}</span></td></tr>'
        for cat, it, dt, st, pc in p["checklist"]
    )

    from .pdf_builder import CSS_TEMPLATE

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{esc(p['title'])} 피드백 보고서</title>
<style>{CSS_TEMPLATE}</style>
</head>
<body>

<section class="page">
  <div class="hero-banner">
    <div class="hero-tag">{esc(course_label)}</div>
    <div class="hero-title">{esc(p['title'])}</div>
    <div class="hero-subtitle">{esc(p['subtitle'])}</div>
    <div class="hero-meta-grid">
      <div>
        <div class="meta-label">작성 팀 / 작성자</div>
        <div class="meta-value">{esc(p['authors'])}</div>
      </div>
      <div>
        <div class="meta-label">검토 대상 문서</div>
        <div class="meta-value">{esc(p['file_count'])}</div>
      </div>
      <div>
        <div class="meta-label">검토 일시</div>
        <div class="meta-value">{esc(p['review_date'])}</div>
      </div>
      <div>
        <div class="meta-label">검토 기관 / 담당</div>
        <div class="meta-value">{review_org}</div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-card-dark">
      <span class="grade-pill {grade_cls}">{esc(p['grade_label'])}</span>
      <div class="score-number">{p['score']}</div>
      <div class="score-denom">TOTAL SCORE / 100</div>
    </div>
    <div class="score-breakdown">{sb_html}</div>
  </div>

  <div class="sec-header">
    <span class="sec-title">1. 총평 및 핵심 심사 의견 (Executive Summary)</span>
    <span class="sec-badge">{esc(p['exec_badge'])}</span>
  </div>

  <div class="callout callout-green">
    <div class="callout-title">🏆 {esc(p['strength_title'])}</div>
    <div class="callout-body">{esc(p['strength_body'])}</div>
  </div>

  <div class="callout callout-red">
    <div class="callout-title">⚠️ {esc(p['defect_title'])}</div>
    <div class="callout-body">{esc(p['defect_body'])}</div>
  </div>

  <table class="audit-table">
    <thead>
      <tr>
        <th style="width:33%;">검토 대상 파일명</th>
        <th style="width:15%;">파일 형식</th>
        <th style="width:16%;">검증 상태</th>
        <th style="width:36%;">핵심 검증 결과 요약</th>
      </tr>
    </thead>
    <tbody>{files_rows}</tbody>
  </table>

  <div class="page-footer">
    <span>{esc(footer_left)}</span>
    <span>Page 1 of 4</span>
  </div>
</section>

<section class="page">
  <div class="sec-header">
    <span class="sec-title">{esc(p['tech_sec_title'])}</span>
    <span class="sec-badge">정밀 감사</span>
  </div>

  {tech_html}

  <div class="callout callout-indigo" style="margin-top:4px;">
    <div class="callout-title">💡 {esc(p.get('p2_note_title', '기술심사위원회 종합 소견'))}</div>
    <div class="callout-body">{esc(p.get('p2_note_body', '기획·데이터 파이프라인·모델 평가·실시간 서빙 간 정합성을 확보하고 3장의 교정 솔루션을 즉시 적용하면 실무 수준의 완성도와 데모 설득력을 크게 높일 수 있습니다.'))}</div>
  </div>

  <div class="page-footer">
    <span>{esc(footer_left)}</span>
    <span>Page 2 of 4</span>
  </div>
</section>

<section class="page">
  <div class="sec-header">
    <span class="sec-title">3. 개선 솔루션 및 기술 보완 가이드 (Actionable Fixes)</span>
    <span class="sec-badge">교정 솔루션</span>
  </div>

  <div class="item-heading" style="margin-bottom:4px;">
    <span class="item-title">📌 영역별 핵심 보완 항목</span>
    <span class="status-pill pill-amber">Action Items</span>
  </div>

  <table class="audit-table">
    <thead>
      <tr>
        <th style="width:21%;">해당 절 / 영역</th>
        <th style="width:36%;">발견된 문제점 및 보완점</th>
        <th style="width:43%;">수정 제안 (Action Item)</th>
      </tr>
    </thead>
    <tbody>{fix_rows}</tbody>
  </table>

  {code_blocks}

  <div class="page-footer">
    <span>{esc(footer_left)}</span>
    <span>Page 3 of 4</span>
  </div>
</section>

<section class="page">
  <div class="sec-header">
    <span class="sec-title">4. 실전 고도화 전략 &amp; 최종 검증 체크리스트 (Success Strategy)</span>
    <span class="sec-badge">검증 가이드</span>
  </div>

  <div class="strategy-grid">{strat_html}</div>

  <div style="font-size: 9.4pt; font-weight: 800; color: #0f172a; margin: 6px 0 5px 0;">
    📋 최종 완결성 점검 체크리스트 (Sherlock Final Checklist)
  </div>

  <table class="audit-table">
    <thead>
      <tr>
        <th style="width:12%;">구분</th>
        <th style="width:24%;">점검 항목</th>
        <th style="width:49%;">점검 내용 및 기준</th>
        <th style="width:15%;">상태</th>
      </tr>
    </thead>
    <tbody>{chk_rows}</tbody>
  </table>

  <div class="cert-box">
    <div class="cert-org">{esc(cert_title)}</div>
    <div class="cert-desc">
      본 기술 검토서는 제출된 기획서·발표자료·산출물의 데이터 정합성, 모델링 타당성, 아키텍처 완성도 및 발표 설득력을 종합 평가하여 발행되었습니다.<br>
      <strong>{esc(p['authors'])}</strong> 의 지속적인 성장과 성공적인 프로젝트 완수를 응원합니다.
    </div>
  </div>

  <div class="page-footer">
    <span>{esc(footer_left)}</span>
    <span>Page 4 of 4</span>
  </div>
</section>

</body>
</html>
"""

