import { execFile } from 'child_process';
import * as path from 'path';
import * as vscode from 'vscode';

export interface Violation {
  filename: string;
  line: number;
  col: number;
  code: string;
  message: string;
  chub_hint: string | null;
  doc_id: string | null;
  severity: 'Breaking' | 'Warning' | 'Info';
}

export function runScan(): Promise<Violation[]> {
  return new Promise((resolve) => {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot) return resolve([]);

    const pythonPath = vscode.workspace.getConfiguration('chubGuard').get<string>('pythonPath', 'python');

    // Try chub-guard-init run-all --json first
    // Falls back to python scripts/chub_guard.py scan --json
    const guardScript = path.join(workspaceRoot, 'scripts', 'chub_guard.py');

    const args = [guardScript, 'scan', '--json'];

    execFile(pythonPath, args, {
      cwd: workspaceRoot,
      timeout: 30000,
      maxBuffer: 1024 * 1024 * 5,
    }, (err, stdout, stderr) => {
      // exit 1 is expected when violations found — not a real error
      if (!stdout || !stdout.trim()) return resolve([]);

      try {
        // Find JSON array in output (may have rich terminal output before it)
        const jsonMatch = stdout.match(/(\[[\s\S]*\])/);
        if (!jsonMatch) return resolve([]);

        const raw = JSON.parse(jsonMatch[1]);
        const violations: Violation[] = raw.map((item: any) => ({
          filename: item.filename || '',
          line: item.location?.row || 1,
          col: item.location?.column || 1,
          code: item.code || 'CHUB',
          message: item.message || 'Deprecated usage detected',
          chub_hint: item.chub_hint || null,
          doc_id: item.doc_id || null,
          severity: getSeverity(item.message || ''),
        }));
        resolve(violations);
      } catch {
        resolve([]);
      }
    });
  });
}

function getSeverity(message: string): 'Breaking' | 'Warning' | 'Info' {
  const lower = message.toLowerCase();
  if (lower.includes('deprecated')) return 'Breaking';
  if (lower.includes('legacy')) return 'Warning';
  return 'Info';
}
