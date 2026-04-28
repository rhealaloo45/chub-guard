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

export function runScan(context: vscode.ExtensionContext): Promise<Violation[]> {
  return new Promise((resolve) => {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot) return resolve([]);

    const pythonPath = vscode.workspace.getConfiguration('chubGuard').get<string>('pythonPath', 'python');

    // Always use the script bundled inside the extension itself.
    // This means the user never needs to have chub_guard.py in their project.
    const guardScript = path.join(context.extensionPath, 'scripts', 'chub_guard.py');

    // --root tells the scanner which directory to scan (the user's project)
    const args = [guardScript, 'scan', '--json', '--root', workspaceRoot];

    const runWithPython = (pyPath: string) => {
      execFile(pyPath, args, {
        cwd: workspaceRoot,
        timeout: 60000,
        maxBuffer: 1024 * 1024 * 5,
      }, (err, stdout, stderr) => {
        // If python not found, try python3
        if (err && (err as any).code === 'ENOENT' && pyPath === 'python') {
          return runWithPython('python3');
        }

        // If python3 also not found, tell the user
        if (err && (err as any).code === 'ENOENT' && pyPath === 'python3') {
          vscode.window.showErrorMessage(
            'chub-guard: Python not found. Please install Python and ensure it is on your PATH, or set chubGuard.pythonPath in settings.'
          );
          return resolve([]);
        }

        if (!stdout || !stdout.trim()) return resolve([]);

        try {
          // Find JSON array in output (may have rich terminal output before it)
          const lines = stdout.trim().split('\n');
          let jsonStr = '';
          for (let i = lines.length - 1; i >= 0; i--) {
            if (lines[i].trim().startsWith('[')) {
              jsonStr = lines[i].trim();
              break;
            }
          }

          if (!jsonStr) {
            // Fallback: match everything between the outermost brackets
            const firstIdx = stdout.indexOf('[');
            const lastIdx = stdout.lastIndexOf(']');
            if (firstIdx !== -1 && lastIdx !== -1 && lastIdx > firstIdx) {
              jsonStr = stdout.substring(firstIdx, lastIdx + 1);
            } else {
              return resolve([]);
            }
          }

          const raw = JSON.parse(jsonStr);
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
        } catch (e) {
          console.error('chub-guard: Failed to parse scan output', e);
          resolve([]);
        }
      });
    };

    runWithPython(pythonPath);
  });
}

function getSeverity(message: string): 'Breaking' | 'Warning' | 'Info' {
  const lower = message.toLowerCase();
  if (lower.includes('deprecated')) return 'Breaking';
  if (lower.includes('legacy')) return 'Warning';
  return 'Info';
}
