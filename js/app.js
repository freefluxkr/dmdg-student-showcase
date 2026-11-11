// app.js - DMDG Aurora Student Projects Showcase
(() => {
  let manifest = null;
  let activeTabId = "stage1";
  let activeFilter = "all";
  let searchQuery = "";
  let currentProject = null;
  let activeSubtab = "presentations";
  let selectedFileIndex = 0;

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
    return u.split("/").map((seg, i) => (i === 0 && seg === ".") ? "." : encodeURIComponent(seg)).join("/");
  }

  async function init() {
    const res = await fetch("./data/manifest.json");
    manifest = await res.json();

    $("siteTitle").textContent = manifest.siteTitle;
    $("repoLink").href = manifest.repoUrl;
    $("generatedAt").textContent = manifest.generatedAt;

    const s = manifest.stats;
    $("kpiProjects").textContent = `${s.totalProjects}건`;
    $("kpiFiles").textContent = `${s.totalFiles}개`;
    $("kpiVideos").textContent = `${s.videosAvailable} 제공 / ${s.videosMissing} 미제공`;
    $("kpiFeedbacks").textContent = `${s.totalFeedbackPdfs}건`;

    const params = new URLSearchParams(window.location.search);
    if (params.get("tab") && manifest.tabs.some((t) => t.id === params.get("tab"))) {
      activeTabId = params.get("tab");
    }

    renderTabs();
    renderCommonBanner();
    renderGrid();
    bindEvents();

    const pid = params.get("project");
    if (pid) {
      const tab = manifest.tabs.find((t) => t.projects.some((p) => p.id === pid));
      if (tab) {
        activeTabId = tab.id;
        renderTabs();
        renderCommonBanner();
        renderGrid();
        const proj = tab.projects.find((p) => p.id === pid);
        if (proj) openModal(proj, "presentations");
      }
    }
  }

  function renderTabs() {
    const wrap = $("mainTabs");
    wrap.innerHTML = manifest.tabs
      .map((t) => {
        const active = t.id === activeTabId ? "active" : "";
        return `<button class="main-tab-btn ${active}" data-tab="${t.id}" type="button">
          <span>${esc(t.label)}</span>
          <span class="tab-count-pill">${t.projects.length}</span>
        </button>`;
      })
      .join("");
  }

  function renderCommonBanner() {
    const wrap = $("commonBannerWrap");
    const tab = manifest.tabs.find((t) => t.id === activeTabId);
    if (!tab || !tab.commonResources || !tab.commonResources.length) {
      wrap.innerHTML = "";
      return;
    }
    const r = tab.commonResources[0];
    wrap.innerHTML = `
      <div class="common-info-banner">
        <div>
          <strong style="color:#67e8f9; font-size:0.9rem;">📌 공통 발표 평가 기준표 (${esc(r.name)})</strong>
          <div style="font-size:0.78rem; color:#cbd5e1; margin-top:2px;">
            총 200점 만점 — 분석모델(50) · 창의성(40) · 인사이트(30) · 사업화(30) · AI 의존도(20) · 데이터출처(10) · 현시점 서비스 가능(10) · 발표태도(10)
          </div>
        </div>
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
          <a class="nav-pill-btn pill-cyan" href="${encodeUrlPath(r.previewUrl)}" target="_blank">👁️ 배점표 열람</a>
          <a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(r.downloadUrl)}" download="${esc(r.name)}">⬇ 배점표 다운로드</a>
        </div>
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
        const vSize = vAvailable ? ` (${fmtBytes(p.demoVideo.files[0].sizeBytes)})` : "";
        const videoPill = vAvailable
          ? `<span class="svc-pill svc-ok">▶ 제공${vSize}</span>`
          : `<span class="svc-pill svc-missing">미제공</span>`;

        const presCount = p.presentations.length + p.datasets.length + p.audios.length;
        const fbName = p.feedbacks.length ? p.feedbacks[0].name : "피드백.pdf";

        return `
        <article class="project-card">
          <div>
            <div class="card-top-meta">
              <div class="author-chips">${authorsHtml}</div>
              <span class="grade-badge ${gradeClass(p.grade)}">${esc(p.grade)} · ${p.score}점</span>
            </div>
            <h3 class="card-title">${esc(p.title)}</h3>
            <p class="card-summary">${esc(p.summary)}</p>

            <div class="service-status-panel">
              <div class="svc-row">
                <span class="svc-label">📄 내용 발표 자료</span>
                <span class="svc-pill svc-ok">${presCount}개 파일 열람·다운로드</span>
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

          <div class="card-actions-row">
            <button class="btn-open-modal" data-open="${p.id}" type="button">🔍 자료 · 영상 · 피드백 열람</button>
            <a class="btn-zip-dl" href="${encodeUrlPath(p.bundleZipUrl)}" download="bundle_${p.id}.zip" title="프로젝트 파일 일괄 ZIP (${fmtBytes(p.bundleZipBytes)})">
              ⬇ ZIP (${fmtBytes(p.bundleZipBytes)})
            </a>
          </div>
        </article>`;
      })
      .join("");
  }

  function openModal(proj, subtab = "presentations") {
    currentProject = proj;
    activeSubtab = subtab;
    selectedFileIndex = 0;
    $("modalTitle").textContent = proj.title;
    $("modalSub").textContent = `참여자: ${proj.authors.join(", ")} · 종합 평가: ${proj.grade} (${proj.score}점) · 총 ${proj.allFiles.length}개 파일`;
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
      ? `<a class="nav-pill-btn pill-cyan" href="${esc(file.externalUrl)}" target="_blank" rel="noopener noreferrer">🌐 외부 사이트 열기</a>`
      : "";
    const newTabUrl = encodeUrlPath(file.previewUrl || file.downloadUrl);
    return `
      <div class="viewer-toolbar">
        <div style="font-size:0.82rem; font-weight:700; color:#e2e8f0; word-break:break-all;">
          ${esc(file.name)} <span style="color:#94a3b8;">(${fmtBytes(file.sizeBytes)})</span>
        </div>
        <div style="display:flex; gap:0.45rem; flex-wrap:wrap;">
          ${extBtn}
          <a class="nav-pill-btn pill-cyan" href="${newTabUrl}" target="_blank" rel="noopener noreferrer">↗ 새 탭에서 보기</a>
          <a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(file.downloadUrl)}" download="${esc(file.name)}">⬇ 원본 다운로드</a>
        </div>
      </div>`;
  }

  function renderFilePreviewElement(file) {
    const url = encodeUrlPath(file.previewUrl || file.downloadUrl);
    if (file.ext === "png" || file.ext === "jpg" || file.ext === "jpeg") {
      return `<div class="single-panel-scroll" style="text-align:center;">
        <img src="${url}" alt="${esc(file.name)}" style="max-width:100%; border-radius:12px; border:1px solid rgba(255,255,255,0.2);" />
      </div>`;
    }
    if (file.ext === "m4a") {
      return `<div class="single-panel-scroll" style="text-align:center; padding-top:3rem;">
        <div style="font-size:1.1rem; font-weight:800; color:#bae6fd; margin-bottom:1rem;">🎧 AI 오디오 브리핑 (${esc(file.name)})</div>
        <audio controls style="width:100%; max-width:560px;" src="${url}"></audio>
      </div>`;
    }
    if (file.ext === "csv") {
      return `<div class="single-panel-scroll" style="text-align:center; padding-top:3rem;">
        <div style="font-size:1.05rem; font-weight:800; color:#fde68a; margin-bottom:0.6rem;">📊 대용량 원천 데이터셋 (${esc(file.name)})</div>
        <p style="color:#cbd5e1; font-size:0.86rem;">파일 크기: ${fmtBytes(file.sizeBytes)} · GitHub Releases 고속 CDN에서 직접 다운로드할 수 있습니다.</p>
        <a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(file.downloadUrl)}" download="${esc(file.name)}">⬇ CSV 원본 다운로드</a>
      </div>`;
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
          const badge = f.ext.toUpperCase();
          return `<button class="file-select-item ${act}" data-fidx="${idx}" type="button">
            <div class="file-item-name">[${badge}] ${esc(f.relPath || f.name)}</div>
            <div class="file-item-meta">${fmtBytes(f.sizeBytes)} · ${f.hostedOn === "releases" ? "GitHub Releases" : "GitHub Pages"}</div>
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

      const v = p.demoVideo.files[0];
      const vUrl = encodeUrlPath(v.previewUrl || v.downloadUrl);
      body.innerHTML = `
        <div class="single-panel-scroll">
          <div class="video-player-wrap">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem; margin-bottom:0.85rem;">
              <div>
                <strong style="color:#6ee7b7; font-size:0.95rem;">🎬 ${esc(v.name)}</strong>
                <span style="color:#94a3b8; font-size:0.8rem; margin-left:0.5rem;">(${fmtBytes(v.sizeBytes)})</span>
              </div>
              <a class="nav-pill-btn pill-emerald" href="${encodeUrlPath(v.downloadUrl)}" download="${esc(v.name)}">⬇ 시연영상 원본 다운로드</a>
            </div>
            <video controls playsinline preload="metadata" src="${vUrl}"></video>
          </div>
        </div>`;
    } else if (activeSubtab === "feedback") {
      // 4페이지 기술 감사 리포트(*_피드백.pdf만) 즉시 열람
      const fbs = p.feedbacks;
      if (!fbs.length) {
        body.innerHTML = `<div class="single-panel-scroll">피드백 PDF가 없습니다.</div>`;
        return;
      }
      if (selectedFileIndex >= fbs.length) selectedFileIndex = 0;
      const cur = fbs[selectedFileIndex];

      if (fbs.length === 1) {
        body.innerHTML = `
          <div class="viewer-pane" style="flex:1;">
            ${renderViewerToolbar(cur)}
            <iframe class="viewer-frame" src="${encodeUrlPath(cur.previewUrl)}" title="${esc(cur.name)}"></iframe>
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
              <iframe class="viewer-frame" src="${encodeUrlPath(cur.previewUrl)}" title="${esc(cur.name)}"></iframe>
            </div>
          </div>`;
      }
    } else if (activeSubtab === "downloads") {
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
    currentProject = null;
    $("modalTitle").textContent = "📦 전체 3단계 프로젝트 자료 통합 인덱스";
    $("modalSub").textContent = `총 ${manifest.stats.totalProjects}개 프로젝트 · ${manifest.stats.totalFiles}개 파일 다운로드 지원`;
    $("modalSubtabs").style.display = "none";
    $("detailModal").classList.add("show");
    document.body.style.overflow = "hidden";

    const rows = manifest.tabs.flatMap((t) =>
      t.projects.map((p) => `
        <tr>
          <td><span class="author-chip">${esc(t.label)}</span></td>
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
            <tr><th>단계 탭</th><th>프로젝트 / 참여자</th><th>시연영상</th><th>파일 수</th><th>일괄 다운로드</th></tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
  }

  function bindEvents() {
    $("mainTabs").addEventListener("click", (e) => {
      const btn = e.target.closest(".main-tab-btn");
      if (!btn) return;
      activeTabId = btn.dataset.tab;
      renderTabs();
      renderCommonBanner();
      renderGrid();
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
      updateSubtabsUI();
      renderModalBody();
    });

    $("modalBody").addEventListener("click", (e) => {
      const item = e.target.closest("[data-fidx]");
      if (!item) return;
      selectedFileIndex = Number(item.dataset.fidx);
      renderModalBody();
    });

    $("btnAllFilesIndex").addEventListener("click", openAllFilesIndexModal);
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
