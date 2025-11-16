#!/bin/bash
# Sync and update dependencies using uv

set -e

echo "🔄 Syncing dependencies with uv..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Sync dependencies
echo "📥 Installing/updating dependencies..."
uv pip sync pyproject.toml

echo "✅ Dependencies synced successfully!"
echo ""
echo "Activate virtual environment with:"
echo "  source .venv/bin/activate"
