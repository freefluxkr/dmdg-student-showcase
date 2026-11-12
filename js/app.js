// app.js - DMDG ACADEMY SHOWCASE (Multi-Track Aurora Portal)
(() => {
  const MODE = window.PORTAL_MODE || { showScores: false, allowDownload: false, assetBase: "." };
  const SHOW_SCORES = Boolean(MODE.showScores);
  const ALLOW_DOWNLOAD = Boolean(MODE.allowDownload);
  const ASSET_BASE = String(MODE.assetBase || ".").replace(/\/$/, "");

  let manifest = null;
  let activeTrackId = "adv_cohort_2";
  let activeTabId = "adv2_analysis";
  let activeFilter = "all";
  let searchQuery = "";
  let currentProject = null;
  let activeSubtab = "presentations";
  let selectedFileIndex = 0;
  let selectedVideoIndex = 0;

  const $ = (id) => document.getElementById(id);

  function fmtBytes(bytes) {
    if (!bytes && bytes !== 0) return "-";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
  }

  function esc(str) {
    return String(str ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function gradeClass(g) {
    if (!g) return "g-a";
    if (g.includes("A+")) return "g-aplus";
    if (g.startsWith("A")) return "g-a";
    if (g.startsWith("B")) return "g-b";
    return "g-c";
  }

  function encodeUrlPath(u) {
    if (!u) return "#";
    if (u.startsWith("http://") || u.startsWith("https://")) return u;
    const clean = u.replace(/^\.\//, "");
    const encoded = clean.split("/").map((seg) => encodeURIComponent(seg)).join("/");
    return `${ASSET_BASE}/${encoded}`;
  }

  function pdfEmbedUrl(u) {
    const base = encodeUrlPath(u);
    return ALLOW_DOWNLOAD ? base : `${base}#toolbar=0&navpanes=0`;
  }

  function getTrack(trackId) {
    const tracks = manifest?.tracks || [];
    return tracks.find((t) => t.id === trackId) || tracks[tracks.length - 1] || null;
  }

  function getTrackTabs(trackId) {
    const tabs = manifest?.tabs || [];
    const matched = tabs.filter((t) => (t.trackId || "adv_cohort_2") === trackId);
    return matched.length ? matched : tabs;
  }

  function syncModeSwitchLinks() {
    const qs = `track=${encodeURIComponent(activeTrackId)}&tab=${encodeURIComponent(activeTabId)}`;
    const toPublic = $("btnToPublic");
    if (toPublic) toPublic.href = `../?${qs}&from=admin`;
    const backAdmin = $("btnBackToAdmin");
    if (backAdmin) backAdmin.href = `./admin/?${qs}`;
  }

  function syncUrlState() {
    try {
      const url = new URL(window.location.href);
      url.searchParams.set("track", activeTrackId);
      url.searchParams.set("tab", activeTabId);
      url.searchParams.delete("from");
      window.history.replaceState({}, "", url.toString());
    } catch (_) {
      /* ignore URL sync errors in restricted contexts */
    }
    syncModeSwitchLinks();
  }

  async function init() {
    const res = await fetch(`${ASSET_BASE}/data/manifest.json`);
    manifest = await res.json();

    if ($("repoLink")) $("repoLink").href = manifest.repoUrl;
    $("generatedAt").textContent = manifest.generatedAt;

    const params = new URLSearchParams(window.location.search);
    const hasAdminMode = ALLOW_DOWNLOAD || SHOW_SCORES;
    let hasAdminReturnAccess = false;
    try {
      if (hasAdminMode) {
        sessionStorage.setItem("dmdg_showcase_admin_session", "1");
      } else {
        const ref = (document.referrer || "").toLowerCase();
        hasAdminReturnAccess =
          params.get("from") === "admin" ||
          sessionStorage.getItem("dmdg_showcase_admin_session") === "1" ||
          ref.includes("/admin");
        if (hasAdminReturnAccess) {
          sessionStorage.setItem("dmdg_showcase_admin_session", "1");
        }
      }
    } catch (_) {
      hasAdminReturnAccess = params.get("from") === "admin";
    }

    if (!ALLOW_DOWNLOAD) {
      if ($("btnBackToAdmin")) {
        $("btnBackToAdmin").style.display = hasAdminReturnAccess ? "" : "none";
      }
      if ($("btnAllFilesIndex")) $("btnAllFilesIndex").style.display = "none";
      if ($("repoLink")) $("repoLink").style.display = "none";
      const dlSubtab = document.querySelector('#modalSubtabs [data-subtab="downloads"]');
      if (dlSubtab) dlSubtab.style.display = "none";
      if ($("kpiFilesLabel")) $("kpiFilesLabel").textContent = "등록된 자료 파일";
    } else {
      if ($("kpiFilesLabel")) $("kpiFilesLabel").textContent = "다운로드 제공 파일";
    }

    activeTrackId = manifest.defaultTrackId || "adv_cohort_2";

    const reqTrack = params.get("track");
    if (reqTrack && (manifest.tracks || []).some((tr) => tr.id === reqTrack)) {
      activeTrackId = reqTrack;
    }

    const reqTab = params.get("tab");
    if (reqTab && manifest.tabs.some((t) => t.id === reqTab)) {
      const tObj = manifest.tabs.find((t) => t.id === reqTab);
      if (tObj) {
        activeTrackId = tObj.trackId || activeTrackId;
        activeTabId = tObj.id;
      }
    } else {
      const tTabs = getTrackTabs(activeTrackId);
      activeTabId = tTabs[0]?.id || manifest.tabs[0]?.id || "stage1";
    }

    const pid = params.get("project");
    if (pid) {
      const pTab = manifest.tabs.find((t) => t.projects.some((p) => p.id === pid));
      if (pTab) {
        activeTrackId = pTab.trackId || activeTrackId;
        activeTabId = pTab.id;
      }
    }

    renderTrackSelector();
    updateTrackHeaderAndKpis();
    renderTabs();
    renderCommonBanner();
    renderGrid();
    bindEvents();
    syncModeSwitchLinks();
    if (params.has("from")) {
      syncUrlState();
    }

    if (pid) {
      const tab = manifest.tabs.find((t) => t.id === activeTabId);
      const proj = tab?.projects.find((p) => p.id === pid);
      if (proj) {
        $("modalSubtabs").style.display = "flex";
        openModal(proj, "presentations");
      }
    }
  }

  function renderTrackSelector() {
    const sel = $("trackSelect");
    const tracks = manifest.tracks || [];
    if (!sel) return;
    sel.innerHTML = tracks
      .map((tr) => `<option value="${esc(tr.id)}">${esc(tr.label)}</option>`)
      .join("");
    sel.value = activeTrackId;
  }

  function updateTrackHeaderAndKpis() {
    const tr = getTrack(activeTrackId);
    const tTabs = getTrackTabs(activeTrackId);
    if (tr) {
      $("siteTitle").textContent = tr.heroTitle || manifest.siteTitle;
      const guide = $("heroSubGuide");
      if (guide) {
        guide.innerHTML = `${esc(tr.subtitle)} <span style="color:#94a3b8;">(전체 6개 과정 · 총 ${manifest.stats.totalProjects}개 프로젝트 아카이브)</span>`;
      }
      const hint = $("trackPeriodHint");
      if (hint) {
        hint.textContent = tr.id === manifest.defaultTrackId
          ? `기본 선택 과정(최신) · ${tTabs.length}개 단계`
          : `${tr.shortLabel} · ${tTabs.length}개 단계`;
      }
    }

    const tProjs = tTabs.flatMap((t) => t.projects);
    const commonCount = tTabs.reduce((acc, t) => acc + ((t.commonResources || []).length), 0);
    const tFiles = tProjs.reduce((acc, p) => acc + p.allFiles.length, 0) + commonCount;
    const tVidYes = tProjs.filter((p) => p.demoVideo.available).length;
    const tVidNo = tProjs.length - tVidYes;
    const tFbs = tProjs.reduce((acc, p) => acc + p.feedbacks.length, 0);

    $("kpiProjects").textContent = `${tProjs.length}건 (전체 ${manifest.stats.totalProjects}건)`;
    $("kpiFiles").textContent = `${tFiles}개 (전체 ${manifest.stats.totalFiles}개)`;
    $("kpiVideos").textContent = `${tVidYes} 제공 / ${tVidNo} 미제공`;
    $("kpiFeedbacks").textContent = `${tFbs}건 (전체 ${manifest.stats.totalFeedbackPdfs}건)`;
  }

  function renderTabs() {
    const wrap = $("mainTabs");
    const tTabs = getTrackTabs(activeTrackId);
    if (!tTabs.some((t) => t.id === activeTabId) && tTabs.length) {
      activeTabId = tTabs[0].id;
    }
    wrap.innerHTML = tTabs
      .map((t) => {
        const active = t.id === activeTabId ? "active" : "";
        return `<button class="main-tab-btn ${active}" data-tab="${esc(t.id)}" type="button">
          <span>${esc(t.label)}</span>
          <span class="tab-count-pill">${t.projects.length}</span>
        </button>`;
      })
      .join("");
  }

  function openCommonResourceModal(resItem) {
    currentProject = null;
    $("modalTitle").textContent = `📌 공통 참고 자료 · ${resItem.name}`;
    $("modalSub").textContent = `${resItem.groupLabel || "교육과정 공통 자료"} · ${fmtBytes(resItem.sizeBytes)}`;
    $("modalSubtabs").style.display = "none";
    $("detailModal").classList.add("show");
    document.body.style.overflow = "hidden";

    if (resItem.role === "video" || resItem.ext === "mp4" || resItem.ext === "mov") {
      const vUrl = encodeUrlPath(resItem.previewUrl || resItem.downloadUrl);
      const dlBtn = ALLOW_DOWNLOAD
        ? `<a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(resItem.downloadUrl)}" download="${esc(resItem.name)}">⬇ 다운로드</a>`
        : `<span class="svc-pill svc-pdf" style="padding:0.3rem 0.75rem;">👁️ 스트리밍 열람 전용</span>`;
      const attrs = ALLOW_DOWNLOAD
        ? 'controls playsinline preload="metadata"'
        : 'controls playsinline preload="metadata" controlsList="nodownload" disablePictureInPicture oncontextmenu="return false;"';
      $("modalBody").innerHTML = `
        <div class="single-panel-scroll">
          <div class="video-player-wrap">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; margin-bottom:0.85rem;">
              <strong style="color:#6ee7b7; font-size:0.95rem;">🎬 ${esc(resItem.name)}</strong>
              ${dlBtn}
            </div>
            <video ${attrs} src="${vUrl}"></video>
          </div>
        </div>`;
      return;
    }

    $("modalBody").innerHTML = `
      <div class="viewer-pane" style="flex:1;">
        ${renderViewerToolbar(resItem)}
        ${renderFilePreviewElement(resItem)}
      </div>`;
  }

  function renderCommonBanner() {
    const wrap = $("commonBannerWrap");
    const tab = manifest.tabs.find((t) => t.id === activeTabId);
    const items = tab?.commonResources || [];
    if (!items.length) {
      wrap.innerHTML = "";
      return;
    }

    // 기존 심화 2기 1차 단일 배점표
    if (items.length === 1 && items[0].role === "rubric") {
      const r = items[0];
      const dlBtn = ALLOW_DOWNLOAD
        ? `<a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(r.downloadUrl)}" download="${esc(r.name)}">⬇ 배점표 다운로드</a>`
        : "";
      wrap.innerHTML = `
        <div class="common-info-banner">
          <div>
            <strong style="color:#67e8f9; font-size:0.9rem;">📌 공통 발표 평가 기준표 (${esc(r.name)})</strong>
            <div style="font-size:0.78rem; color:#cbd5e1; margin-top:2px;">
              총 200점 만점 — 분석모델(50) · 창의성(40) · 인사이트(30) · 사업화(30) · AI 의존도(20) · 데이터출처(10) · 현시점 서비스 가능(10) · 발표태도(10)
            </div>
          </div>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
            <a class="nav-pill-btn pill-cyan" href="${encodeUrlPath(r.previewUrl)}" target="_blank" rel="noopener noreferrer">👁️ 배점표 열람</a>
            ${dlBtn}
          </div>
        </div>`;
      return;
    }

    const photos = items.filter((i) => i.role === "photo");
    const videos = items.filter((i) => i.role === "video");
    const docs = items.filter((i) => i.role !== "photo" && i.role !== "video");

    const vidHtml = videos.length
      ? `<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.6rem;">
          <strong style="color:#6ee7b7; font-size:0.88rem;">🎬 ${esc(videos[0].groupLabel || "공통 시연 샘플 영상")}</strong>
          <div style="display:flex; gap:0.45rem; flex-wrap:wrap;">
            ${videos.map((v) => {
              const rawIdx = items.indexOf(v);
              const label = v.relPath || v.name;
              return `<button class="nav-pill-btn pill-cyan" data-common-idx="${rawIdx}" type="button">▶ ${esc(label)} (${fmtBytes(v.sizeBytes)})</button>`;
            }).join("")}
          </div>
        </div>`
      : "";

    const photoHtml = photos.length
      ? `<details open>
          <summary style="cursor:pointer; font-size:0.84rem; font-weight:800; color:#bae6fd; margin-bottom:0.55rem; user-select:none;">
            📸 2차 PRJ 현장 발표 사진 (${photos.length}장 · 5열 그리드 / 클릭하여 확대 또는 접기)
          </summary>
          <div class="common-photo-grid">
            ${photos.map((ph) => {
              const rawIdx = items.indexOf(ph);
              const noCtx = ALLOW_DOWNLOAD ? "" : 'oncontextmenu="return false;" draggable="false"';
              return `<button class="common-photo-card" data-common-idx="${rawIdx}" type="button" title="${esc(ph.name)}" style="padding:0; cursor:pointer;">
                <img src="${encodeUrlPath(ph.previewUrl)}" alt="${esc(ph.name)}" loading="lazy" ${noCtx} />
              </button>`;
            }).join("")}
          </div>
        </details>`
      : "";

    const docsHtml = docs.length
      ? `<details>
          <summary style="cursor:pointer; font-size:0.86rem; font-weight:800; color:#67e8f9; user-select:none;">
            📂 공통 배포 자료 · 데이터셋 · 일정 엑셀 (${docs.length}건 펼쳐보기)
          </summary>
          <div class="common-file-list" style="margin-top:0.65rem;">
            ${docs.map((d) => {
              const rawIdx = items.indexOf(d);
              const canPreview = Boolean(d.previewUrl) && !["csv", "zip"].includes(d.ext);
              const viewBtn = canPreview
                ? `<button class="nav-pill-btn pill-cyan" style="padding:0.25rem 0.6rem; font-size:0.74rem;" data-common-idx="${rawIdx}" type="button">👁️ 열람</button>`
                : "";
              const dlBtn = ALLOW_DOWNLOAD
                ? `<a class="nav-pill-btn pill-emerald" style="padding:0.25rem 0.6rem; font-size:0.74rem;" href="${encodeUrlPath(d.downloadUrl)}" download="${esc(d.name)}">⬇</a>`
                : (!canPreview ? `<span style="font-size:0.7rem; color:#94a3b8;">/admin 전용</span>` : "");
              return `<div class="common-file-pill">
                <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" title="${esc(d.relPath || d.name)}">
                  <strong>[${esc((d.ext || "").toUpperCase())}]</strong> ${esc(d.name)} <span style="color:#94a3b8;">(${fmtBytes(d.sizeBytes)})</span>
                </span>
                <span style="display:inline-flex; gap:0.35rem; flex-shrink:0;">${viewBtn}${dlBtn}</span>
              </div>`;
            }).join("")}
          </div>
        </details>`
      : "";

    wrap.innerHTML = `
      <div class="common-info-banner common-resources-box">
        ${vidHtml}
        ${photoHtml}
        ${docsHtml}
      </div>`;
  }

  function getFilteredProjects() {
    const tab = manifest.tabs.find((t) => t.id === activeTabId);
    if (!tab) return [];
    const q = searchQuery.trim().toLowerCase();
    return tab.projects.filter((p) => {
      if (activeFilter === "video-yes" && !p.demoVideo.available) return false;
      if (activeFilter === "video-no" && p.demoVideo.available) return false;
      if (!q) return true;
      const hay = [
        p.title,
        p.summary,
        ...p.authors,
        ...p.allFiles.map((f) => f.name),
      ]
        .join(" ")
        .toLowerCase();
      return hay.includes(q);
    });
  }

  function renderGrid() {
    const grid = $("projectsGrid");
    const list = getFilteredProjects();
    if (!list.length) {
      grid.innerHTML = `<div class="project-card" style="grid-column:1/-1; text-align:center; padding:2.5rem;">
        <div style="font-size:1.1rem; font-weight:800; color:#cbd5e1;">검색 또는 필터 조건에 해당하는 프로젝트가 없습니다.</div>
      </div>`;
      return;
    }

    grid.innerHTML = list
      .map((p) => {
        const authorsHtml = p.authors.map((a) => `<span class="author-chip">${esc(a)}</span>`).join("");
        const vAvailable = p.demoVideo.available;
        const vCountLabel = p.demoVideo.files.length > 1
          ? `▶ ${p.demoVideo.files.length}편 제공`
          : (vAvailable ? `▶ 제공 (${fmtBytes(p.demoVideo.files[0].sizeBytes)})` : "미제공");
        const videoPill = vAvailable
          ? `<span class="svc-pill svc-ok">${esc(vCountLabel)}</span>`
          : `<span class="svc-pill svc-missing">미제공</span>`;

        const presCount = p.presentations.length + p.datasets.length + p.audios.length;
        const presBadgeText = ALLOW_DOWNLOAD ? `${presCount}개 파일 열람·다운로드` : `${presCount}개 파일 열람 가능`;
        const fbName = p.feedbacks.length ? p.feedbacks[0].name : "피드백.pdf";

        const gradeHtml = SHOW_SCORES
          ? `<span class="grade-badge ${gradeClass(p.grade)}">${esc(p.grade)} · ${p.score}점</span>`
          : "";

        const zipHtml = ALLOW_DOWNLOAD
          ? `<a class="btn-zip-dl" href="${encodeUrlPath(p.bundleZipUrl)}" download="bundle_${p.id}.zip" title="프로젝트 파일 일괄 ZIP (${fmtBytes(p.bundleZipBytes)})">
              ⬇ ZIP (${fmtBytes(p.bundleZipBytes)})
            </a>`
          : "";

        const rowStyle = ALLOW_DOWNLOAD ? "" : 'style="grid-template-columns: 1fr;"';

        return `
        <article class="project-card">
          <div>
            <div class="card-top-meta">
              <div class="author-chips">${authorsHtml}</div>
              ${gradeHtml}
            </div>
            <h3 class="card-title">${esc(p.title)}</h3>
            <p class="card-summary">${esc(p.summary)}</p>

            <div class="service-status-panel">
              <div class="svc-row">
                <span class="svc-label">📄 내용 발표 자료</span>
                <span class="svc-pill svc-ok">${presBadgeText}</span>
              </div>
              <div class="svc-row">
                <span class="svc-label">🎬 시연 영상</span>
                ${videoPill}
              </div>
              <div class="svc-row">
                <span class="svc-label">🏛️ 피드백 리포트</span>
                <span class="svc-pill svc-pdf" title="${esc(fbName)}">PDF (${p.feedbacks.length}건) 제공</span>
              </div>
            </div>
          </div>

          <div class="card-actions-row" ${rowStyle}>
            <button class="btn-open-modal" data-open="${p.id}" type="button">🔍 자료 · 영상 · 피드백 열람</button>
            ${zipHtml}
          </div>
        </article>`;
      })
      .join("");
  }

  function openModal(proj, subtab = "presentations") {
    currentProject = proj;
    activeSubtab = subtab;
    selectedFileIndex = 0;
    selectedVideoIndex = 0;
    $("modalTitle").textContent = proj.title;
    $("modalSub").textContent = SHOW_SCORES
      ? `참여자: ${proj.authors.join(", ")} · 종합 평가: ${proj.grade} (${proj.score}점) · 총 ${proj.allFiles.length}개 파일`
      : `참여자: ${proj.authors.join(", ")} · 총 ${proj.allFiles.length}개 파일`;
    $("detailModal").classList.add("show");
    document.body.style.overflow = "hidden";
    updateSubtabsUI();
    renderModalBody();
  }

  function closeModal() {
    $("detailModal").classList.remove("show");
    document.body.style.overflow = "";
    $("modalBody").innerHTML = "";
  }

  function updateSubtabsUI() {
    document.querySelectorAll("#modalSubtabs .subtab-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.subtab === activeSubtab);
    });
  }

  function renderViewerToolbar(file) {
    const extBtn = file.externalUrl
      ? `<a class="nav-pill-btn pill-cyan" href="${esc(file.externalUrl)}" target="_blank" rel="noopener noreferrer">Git으로 접속</a>`
      : "";
    const newTabUrl = encodeUrlPath(file.previewUrl || file.downloadUrl);

    const actionButtons = ALLOW_DOWNLOAD
      ? `${extBtn}
         <a class="nav-pill-btn pill-cyan" href="${newTabUrl}" target="_blank" rel="noopener noreferrer">↗ 새 탭에서 보기</a>
         <a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(file.downloadUrl)}" download="${esc(file.name)}">⬇ 원본 다운로드</a>`
      : `${extBtn}
         <span class="svc-pill svc-pdf" style="padding:0.3rem 0.75rem;">👁️ 열람 전용 (다운로드 비활성화)</span>`;

    return `
      <div class="viewer-toolbar">
        <div style="font-size:0.82rem; font-weight:700; color:#e2e8f0; word-break:break-all;">
          ${esc(file.name)} <span style="color:#94a3b8;">(${fmtBytes(file.sizeBytes)})</span>
        </div>
        <div style="display:flex; gap:0.45rem; flex-wrap:wrap; align-items:center;">
          ${actionButtons}
        </div>
      </div>`;
  }

  function renderFilePreviewElement(file) {
    const url = encodeUrlPath(file.previewUrl || file.downloadUrl);
    if (file.ext === "png" || file.ext === "jpg" || file.ext === "jpeg") {
      const noCtx = ALLOW_DOWNLOAD ? "" : 'oncontextmenu="return false;" draggable="false"';
      return `<div class="single-panel-scroll" style="text-align:center;">
        <img src="${url}" alt="${esc(file.name)}" ${noCtx} style="max-width:100%; border-radius:12px; border:1px solid rgba(255,255,255,0.2);" />
      </div>`;
    }
    if (file.ext === "m4a") {
      const audioAttr = ALLOW_DOWNLOAD ? "controls" : 'controls controlsList="nodownload" oncontextmenu="return false;"';
      return `<div class="single-panel-scroll" style="text-align:center; padding-top:3rem;">
        <div style="font-size:1.1rem; font-weight:800; color:#bae6fd; margin-bottom:1rem;">🎧 AI 오디오 브리핑 (${esc(file.name)})</div>
        <audio ${audioAttr} style="width:100%; max-width:560px;" src="${url}"></audio>
      </div>`;
    }
    if (file.ext === "csv" || file.ext === "zip") {
      const labelType = file.ext.toUpperCase();
      const dlAction = ALLOW_DOWNLOAD
        ? `<a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(file.downloadUrl)}" download="${esc(file.name)}">⬇ ${labelType} 원본 다운로드</a>`
        : `<span class="svc-pill svc-missing" style="padding:0.4rem 0.95rem; font-size:0.84rem;">원천 파일(${labelType}) 다운로드는 관리자(/admin) 전용입니다</span>`;
      return `<div class="single-panel-scroll" style="text-align:center; padding-top:3rem;">
        <div style="font-size:1.05rem; font-weight:800; color:#fde68a; margin-bottom:0.6rem;">📊 대용량 원천 자료 (${esc(file.name)})</div>
        <p style="color:#cbd5e1; font-size:0.86rem;">파일 크기: ${fmtBytes(file.sizeBytes)}</p>
        ${dlAction}
      </div>`;
    }
    if (file.ext === "pdf") {
      return `<iframe class="viewer-frame" src="${pdfEmbedUrl(file.previewUrl || file.downloadUrl)}" title="${esc(file.name)}"></iframe>`;
    }
    return `<iframe class="viewer-frame" src="${url}" title="${esc(file.name)}" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>`;
  }

  function renderModalBody() {
    const body = $("modalBody");
    const p = currentProject;
    if (!p) return;

    if (activeSubtab === "presentations") {
      const files = [...p.presentations, ...p.audios, ...p.datasets];
      if (!files.length) {
        body.innerHTML = `<div class="single-panel-scroll">등록된 발표 자료가 없습니다.</div>`;
        return;
      }
      if (selectedFileIndex >= files.length) selectedFileIndex = 0;
      const cur = files[selectedFileIndex];

      const sidebar = files
        .map((f, idx) => {
          const act = idx === selectedFileIndex ? "active" : "";
          const badge = (f.ext || "file").toUpperCase();
          return `<button class="file-select-item ${act}" data-fidx="${idx}" type="button">
            <div class="file-item-name">[${esc(badge)}] ${esc(f.relPath || f.name)}</div>
            <div class="file-item-meta">${fmtBytes(f.sizeBytes)}</div>
          </button>`;
        })
        .join("");

      body.innerHTML = `
        <div class="split-viewer">
          <div class="file-sidebar">${sidebar}</div>
          <div class="viewer-pane">
            ${renderViewerToolbar(cur)}
            ${renderFilePreviewElement(cur)}
          </div>
        </div>`;
    } else if (activeSubtab === "video") {
      if (!p.demoVideo.available) {
        const audioNote = p.audios.length
          ? `<div style="margin-top:1rem;"><button class="nav-pill-btn pill-cyan" id="jumpToAudioBtn" type="button">🎧 대신 AI 오디오 브리핑(.m4a) 듣기</button></div>`
          : "";
        body.innerHTML = `
          <div class="single-panel-scroll">
            <div class="video-missing-box">
              <div class="video-missing-badge">미제공</div>
              <h3 style="margin:0 0 0.5rem; color:#ffffff;">시연 영상 파일(.mp4)이 제출되지 않았습니다</h3>
              <p style="margin:0; color:#cbd5e1; font-size:0.88rem;">
                본 프로젝트 폴더에는 시연 영상 파일이 포함되지 않아 <strong>미제공</strong>으로 표시됩니다.<br>
                상단 <strong>[내용 발표 자료]</strong> 또는 <strong>[피드백 (PDF)]</strong> 탭에서 상세 내용을 확인하실 수 있습니다.
              </p>
              ${audioNote}
            </div>
          </div>`;
        const jumpBtn = $("jumpToAudioBtn");
        if (jumpBtn) {
          jumpBtn.onclick = () => {
            activeSubtab = "presentations";
            selectedFileIndex = p.presentations.length;
            updateSubtabsUI();
            renderModalBody();
          };
        }
        return;
      }

      const vFiles = p.demoVideo.files;
      if (selectedVideoIndex >= vFiles.length) selectedVideoIndex = 0;
      const v = vFiles[selectedVideoIndex];
      const vUrl = encodeUrlPath(v.previewUrl || v.downloadUrl);
      const videoDlBtn = ALLOW_DOWNLOAD
        ? `<a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(v.downloadUrl)}" download="${esc(v.name)}">⬇ 시연영상 원본 다운로드</a>`
        : `<span class="svc-pill svc-pdf" style="padding:0.3rem 0.75rem;">👁️ 스트리밍 열람 전용</span>`;
      const videoAttrs = ALLOW_DOWNLOAD
        ? 'controls playsinline preload="metadata"'
        : 'controls playsinline preload="metadata" controlsList="nodownload" disablePictureInPicture oncontextmenu="return false;"';

      const switcher = vFiles.length > 1
        ? `<div class="video-switcher-bar">
            ${vFiles.map((vf, idx) => `<button class="filter-chip ${idx === selectedVideoIndex ? "active" : ""}" data-vidx="${idx}" type="button">🎬 영상 ${idx + 1}: ${esc(vf.name)} (${fmtBytes(vf.sizeBytes)})</button>`).join("")}
          </div>`
        : "";

      body.innerHTML = `
        <div class="single-panel-scroll">
          <div class="video-player-wrap">
            ${switcher}
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; margin-bottom:0.85rem;">
              <div>
                <strong style="color:#6ee7b7; font-size:0.95rem;">🎬 ${esc(v.name)}</strong>
                <span style="color:#94a3b8; font-size:0.8rem; margin-left:0.5rem;">(${fmtBytes(v.sizeBytes)})</span>
              </div>
              ${videoDlBtn}
            </div>
            <video ${videoAttrs} src="${vUrl}"></video>
          </div>
        </div>`;
    } else if (activeSubtab === "feedback") {
      const fbs = p.feedbacks;
      if (!fbs.length) {
        body.innerHTML = `<div class="single-panel-scroll">피드백 PDF가 없습니다.</div>`;
        return;
      }
      if (selectedFileIndex >= fbs.length) selectedFileIndex = 0;
      const cur = fbs[selectedFileIndex];
      const fbSrc = pdfEmbedUrl(cur.previewUrl);

      if (fbs.length === 1) {
        body.innerHTML = `
          <div class="viewer-pane" style="flex:1;">
            ${renderViewerToolbar(cur)}
            <iframe class="viewer-frame" src="${fbSrc}" title="${esc(cur.name)}"></iframe>
          </div>`;
      } else {
        const sidebar = fbs
          .map((f, idx) => `<button class="file-select-item ${idx === selectedFileIndex ? "active" : ""}" data-fidx="${idx}" type="button">
            <div class="file-item-name">[PDF] ${esc(f.name)}</div>
            <div class="file-item-meta">${fmtBytes(f.sizeBytes)} · 4페이지 기술 감사 리포트</div>
          </button>`)
          .join("");
        body.innerHTML = `
          <div class="split-viewer">
            <div class="file-sidebar">${sidebar}</div>
            <div class="viewer-pane">
              ${renderViewerToolbar(cur)}
              <iframe class="viewer-frame" src="${fbSrc}" title="${esc(cur.name)}"></iframe>
            </div>
          </div>`;
      }
    } else if (activeSubtab === "downloads") {
      if (!ALLOW_DOWNLOAD) {
        body.innerHTML = `<div class="single-panel-scroll">다운로드는 관리자(/admin) 페이지에서만 제공됩니다.</div>`;
        return;
      }
      const rows = p.allFiles
        .map((f) => `
          <tr>
            <td><strong>${esc(f.relPath || f.name)}</strong></td>
            <td><span class="author-chip">${esc((f.ext || "file").toUpperCase())}</span></td>
            <td>${fmtBytes(f.sizeBytes)}</td>
            <td>${f.hostedOn === "releases" ? "GitHub Releases" : "GitHub Pages"}</td>
            <td><a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(f.downloadUrl)}" download="${esc(f.name)}">⬇ 다운로드</a></td>
          </tr>`)
        .join("");

      body.innerHTML = `
        <div class="single-panel-scroll">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.75rem; margin-bottom:1rem;">
            <div>
              <h3 style="margin:0; color:#ffffff; font-size:1rem;">📦 전체 파일 목록 (${p.allFiles.length}개)</h3>
              <div style="font-size:0.78rem; color:#94a3b8;">모든 발표자료·영상·피드백 PDF·원천 데이터를 개별 또는 일괄 ZIP으로 다운로드할 수 있습니다.</div>
            </div>
            <a class="btn-zip-dl" href="${encodeUrlPath(p.bundleZipUrl)}" download="bundle_${p.id}.zip">
              📦 프로젝트 전체 ZIP 다운로드 (${fmtBytes(p.bundleZipBytes)})
            </a>
          </div>
          <table class="dl-table">
            <thead>
              <tr>
                <th>파일명 / 경로</th>
                <th>형식</th>
                <th>크기</th>
                <th>저장소</th>
                <th>다운로드</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>`;
    }
  }

  function openAllFilesIndexModal() {
    if (!ALLOW_DOWNLOAD) return;
    currentProject = null;
    $("modalTitle").textContent = "📦 전체 교육과정 프로젝트 자료 통합 인덱스";
    $("modalSub").textContent = `총 ${manifest.tracks.length}개 과정 · ${manifest.stats.totalProjects}개 프로젝트 · ${manifest.stats.totalFiles}개 파일 다운로드 지원`;
    $("modalSubtabs").style.display = "none";
    $("detailModal").classList.add("show");
    document.body.style.overflow = "hidden";

    const rows = manifest.tabs.flatMap((t) =>
      t.projects.map((p) => `
        <tr>
          <td><span class="author-chip">${esc(t.trackLabel || "심화 2기")}</span></td>
          <td><span class="author-chip">${esc(t.tabBadge || t.label)}</span></td>
          <td><strong>${esc(p.title)}</strong><div style="font-size:0.74rem; color:#94a3b8;">${esc(p.authors.join(", "))}</div></td>
          <td>${p.demoVideo.available ? '<span class="svc-pill svc-ok">제공</span>' : '<span class="svc-pill svc-missing">미제공</span>'}</td>
          <td>${p.allFiles.length}개</td>
          <td><a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(p.bundleZipUrl)}" download="bundle_${p.id}.zip">⬇ ZIP (${fmtBytes(p.bundleZipBytes)})</a></td>
        </tr>`)
    ).join("");

    $("modalBody").innerHTML = `
      <div class="single-panel-scroll">
        <table class="dl-table">
          <thead>
            <tr><th>교육과정</th><th>단계</th><th>프로젝트 / 참여자</th><th>시연영상</th><th>파일 수</th><th>일괄 다운로드</th></tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
  }

  function bindEvents() {
    if ($("trackSelect")) {
      $("trackSelect").addEventListener("change", (e) => {
        activeTrackId = e.target.value;
        const tTabs = getTrackTabs(activeTrackId);
        activeTabId = tTabs[0]?.id || activeTabId;
        activeFilter = "all";
        document.querySelectorAll("#filterChips .filter-chip").forEach((c) => c.classList.toggle("active", c.dataset.filter === "all"));
        updateTrackHeaderAndKpis();
        renderTabs();
        renderCommonBanner();
        renderGrid();
        syncUrlState();
      });
    }

    $("mainTabs").addEventListener("click", (e) => {
      const btn = e.target.closest(".main-tab-btn");
      if (!btn) return;
      activeTabId = btn.dataset.tab;
      renderTabs();
      renderCommonBanner();
      renderGrid();
      syncUrlState();
    });

    $("commonBannerWrap").addEventListener("click", (e) => {
      const btn = e.target.closest("[data-common-idx]");
      if (!btn) return;
      const tab = manifest.tabs.find((t) => t.id === activeTabId);
      const item = tab?.commonResources?.[Number(btn.dataset.commonIdx)];
      if (item) openCommonResourceModal(item);
    });

    $("filterChips").addEventListener("click", (e) => {
      const btn = e.target.closest(".filter-chip");
      if (!btn) return;
      activeFilter = btn.dataset.filter;
      document.querySelectorAll("#filterChips .filter-chip").forEach((c) => c.classList.remove("active"));
      btn.classList.add("active");
      renderGrid();
    });

    $("searchInput").addEventListener("input", (e) => {
      searchQuery = e.target.value;
      renderGrid();
    });

    $("projectsGrid").addEventListener("click", (e) => {
      const btn = e.target.closest("[data-open]");
      if (!btn) return;
      const pid = btn.dataset.open;
      const tab = manifest.tabs.find((t) => t.id === activeTabId);
      const proj = tab?.projects.find((p) => p.id === pid);
      if (proj) {
        $("modalSubtabs").style.display = "flex";
        openModal(proj, "presentations");
      }
    });

    $("modalSubtabs").addEventListener("click", (e) => {
      const btn = e.target.closest(".subtab-btn");
      if (!btn) return;
      activeSubtab = btn.dataset.subtab;
      selectedFileIndex = 0;
      selectedVideoIndex = 0;
      updateSubtabsUI();
      renderModalBody();
    });

    $("modalBody").addEventListener("click", (e) => {
      const item = e.target.closest("[data-fidx]");
      if (item) {
        selectedFileIndex = Number(item.dataset.fidx);
        renderModalBody();
        return;
      }
      const vbtn = e.target.closest("[data-vidx]");
      if (vbtn) {
        selectedVideoIndex = Number(vbtn.dataset.vidx);
        renderModalBody();
      }
    });

    if ($("btnAllFilesIndex")) {
      $("btnAllFilesIndex").addEventListener("click", openAllFilesIndexModal);
    }
    $("modalCloseBtn").addEventListener("click", closeModal);
    $("detailModal").addEventListener("click", (e) => {
      if (e.target === $("detailModal")) closeModal();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && $("detailModal").classList.contains("show")) closeModal();
    });
  }

  init().catch((err) => {
    console.error(err);
    $("projectsGrid").innerHTML = `<div class="project-card">데이터 로드 오류: ${esc(err.message)}</div>`;
  });
})();
