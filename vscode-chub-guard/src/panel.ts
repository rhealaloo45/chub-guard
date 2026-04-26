import * as vscode from 'vscode';
import * as path from 'path';
import { Violation } from './runner';
import { forceCommit } from './hookManager';

type HookStatus = 'active' | 'paused' | 'not-installed';

export class ChubGuardPanel {
  private static _panel: vscode.WebviewPanel | undefined;
  private static _violations: Violation[] = [];
  private static _hookStatus: HookStatus = 'not-installed';

  static show(extensionUri: vscode.Uri, violations: Violation[], hookStatus: HookStatus) {
    this._violations = violations;
    this._hookStatus = hookStatus;

    if (this._panel) {
      this._panel.reveal(vscode.ViewColumn.Two);
      this._panel.webview.html = this._getHtml(violations, hookStatus);
      return;
    }

    this._panel = vscode.window.createWebviewPanel(
      'chubGuard',
      '🛡️ chub-guard',
      vscode.ViewColumn.Two,
      { enableScripts: true }
    );

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
          const confirm = await vscode.window.showWarningMessage(
            'This will bypass the chub-guard pre-commit hook. Deprecated code will be committed. Are you sure?',
            { modal: true },
            'Yes, commit anyway'
          );
          if (confirm === 'Yes, commit anyway') {
            await forceCommit();
          }
          break;
        }
        case 'useLLM': {
          const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
          const reportPath = path.join(workspaceRoot, 'chub_guard_report.md');
          try {
            const doc = await vscode.workspace.openTextDocument(reportPath);
            await vscode.window.showTextDocument(doc, vscode.ViewColumn.One);
            const content = doc.getText();
            await vscode.env.clipboard.writeText(content);
            vscode.window.showInformationMessage('Report copied to clipboard. Paste into your coding agent to fix all issues.');
          } catch {
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

  static updateViolations(violations: Violation[], hookStatus: HookStatus) {
    this._violations = violations;
    this._hookStatus = hookStatus;
    if (this._panel) {
      this._panel.webview.html = this._getHtml(violations, hookStatus);
    }
  }

  static updateHookStatus(hookStatus: HookStatus) {
    this._hookStatus = hookStatus;
    if (this._panel) {
      this._panel.webview.html = this._getHtml(this._violations, hookStatus);
    }
  }

  private static _getHtml(violations: Violation[], hookStatus: HookStatus): string {
    const hookColor = hookStatus === 'active' ? '#4caf50' : hookStatus === 'paused' ? '#ff9800' : '#9e9e9e';
    const hookLabel = hookStatus === 'active' ? '🟢 Active' : hookStatus === 'paused' ? '🔴 Paused' : '⚫ Not installed';
    const hookBtn = hookStatus === 'active'
      ? `<button onclick="vscode.postMessage({command:'pauseHook'})">Pause Hook</button>`
      : hookStatus === 'paused'
      ? `<button onclick="vscode.postMessage({command:'resumeHook'})">Resume Hook</button>`
      : '';

    const violationRows = violations.map((v, i) => {
      const sevColor = v.severity === 'Breaking' ? '#f44336' : v.severity === 'Warning' ? '#ff9800' : '#2196f3';
      const sevIcon = v.severity === 'Breaking' ? '🔴' : v.severity === 'Warning' ? '🟡' : '🔵';
      return `
        <div class="violation" id="v${i}">
          <input type="checkbox" id="cb${i}" onchange="toggleDone(${i})">
          <div class="violation-body">
            <span class="sev" style="color:${sevColor}">${sevIcon} ${v.severity}</span>
            <span class="file" onclick="jump(${i})">${v.filename}:${v.line}</span>
            <span class="msg">${escapeHtml(v.message)}</span>
            ${v.doc_id ? `<span class="doc">[${v.doc_id}]</span>` : ''}
          </div>
        </div>`;
    }).join('');

    const violationData = JSON.stringify(violations.map(v => ({
      file: v.filename,
      line: v.line
    })));

    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  body { font-family: var(--vscode-font-family); font-size: 13px; color: var(--vscode-foreground); padding: 12px; margin: 0; }
  h2 { font-size: 14px; margin: 0 0 12px; display: flex; align-items: center; gap: 8px; }
  .count { color: #f44336; font-weight: 600; }
  .violation { display: flex; align-items: flex-start; gap: 8px; padding: 8px 0; border-bottom: 1px solid var(--vscode-widget-border, #333); }
  .violation.done { opacity: 0.4; text-decoration: line-through; }
  .violation-body { flex: 1; display: flex; flex-direction: column; gap: 2px; }
  .sev { font-size: 11px; font-weight: 600; }
  .file { color: var(--vscode-textLink-foreground, #4fc3f7); cursor: pointer; font-size: 12px; text-decoration: underline; }
  .file:hover { opacity: 0.8; }
  .msg { font-size: 12px; color: var(--vscode-foreground); }
  .doc { font-size: 11px; color: var(--vscode-descriptionForeground); }
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

${violations.length === 0
  ? '<div class="empty">✓ No deprecated patterns detected.</div>'
  : `<div id="violations">${violationRows}</div>
     <div class="actions">
       <button onclick="fixManually()">Fix Manually</button>
       <button class="secondary" onclick="useLLM()">Use LLM</button>
     </div>`
}

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
    // Jump to first unchecked violation
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
      // Auto-jump to next unchecked
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

function escapeHtml(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
