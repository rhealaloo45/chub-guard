import * as vscode from 'vscode';
import * as path from 'path';
import { Violation } from './runner';

export function updateDiagnostics(
  collection: vscode.DiagnosticCollection,
  violations: Violation[]
) {
  collection.clear();

  const byFile = new Map<string, vscode.Diagnostic[]>();

  for (const v of violations) {
    const filePath = path.isAbsolute(v.filename)
      ? v.filename
      : path.join(vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '', v.filename);

    const uri = vscode.Uri.file(filePath);
    const line = Math.max(0, v.line - 1);
    const col = Math.max(0, v.col - 1);
    const range = new vscode.Range(line, col, line, col + 100);

    const severity = v.severity === 'Breaking'
      ? vscode.DiagnosticSeverity.Error
      : v.severity === 'Warning'
      ? vscode.DiagnosticSeverity.Warning
      : vscode.DiagnosticSeverity.Information;

    const diag = new vscode.Diagnostic(range, v.message, severity);
    diag.source = 'chub-guard';
    diag.code = v.code;

    // Attach hint as related information for hover tooltip
    if (v.chub_hint) {
      diag.relatedInformation = [
        new vscode.DiagnosticRelatedInformation(
          new vscode.Location(vscode.Uri.file(filePath), range),
          `Fix: ${v.chub_hint.substring(0, 200)}`
        )
      ];
    }

    const key = uri.toString();
    if (!byFile.has(key)) byFile.set(key, []);
    byFile.get(key)!.push(diag);
  }

  for (const [uriStr, diags] of byFile) {
    collection.set(vscode.Uri.parse(uriStr), diags);
  }
}

export function clearDiagnostics(collection: vscode.DiagnosticCollection) {
  collection.clear();
}
