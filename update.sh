#!/bin/bash

# MoltMobo Update Script
# Updates your local MoltMobo installation with latest changes from GitHub

echo "======================================================================"
echo "🔄 MoltMobo Update Script"
echo "======================================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "moltmobo_enhanced.py" ]; then
    echo -e "${RED}❌ Error: Not in MoltMobo directory${NC}"
    echo "Please run this script from the moltmobo folder"
    exit 1
fi

echo "📍 Current directory: $(pwd)"
echo ""

# Step 1: Backup current .env file
echo "📦 Step 1: Backing up your .env file..."
if [ -f ".env" ]; then
    cp .env .env.backup
    echo -e "${GREEN}✓ .env backed up to .env.backup${NC}"
else
    echo -e "${YELLOW}⚠️  No .env file found (will create after update)${NC}"
fi
echo ""

# Step 2: Check for local changes
echo "🔍 Step 2: Checking for local changes..."
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${GREEN}✓ No local changes detected${NC}"
else
    echo -e "${YELLOW}⚠️  You have local changes${NC}"
    echo ""
    echo "Your changes:"
    git status --short
    echo ""
    read -p "Do you want to stash your changes? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git stash save "Auto-stash before update $(date)"
        echo -e "${GREEN}✓ Changes stashed${NC}"
    else
        echo -e "${RED}❌ Cannot update with uncommitted changes${NC}"
        echo "Please commit or stash your changes first"
        exit 1
    fi
fi
echo ""

# Step 3: Fetch latest changes
echo "📥 Step 3: Fetching latest changes from GitHub..."
git fetch origin main
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Fetched latest changes${NC}"
else
    echo -e "${RED}❌ Failed to fetch changes${NC}"
    exit 1
fi
echo ""

# Step 4: Show what will be updated
echo "📋 Step 4: Changes to be applied..."
CHANGES=$(git log HEAD..origin/main --oneline)
if [ -z "$CHANGES" ]; then
    echo -e "${GREEN}✓ Already up to date!${NC}"
    echo ""
    echo "Your MoltMobo is already running the latest version 🎉"
    exit 0
else
    echo "$CHANGES"
fi
echo ""

# Step 5: Confirm update
read -p "Do you want to apply these updates? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Update cancelled${NC}"
    exit 0
fi
echo ""

# Step 6: Pull changes
echo "⬇️  Step 6: Pulling latest changes..."
git pull origin main
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Successfully pulled latest changes${NC}"
else
    echo -e "${RED}❌ Failed to pull changes${NC}"
    exit 1
fi
echo ""

# Step 7: Restore .env file
echo "🔧 Step 7: Restoring your .env file..."
if [ -f ".env.backup" ]; then
    cp .env.backup .env
    echo -e "${GREEN}✓ .env file restored${NC}"
fi
echo ""

# Step 8: Update dependencies
echo "📦 Step 8: Updating dependencies..."
read -p "Do you want to update Python packages? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if in Termux
    if [ -d "/data/data/com.termux" ]; then
        echo "Detected Termux - using requirements-termux.txt"
        pip install --upgrade -r requirements-termux.txt
    else
        echo "Using standard requirements.txt"
        pip install --upgrade -r requirements.txt
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies updated${NC}"
    else
        echo -e "${YELLOW}⚠️  Some dependencies failed to update${NC}"
    fi
else
    echo -e "${YELLOW}Skipped dependency update${NC}"
fi
echo ""

# Step 9: Run tests
echo "🧪 Step 9: Testing installation..."
read -p "Do you want to run tests? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python quick_test.py
fi
echo ""

# Step 10: Summary
echo "======================================================================"
echo "✅ UPDATE COMPLETE!"
echo "======================================================================"
echo ""
echo "📊 Summary:"
echo "  • Repository updated to latest version"
echo "  • Your .env file preserved"
echo "  • Dependencies updated (if selected)"
echo ""
echo "🚀 What's New:"
git log HEAD~5..HEAD --pretty=format:"  • %s" --reverse
echo ""
echo ""
echo "💡 Next Steps:"
echo "  1. Review changes: git log -5"
echo "  2. Test: python quick_test.py"
echo "  3. Run: python moltmobo_enhanced.py"
echo ""
echo "📚 Documentation:"
echo "  • README.md - Complete guide"
echo "  • CHANGELOG.md - All changes"
echo ""
echo "======================================================================"
