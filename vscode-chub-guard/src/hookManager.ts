import { execSync } from 'child_process';
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

type HookStatus = 'active' | 'paused' | 'not-installed';

let _status: HookStatus = 'not-installed';

function getRepoRoot(): string | null {
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || null;
}

// VULN-11: Recover from orphaned backup files on extension activation
export function recoverOrphanedBackup(): void {
  const root = getRepoRoot();
  if (!root) return;
  const config = path.join(root, '.pre-commit-config.yaml');
  const backup = path.join(root, '.pre-commit-config.yaml.bak');
  const lockFile = backup + '.lock';

  if (fs.existsSync(lockFile)) {
    console.warn('[chub-guard] Found orphaned lock file — recovering backup.');
    try {
      if (fs.existsSync(backup) && !fs.existsSync(config)) {
        fs.renameSync(backup, config);
      }
      fs.unlinkSync(lockFile);
    } catch (e) {
      console.warn('[chub-guard] Recovery failed:', e);
    }
  }
}

export function getHookStatus(): HookStatus {
  const root = getRepoRoot();
  if (!root) return 'not-installed';
  const config = path.join(root, '.pre-commit-config.yaml');
  const backup = path.join(root, '.pre-commit-config.yaml.bak');
  if (fs.existsSync(backup)) return 'paused';
  if (fs.existsSync(config)) return 'active';
  return 'not-installed';
}

export async function pauseHook(): Promise<void> {
  const root = getRepoRoot();
  if (!root) return;
  const config = path.join(root, '.pre-commit-config.yaml');
  const backup = path.join(root, '.pre-commit-config.yaml.bak');
  const lockFile = backup + '.lock';
  try {
    if (fs.existsSync(config)) {
      // VULN-11: Write lock file before rename to detect crashes
      fs.writeFileSync(lockFile, process.pid.toString(), 'utf8');
      fs.renameSync(config, backup);
      try {
        execSync('pre-commit uninstall', { cwd: root, stdio: 'pipe' });
      } catch (e: any) {
        console.warn('[chub-guard] pre-commit uninstall warning:', e.message);
      }
      // Remove lock after successful operation
      if (fs.existsSync(lockFile)) fs.unlinkSync(lockFile);
    }
  } catch (e: any) {
    console.warn('[chub-guard] pauseHook error:', e.message);
    // Clean up lock on failure
    if (fs.existsSync(lockFile)) fs.unlinkSync(lockFile);
  }
}

export async function resumeHook(): Promise<void> {
  const root = getRepoRoot();
  if (!root) return;
  const config = path.join(root, '.pre-commit-config.yaml');
  const backup = path.join(root, '.pre-commit-config.yaml.bak');
  const lockFile = backup + '.lock';
  try {
    if (fs.existsSync(backup)) {
      fs.writeFileSync(lockFile, process.pid.toString(), 'utf8');
      fs.renameSync(backup, config);
      try {
        execSync('pre-commit install', { cwd: root, stdio: 'pipe' });
      } catch (e: any) {
        console.warn('[chub-guard] pre-commit install warning:', e.message);
      }
      if (fs.existsSync(lockFile)) fs.unlinkSync(lockFile);
    }
  } catch (e: any) {
    console.warn('[chub-guard] resumeHook error:', e.message);
    if (fs.existsSync(lockFile)) fs.unlinkSync(lockFile);
  }
}

// VULN-07: Scoped force commit — only bypasses chub-guard hook, not all hooks
export async function forceCommit(): Promise<void> {
  const root = getRepoRoot();
  if (!root) return;

  const hookPath = path.join(root, '.git', 'hooks', 'pre-commit');
  const bakPath = hookPath + '.chub-bak';

  if (!fs.existsSync(hookPath)) {
    // No pre-commit hook — just open terminal for normal commit
    const terminal = vscode.window.createTerminal('chub-guard: Commit');
    terminal.sendText('git commit');
    terminal.show();
    return;
  }

  try {
    // Temporarily rename only the pre-commit hook
    fs.renameSync(hookPath, bakPath);
    const terminal = vscode.window.createTerminal('chub-guard: Force Commit');
    terminal.sendText('git commit');
    terminal.show();

    // Restore hook after a delay (give user time to complete commit)
    setTimeout(() => {
      try {
        if (fs.existsSync(bakPath)) {
          fs.renameSync(bakPath, hookPath);
        }
      } catch (restoreErr: any) {
        console.warn('[chub-guard] Failed to restore pre-commit hook:', restoreErr.message);
        vscode.window.showWarningMessage(
          `chub-guard: Could not auto-restore pre-commit hook. Run: mv ${bakPath} ${hookPath}`
        );
      }
    }, 30000); // 30 seconds
  } catch (e: any) {
    // Restore immediately on error
    if (fs.existsSync(bakPath)) {
      try { fs.renameSync(bakPath, hookPath); } catch { /* best effort */ }
    }
    vscode.window.showErrorMessage(`Force commit failed: ${e.message}`);
  }
}

