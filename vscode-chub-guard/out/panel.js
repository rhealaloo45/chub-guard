"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ChubGuardPanel = void 0;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const hookManager_1 = require("./hookManager");
class ChubGuardPanel {
    static _panel;
    static _violations = [];
    static _hookStatus = 'not-installed';
    static show(extensionUri, violations, hookStatus) {
        this._violations = violations;
        this._hookStatus = hookStatus;
        if (this._panel) {
            this._panel.reveal(vscode.ViewColumn.Two);
            this._panel.webview.html = this._getHtml(violations, hookStatus);
            return;
        }
        this._panel = vscode.window.createWebviewPanel('chubGuard', '🛡️ chub-guard', vscode.ViewColumn.Two, { enableScripts: true });
        this._panel.webview.html = this._getHtml(violations, hookStatus);
        this._panel.webview.onDidReceiveMessage(async (msg) => {
            switch (msg.command) {
                case 'jumpToLine': {
                    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
                    const filePath = path.isAbsolute(msg.file)
                        ? msg.file
                        : path.join(workspaceRoot, msg.file);
                    const doc = await vscode.workspace.openTextDocument(filePath);
                    const editor = await vscode.window.showTextDocument(doc, vscode.ViewColumn.One);
                    const line = Math.max(0, msg.line - 1);
                    const range = new vscode.Range(line, 0, line, 0);
                    editor.selection = new vscode.Selection(line, 0, line, 0);
                    editor.revealRange(range, vscode.TextEditorRevealType.InCenter);
                    break;
                }
                case 'pauseHook':
                    vscode.commands.executeCommand('chubGuard.pauseHook');
                    break;
                case 'resumeHook':
                    vscode.commands.executeCommand('chubGuard.resumeHook');
                    break;
                case 'forceCommit': {
                    const confirm = await vscode.window.showWarningMessage('This will bypass the chub-guard pre-commit hook. Deprecated code will be committed. Are you sure?', { modal: true }, 'Yes, commit anyway');
                    if (confirm === 'Yes, commit anyway') {
                        await (0, hookManager_1.forceCommit)();
                    }
                    break;
                }
                case 'useLLM': {
                    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
                    const reportPath = path.join(workspaceRoot, 'chub_guard_report.md');
                    try {
                        const doc = await vscode.workspace.openTextDocument(reportPath);
                        const content = doc.getText();
                        await vscode.env.clipboard.writeText(content);
                        vscode.window.showInformationMessage('Report copied to clipboard. Paste into your coding agent to fix all issues.');
                    }
                    catch {
                        vscode.window.showErrorMessage('chub_guard_report.md not found. Run a scan first.');
                    }
                    break;
                }
                case 'hidePanel':
                    vscode.commands.executeCommand('chubGuard.hidePanel');
                    break;
            }
        });
        this._panel.onDidDispose(() => { this._panel = undefined; });
    }
    static updateViolations(violations, hookStatus) {
        this._violations = violations;
        this._hookStatus = hookStatus;
        if (this._panel) {
            this._panel.webview.html = this._getHtml(violations, hookStatus);
        }
    }
    static updateHookStatus(hookStatus) {
        this._hookStatus = hookStatus;
        if (this._panel) {
            this._panel.webview.html = this._getHtml(this._violations, hookStatus);
        }
    }
    static _getHtml(violations, hookStatus) {
        const hookColor = hookStatus === 'active' ? '#4caf50' : hookStatus === 'paused' ? '#ff9800' : '#9e9e9e';
        const hookLabel = hookStatus === 'active' ? '🟢 Active' : hookStatus === 'paused' ? '🔴 Paused' : '⚫ Not installed';
        const hookBtn = hookStatus === 'active'
            ? `<button onclick="vscode.postMessage({command:'pauseHook'})">Pause Hook</button>`
            : hookStatus === 'paused'
                ? `<button onclick="vscode.postMessage({command:'resumeHook'})">Resume Hook</button>`
                : '';
        // Group violations by filename
        const grouped = new Map();
        violations.forEach((v, i) => {
            const key = v.filename;
            if (!grouped.has(key))
                grouped.set(key, []);
            grouped.get(key).push({ v, i });
        });
        // Build file-grouped HTML
        const fileGroups = Array.from(grouped.entries()).map(([filename, items]) => {
            const shortName = path.basename(filename);
            const breakingCount = items.filter(x => x.v.severity === 'Breaking').length;
            const warningCount = items.filter(x => x.v.severity === 'Warning').length;
            const infoCount = items.filter(x => x.v.severity === 'Info').length;
            const badges = [];
            if (breakingCount > 0)
                badges.push(`<span class="badge breaking">${breakingCount} breaking</span>`);
            if (warningCount > 0)
                badges.push(`<span class="badge warning">${warningCount} warning</span>`);
            if (infoCount > 0)
                badges.push(`<span class="badge info">${infoCount} info</span>`);
            const rows = items.map(({ v, i }) => {
                const sevColor = v.severity === 'Breaking' ? '#f44336' : v.severity === 'Warning' ? '#ff9800' : '#2196f3';
                const sevIcon = v.severity === 'Breaking' ? '🔴' : v.severity === 'Warning' ? '🟡' : '🔵';
                return `
          <div class="violation" id="v${i}">
            <input type="checkbox" id="cb${i}" onchange="toggleDone(${i})">
            <div class="violation-body">
              <div class="violation-header">
                <span class="sev" style="color:${sevColor}">${sevIcon} ${v.severity}</span>
                <span class="line-link" onclick="jump(${i})">Line ${v.line}</span>
              </div>
              <span class="msg">${escapeHtml(v.message)}</span>
              ${v.doc_id ? `<span class="doc">[${v.doc_id}]</span>` : ''}
            </div>
          </div>`;
            }).join('');
            return `
        <details class="file-group" open>
          <summary class="file-header">
            <span class="file-icon">📄</span>
            <span class="file-name" title="${escapeHtml(filename)}">${escapeHtml(shortName)}</span>
            <span class="file-count">${items.length}</span>
            <div class="badge-row">${badges.join('')}</div>
          </summary>
          <div class="file-path">${escapeHtml(filename)}</div>
          <div class="file-violations">${rows}</div>
        </details>`;
        }).join('');
        const violationData = JSON.stringify(violations.map(v => ({
            file: v.filename,
            line: v.line
        })));
        const fileCount = grouped.size;
        return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body { font-family: var(--vscode-font-family); font-size: 13px; color: var(--vscode-foreground); padding: 12px; margin: 0; }
  h2 { font-size: 14px; margin: 0 0 4px; display: flex; align-items: center; gap: 8px; }
  .summary { font-size: 11px; color: var(--vscode-descriptionForeground); margin-bottom: 12px; }
  .count { color: #f44336; font-weight: 600; }

  /* File group dropdown */
  .file-group { margin-bottom: 6px; border: 1px solid var(--vscode-widget-border, #333); border-radius: 5px; overflow: hidden; }
  .file-header { padding: 7px 10px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 12px; list-style: none; background: var(--vscode-sideBar-background); user-select: none; }
  .file-header::-webkit-details-marker { display: none; }
  .file-header::before { content: '▶'; font-size: 9px; transition: transform 0.15s; color: var(--vscode-descriptionForeground); }
  details[open] > .file-header::before { transform: rotate(90deg); }
  .file-header:hover { background: var(--vscode-list-hoverBackground); }
  .file-icon { font-size: 14px; }
  .file-name { font-weight: 600; color: var(--vscode-textLink-foreground); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
  .file-count { font-size: 10px; background: var(--vscode-badge-background); color: var(--vscode-badge-foreground); padding: 1px 6px; border-radius: 10px; font-weight: 600; min-width: 16px; text-align: center; }
  .file-path { font-size: 10px; color: var(--vscode-descriptionForeground); padding: 2px 10px 4px; background: var(--vscode-editor-background); border-bottom: 1px solid var(--vscode-widget-border, #333); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .file-violations { padding: 0 10px; background: var(--vscode-editor-background); }

  .badge-row { display: flex; gap: 4px; margin-left: auto; }
  .badge { font-size: 9px; padding: 1px 5px; border-radius: 3px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.3px; }
  .badge.breaking { background: rgba(244,67,54,0.15); color: #f44336; }
  .badge.warning { background: rgba(255,152,0,0.15); color: #ff9800; }
  .badge.info { background: rgba(33,150,243,0.15); color: #2196f3; }

  /* Individual violations inside file groups */
  .violation { display: flex; align-items: flex-start; gap: 8px; padding: 7px 0; border-bottom: 1px solid var(--vscode-widget-border, #222); }
  .violation:last-child { border-bottom: none; }
  .violation.done { opacity: 0.35; }
  .violation.done .msg { text-decoration: line-through; }
  .violation-body { flex: 1; display: flex; flex-direction: column; gap: 2px; }
  .violation-header { display: flex; align-items: center; gap: 8px; }
  .sev { font-size: 11px; font-weight: 600; }
  .line-link { color: var(--vscode-textLink-foreground, #4fc3f7); cursor: pointer; font-size: 11px; text-decoration: underline; font-weight: 600; }
  .line-link:hover { opacity: 0.8; }
  .msg { font-size: 12px; color: var(--vscode-foreground); line-height: 1.4; }
  .doc { font-size: 10px; color: var(--vscode-descriptionForeground); }

  .actions { display: flex; gap: 8px; margin: 14px 0; flex-wrap: wrap; }
  button { padding: 5px 12px; font-size: 12px; border: 1px solid var(--vscode-button-border, transparent); border-radius: 3px; cursor: pointer; background: var(--vscode-button-background); color: var(--vscode-button-foreground); }
  button:hover { background: var(--vscode-button-hoverBackground); }
  button.secondary { background: var(--vscode-button-secondaryBackground); color: var(--vscode-button-secondaryForeground); }
  .hook-section { margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--vscode-widget-border, #333); }
  .hook-row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .hook-label { font-size: 12px; }
  .empty { color: var(--vscode-descriptionForeground); padding: 20px 0; text-align: center; }
  .hide-hint { font-size: 11px; color: var(--vscode-descriptionForeground); margin-top: 4px; cursor: pointer; text-decoration: underline; }
</style>
</head>
<body>
<h2>🛡️ chub-guard &nbsp;<span class="count">${violations.length} issue${violations.length !== 1 ? 's' : ''}</span></h2>
<div class="summary">${violations.length > 0 ? `across ${fileCount} file${fileCount !== 1 ? 's' : ''}` : ''}</div>

${violations.length === 0
            ? '<div class="empty">✓ No deprecated patterns detected.</div>'
            : `<div id="violations">${fileGroups}</div>
     <div class="actions">
       <button onclick="fixManually()">Fix Manually</button>
       <button class="secondary" onclick="useLLM()">📋 Copy to fix with LLM</button>
     </div>`}

<div class="hook-section">
  <div class="hook-row">
    <span class="hook-label">Pre-commit hook: <strong style="color:${hookColor}">${hookLabel}</strong></span>
    ${hookBtn}
    <button class="secondary" onclick="forceCommit()">Force Commit</button>
  </div>
</div>

<div class="hide-hint" onclick="hidePanel()">Hide panel on save</div>

<script>
  const vscode = acquireVsCodeApi();
  const violations = ${violationData};
  let currentIdx = 0;

  function jump(idx) {
    const v = violations[idx];
    vscode.postMessage({ command: 'jumpToLine', file: v.file, line: v.line });
  }

  function fixManually() {
    const unchecked = violations.findIndex((_, i) => {
      const cb = document.getElementById('cb' + i);
      return cb && !cb.checked;
    });
    if (unchecked >= 0) jump(unchecked);
  }

  function useLLM() {
    vscode.postMessage({ command: 'useLLM' });
  }

  function forceCommit() {
    vscode.postMessage({ command: 'forceCommit' });
  }

  function hidePanel() {
    vscode.postMessage({ command: 'hidePanel' });
  }

  function toggleDone(idx) {
    const row = document.getElementById('v' + idx);
    const cb = document.getElementById('cb' + idx);
    if (row && cb) {
      row.classList.toggle('done', cb.checked);
      if (cb.checked) {
        const next = violations.findIndex((_, i) => i > idx && !document.getElementById('cb' + i)?.checked);
        if (next >= 0) jump(next);
      }
    }
  }

  function escapeHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }
</script>
</body>
</html>`;
    }
}
exports.ChubGuardPanel = ChubGuardPanel;
function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
