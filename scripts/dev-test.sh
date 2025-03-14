#!/bin/bash
# Script to rebuild and test vibe-docs initialization in a test project

# Configuration
TEST_PROJECT_DIR="$HOME/Development/test"

# Step 1: Rebuild the vibe-docs project
echo "🔨 Rebuilding vibe-docs..."
npm run build

# Step 2: Create a fresh test directory
echo "🗂️ Creating test directory at $TEST_PROJECT_DIR..."
mkdir -p "$TEST_PROJECT_DIR"
rm -rf "$TEST_PROJECT_DIR/docs" 2>/dev/null

# Step 3: Run the init-docs command directly
echo "🚀 Testing init-docs..."
node ./dist/index.js init --directory="$TEST_PROJECT_DIR/docs" --template=standard

# Step 4: Verify the result
echo ""
echo "📋 Results:"
if [ -d "$TEST_PROJECT_DIR/docs" ]; then
  echo "✅ docs directory created successfully"
  echo "📁 Files created:"
  ls -la "$TEST_PROJECT_DIR/docs"
else
  echo "❌ Failed to create docs directory"
fi

echo ""
echo "Done!"
