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

function isPreCommitInstalled() {
  try {
    execSync('pre-commit --version', { stdio: 'ignore' });
    return true;
  } catch {
    return false;
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

// ─── Main ─────────────────────────────────────────────────────────────────────

console.log('');
console.log('chub-guard-init');
console.log('───────────────────────────────────────');
console.log('Setting up chub_guard in this project...');
console.log('');

// 1. Create directories
try { mkdirSync(join(cwd, 'scripts'), { recursive: true }); } catch {}
try { mkdirSync(join(cwd, '.chub-docs'), { recursive: true }); } catch {}

// 2. Write files (with overwrite protection)
await safeWrite(join(cwd, 'scripts', 'chub_guard.py'), CHUB_GUARD_PY, 'scripts/chub_guard.py');
await safeWrite(join(cwd, '.pre-commit-config.yaml'), PRE_COMMIT_YAML, '.pre-commit-config.yaml');
await safeWrite(join(cwd, '.chub-docs', 'registry.json'), REGISTRY_JSON, '.chub-docs/registry.json');

console.log('');

// 3. Check for git repo
if (!isGitRepo()) {
  console.log('⚠ No .git directory found.');
  console.log('  Run git init first, then: pre-commit install');
  console.log('');
  process.exit(0);
}

// 4. Run pre-commit install
if (isPreCommitInstalled()) {
  try {
    execSync('pre-commit install', { cwd, stdio: 'inherit' });
    console.log('');
    console.log('✓ pre-commit hook installed');
    console.log('');
    console.log('───────────────────────────────────────');
    console.log('Done! chub_guard will now run on every commit.');
    console.log('');
    console.log('Next steps:');
    console.log('  1. Install chub:  npm install -g @aisuite/chub');
    console.log('  2. Make a commit to test the guard');
    console.log('');
  } catch {
    console.log('⚠ pre-commit install failed. Run manually: pre-commit install');
  }
} else {
  console.log('⚠ pre-commit not found. To finish setup:');
  console.log('');
  console.log('  pip install pre-commit');
  console.log('  pre-commit install');
  console.log('');
  console.log('Then install chub: npm install -g @aisuite/chub');
}
