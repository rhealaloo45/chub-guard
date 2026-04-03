#!/bin/bash
set -e

# Create a temporary directory for the demo
TEMP_DIR=$(mktemp -d)
echo "🚀 Creating temporary git repo at $TEMP_DIR"
cd "$TEMP_DIR"

# Initialize git
git init -q

# Set up dummy git user for commits
git config user.name "Demo User"
git config user.email "demo@example.com"

# Copy the actual tool files to the demo repo
cp -r "$OLDPWD/scripts" .
cp -r "$OLDPWD/.chub-docs" .
cp "$OLDPWD/.pre-commit-config.yaml" .
cp "$OLDPWD/pyproject.toml" .

# Install pre-commit
echo "📦 Installing pre-commit hook..."
pre-commit install >/dev/null 2>&1

# Add base files and make an initial commit so we have a clean state
git add scripts .chub-docs .pre-commit-config.yaml pyproject.toml
git commit -m "Initial commit of tool" -q

echo "=========================================================="
echo "📝 Creating a file with a DEPRECATED import..."
echo "import google.generativeai as genai" > test_app.py
echo "client = genai.Client()" >> test_app.py
git add test_app.py

echo "=========================================================="
echo "🔄 Attempting to commit the deprecated code..."
echo "=========================================================="

# We expect this commit to fail, so we don't exit on error
set +e
git commit -m "Add test app with deprecated import"
COMMIT_STATUS=$?
set -e

if [ $COMMIT_STATUS -ne 0 ]; then
    echo "=========================================================="
    echo "✅ SUCCESS: The pre-commit hook correctly BLOCKED the commit."
else
    echo "=========================================================="
    echo "❌ ERROR: The pre-commit hook allowed the deprecated commit."
    exit 1
fi

echo "=========================================================="
echo "🛠️  Fixing the import to use the current API..."
echo "from google import genai" > test_app.py
echo "client = genai.Client()" >> test_app.py
git add test_app.py

echo "=========================================================="
echo "🔄 Attempting to commit the FIXED code..."
echo "=========================================================="

git commit -m "Add test app with fixed import"

echo "=========================================================="
echo "✅ SUCCESS: The fixed commit was ACCEPTED."
echo "=========================================================="

echo "🧹 Cleaning up..."
cd "$OLDPWD"
rm -rf "$TEMP_DIR"
echo "✨ Demo complete!"
