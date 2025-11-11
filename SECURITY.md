# 🔒 SECURITY CHECKLIST

## ✅ What's Already Protected

Your `.gitignore` is configured to **NEVER commit**:

- ✅ `.streamlit/` folder (contains secrets.toml)
- ✅ `.venv/` folder (virtual environment)
- ✅ `data/known_contacts.json` (your personal contacts)
- ✅ `.env` files (environment variables)
- ✅ Any file with "password" or "credentials" in name
- ✅ `secrets.toml` anywhere in project

## 🔍 Verify No Secrets in GitHub

Run this command to check what's on GitHub:

```powershell
git ls-files | Select-String -Pattern "secret|password|credential|\.env|\.streamlit"
```

**Expected result:** No matches (clean output)

If any sensitive files appear, see "Emergency: Remove Secrets" section below.

## 📋 Safe Files to Commit

These are **SAFE** to push to GitHub:

- ✅ `main.py` (no hardcoded secrets)
- ✅ `agents/*.py` (uses st.secrets)
- ✅ `utils/*.py` (uses st.secrets)
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ All documentation (`.md` files)
- ✅ `secrets.toml.template` (template only, no real values)
- ✅ `.gitignore`
- ✅ `data/known_contacts.example.json` (example only)

## 🚫 NEVER Commit These

**CRITICAL - NEVER push to GitHub:**

- ❌ `.streamlit/secrets.toml` (real secrets)
- ❌ `.venv/` folder (too large, contains packages)
- ❌ `data/known_contacts.json` (your real contacts)
- ❌ `.env` files (environment variables)
- ❌ Any file with real API keys, passwords, or emails

## 🛡️ How to Store Secrets Safely

### Option 1: Local Development (Recommended)

```powershell
# Create .streamlit folder
New-Item -ItemType Directory -Force -Path .streamlit

# Copy template
Copy-Item secrets.toml.template .streamlit\secrets.toml

# Edit with your real values
notepad .streamlit\secrets.toml
```

File: `.streamlit/secrets.toml` (gitignored ✅)
```toml
GOOGLE_API_KEY = "your_real_api_key"
SENDER_EMAIL = "your@gmail.com"
EMAIL_PASSWORD = "your app password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

### Option 2: Environment Variables

```powershell
# Set for current session
$env:GOOGLE_API_KEY = "your_key"
$env:SENDER_EMAIL = "your@gmail.com"
$env:EMAIL_PASSWORD = "your_password"

# Or create .env file (gitignored ✅)
@"
GOOGLE_API_KEY=your_key
SENDER_EMAIL=your@gmail.com
EMAIL_PASSWORD=your_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
"@ | Out-File -FilePath .env -Encoding UTF8
```

### Option 3: Streamlit Cloud (For Deployment)

When deploying:
1. Push code to GitHub (no secrets)
2. In Streamlit Cloud dashboard → App Settings → Secrets
3. Paste secrets in TOML format (see `SECRETS-FORMAT.md`)

## 🔐 Security Best Practices

### ✅ DO:

1. **Use .streamlit/secrets.toml** for local development
2. **Use Streamlit Cloud Secrets** for deployment
3. **Use Gmail App Passwords** (not regular password)
4. **Keep .gitignore updated** and test it regularly
5. **Use different API keys** for dev/production
6. **Review commits** before pushing
7. **Enable 2FA** on GitHub account

### ❌ DON'T:

1. **Never hardcode secrets** in .py files
2. **Never commit .streamlit/** folder
3. **Never share secrets** in chat, email, or screenshots
4. **Never use real Gmail password** (use App Password)
5. **Never commit .venv/** folder
6. **Never push real contacts** to public repo
7. **Never disable .gitignore** rules

## 🚨 Emergency: Remove Secrets from GitHub

If you accidentally committed secrets:

### Step 1: Immediately Revoke Compromised Credentials

```
1. Gemini API Key: https://makersuite.google.com/app/apikey → Revoke
2. Gmail App Password: https://myaccount.google.com/security → Remove
3. Generate new credentials
```

### Step 2: Remove from Git History

```powershell
# Remove file from all commits (DANGEROUS - backup first!)
git filter-branch --force --index-filter `
  "git rm --cached --ignore-unmatch .streamlit/secrets.toml" `
  --prune-empty --tag-name-filter cat -- --all

# Force push (overwrites remote)
git push origin --force --all
```

### Step 3: Add to .gitignore (if not already)

```powershell
echo ".streamlit/" >> .gitignore
git add .gitignore
git commit -m "Add secrets to gitignore"
git push
```

### Step 4: Verify Removal

Check GitHub repository - secrets file should be gone from all commits.

## 📊 Regular Security Checks

### Weekly Checklist:

```powershell
# 1. Check what's tracked by git
git ls-files

# 2. Check for sensitive patterns
git ls-files | Select-String -Pattern "secret|password|key"

# 3. Verify .gitignore is working
git status --ignored

# 4. Check for large files (might be .venv)
git ls-files | ForEach-Object { Get-Item $_ } | Where-Object { $_.Length -gt 1MB }
```

### Before Every Commit:

```powershell
# Review what you're about to commit
git status
git diff

# Check for secrets in staged files
git diff --cached | Select-String -Pattern "API|password|secret|key"
```

## 🔍 Test Your Security

Run these commands - they should all return clean:

```powershell
# No secrets in tracked files
git grep -i "password\|secret\|api.*key" -- "*.py" "*.toml"

# No .streamlit in repository
git ls-files | Select-String "\.streamlit"

# No real contacts file
git ls-files | Select-String "known_contacts\.json"

# .gitignore is working
Test-Path .streamlit\secrets.toml
# Should return True if file exists, but git status should NOT show it
```

## 📝 Current Status

Based on your repository setup:

- ✅ `.gitignore` properly configured
- ✅ No `.streamlit/` folder in repo
- ✅ No secrets files committed
- ✅ Template file created (`secrets.toml.template`)
- ✅ Safe to push to GitHub

## 🎯 Next Steps

1. **Create local secrets file:**
   ```powershell
   New-Item -ItemType Directory -Force -Path .streamlit
   Copy-Item secrets.toml.template .streamlit\secrets.toml
   notepad .streamlit\secrets.toml  # Fill in real values
   ```

2. **Verify it's ignored:**
   ```powershell
   git status  # Should NOT show .streamlit/secrets.toml
   ```

3. **Test the app:**
   ```powershell
   streamlit run main.py
   ```

4. **Commit updated .gitignore:**
   ```powershell
   git add .gitignore secrets.toml.template SECURITY.md
   git commit -m "Enhanced security: updated .gitignore and added templates"
   git push
   ```

## 📞 Resources

- **GitHub Security:** https://docs.github.com/en/code-security
- **Streamlit Secrets:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- **Git Filter-Branch:** https://git-scm.com/docs/git-filter-branch
- **Gmail App Passwords:** https://support.google.com/accounts/answer/185833

---

**Your secrets are safe! 🔒**

All sensitive data is properly gitignored and will never be committed to GitHub.
