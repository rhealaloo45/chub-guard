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
function runScan() {
    return new Promise((resolve) => {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot)
            return resolve([]);
        const pythonPath = vscode.workspace.getConfiguration('chubGuard').get('pythonPath', 'python');
        // Try chub-guard-init run-all --json first
        // Falls back to python scripts/chub_guard.py scan --json
        const guardScript = path.join(workspaceRoot, 'scripts', 'chub_guard.py');
        const args = [guardScript, 'scan', '--json'];
        (0, child_process_1.execFile)(pythonPath, args, {
            cwd: workspaceRoot,
            timeout: 30000,
            maxBuffer: 1024 * 1024 * 5,
        }, (err, stdout, stderr) => {
            // exit 1 is expected when violations found — not a real error
            if (!stdout || !stdout.trim())
                return resolve([]);
            try {
                // Find JSON array in output (may have rich terminal output before it)
                const jsonMatch = stdout.match(/(\[[\s\S]*\])/);
                if (!jsonMatch)
                    return resolve([]);
                const raw = JSON.parse(jsonMatch[1]);
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
            catch {
                resolve([]);
            }
        });
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
