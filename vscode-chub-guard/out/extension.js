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
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
const runner_1 = require("./runner");
const diagnostics_1 = require("./diagnostics");
const panel_1 = require("./panel");
const hookManager_1 = require("./hookManager");
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
function activate(context) {
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBar.command = 'chubGuard.scan';
    statusBar.show();
    context.subscriptions.push(statusBar);
    const diagCollection = vscode.languages.createDiagnosticCollection('chub-guard');
    context.subscriptions.push(diagCollection);
    // Auto-setup on activation
    autoSetup(statusBar);
    // Scan on file save
    context.subscriptions.push(vscode.workspace.onDidSaveTextDocument(async (doc) => {
        const ext = path.extname(doc.fileName);
        const supported = ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp'];
        if (!supported.includes(ext))
            return;
        statusBar.text = '$(sync~spin) chub-guard scanning...';
        const violations = await (0, runner_1.runScan)();
        (0, diagnostics_1.updateDiagnostics)(diagCollection, violations);
        if (violations.length === 0) {
            statusBar.text = '$(check) chub-guard: Clean';
            panel_1.ChubGuardPanel.updateViolations([], (0, hookManager_1.getHookStatus)());
            return;
        }
        statusBar.text = `$(warning) chub-guard: ${violations.length} issue${violations.length !== 1 ? 's' : ''}`;
        const showOnSave = vscode.workspace.getConfiguration('chubGuard').get('showPanelOnSave', true);
        if (showOnSave) {
            panel_1.ChubGuardPanel.show(context.extensionUri, violations, (0, hookManager_1.getHookStatus)());
        }
        else {
            panel_1.ChubGuardPanel.updateViolations(violations, (0, hookManager_1.getHookStatus)());
        }
    }));
    // Commands
    context.subscriptions.push(vscode.commands.registerCommand('chubGuard.scan', async () => {
        statusBar.text = '$(sync~spin) chub-guard scanning...';
        const violations = await (0, runner_1.runScan)();
        (0, diagnostics_1.updateDiagnostics)(diagCollection, violations);
        statusBar.text = violations.length === 0
            ? '$(check) chub-guard: Clean'
            : `$(warning) chub-guard: ${violations.length} issue${violations.length !== 1 ? 's' : ''}`;
        panel_1.ChubGuardPanel.show(context.extensionUri, violations, (0, hookManager_1.getHookStatus)());
    }), vscode.commands.registerCommand('chubGuard.pauseHook', async () => {
        await (0, hookManager_1.pauseHook)();
        vscode.window.showInformationMessage('chub-guard: Pre-commit hook paused. Commits will not be blocked.');
        panel_1.ChubGuardPanel.updateHookStatus((0, hookManager_1.getHookStatus)());
    }), vscode.commands.registerCommand('chubGuard.resumeHook', async () => {
        await (0, hookManager_1.resumeHook)();
        vscode.window.showInformationMessage('chub-guard: Pre-commit hook resumed.');
        panel_1.ChubGuardPanel.updateHookStatus((0, hookManager_1.getHookStatus)());
    }), vscode.commands.registerCommand('chubGuard.hidePanel', () => {
        vscode.workspace.getConfiguration('chubGuard').update('showPanelOnSave', false, true);
        vscode.window.showInformationMessage('chub-guard: Panel hidden on save. Use "chub-guard: Scan Now" to show manually.');
    }), vscode.commands.registerCommand('chubGuard.showPanel', () => {
        vscode.workspace.getConfiguration('chubGuard').update('showPanelOnSave', true, true);
    }));
}
exports.activate = activate;
function autoSetup(statusBar) {
    const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceRoot)
        return;
    const guardScript = path.join(workspaceRoot, 'scripts', 'chub_guard.py');
    if (fs.existsSync(guardScript))
        return;
    statusBar.text = '$(sync~spin) chub-guard: Setting up...';
    // Try pip first, then fall back to pipx
    const setupCommands = [
        'pip install chub-guard-init && chub-guard-init',
        'pip3 install chub-guard-init && chub-guard-init',
        'pipx run chub-guard-init',
    ];
    let setupDone = false;
    for (const cmd of setupCommands) {
        try {
            (0, child_process_1.execSync)(cmd, { cwd: workspaceRoot, timeout: 60000, stdio: 'pipe' });
            setupDone = true;
            break;
        }
        catch {
            continue;
        }
    }
    if (setupDone) {
        statusBar.text = '$(check) chub-guard: Ready';
        vscode.window.showInformationMessage('chub-guard was automatically set up in this project. A pre-commit hook is now active.', 'View what was installed').then(choice => {
            if (choice === 'View what was installed') {
                vscode.workspace.openTextDocument(path.join(workspaceRoot, 'scripts', 'chub_guard.py'))
                    .then(doc => vscode.window.showTextDocument(doc));
            }
        });
    }
    else {
        // pip not found — extension still works using bundled deprecations
        statusBar.text = '$(warning) chub-guard: Limited mode';
        vscode.window.showWarningMessage('chub-guard: Could not auto-install. Install manually: pip install chub-guard-init && chub-guard-init', 'Copy command').then(choice => {
            if (choice === 'Copy command') {
                vscode.env.clipboard.writeText('pip install chub-guard-init && chub-guard-init');
            }
        });
    }
}
function deactivate() { }
exports.deactivate = deactivate;
