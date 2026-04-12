import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dir = fileURLToPath(new URL('.', import.meta.url));
const repoRoot = path.join(__dir, '..', '..');
const initRoot = path.join(__dir, '..');

// Create assets dir inside init
const assetsDir = path.join(initRoot, 'assets');
fs.mkdirSync(path.join(assetsDir, 'scripts'), { recursive: true });
fs.mkdirSync(path.join(assetsDir, '.chub-docs'), { recursive: true });

// Copy current files from repo into the package so npm can bundle them
fs.copyFileSync(path.join(repoRoot, 'scripts', 'chub_guard.py'), path.join(assetsDir, 'scripts', 'chub_guard.py'));
fs.copyFileSync(path.join(repoRoot, '.pre-commit-config.yaml'), path.join(assetsDir, '.pre-commit-config.yaml'));
fs.copyFileSync(path.join(repoRoot, '.chub-docs', 'registry.json'), path.join(assetsDir, '.chub-docs', 'registry.json'));

console.log('✅ Prepack: Copied fresh files from repo to init/assets/ for packaging.');
