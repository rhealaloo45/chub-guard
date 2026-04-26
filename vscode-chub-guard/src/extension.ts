import * as vscode from 'vscode';
import { runScan } from './runner';
import { updateDiagnostics, clearDiagnostics } from './diagnostics';
import { ChubGuardPanel } from './panel';
import { pauseHook, resumeHook, getHookStatus } from './hookManager';
import { execSync } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

export function activate(context: vscode.ExtensionContext) {
  const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
  statusBar.command = 'chubGuard.scan';
  statusBar.show();
  context.subscriptions.push(statusBar);

  const diagCollection = vscode.languages.createDiagnosticCollection('chub-guard');
  context.subscriptions.push(diagCollection);

  // Auto-setup on activation
  autoSetup(statusBar);

  // Scan on file save
  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(async (doc) => {
      const ext = path.extname(doc.fileName);
      const supported = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp'];
      if (!supported.includes(ext)) return;

      statusBar.text = '$(sync~spin) chub-guard scanning...';
      const violations = await runScan();
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
      const violations = await runScan();
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

function autoSetup(statusBar: vscode.StatusBarItem) {
  const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!workspaceRoot) return;

  const guardScript = path.join(workspaceRoot, 'scripts', 'chub_guard.py');
  if (fs.existsSync(guardScript)) return;

  statusBar.text = '$(sync~spin) chub-guard: Setting up...';

  // Try pip first, then fall back to pipx
  const setupCommands = [
    'pip install chub-guard-init && chub-guard-init',
    'pip3 install chub-guard-init && chub-guard-init',
    'pipx run chub-guard-init',
  ];

  let setupDone = false;
  for (const cmd of setupCommands) {
    try {
      execSync(cmd, { cwd: workspaceRoot, timeout: 60000, stdio: 'pipe' });
      setupDone = true;
      break;
    } catch {
      continue;
    }
  }

  if (setupDone) {
    statusBar.text = '$(check) chub-guard: Ready';
    vscode.window.showInformationMessage(
      'chub-guard was automatically set up in this project. A pre-commit hook is now active.',
      'View what was installed'
    ).then(choice => {
      if (choice === 'View what was installed') {
        vscode.workspace.openTextDocument(path.join(workspaceRoot, 'scripts', 'chub_guard.py'))
          .then(doc => vscode.window.showTextDocument(doc));
      }
    });
  } else {
    // pip not found — extension still works using bundled deprecations
    statusBar.text = '$(warning) chub-guard: Limited mode';
    vscode.window.showWarningMessage(
      'chub-guard: Could not auto-install. Install manually: pip install chub-guard-init && chub-guard-init',
      'Copy command'
    ).then(choice => {
      if (choice === 'Copy command') {
        vscode.env.clipboard.writeText('pip install chub-guard-init && chub-guard-init');
      }
    });
  }
}

export function deactivate() {}
