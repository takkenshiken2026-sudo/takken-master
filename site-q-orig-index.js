/**
 * 実践演習一覧 q/orig/index.html — 絞り込み・表示（過去問 site-q-index.js 相当）
 * 再生成: python3 tools/build_practice_question_pages.py
 */
(() => {
  'use strict';

  const PAGE_SIZE = 50;

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const dataEl = document.getElementById('q-orig-index-data');
  const ITEMS = dataEl ? JSON.parse(dataEl.textContent || '[]') : [];

  const q = document.getElementById('q-orig-q');
  const catChips = $$('.q-orig-chip-btn[data-cat]');
  const levelChips = $$('.q-orig-level-btn[data-level]');
  const statusChips = $$('.q-orig-status-btn[data-status]');
  const hit = document.getElementById('q-orig-hit');
  const empty = document.getElementById('q-orig-empty');
  const toolbarReset = document.getElementById('q-orig-reset');
  const activeFilters = document.getElementById('q-orig-active-filters');
  const toolbar = document.querySelector('.past-index-tools');
  const fieldRow = document.getElementById('q-orig-field-row');
  const jumpLinks = $$('.q-index-field-link[data-field]');
  const topBtn = document.getElementById('q-orig-top');
  const pagBar = document.getElementById('q-orig-pagination');
  const unitView = document.getElementById('q-orig-view-unit');
  const flatView = document.getElementById('q-orig-view-flat');
  const flatBody = document.getElementById('q-orig-flat-body');

  let activeCat = 'all';
  let activeLevel = 'all';
  let activeStatus = 'all';
  let page = 1;
  let urlSyncTimer = null;

  const norm = (s) => (s || '').toString().trim().toLowerCase();

  const appData = (() => {
    try {
      const raw = localStorage.getItem('exam_site_shell_v1');
      if (!raw) return null;
      const db = JSON.parse(raw);
      const u = db.__guest__ || Object.values(db).find((x) => x && (x.answers || x.bookmarks));
      if (!u) return null;
      return { answers: u.answers || {}, bookmarks: u.bookmarks || {} };
    } catch (e) {
      return null;
    }
  })();

  function parseSearchTokens(raw) {
    const parts = norm(raw).split(/\s+/).filter(Boolean);
    const inc = [];
    const exc = [];
    parts.forEach((p) => {
      if (p.startsWith('-') && p.length > 1) exc.push(p.slice(1));
      else inc.push(p);
    });
    return { inc, exc };
  }

  function matchesSearch(item, tokens) {
    const hay = norm(item.search);
    if (tokens.inc.length && !tokens.inc.every((t) => hay.includes(t))) return false;
    if (tokens.exc.some((t) => hay.includes(t))) return false;
    return true;
  }

  function matchesStatus(item) {
    if (activeStatus === 'all') return true;
    if (!appData) return false;
    const id = String(item.appId);
    if (activeStatus === 'bookmark') return !!appData.bookmarks[id];
    if (activeStatus === 'wrong') {
      const a = appData.answers[id];
      return a && a.ans != null && Number(a.ans) !== Number(item.correct);
    }
    return true;
  }

  function itemVisible(item) {
    const tokens = parseSearchTokens(q?.value || '');
    if (!matchesSearch(item, tokens)) return false;
    if (activeCat !== 'all' && item.category !== activeCat) return false;
    if (activeLevel !== 'all' && String(item.level) !== activeLevel) return false;
    return matchesStatus(item);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function highlightText(text, query) {
    const raw = text || '';
    const tokens = parseSearchTokens(query).inc.filter((t) => t.length >= 2);
    if (!tokens.length) return escapeHtml(raw);
    let spans = [{ start: 0, end: raw.length, hl: false }];
    tokens.forEach((tok) => {
      const sliceLower = raw.toLowerCase();
      const next = [];
      spans.forEach((sp) => {
        const slice = raw.slice(sp.start, sp.end);
        const sliceLower = slice.toLowerCase();
        let idx = 0;
        while (idx < slice.length) {
          const at = sliceLower.indexOf(tok, idx);
          if (at < 0) {
            next.push({ start: sp.start + idx, end: sp.end, hl: false });
            break;
          }
          if (at > idx) next.push({ start: sp.start + idx, end: sp.start + at, hl: false });
          next.push({ start: sp.start + at, end: sp.start + at + tok.length, hl: true });
          idx = at + tok.length;
        }
      });
      spans = next;
    });
    return spans
      .map((sp) => {
        const part = raw.slice(sp.start, sp.end);
        return sp.hl ? `<mark class="q-hit-mark">${escapeHtml(part)}</mark>` : escapeHtml(part);
      })
      .join('');
  }

  function rowHtml(item, query) {
    const preview = item.preview
      ? highlightText(item.preview, query)
      : '<span class="q-year-table-desc--empty">問題文は各ページで確認できます</span>';
    const href = escapeHtml(item.href);
    const appHref = escapeHtml(`../../index.html#orig-play-${item.appId}`);
    return `<tr class="q-year-table-row" tabindex="0" data-app-id="${item.appId}" data-href="${href}" data-category="${escapeHtml(item.category)}" data-level="${item.level}" data-unit="${escapeHtml(item.unit)}" data-field="${escapeHtml(item.field)}">
<td class="q-year-table-no" data-label="ID"><a href="${href}">${item.appId}</a></td>
<td class="q-year-table-cat" data-label="分野">${escapeHtml(item.category)}</td>
<td class="q-year-table-level" data-label="レベル">L${item.level}</td>
<td class="q-year-table-desc" data-label="問題文">${preview}</td>
<td class="q-year-table-action" data-label="操作"><a class="q-row-link" href="${href}">解説</a> <a class="q-row-link q-row-link-app" href="${appHref}">演習</a></td></tr>`;
  }

  function tableHead() {
    return `<thead><tr><th scope="col">ID</th><th scope="col">分野</th><th scope="col">レベル</th><th scope="col">問題文（抜粋）</th><th scope="col">操作</th></tr></thead>`;
  }

  function bindRows(root) {
    root.querySelectorAll('.q-year-table-row').forEach((row) => {
      if (row.dataset.bound) return;
      row.dataset.bound = '1';
      const go = (href) => {
        if (href) window.location.href = href;
      };
      row.addEventListener('click', (e) => {
        if (e.target.closest('a')) return;
        go(row.dataset.href);
      });
      row.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          go(row.dataset.href);
        }
      });
    });
  }

  function hasActiveFilters() {
    return (
      (q?.value || '').trim() !== '' ||
      activeCat !== 'all' ||
      activeLevel !== 'all' ||
      activeStatus !== 'all'
    );
  }

  function renderActiveFilters() {
    if (!activeFilters) return;
    const tags = [];
    const query = (q?.value || '').trim();
    if (query) tags.push({ type: 'q', label: `検索: ${query}` });
    if (activeCat !== 'all') tags.push({ type: 'cat', label: activeCat });
    if (activeLevel !== 'all') tags.push({ type: 'level', label: `レベル${activeLevel}` });
    if (activeStatus !== 'all') {
      const labels = { wrong: '不正解のみ', bookmark: 'ブックマーク' };
      tags.push({ type: 'status', label: labels[activeStatus] || activeStatus });
    }
    if (!tags.length) {
      activeFilters.classList.add('hide');
      activeFilters.innerHTML = '';
      return;
    }
    activeFilters.classList.remove('hide');
    activeFilters.innerHTML =
      '<span class="q-index-active-label">適用中</span>' +
      tags
        .map(
          (t) =>
            `<button type="button" class="q-index-active-tag" data-remove="${t.type}">${escapeHtml(t.label)} <span class="q-index-active-tag-remove" aria-hidden="true">×</span></button>`
        )
        .join('');
    activeFilters.querySelectorAll('[data-remove]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const t = btn.dataset.remove;
        if (t === 'q' && q) q.value = '';
        if (t === 'cat') {
          activeCat = 'all';
          catChips.forEach((b) => b.classList.toggle('on', (b.dataset.cat || 'all') === 'all'));
        }
        if (t === 'level') {
          activeLevel = 'all';
          levelChips.forEach((b) => b.classList.toggle('on', (b.dataset.level || 'all') === 'all'));
        }
        if (t === 'status') {
          activeStatus = 'all';
          statusChips.forEach((b) => b.classList.toggle('on', (b.dataset.status || 'all') === 'all'));
        }
        apply();
      });
    });
  }

  function syncUrl() {
    if (urlSyncTimer) clearTimeout(urlSyncTimer);
    urlSyncTimer = setTimeout(() => {
      const params = new URLSearchParams();
      const query = (q?.value || '').trim();
      if (query) params.set('q', query);
      if (activeCat !== 'all') params.set('cat', activeCat);
      if (activeLevel !== 'all') params.set('level', activeLevel);
      if (activeStatus !== 'all') params.set('status', activeStatus);
      if (page > 1) params.set('page', String(page));
      const qs = params.toString();
      const next = qs ? `${location.pathname}?${qs}` : location.pathname;
      history.replaceState(null, '', next);
    }, 200);
  }

  function readUrl() {
    const params = new URLSearchParams(location.search);
    if (params.has('q') && q) q.value = params.get('q') || '';
    activeCat = params.get('cat') || 'all';
    activeLevel = params.get('level') || 'all';
    activeStatus = params.get('status') || 'all';
    page = Math.max(1, parseInt(params.get('page') || '1', 10) || 1);
    catChips.forEach((b) => b.classList.toggle('on', (b.dataset.cat || 'all') === activeCat));
    levelChips.forEach((b) => b.classList.toggle('on', (b.dataset.level || 'all') === activeLevel));
    statusChips.forEach((b) => b.classList.toggle('on', (b.dataset.status || 'all') === activeStatus));
  }

  function visibleItems() {
    return ITEMS.filter(itemVisible);
  }

  function paginate(list) {
    const totalPages = Math.max(1, Math.ceil(list.length / PAGE_SIZE));
    if (page > totalPages) page = totalPages;
    const start = (page - 1) * PAGE_SIZE;
    return { slice: list.slice(start, start + PAGE_SIZE), totalPages, total: list.length };
  }

  function renderPagination(total, totalPages) {
    if (!pagBar) return;
    if (total <= PAGE_SIZE) {
      pagBar.classList.add('hide');
      pagBar.innerHTML = '';
      return;
    }
    pagBar.classList.remove('hide');
    const prev = page > 1 ? page - 1 : null;
    const next = page < totalPages ? page + 1 : null;
    pagBar.innerHTML = `
<button type="button" class="q-index-page-btn" data-page="${prev || ''}" ${prev ? '' : 'disabled'}>前へ</button>
<span class="q-index-page-info">${page} / ${totalPages} ページ（${total}問）</span>
<button type="button" class="q-index-page-btn" data-page="${next || ''}" ${next ? '' : 'disabled'}>次へ</button>`;
    pagBar.querySelectorAll('[data-page]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const p = parseInt(btn.dataset.page, 10);
        if (!p) return;
        page = p;
        apply(false);
        flatView?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  function applyUnitView(visible, query) {
    const ids = new Set(visible.map((x) => x.appId));
    $$('.q-index-field-block', unitView).forEach((fieldBlock) => {
      let fieldShown = 0;
      $$('.q-index-unit-block', fieldBlock).forEach((unitBlock) => {
        const rows = $$('.q-year-table-row', unitBlock);
        let shown = 0;
        rows.forEach((row) => {
          const id = Number(row.dataset.appId);
          const ok = ids.has(id);
          row.classList.toggle('hide', !ok);
          if (ok) shown++;
        });
        unitBlock.classList.toggle('hide', shown === 0);
        if (shown) fieldShown += shown;
      });
      fieldBlock.classList.toggle('hide', fieldShown === 0);
      const countEl = $('.q-index-year-count', fieldBlock);
      if (countEl) {
        const total = Number(countEl.dataset.total) || 0;
        countEl.textContent = fieldShown === total ? `${total}問` : `${fieldShown} / ${total}問`;
      }
    });
    jumpLinks.forEach((link) => {
      const fid = link.dataset.field;
      const block = document.getElementById(`field-${fid}`);
      const hidden = !block || block.classList.contains('hide');
      link.classList.toggle('hide', hidden);
      if (hidden) link.setAttribute('tabindex', '-1');
      else link.removeAttribute('tabindex');
    });
    $$('.q-year-table-desc', unitView).forEach((cell) => {
      const row = cell.closest('tr');
      if (!row || row.classList.contains('hide')) return;
      const item = ITEMS.find((x) => String(x.appId) === row.dataset.appId);
      if (!item) return;
      cell.innerHTML = item.preview
        ? highlightText(item.preview, query)
        : '<span class="q-year-table-desc--empty">問題文は各ページで確認できます</span>';
    });
    bindRows(unitView);
  }

  function renderFlatView(visible, query) {
    if (!flatBody) return;
    flatView?.classList.remove('hide');
    const { slice } = paginate(visible);
    flatBody.innerHTML = slice.map((it) => rowHtml(it, query)).join('');
    bindRows(flatView);
  }

  function apply(syncUrlFlag = true) {
    const query = q?.value || '';
    const visible = visibleItems();
    const total = ITEMS.length;
    const shown = visible.length;
    const useFlat = shown > 120 || (query && query.length > 0);

    applyUnitView(visible, query);
    if (useFlat) {
      renderFlatView(visible, query);
    } else if (flatView) {
      flatView.classList.add('hide');
      if (pagBar) pagBar.classList.add('hide');
    }

    if (hit) hit.textContent = `${shown} / ${total} 問`;
    if (empty) empty.classList.toggle('hide', shown !== 0);
    if (!useFlat) renderPagination(shown, Math.max(1, Math.ceil(shown / PAGE_SIZE)));
    else renderPagination(shown, Math.max(1, Math.ceil(shown / PAGE_SIZE)));
    renderActiveFilters();
    if (toolbarReset) toolbarReset.classList.toggle('hide', !hasActiveFilters());
    if (syncUrlFlag) syncUrl();
  }

  function resetAll() {
    if (q) q.value = '';
    activeCat = 'all';
    activeLevel = 'all';
    activeStatus = 'all';
    page = 1;
    catChips.forEach((b) => b.classList.toggle('on', (b.dataset.cat || 'all') === 'all'));
    levelChips.forEach((b) => b.classList.toggle('on', (b.dataset.level || 'all') === 'all'));
    statusChips.forEach((b) => b.classList.toggle('on', (b.dataset.status || 'all') === 'all'));
    apply();
    q?.focus();
  }

  function initFieldCollapse() {
    $$('.q-index-field-block', unitView).forEach((block) => {
      const btn = $('.q-index-year-toggle', block);
      if (!btn) return;
      btn.addEventListener('click', () => {
        const now = block.classList.toggle('is-collapsed');
        btn.setAttribute('aria-expanded', now ? 'false' : 'true');
      });
    });
  }

  q?.addEventListener('input', () => {
    page = 1;
    apply();
  });
  toolbarReset?.addEventListener('click', resetAll);
  document.getElementById('q-orig-empty-reset')?.addEventListener('click', resetAll);

  catChips.forEach((btn) => {
    btn.addEventListener('click', () => {
      catChips.forEach((b) => b.classList.remove('on'));
      btn.classList.add('on');
      activeCat = btn.dataset.cat || 'all';
      page = 1;
      apply();
    });
  });
  levelChips.forEach((btn) => {
    btn.addEventListener('click', () => {
      levelChips.forEach((b) => b.classList.remove('on'));
      btn.classList.add('on');
      activeLevel = btn.dataset.level || 'all';
      page = 1;
      apply();
    });
  });
  statusChips.forEach((btn) => {
    btn.addEventListener('click', () => {
      statusChips.forEach((b) => b.classList.remove('on'));
      btn.classList.add('on');
      activeStatus = btn.dataset.status || 'all';
      page = 1;
      apply();
    });
  });

  document.addEventListener('keydown', (e) => {
    const tag = (e.target && e.target.tagName) || '';
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(tag) || e.target?.isContentEditable;
    if (e.key === '/' && !typing) {
      e.preventDefault();
      q?.focus();
      return;
    }
    if (e.key !== 'Escape' || typing) return;
    if (document.activeElement === q && q?.value) {
      q.value = '';
      page = 1;
      apply();
      return;
    }
    if (hasActiveFilters()) resetAll();
  });

  if (toolbar) {
    const onScroll = () => {
      toolbar.classList.toggle('is-scrolled', toolbar.getBoundingClientRect().top <= 56);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  topBtn?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  window.addEventListener(
    'scroll',
    () => topBtn?.classList.toggle('is-visible', window.scrollY > 480),
    { passive: true }
  );

  readUrl();
  initFieldCollapse();
  bindRows(unitView);
  apply(false);
})();
