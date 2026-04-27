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

    let pythonPath = vscode.workspace.getConfiguration('chubGuard').get<string>('pythonPath', 'python');

    const guardScript = path.join(workspaceRoot, 'scripts', 'chub_guard.py');
    const args = [guardScript, 'scan', '--json'];

    const runWithPython = (pyPath: string) => {
      execFile(pyPath, args, {
        cwd: workspaceRoot,
        timeout: 30000,
        maxBuffer: 1024 * 1024 * 5,
      }, (err, stdout, stderr) => {
        // If it failed due to python not found, and we used 'python', try 'python3'
        if (err && (err as any).code === 'ENOENT' && pyPath === 'python') {
          return runWithPython('python3');
        }

        if (!stdout || !stdout.trim()) return resolve([]);

        try {
          // The JSON is always printed as a single line at the end by json.dumps(output)
          // Find the last line that starts with [
          const lines = stdout.trim().split('\n');
          let jsonStr = '';
          for (let i = lines.length - 1; i >= 0; i--) {
            if (lines[i].trim().startsWith('[')) {
              jsonStr = lines[i].trim();
              break;
            }
          }

          if (!jsonStr) {
            // Fallback to match everything between the outermost brackets
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
          console.error("Failed to parse chub-guard JSON", e);
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
