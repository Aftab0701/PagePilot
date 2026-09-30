/**
 * PagePilot — Client Application Logic
 * Implements full state management, real-time agent streaming,
 * tab switching, clipboard actions, settings drawer, and theme toggling.
 */

// Helper utility
const $ = (id) => document.getElementById(id);
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Sample simulation repository data (faithful to sample UI)
const repos = [
  ["agent-kit/harbor", "41.2k", "Build agents that plan, use tools, and recover from mistakes.", "Python", 1],
  ["lumen-labs/tinyvision", "18.7k", "Small on-device vision models with a two-line API.", "Rust", 0],
  ["open-reason/deepthread", "33.9k", "Open reasoning model with a full training recipe and evals.", "Python", 1],
  ["nova-dev/ragstack", "12.4k", "Retrieval pipelines you can debug, from chunking to reranking.", "TypeScript", 1],
  ["kiln-ai/kiln", "9.8k", "Fine-tune and evaluate small language models without a cluster.", "Python", 0],
  ["mapmaker/pixelflow", "7.1k", "Generate UI layouts from a sketch and a short brief.", "Go", 0]
];

const simulatedSteps = [
  ["Open GitHub Trending", "The task names the page, so I'll go there directly instead of searching.", "Go to github.com/trending", "github.com/trending"],
  ["Read the list", "Twenty-five repositories are listed. I need to tell which ones are about AI.", "Read all 25 repositories", "github.com/trending"],
  ["Pick the top three", "Three repos are clearly about AI agents, reasoning and retrieval. I'll take the highest-ranked of those.", "Highlight 3 matches", "github.com/trending"],
  ["Collect the details", "The task asks for stars and descriptions, so I'll copy both for each repo.", "Copy stars and description", "github.com/trending"],
  ["Write the answer", "Everything the task asked for is in hand, so I can stop here.", "Finish", "github.com/trending"]
];

const hits = repos.filter((r) => r[4]);

// State
let executionId = 0;
let isRunning = false;
let socket = null;
let runHistory = [];

// Initialize Repo rows in preview viewport
function initPreviewRows() {
  const container = $('repo-rows');
  if (!container) return;
  container.innerHTML = repos
    .map(
      (r) => `
    <div class="row" data-match="${r[4]}">
      <div>
        <b>${r[0]}</b>
        <p>${r[2]}</p>
      </div>
      <span>★ ${r[1]}</span>
    </div>
  `
    )
    .join('');
}

// Tab Switching logic
function switchTab(index) {
  document.querySelectorAll('.tabs button').forEach((b) => {
    b.setAttribute('aria-selected', b.dataset.t == index);
  });
  document.querySelectorAll('.pane').forEach((p, i) => {
    p.classList.toggle('on', i == index);
  });
}

document.querySelector('.tabs').addEventListener('click', (e) => {
  const btn = e.target.closest('button');
  if (btn && btn.dataset.t !== undefined) {
    switchTab(btn.dataset.t);
  }
});

// Status pill updater
function updateStatus(title, subtitle, isWorking, isError = false) {
  $('stt').textContent = title;
  $('sts').textContent = subtitle;
  const statusEl = $('st');
  statusEl.className = 'status' + (isWorking ? ' go' : '') + (isError ? ' err' : '');
}

// Result Renderer
function renderResult(customTitle, customSubtitle, customItems, markdownText) {
  const container = $('result-container');
  if (!container) return;

  const items = customItems || hits.slice(0, 3);
  const title = customTitle || "Top 3 trending AI repositories";
  const subtitle = customSubtitle || "Extracted from github.com/trending";

  let html = `
    <h3>${title}</h3>
    <p>${subtitle}</p>
  `;

  html += items
    .map(
      (r) => `
    <div class="repo">
      <div>${r[0]}<em>★ ${r[1]}</em></div>
      <p>${r[2]}</p>
    </div>
  `
    )
    .join('');

  html += `
    <div class="foot">
      <button class="b" id="cp-text" type="button">Copy text</button>
      <button class="b" id="cp-md" type="button">Copy as Markdown</button>
    </div>
  `;

  container.innerHTML = html;

  const rawMd =
    markdownText ||
    `### ${title}\n\n` +
      items
        .map((r, i) => `${i + 1}. **${r[0]}** — ${r[1]} stars\n   ${r[2]}`)
        .join('\n');

  const rawText = items.map((r) => `${r[0]} (${r[1]} stars): ${r[2]}`).join('\n');

  const setupCopy = (btnId, text) => {
    const b = $(btnId);
    if (!b) return;
    b.onclick = async () => {
      try {
        await navigator.clipboard.writeText(text);
        const orig = b.textContent;
        b.textContent = 'Copied!';
        showToast('Copied to clipboard', 'success');
        setTimeout(() => (b.textContent = orig), 1400);
      } catch (err) {
        showToast('Clipboard access denied', 'error');
      }
    };
  };

  setupCopy('cp-text', rawText);
  setupCopy('cp-md', rawMd);
}

// Toast notification helper
function showToast(message, type = 'info') {
  const root = $('toast-root');
  if (!root) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  root.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    toast.style.transition = 'all 0.2s ease';
    setTimeout(() => toast.remove(), 200);
  }, 2600);
}

// UI State Reset
function resetRunUI() {
  $('timeline-reasoning').innerHTML = '';
  $('timeline-actions').innerHTML = '';
  $('c0').textContent = '0';
  $('c1').textContent = '0';
  $('pg').style.width = '0%';
  $('result-container').innerHTML = '<div class="empty">The answer will appear here when PagePilot finishes.</div>';
  document.querySelectorAll('.row').forEach((r) => r.classList.remove('hit'));
  $('live-screenshot').style.display = 'none';
  $('preview-frame').style.display = 'block';
}

// Simulated Run (Preview Mode)
async function runSimulated(isInitial = false) {
  const currentId = ++executionId;
  const delay = isInitial ? 0 : 1200;

  resetRunUI();
  isRunning = true;
  $('go-btn').disabled = true;
  $('stop-btn').disabled = false;

  if (!isInitial) switchTab(0);

  for (let i = 0; i < simulatedSteps.length; i++) {
    updateStatus('Working', `Step ${i + 1} of ${simulatedSteps.length}`, true);
    await sleep(delay);
    if (currentId !== executionId) return;

    const s = simulatedSteps[i];
    $('timeline-reasoning').insertAdjacentHTML(
      'beforeend',
      `<li><b>${s[0]}</b><span>${s[1]}</span></li>`
    );
    $('timeline-actions').insertAdjacentHTML(
      'beforeend',
      `<li><b>${s[2]}</b><span>${s[3]}</span></li>`
    );

    $('c0').textContent = i + 1;
    $('c1').textContent = i + 1;
    $('viewport-url').textContent = s[3];

    // Highlight row on step 3
    if (i === 2) {
      const rows = [...document.querySelectorAll('.row')];
      rows.forEach((r) => {
        if (r.dataset.match === '1') {
          r.classList.add('hit');
        }
      });
    }

    $('pg').style.width = `${((i + 1) / simulatedSteps.length) * 100}%`;
  }

  await sleep(delay / 2);
  if (currentId !== executionId) return;

  renderResult();
  updateStatus('Done', `${simulatedSteps.length} steps · 9 s`, false);
  $('go-btn').disabled = false;
  $('stop-btn').disabled = true;
  isRunning = false;
  switchTab(2);

  // Record into history
  runHistory.unshift({
    task: $('task').value,
    timestamp: new Date().toLocaleTimeString(),
    status: 'Completed',
    steps: simulatedSteps.length
  });
  renderHistory();
}

// Real Agent Execution via WebSocket
function runLiveAgent(taskText) {
  const isShowBrowser = $('sw-browser').getAttribute('aria-checked') === 'true';
  const settings = getStoredSettings();

  resetRunUI();
  isRunning = true;
  $('go-btn').disabled = true;
  $('stop-btn').disabled = false;
  updateStatus('Connecting', 'Initializing agent engine...', true);
  switchTab(0);

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/agent`;

  try {
    socket = new WebSocket(wsUrl);
  } catch (e) {
    showToast('Cannot connect to backend websocket. Falling back to preview mode.', 'error');
    runSimulated(false);
    return;
  }

  socket.onopen = () => {
    updateStatus('Working', 'Agent running...', true);
    socket.send(
      JSON.stringify({
        action: 'start',
        task: taskText,
        settings: {
          ...settings,
          headless: !isShowBrowser
        }
      })
    );
  };

  let stepCount = 0;

  socket.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.type === 'step') {
        stepCount++;
        $('timeline-reasoning').insertAdjacentHTML(
          'beforeend',
          `<li><b>Step ${stepCount}</b><span>${msg.thought || msg.action}</span></li>`
        );
        $('timeline-actions').insertAdjacentHTML(
          'beforeend',
          `<li><b>${msg.action || 'Navigate'}</b><span>${msg.url || ''}</span></li>`
        );
        $('c0').textContent = stepCount;
        $('c1').textContent = stepCount;
        if (msg.url) $('viewport-url').textContent = msg.url;

        // Screenshot streaming
        if (msg.screenshot) {
          const img = $('live-screenshot');
          img.src = `data:image/jpeg;base64,${msg.screenshot}`;
          img.style.display = 'block';
          $('preview-frame').style.display = 'none';
        }

        const maxSteps = settings.maxSteps || 25;
        $('pg').style.width = `${Math.min(100, (stepCount / maxSteps) * 100)}%`;
        updateStatus('Working', `Step ${stepCount}`, true);
      } else if (msg.type === 'done') {
        isRunning = false;
        $('go-btn').disabled = false;
        $('stop-btn').disabled = true;
        $('pg').style.width = '100%';
        updateStatus('Done', `${stepCount} steps`, false);

        $('result-container').innerHTML = `
          <h3>Agent Completed</h3>
          <p>${msg.summary || 'Task finished successfully.'}</p>
          <div class="foot">
            <button class="b" id="cp-live-res">Copy Result</button>
          </div>
        `;
        $('cp-live-res').onclick = () => {
          navigator.clipboard.writeText(msg.summary || 'Done');
          showToast('Copied to clipboard', 'success');
        };
        switchTab(2);
      } else if (msg.type === 'error') {
        isRunning = false;
        $('go-btn').disabled = false;
        $('stop-btn').disabled = true;
        updateStatus('Error', msg.message || 'Execution error', false, true);
        showToast(msg.message || 'Agent encountered an error', 'error');
      }
    } catch (err) {
      console.error('Failed to parse WebSocket message', err);
    }
  };

  socket.onerror = () => {
    if (isRunning) {
      showToast('WebSocket error. Falling back to local preview mode.', 'error');
      runSimulated(false);
    }
  };

  socket.onclose = () => {
    if (isRunning) {
      updateStatus('Disconnected', 'Connection closed', false);
      $('go-btn').disabled = false;
      $('stop-btn').disabled = true;
      isRunning = false;
    }
  };
}

// Start button handler
$('go-btn').onclick = () => {
  const isPreview = $('sw-preview').getAttribute('aria-checked') === 'true';
  const taskText = $('task').value.trim();
  if (!taskText) {
    showToast('Please enter a task description', 'error');
    return;
  }

  if (isPreview) {
    runSimulated(false);
  } else {
    runLiveAgent(taskText);
  }
};

// Stop button handler
$('stop-btn').onclick = () => {
  executionId++;
  isRunning = false;
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ action: 'stop' }));
    socket.close();
  }
  updateStatus('Stopped', 'You ended the run', false);
  $('go-btn').disabled = false;
  $('stop-btn').disabled = true;
  showToast('Run halted', 'info');
};

// Switches logic
document.querySelectorAll('.sw').forEach((button) => {
  button.onclick = () => {
    const current = button.getAttribute('aria-checked') === 'true';
    button.setAttribute('aria-checked', (!current).toString());
  };
});

// Example Prompt Chips
document.querySelector('.ex').onclick = (e) => {
  if (e.target.tagName === 'BUTTON') {
    const text = e.target.textContent;
    const taskMap = {
      'Trending AI repos': 'Go to github.com/trending, find the top 3 trending AI repos, and list their stars and descriptions.',
      'Top Hacker News stories': 'Go to news.ycombinator.com, find the top 3 articles with the highest points, and copy their links.',
      'Summarize a Wikipedia article': 'Navigate to en.wikipedia.org/wiki/Artificial_intelligence and extract the first overview paragraph.',
      'Python 3.12 release notes': 'Visit docs.python.org/3/whatsnew/3.12.html and extract key performance optimizations.'
    };
    $('task').value = taskMap[text] || text;
  }
};

// Theme Toggle
const themeBtn = $('theme-btn');
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('pagepilot-theme', theme);
}

themeBtn.onclick = () => {
  const current = document.documentElement.getAttribute('data-theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next);
};

// Initialize Theme
const savedTheme = localStorage.getItem('pagepilot-theme');
if (savedTheme) {
  applyTheme(savedTheme);
}

// Settings Drawer Management
const settingsBtn = $('settings-btn');
const settingsDrawer = $('settings-drawer');
const closeSettings = $('close-settings');
const saveSettingsBtn = $('save-settings');
const resetSettingsBtn = $('reset-settings');

function openDrawer() {
  settingsDrawer.classList.add('open');
  settingsDrawer.setAttribute('aria-hidden', 'false');
}

function closeDrawer() {
  settingsDrawer.classList.remove('open');
  settingsDrawer.setAttribute('aria-hidden', 'true');
}

settingsBtn.onclick = openDrawer;
closeSettings.onclick = closeDrawer;
settingsDrawer.onclick = (e) => {
  if (e.target === settingsDrawer) closeDrawer();
};

function getStoredSettings() {
  const raw = localStorage.getItem('pagepilot-settings');
  if (raw) {
    try {
      return JSON.parse(raw);
    } catch (e) {}
  }
  return {
    provider: 'google',
    model: 'gemini-2.5-flash',
    apiKey: '',
    temperature: 0.4,
    maxSteps: 25,
    vision: true,
    headless: true,
    keepOpen: false,
    cdpUrl: ''
  };
}

function populateSettingsUI() {
  const s = getStoredSettings();
  $('cfg-provider').value = s.provider || 'google';
  $('cfg-model').value = s.model || 'gemini-2.5-flash';
  $('cfg-key').value = s.apiKey || '';
  $('cfg-temp').value = s.temperature ?? 0.4;
  $('cfg-max-steps').value = s.maxSteps ?? 25;
  $('cfg-vision').checked = s.vision !== false;
  $('cfg-headless').checked = !!s.headless;
  $('cfg-keep-open').checked = !!s.keepOpen;
  $('cfg-cdp').value = s.cdpUrl || '';
  $('model-pill').textContent = s.model || 'Gemini 2.5 Flash';
}

saveSettingsBtn.onclick = () => {
  const newSettings = {
    provider: $('cfg-provider').value,
    model: $('cfg-model').value,
    apiKey: $('cfg-key').value,
    temperature: parseFloat($('cfg-temp').value) || 0.4,
    maxSteps: parseInt($('cfg-max-steps').value, 10) || 25,
    vision: $('cfg-vision').checked,
    headless: $('cfg-headless').checked,
    keepOpen: $('cfg-keep-open').checked,
    cdpUrl: $('cfg-cdp').value.trim()
  };
  localStorage.setItem('pagepilot-settings', JSON.stringify(newSettings));
  $('model-pill').textContent = newSettings.model;
  closeDrawer();
  showToast('Settings saved successfully', 'success');
};

resetSettingsBtn.onclick = () => {
  localStorage.removeItem('pagepilot-settings');
  populateSettingsUI();
  showToast('Settings reset to defaults', 'info');
};

// History Modal Management
const historyBtn = $('history-btn');
const historyModal = $('history-modal');
const closeHistory = $('close-history');
const clearHistoryBtn = $('clear-history');

function renderHistory() {
  const list = $('history-list');
  if (!list) return;
  if (runHistory.length === 0) {
    list.innerHTML = '<div class="empty">No past execution logs in this session.</div>';
    return;
  }
  list.innerHTML = runHistory
    .map(
      (h) => `
    <div style="padding: 10px 0; border-bottom: 1px solid var(--line); font-size: 13.5px;">
      <div style="display: flex; justify-content: space-between; font-weight: 600;">
        <span>${h.status} (${h.steps} steps)</span>
        <span style="color: var(--mut); font-weight: 400;">${h.timestamp}</span>
      </div>
      <p style="color: var(--mut); margin-top: 3px; font-size: 13px;">${h.task}</p>
    </div>
  `
    )
    .join('');
}

historyBtn.onclick = () => {
  historyModal.classList.add('open');
  historyModal.setAttribute('aria-hidden', 'false');
  renderHistory();
};

closeHistory.onclick = () => {
  historyModal.classList.remove('open');
  historyModal.setAttribute('aria-hidden', 'true');
};

historyModal.onclick = (e) => {
  if (e.target === historyModal) {
    historyModal.classList.remove('open');
    historyModal.setAttribute('aria-hidden', 'true');
  }
};

clearHistoryBtn.onclick = () => {
  runHistory = [];
  renderHistory();
  showToast('History cleared', 'info');
};

// Initialize Application
initPreviewRows();
populateSettingsUI();
runSimulated(true);
