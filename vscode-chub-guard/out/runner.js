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
exports.runScan = runScan;
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const vscode = __importStar(require("vscode"));
function runScan(context) {
    return new Promise((resolve) => {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot)
            return resolve([]);
        const pythonPath = vscode.workspace.getConfiguration('chubGuard').get('pythonPath', 'python');
        // Always use the script bundled inside the extension itself.
        // This means the user never needs to have chub_guard.py in their project.
        const guardScript = path.join(context.extensionPath, 'scripts', 'chub_guard.py');
        // --root tells the scanner which directory to scan (the user's project)
        const args = [guardScript, 'scan', '--json', '--root', workspaceRoot];
        const runWithPython = (pyPath) => {
            (0, child_process_1.execFile)(pyPath, args, {
                cwd: workspaceRoot,
                timeout: 60000,
                maxBuffer: 1024 * 1024 * 5,
            }, (err, stdout, stderr) => {
                // If python not found, try python3
                if (err && err.code === 'ENOENT' && pyPath === 'python') {
                    return runWithPython('python3');
                }
                // If python3 also not found, tell the user
                if (err && err.code === 'ENOENT' && pyPath === 'python3') {
                    vscode.window.showErrorMessage('chub-guard: Python not found. Please install Python and ensure it is on your PATH, or set chubGuard.pythonPath in settings.');
                    return resolve([]);
                }
                if (!stdout || !stdout.trim())
                    return resolve([]);
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
                        }
                        else {
                            return resolve([]);
                        }
                    }
                    const raw = JSON.parse(jsonStr);
                    const violations = raw.map((item) => ({
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
                }
                catch (e) {
                    console.error('chub-guard: Failed to parse scan output', e);
                    resolve([]);
                }
            });
        };
        runWithPython(pythonPath);
    });
}
function getSeverity(message) {
    const lower = message.toLowerCase();
    if (lower.includes('deprecated'))
        return 'Breaking';
    if (lower.includes('legacy'))
        return 'Warning';
    return 'Info';
}
