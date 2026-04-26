import { execSync } from 'child_process';
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

type HookStatus = 'active' | 'paused' | 'not-installed';

let _status: HookStatus = 'not-installed';

export function getHookStatus(): HookStatus {
  const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!root) return 'not-installed';
  const config = path.join(root, '.pre-commit-config.yaml');
  const backup = path.join(root, '.pre-commit-config.yaml.bak');
  if (fs.existsSync(backup)) return 'paused';
  if (fs.existsSync(config)) return 'active';
  return 'not-installed';
}

export async function pauseHook(): Promise<void> {
  const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!root) return;
  const config = path.join(root, '.pre-commit-config.yaml');
  const backup = path.join(root, '.pre-commit-config.yaml.bak');
  try {
    if (fs.existsSync(config)) {
      fs.renameSync(config, backup);
      execSync('pre-commit uninstall', { cwd: root, stdio: 'pipe' });
    }
  } catch { /* graceful */ }
}

export async function resumeHook(): Promise<void> {
  const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!root) return;
  const config = path.join(root, '.pre-commit-config.yaml');
  const backup = path.join(root, '.pre-commit-config.yaml.bak');
  try {
    if (fs.existsSync(backup)) {
      fs.renameSync(backup, config);
      execSync('pre-commit install', { cwd: root, stdio: 'pipe' });
    }
  } catch { /* graceful */ }
}

export async function forceCommit(): Promise<void> {
  const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (!root) return;
  try {
    // Open terminal and run git commit --no-verify
    // Let user type their commit message
    const terminal = vscode.window.createTerminal('chub-guard: Force Commit');
    terminal.sendText('git commit --no-verify');
    terminal.show();
  } catch (e) {
    vscode.window.showErrorMessage(`Force commit failed: ${e}`);
  }
}
