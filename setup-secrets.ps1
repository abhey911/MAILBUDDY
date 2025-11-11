# Setup Local Secrets for MailBuddy
# Run this script to create your local secrets file

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MailBuddy Secrets Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if .streamlit folder exists
if (-not (Test-Path ".streamlit")) {
    Write-Host "Creating .streamlit folder..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path .streamlit | Out-Null
    Write-Host "✓ Created .streamlit folder" -ForegroundColor Green
} else {
    Write-Host "✓ .streamlit folder already exists" -ForegroundColor Green
}

# Check if secrets.toml already exists
if (Test-Path ".streamlit\secrets.toml") {
    Write-Host ""
    Write-Host "⚠️  WARNING: .streamlit\secrets.toml already exists!" -ForegroundColor Yellow
    Write-Host ""
    $overwrite = Read-Host "Do you want to overwrite it? (yes/no)"
    
    if ($overwrite -ne "yes") {
        Write-Host ""
        Write-Host "Setup cancelled. Your existing secrets.toml was not modified." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "To edit your secrets manually:" -ForegroundColor Cyan
        Write-Host "  notepad .streamlit\secrets.toml" -ForegroundColor White
        Write-Host ""
        exit
    }
}

# Copy template
Write-Host ""
Write-Host "Creating secrets file from template..." -ForegroundColor Yellow

if (Test-Path "secrets.toml.template") {
    Copy-Item "secrets.toml.template" ".streamlit\secrets.toml" -Force
    Write-Host "✓ Created .streamlit\secrets.toml" -ForegroundColor Green
} else {
    Write-Host "✗ Template file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Creating basic secrets.toml..." -ForegroundColor Yellow
    
    $secretsContent = @"
# MailBuddy Secrets Configuration
# IMPORTANT: This file is gitignored - your secrets are safe!

# Google Gemini API Key
# Get from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# Gmail Configuration
SENDER_EMAIL = "your.email@gmail.com"

# Gmail App Password (NOT regular password!)
# Get from: https://myaccount.google.com/security
EMAIL_PASSWORD = "your app password with spaces"

# SMTP Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
"@
    
    $secretsContent | Out-File -FilePath ".streamlit\secrets.toml" -Encoding UTF8
    Write-Host "✓ Created .streamlit\secrets.toml" -ForegroundColor Green
}

# Verify it's gitignored
Write-Host ""
Write-Host "Verifying security..." -ForegroundColor Yellow

$gitStatus = git status --porcelain 2>&1 | Out-String

if ($gitStatus -match "\.streamlit") {
    Write-Host "✗ WARNING: .streamlit folder is NOT ignored by git!" -ForegroundColor Red
    Write-Host "  Please check your .gitignore file" -ForegroundColor Red
} else {
    Write-Host "✓ .streamlit folder is properly gitignored" -ForegroundColor Green
}

# Open file for editing
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Next Steps" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Opening secrets.toml for editing..." -ForegroundColor Yellow
Write-Host ""
Write-Host "2. You need to fill in these values:" -ForegroundColor Yellow
Write-Host "   • GOOGLE_API_KEY - Get from: https://makersuite.google.com/app/apikey" -ForegroundColor White
Write-Host "   • SENDER_EMAIL - Your Gmail address" -ForegroundColor White
Write-Host "   • EMAIL_PASSWORD - Gmail App Password (NOT regular password!)" -ForegroundColor White
Write-Host "     Get from: https://myaccount.google.com/security" -ForegroundColor White
Write-Host ""
Write-Host "3. Save the file and close the editor" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Run: streamlit run main.py" -ForegroundColor Yellow
Write-Host ""

# Ask if user wants to open the file now
$openNow = Read-Host "Open secrets.toml in notepad now? (yes/no)"

if ($openNow -eq "yes") {
    notepad .streamlit\secrets.toml
    Write-Host ""
    Write-Host "✓ File opened! Fill in your credentials and save." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "To edit later, run:" -ForegroundColor Cyan
    Write-Host "  notepad .streamlit\secrets.toml" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "For detailed help, see:" -ForegroundColor Yellow
Write-Host "  • SECURITY.md - Security best practices" -ForegroundColor White
Write-Host "  • SECRETS-FORMAT.md - Secrets format reference" -ForegroundColor White
Write-Host "  • docs/IMAP-SETUP.md - Gmail setup guide" -ForegroundColor White
Write-Host ""
Write-Host "Your secrets are safe! 🔒" -ForegroundColor Green
Write-Host "The .streamlit folder is gitignored and will NEVER be committed." -ForegroundColor Green
Write-Host ""
