(() => {
  const data = window.ATLAS_DATA;
  if (!data) {
    document.body.innerHTML =
      "<p style='padding:2rem;font-family:sans-serif'>Missing atlas-data.js</p>";
    return;
  }

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  const ACTIONS =
    data.absorbActions || {
      "adopt-core": "USE_NOW",
      "adopt-adjacent": "WIRE_WHEN_NEEDED",
      pilot: "GATED_PILOT",
      evaluate: "ABSORB_PATTERN",
      benchmark: "RESEARCH_ONLY",
      watch: "WATCH",
      reference: "REFERENCE",
      "strategic-exception": "EXCEPTION_REVIEW",
    };

  const classByExample = new Map();
  data.classes.forEach((c) => {
    (c.examples || []).forEach((repo) => classByExample.set(repo, c.id));
  });

  function classFor(project) {
    return project.class || classByExample.get(project.repo) || "S";
  }

  function actionFor(project) {
    return project.action || ACTIONS[project.priority] || "WATCH";
  }

  function formatStars(n) {
    if (n >= 1_000_000) return (n / 1_000_000).toFixed(1).replace(/\.0$/, "") + "M";
    if (n >= 10_000) return Math.round(n / 1000) + "k";
    if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, "") + "k";
    return String(n);
  }

  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function toast(msg) {
    const el = $("#toast");
    if (!el) return;
    el.hidden = false;
    el.textContent = msg;
    clearTimeout(toast._t);
    toast._t = setTimeout(() => {
      el.hidden = true;
    }, 2200);
  }

  // Stats
  const stats = $("#stats");
  const c = data.counts || {};
  [
    [c.resolved ?? data.projects.length, "projects"],
    [c.thresholdProjects ?? "—", "≥10k stars"],
    [c.categories ?? "—", "categories"],
    [data.classes.length, "taxonomy classes"],
  ].forEach(([value, label]) => {
    const el = document.createElement("div");
    el.className = "stat";
    el.innerHTML = `<b>${value}</b><span>${label}</span>`;
    stats.appendChild(el);
  });

  // Stack
  const stack = data.stack || {};
  const stackItems = [
    ["Human", stack.human],
    ["Task control", stack.taskControl],
    ["Workers", (stack.workers || []).join(" · ")],
    ["Durability", stack.durability],
    ["Interop", (stack.interop || []).join(" · ")],
  ];
  const stackList = $("#stack-list");
  stackItems.forEach(([title, detail], i) => {
    const li = document.createElement("li");
    li.innerHTML = `<span class="n">${i + 1}</span><div><strong>${title}</strong><span>${detail || ""}</span></div>`;
    stackList.appendChild(li);
  });
  $("#stack-rule").textContent = stack.rule || "";

  // Mode
  let mode = "human";
  function setMode(next) {
    mode = next;
    document.body.dataset.mode = mode;
    $$(".mode-btn").forEach((btn) => {
      const on = btn.dataset.mode === mode;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    if (mode === "human") {
      $("#hero-title").textContent = "What should we adopt, pilot, absorb, or refuse?";
      $("#hero-lede").innerHTML =
        "One map for coding harnesses, meta-harnesses, control planes, frameworks, and runtimes — with a single rule: <strong>one accountable owner per layer</strong>.";
      $("#jobs-title").textContent = "Human operator jobs";
      $("#jobs-sub").textContent =
        "Command calmly. Decide with gates. See evidence. Feel premium clarity.";
      renderJobs(data.humanJobs);
    } else {
      $("#hero-title").textContent = "Route work by class before you spawn.";
      $("#hero-lede").innerHTML =
        "Agents: classify A–F, pick one layer owner, inject path bans, require maker≠checker proof. <strong>Stars are discovery. Receipts are truth. Absorb before install.</strong>";
      $("#jobs-title").textContent = "Agent router jobs";
      $("#jobs-sub").textContent =
        "Taxonomy → admission → execution → evidence → absorb or HOLD.";
      renderJobs(data.agentJobs);
    }
  }

  function renderJobs(jobs) {
    const grid = $("#job-grid");
    grid.innerHTML = "";
    (jobs || []).forEach((j) => {
      const card = document.createElement("article");
      card.className = "job";
      card.innerHTML = `<h3>${j.title}</h3><p>${j.detail}</p>`;
      grid.appendChild(card);
    });
  }

  $$(".mode-btn").forEach((btn) => {
    btn.addEventListener("click", () => setMode(btn.dataset.mode));
  });

  // Taxonomy
  let activeClass = data.classes[0]?.id || "A";
  let classFilter = null;
  let categoryFilters = null;
  const taxRail = $("#tax-rail");
  data.classes.forEach((cls) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tax-card";
    btn.dataset.id = cls.id;
    btn.setAttribute("role", "listitem");
    btn.innerHTML = `<span class="id">Class ${cls.id}</span><span class="name">${cls.name}</span>`;
    btn.addEventListener("click", () => {
      activeClass = cls.id;
      classFilter = cls.id;
      categoryFilters = null;
      renderTax();
      renderChips();
      // clear other filters for focused class view
      $("#priority").value = "";
      $("#category").value = "";
      $("#action").value = "";
      $("#q").value = "";
      renderTable();
      $("#catalog").scrollIntoView({ behavior: "smooth", block: "start" });
    });
    taxRail.appendChild(btn);
  });

  function renderTax() {
    $$(".tax-card").forEach((b) => b.classList.toggle("is-active", b.dataset.id === activeClass));
    const cls = data.classes.find((c) => c.id === activeClass);
    if (!cls) return;
    const detail = $("#tax-detail");
    const links = (cls.examples || [])
      .map((repo) => {
        const p = data.projects.find((x) => x.repo === repo);
        const href = p?.url || `https://github.com/${repo}`;
        return `<li><a href="${href}" target="_blank" rel="noreferrer">${repo}</a></li>`;
      })
      .join("");
    detail.innerHTML = `
      <h3>Class ${cls.id} · ${cls.name}</h3>
      <p class="job">${cls.job}</p>
      <div class="meta-grid">
        <div>
          <h4>Examples</h4>
          <ul>${links}</ul>
        </div>
        <div>
          <h4>Boundary</h4>
          <p>${cls.not}</p>
          <h4 style="margin-top:0.9rem">Estate posture</h4>
          <p>${cls.estate}</p>
        </div>
      </div>`;
  }

  // Class chips
  const chips = $("#class-chips");
  function renderChips() {
    chips.innerHTML = "";
    const all = document.createElement("button");
    all.type = "button";
    all.className = "chip" + (classFilter ? "" : " is-active");
    all.textContent = "All classes";
    all.addEventListener("click", () => {
      classFilter = null;
      categoryFilters = null;
      renderChips();
      renderTable();
    });
    chips.appendChild(all);
    data.classes.forEach((cls) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "chip" + (classFilter === cls.id ? " is-active" : "");
      b.textContent = `${cls.id} · ${cls.name.split(" ")[0]}`;
      b.title = cls.name;
      b.addEventListener("click", () => {
        classFilter = cls.id;
        categoryFilters = null;
        activeClass = cls.id;
        renderTax();
        renderChips();
        renderTable();
      });
      chips.appendChild(b);
    });
  }

  // System map
  const layers = [
    {
      id: "human",
      label: "Human",
      title: "Command center",
      blurb: "Hermes + Queen · one receive gateway",
    },
    {
      id: "gov",
      label: "Govern",
      title: "Control plane",
      blurb: "Kanban now · Paperclip gated",
      filterCat: ["control-plane", "coding-control-plane"],
    },
    {
      id: "exec",
      label: "Execute",
      title: "Runtimes & coding",
      blurb: "Hermes · Codex · Claude · OpenCode · AGY",
      filterCat: ["agent-runtime", "coding-agent", "rust-runtime"],
    },
    {
      id: "coord",
      label: "Coordinate",
      title: "Durable work",
      blurb: "Cron · Temporal · n8n",
      filterCat: ["durable-execution", "workflow-automation"],
    },
    {
      id: "trust",
      label: "Trust",
      title: "Proof layer",
      blurb: "Evals · sandbox · secrets · Git",
      filterCat: ["eval-security", "observability", "sandbox-security", "identity-secrets"],
    },
  ];
  const mapStage = $("#map-stage");
  layers.forEach((layer) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "map-node";
    btn.dataset.id = layer.id;
    btn.innerHTML = `<div class="layer">${layer.label}</div><strong>${layer.title}</strong><span>${layer.blurb}</span>`;
    btn.addEventListener("click", () => {
      $$(".map-node").forEach((n) => n.classList.toggle("is-active", n === btn));
      if (layer.filterCat) {
        classFilter = null;
        categoryFilters = layer.filterCat;
        renderChips();
        $("#category").value = "";
        $("#priority").value = "";
        $("#action").value = "";
        $("#q").value = "";
        renderTable();
        $("#catalog").scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
    mapStage.appendChild(btn);
  });

  // Filters
  const prioritySel = $("#priority");
  const categorySel = $("#category");
  const actionSel = $("#action");
  const qInput = $("#q");

  (data.priorityOrder || []).forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p;
    opt.textContent = p;
    prioritySel.appendChild(opt);
  });
  const cats = [...new Set(data.projects.map((p) => p.category))].sort();
  cats.forEach((cat) => {
    const opt = document.createElement("option");
    opt.value = cat;
    opt.textContent = (data.categoryLabels && data.categoryLabels[cat]) || cat;
    categorySel.appendChild(opt);
  });
  const actionSet = [...new Set(Object.values(ACTIONS))];
  actionSet.forEach((a) => {
    const opt = document.createElement("option");
    opt.value = a;
    opt.textContent = a;
    actionSel.appendChild(opt);
  });

  function matches(project) {
    const q = qInput.value.trim().toLowerCase();
    const pr = prioritySel.value;
    const cat = categorySel.value;
    const act = actionSel.value;
    if (pr && project.priority !== pr) return false;
    if (cat && project.category !== cat) return false;
    if (categoryFilters && !categoryFilters.includes(project.category)) return false;
    if (act && actionFor(project) !== act) return false;
    if (classFilter && classFor(project) !== classFilter) return false;
    if (!q) return true;
    const hay = [
      project.repo,
      project.description,
      project.why,
      project.language,
      project.category,
      project.priority,
      actionFor(project),
      classFor(project),
    ]
      .join(" ")
      .toLowerCase();
    return hay.includes(q);
  }

  function filtered() {
    const list = data.projects.filter(matches);
    const pOrder = data.priorityOrder || [];
    list.sort((a, b) => {
      const pa = pOrder.indexOf(a.priority);
      const pb = pOrder.indexOf(b.priority);
      const ia = pa === -1 ? 99 : pa;
      const ib = pb === -1 ? 99 : pb;
      if (ia !== ib) return ia - ib;
      return b.stars - a.stars;
    });
    return list;
  }

  function renderTable() {
    const rows = $("#rows");
    rows.innerHTML = "";
    const list = filtered();
    list.slice(0, 140).forEach((p) => {
      const tr = document.createElement("tr");
      const cls = classFor(p);
      const act = actionFor(p);
      const license = p.licenseReview ? `${p.license} · review` : p.license;
      tr.innerHTML = `
        <td class="repo">
          <a href="${p.url}" target="_blank" rel="noreferrer">${p.repo}</a>
          <small>${p.language} · ${license}</small>
        </td>
        <td><span class="pill">Class ${cls}</span><br><span class="pill">${(data.categoryLabels && data.categoryLabels[p.category]) || p.category}</span></td>
        <td><span class="action-pill ${act}">${act}</span></td>
        <td><span class="pill ${p.priority}">${p.priority}</span></td>
        <td class="num">${formatStars(p.stars)}</td>
        <td class="why">${escapeHtml(p.why)}</td>`;
      rows.appendChild(tr);
    });

    $("#cat-meta").textContent = `${list.length} matching · showing ${Math.min(
      list.length,
      140
    )} · atlas v${data.version || 1} · ${data.generatedAt}`;
    $("#footnote").textContent = categoryFilters
      ? `Filtered to system layer categories: ${categoryFilters.join(", ")}. Clear or press Esc to widen.`
      : classFilter
        ? `Filtered to taxonomy class ${classFilter}. Clear or press Esc to widen.`
        : "Action legend: USE_NOW · ADOPT_STANDARD · WIRE_WHEN_NEEDED · GATED_PILOT · ABSORB_PATTERN · RESEARCH_ONLY. License NOASSERTION requires manual review.";
  }

  function clearFilters() {
    classFilter = null;
    categoryFilters = null;
    qInput.value = "";
    prioritySel.value = "";
    categorySel.value = "";
    actionSel.value = "";
    $$(".map-node").forEach((n) => n.classList.remove("is-active"));
    renderChips();
    renderTable();
    toast("Filters cleared");
  }

  qInput.addEventListener("input", renderTable);
  prioritySel.addEventListener("change", () => {
    classFilter = null;
    categoryFilters = null;
    renderChips();
    renderTable();
  });
  categorySel.addEventListener("change", () => {
    classFilter = null;
    categoryFilters = null;
    renderChips();
    renderTable();
  });
  actionSel.addEventListener("change", renderTable);

  $("#btn-clear").addEventListener("click", clearFilters);
  $("#btn-copy-json").addEventListener("click", async () => {
    const payload = filtered().slice(0, 140).map((p) => ({
      repo: p.repo,
      class: classFor(p),
      action: actionFor(p),
      priority: p.priority,
      stars: p.stars,
      why: p.why,
      url: p.url,
    }));
    try {
      await navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
      toast(`Copied ${payload.length} projects JSON`);
    } catch {
      toast("Clipboard blocked — select table instead");
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      clearFilters();
      return;
    }
    if (e.key === "/" && document.activeElement !== qInput && document.activeElement?.tagName !== "INPUT") {
      e.preventDefault();
      qInput.focus();
    }
  });

  setMode("human");
  renderTax();
  renderChips();
  renderTable();
})();
