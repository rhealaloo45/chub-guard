import * as vscode from 'vscode';
import { runScan } from './runner';
import { updateDiagnostics, clearDiagnostics } from './diagnostics';
import { ChubGuardPanel } from './panel';
import { pauseHook, resumeHook, getHookStatus } from './hookManager';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  vscode.window.showInformationMessage('chub-guard extension is now active!');

  const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  statusBar.command = 'chubGuard.scan';
  statusBar.text = '$(shield) chub-guard';
  statusBar.show();
  context.subscriptions.push(statusBar);

  const diagCollection = vscode.languages.createDiagnosticCollection('chub-guard');
  context.subscriptions.push(diagCollection);

  // Scan on file save
  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(async (doc) => {
      const ext = path.extname(doc.fileName);
      const supported = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp'];
      if (!supported.includes(ext)) return;

      statusBar.text = '$(sync~spin) chub-guard scanning...';
      const violations = await runScan(context);
      updateDiagnostics(diagCollection, violations);

      if (violations.length === 0) {
        statusBar.text = '$(check) chub-guard: Clean';
        ChubGuardPanel.updateViolations([], getHookStatus());
        return;
      }

      statusBar.text = `$(warning) chub-guard: ${violations.length} issue${violations.length !== 1 ? 's' : ''}`;

      const showOnSave = vscode.workspace.getConfiguration('chubGuard').get<boolean>('showPanelOnSave', true);
      if (showOnSave) {
        ChubGuardPanel.show(context.extensionUri, violations, getHookStatus());
      } else {
        ChubGuardPanel.updateViolations(violations, getHookStatus());
      }
    })
  );

  // Commands
  context.subscriptions.push(
    vscode.commands.registerCommand('chubGuard.scan', async () => {
      statusBar.text = '$(sync~spin) chub-guard scanning...';
      const violations = await runScan(context);
      updateDiagnostics(diagCollection, violations);
      statusBar.text = violations.length === 0
        ? '$(check) chub-guard: Clean'
        : `$(warning) chub-guard: ${violations.length} issue${violations.length !== 1 ? 's' : ''}`;
      ChubGuardPanel.show(context.extensionUri, violations, getHookStatus());
    }),

    vscode.commands.registerCommand('chubGuard.pauseHook', async () => {
      await pauseHook();
      vscode.window.showInformationMessage('chub-guard: Pre-commit hook paused. Commits will not be blocked.');
      ChubGuardPanel.updateHookStatus(getHookStatus());
    }),

    vscode.commands.registerCommand('chubGuard.resumeHook', async () => {
      await resumeHook();
      vscode.window.showInformationMessage('chub-guard: Pre-commit hook resumed.');
      ChubGuardPanel.updateHookStatus(getHookStatus());
    }),

    vscode.commands.registerCommand('chubGuard.hidePanel', () => {
      vscode.workspace.getConfiguration('chubGuard').update('showPanelOnSave', false, true);
      vscode.window.showInformationMessage('chub-guard: Panel hidden on save. Use "chub-guard: Scan Now" to show manually.');
    }),

    vscode.commands.registerCommand('chubGuard.showPanel', () => {
      vscode.workspace.getConfiguration('chubGuard').update('showPanelOnSave', true, true);
    })
  );
}

export function deactivate() {}
