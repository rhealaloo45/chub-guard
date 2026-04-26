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
exports.updateDiagnostics = updateDiagnostics;
exports.clearDiagnostics = clearDiagnostics;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
function updateDiagnostics(collection, violations) {
    collection.clear();
    const byFile = new Map();
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
                new vscode.DiagnosticRelatedInformation(new vscode.Location(vscode.Uri.file(filePath), range), `Fix: ${v.chub_hint.substring(0, 200)}`)
            ];
        }
        const key = uri.toString();
        if (!byFile.has(key))
            byFile.set(key, []);
        byFile.get(key).push(diag);
    }
    for (const [uriStr, diags] of byFile) {
        collection.set(vscode.Uri.parse(uriStr), diags);
    }
}
function clearDiagnostics(collection) {
    collection.clear();
}
