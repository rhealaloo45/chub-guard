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
exports.forceCommit = exports.resumeHook = exports.pauseHook = exports.getHookStatus = void 0;
const child_process_1 = require("child_process");
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
let _status = 'not-installed';
function getHookStatus() {
    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!root)
        return 'not-installed';
    const config = path.join(root, '.pre-commit-config.yaml');
    const backup = path.join(root, '.pre-commit-config.yaml.bak');
    if (fs.existsSync(backup))
        return 'paused';
    if (fs.existsSync(config))
        return 'active';
    return 'not-installed';
}
exports.getHookStatus = getHookStatus;
async function pauseHook() {
    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!root)
        return;
    const config = path.join(root, '.pre-commit-config.yaml');
    const backup = path.join(root, '.pre-commit-config.yaml.bak');
    try {
        if (fs.existsSync(config)) {
            fs.renameSync(config, backup);
            (0, child_process_1.execSync)('pre-commit uninstall', { cwd: root, stdio: 'pipe' });
        }
    }
    catch { /* graceful */ }
}
exports.pauseHook = pauseHook;
async function resumeHook() {
    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!root)
        return;
    const config = path.join(root, '.pre-commit-config.yaml');
    const backup = path.join(root, '.pre-commit-config.yaml.bak');
    try {
        if (fs.existsSync(backup)) {
            fs.renameSync(backup, config);
            (0, child_process_1.execSync)('pre-commit install', { cwd: root, stdio: 'pipe' });
        }
    }
    catch { /* graceful */ }
}
exports.resumeHook = resumeHook;
async function forceCommit() {
    const root = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!root)
        return;
    try {
        // Open terminal and run git commit --no-verify
        // Let user type their commit message
        const terminal = vscode.window.createTerminal('chub-guard: Force Commit');
        terminal.sendText('git commit --no-verify');
        terminal.show();
    }
    catch (e) {
        vscode.window.showErrorMessage(`Force commit failed: ${e}`);
    }
}
exports.forceCommit = forceCommit;
