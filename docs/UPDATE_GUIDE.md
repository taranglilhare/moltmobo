# 🔄 MoltMobo Update Guide

**Keep your MoltMobo installation up-to-date with latest features!**

---

## 🚀 Quick Update

### One-Command Update:

```bash
cd moltmobo
bash update.sh
```

**That's it!** The script will:
- ✅ Backup your `.env` file
- ✅ Check for local changes
- ✅ Fetch latest updates
- ✅ Show what's new
- ✅ Update code
- ✅ Restore your settings
- ✅ Update dependencies
- ✅ Run tests

---

## 📋 Manual Update (Step-by-Step)

If you prefer manual control:

### Step 1: Backup Your Settings

```bash
cd moltmobo

# Backup .env file
cp .env .env.backup

# Backup any custom files
cp -r plugins plugins.backup
```

### Step 2: Check Current Status

```bash
# See current version
git log -1 --oneline

# Check for local changes
git status
```

### Step 3: Stash Local Changes (if any)

```bash
# Save your changes temporarily
git stash save "My changes before update"

# Or commit them
git add .
git commit -m "My custom changes"
```

### Step 4: Fetch Latest Changes

```bash
# Fetch from GitHub
git fetch origin main

# See what's new
git log HEAD..origin/main --oneline
```

### Step 5: Pull Updates

```bash
# Pull latest changes
git pull origin main
```

### Step 6: Restore Your Settings

```bash
# Restore .env file
cp .env.backup .env

# Restore custom plugins (if needed)
cp -r plugins.backup/* plugins/
```

### Step 7: Update Dependencies

**For Termux:**
```bash
pip install --upgrade -r requirements-termux.txt
```

**For PC:**
```bash
pip install --upgrade -r requirements.txt
```

### Step 8: Test

```bash
# Quick test
python quick_test.py

# Full demo
python complete_demo.py
```

---

## 🔧 Common Update Scenarios

### Scenario 1: Simple Update (No Local Changes)

```bash
cd moltmobo
git pull origin main
pip install --upgrade -r requirements-termux.txt
python quick_test.py
```

**Done in 30 seconds!**

### Scenario 2: Update with Local Changes

```bash
cd moltmobo

# Save your changes
git stash

# Update
git pull origin main

# Restore your changes
git stash pop

# Update dependencies
pip install --upgrade -r requirements-termux.txt
```

### Scenario 3: Force Update (Discard Local Changes)

```bash
cd moltmobo

# ⚠️ WARNING: This will delete your local changes!
git reset --hard origin/main

# Restore .env
cp .env.backup .env

# Update dependencies
pip install --upgrade -r requirements-termux.txt
```

### Scenario 4: Update Specific Feature

```bash
cd moltmobo

# Update only specific files
git checkout origin/main -- ar_overlay.py
git checkout origin/main -- docs/AR_OVERLAY.md

# Test
python demo_ar.py
```

---

## 📦 Update Only Dependencies

If code is up-to-date but you want latest packages:

```bash
cd moltmobo

# Termux
pip install --upgrade -r requirements-termux.txt

# PC
pip install --upgrade -r requirements.txt
```

---

## 🔍 Check for Updates

### See if Updates Available:

```bash
cd moltmobo

# Fetch latest
git fetch origin main

# Check difference
git log HEAD..origin/main --oneline
```

**Output:**
```
abc1234 Add AR Overlay feature
def5678 Fix Termux compatibility
ghi9012 Update README
```

If you see commits, updates are available!

### See What Changed:

```bash
# Detailed changes
git log HEAD..origin/main

# File changes
git diff HEAD..origin/main --stat

# Specific file changes
git diff HEAD..origin/main -- ar_overlay.py
```

---

## 🛡️ Safe Update Practices

### 1. Always Backup

```bash
# Backup entire directory
cp -r moltmobo moltmobo.backup

# Or just important files
cp .env .env.backup
cp -r data data.backup
```

### 2. Test After Update

```bash
# Test APIs
python quick_test.py

# Test features
python demo_ar.py
python complete_demo.py

# Run agent
python moltmobo_enhanced.py
```

### 3. Rollback if Needed

```bash
# Go back to previous version
git log --oneline  # Find commit hash
git reset --hard <commit-hash>

# Or restore from backup
rm -rf moltmobo
cp -r moltmobo.backup moltmobo
```

---

## 📅 Update Schedule

### Recommended:

- **Weekly**: Check for updates
- **Monthly**: Full update with dependencies
- **On new features**: Update immediately

### Check Update Frequency:

```bash
# See when last updated
git log -1 --format="%ar"

# See all recent updates
git log --since="1 week ago" --oneline
```

---

## 🔔 Auto-Update (Advanced)

### Create Cron Job:

```bash
# Edit crontab
crontab -e

# Add this line (check daily at 2 AM)
0 2 * * * cd ~/moltmobo && bash update.sh -y
```

### Create Update Alias:

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'alias moltmobo-update="cd ~/moltmobo && bash update.sh"' >> ~/.bashrc

# Reload
source ~/.bashrc

# Now just type:
moltmobo-update
```

---

## 🐛 Troubleshooting Updates

### Issue: Merge Conflicts

```bash
# See conflicting files
git status

# Option 1: Keep their changes
git checkout --theirs <file>

# Option 2: Keep your changes
git checkout --ours <file>

# Option 3: Manual merge
nano <file>  # Edit and resolve conflicts
git add <file>
git commit
```

### Issue: Update Failed

```bash
# Reset to clean state
git reset --hard HEAD

# Try again
git pull origin main
```

### Issue: Dependencies Won't Install

```bash
# Clear pip cache
pip cache purge

# Reinstall
pip install --upgrade --force-reinstall -r requirements-termux.txt
```

### Issue: Lost .env File

```bash
# Restore from backup
cp .env.backup .env

# Or recreate
cp .env.example .env
nano .env  # Add your API keys
```

---

## 📊 Update History

### View Changelog:

```bash
# See all changes
git log --oneline

# See changes with details
git log --pretty=format:"%h - %s (%ar)" --graph

# See specific file history
git log --follow -- ar_overlay.py
```

### Compare Versions:

```bash
# Compare current with 5 commits ago
git diff HEAD~5..HEAD

# Compare specific commits
git diff abc1234..def5678
```

---

## 💡 Update Tips

1. **Always backup .env** - Your API keys are precious!
2. **Read changelog** - Know what's changing
3. **Test after update** - Ensure everything works
4. **Update regularly** - Get latest features and fixes
5. **Keep backups** - Safety first!

---

## 🎯 Quick Commands Reference

```bash
# Check for updates
git fetch origin main && git log HEAD..origin/main --oneline

# Quick update
git pull origin main && pip install --upgrade -r requirements-termux.txt

# Full update with backup
cp .env .env.backup && git pull origin main && cp .env.backup .env

# Rollback
git reset --hard HEAD~1

# Force update
git reset --hard origin/main

# Update script
bash update.sh
```

---

## 📚 Related Documentation

- **Installation**: [docs/TERMUX_INSTALL.md](docs/TERMUX_INSTALL.md)
- **Troubleshooting**: [TERMUX_FIX.md](TERMUX_FIX.md)
- **Features**: [README.md](README.md)

---

**Keep MoltMobo updated for latest features!** 🚀

**Update Time**: ~2 minutes  
**Frequency**: Weekly recommended  
**Safety**: Always backup first!
