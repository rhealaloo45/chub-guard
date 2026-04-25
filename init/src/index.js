#!/usr/bin/env node
import { mkdirSync, writeFileSync, existsSync, readFileSync } from 'fs';
import { execSync } from 'child_process';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { createInterface } from 'readline';

const cwd = process.cwd();

// Resolve paths to source files bundled in this package's assets folder
const __dir = fileURLToPath(new URL('.', import.meta.url));
const assetsDir = join(__dir, '..', 'assets');

const CHUB_GUARD_PY   = readFileSync(join(assetsDir, 'scripts', 'chub_guard.py'), 'utf8');
const PRE_COMMIT_YAML = readFileSync(join(assetsDir, '.pre-commit-config.yaml'), 'utf8');
const REGISTRY_JSON   = readFileSync(join(assetsDir, '.chub-docs', 'registry.json'), 'utf8');

// ─── Helpers ──────────────────────────────────────────────────────────────────

function getPreCommitCommand() {
  try {
    execSync('pre-commit --version', { stdio: 'ignore' });
    return 'pre-commit';
  } catch {}
  const py = getPythonCommand();
  if (py) {
    try {
      execSync(`${py} -m pre_commit --version`, { stdio: 'ignore' });
      return `${py} -m pre_commit`;
    } catch {}
  }
  return null;
}

function getPythonCommand() {
  try {
    execSync('python3 --version', { stdio: 'ignore' });
    return 'python3';
  } catch {}
  try {
    execSync('python --version', { stdio: 'ignore' });
    return 'python';
  } catch {}
  return null;
}

function updateGitignore() {
  const gitignorePath = join(cwd, '.gitignore');
  const ignoreLines = [
    '',
    '# chub-guard cache',
    '.chub-docs/*.md',
    'scripts/__pycache__/',
  ];
  
  let content = '';
  if (existsSync(gitignorePath)) {
    content = readFileSync(gitignorePath, 'utf8');
  }
  
  // Filter out lines that already exist
  const linesToAdd = ignoreLines.filter(line => {
    if (line === '') return false;
    return !content.includes(line);
  });
  
  if (linesToAdd.length > 0) {
    const prefix = content === '' ? '' : (content.endsWith('\n') ? '' : '\n');
    const addition = (content === '' ? '' : '\n# chub-guard\n') + linesToAdd.join('\n') + '\n';
    writeFileSync(gitignorePath, content + prefix + addition, 'utf8');
    console.log('✓ Updated .gitignore');
  }
}

function isGitRepo() {
  return existsSync(join(cwd, '.git'));
}

async function ask(question) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase());
    });
  });
}

async function safeWrite(filePath, content, label) {
  if (existsSync(filePath)) {
    const answer = await ask(`⚠ ${label} already exists. Overwrite? (y/n): `);
    if (answer !== 'y') {
      console.log(`  skipped ${label}`);
      return;
    }
  }
  try {
    writeFileSync(filePath, content, 'utf8');
    console.log(`✓ ${label}`);
  } catch (err) {
    console.log(`✗ Failed to write ${label}: ${err.message}`);
  }
}

function installChub() {
  console.log('📦 Checking for @aisuite/chub documentation engine...');
  try {
    // Check if installed globally
    execSync('chub --version', { stdio: 'ignore' });
    console.log('✓ @aisuite/chub is already installed');
  } catch {
    console.log('  Installing @aisuite/chub globally...');
    try {
      execSync('npm install -g @aisuite/chub', { stdio: 'inherit' });
      console.log('✓ @aisuite/chub installed successfully');
    } catch (err) {
      console.log('⚠ Failed to install @aisuite/chub automatically.');
      console.log('  Please run manually: npm install -g @aisuite/chub');
    }
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
if (args[0] === 'run-all') {
  const guardPath = join(cwd, 'scripts', 'chub_guard.py');
  if (!existsSync(guardPath)) {
    console.log('❌ Error: chub_guard.py not found in scripts/. Run npx chub-guard-init first.');
    process.exit(1);
  }
  
  console.log('');
  console.log('🚀 Running chub-guard on all project files...');
  console.log('───────────────────────────────────────');
  console.log('  This will scan every file in the project and generate');
  console.log('  a detailed markdown report in your root directory.');
  console.log('');
  try {
    const py = getPythonCommand() || 'python';
    execSync(`${py} "${guardPath}" run`, { stdio: 'inherit' });
    process.exit(0);
  } catch (err) {
    process.exit(1);
  }
}

console.log('');
console.log('chub-guard-init');
console.log('───────────────────────────────────────');
console.log('Setting up chub_guard in this project...');
console.log('');

// 1. Install chub engine
installChub();
console.log('');

// 2. Create directories
try { mkdirSync(join(cwd, 'scripts'), { recursive: true }); } catch {}
try { mkdirSync(join(cwd, '.chub-docs'), { recursive: true }); } catch {}

// 3. Write files (with overwrite protection)
await safeWrite(join(cwd, 'scripts', 'chub_guard.py'), CHUB_GUARD_PY, 'scripts/chub_guard.py');
await safeWrite(join(cwd, '.pre-commit-config.yaml'), PRE_COMMIT_YAML, '.pre-commit-config.yaml');
await safeWrite(join(cwd, '.chub-docs', 'registry.json'), REGISTRY_JSON, '.chub-docs/registry.json');

// 4. Update .gitignore
updateGitignore();

console.log('');

// 5. Check for git repo
if (!isGitRepo()) {
  console.log('⚠ No .git directory found.');
  console.log('  Run git init first, then: pre-commit install');
  console.log('');
  process.exit(0);
}

// 6. Run pre-commit install
const preCommitCmd = getPreCommitCommand();
if (preCommitCmd) {
  try {
    execSync(`${preCommitCmd} install`, { cwd, stdio: 'inherit' });
    console.log('');
    console.log('✓ pre-commit hook installed');
    console.log('');
    console.log('───────────────────────────────────────');
    console.log('Done! chub_guard will now run on every commit.');
    console.log('');
    console.log('Next steps:');
    console.log('  1. Make a commit to test the guard');
    console.log('  2. Or run manually on the whole project: npx chub-guard-init run-all');
    console.log('');
  } catch {
    console.log(`⚠ ${preCommitCmd} install failed. Run manually: ${preCommitCmd} install`);
  }
} else {
  console.log('⚠ pre-commit not found. To finish setup:');
  console.log('');
  print('  pip install pre-commit');
  print('  pre-commit install');
  console.log('');
}
