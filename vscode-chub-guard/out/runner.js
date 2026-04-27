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
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.runScan = void 0;
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const vscode = __importStar(require("vscode"));
function runScan() {
    return new Promise((resolve) => {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot)
            return resolve([]);
        let pythonPath = vscode.workspace.getConfiguration('chubGuard').get('pythonPath', 'python');
        const guardScript = path.join(workspaceRoot, 'scripts', 'chub_guard.py');
        const args = [guardScript, 'scan', '--json'];
        const runWithPython = (pyPath) => {
            (0, child_process_1.execFile)(pyPath, args, {
                cwd: workspaceRoot,
                timeout: 30000,
                maxBuffer: 1024 * 1024 * 5,
            }, (err, stdout, stderr) => {
                // If it failed due to python not found, and we used 'python', try 'python3'
                if (err && err.code === 'ENOENT' && pyPath === 'python') {
                    return runWithPython('python3');
                }
                if (!stdout || !stdout.trim())
                    return resolve([]);
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
                    console.error("Failed to parse chub-guard JSON", e);
                    resolve([]);
                }
            });
        };
        runWithPython(pythonPath);
    });
}
exports.runScan = runScan;
function getSeverity(message) {
    const lower = message.toLowerCase();
    if (lower.includes('deprecated'))
        return 'Breaking';
    if (lower.includes('legacy'))
        return 'Warning';
    return 'Info';
}
