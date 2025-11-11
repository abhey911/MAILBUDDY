# MailBuddy Setup Script
# Run this script to set up MailBuddy on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MailBuddy Setup Script" -ForegroundColor Cyan
Write-Host "  Think Less, Send Smart" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists. Skipping..." -ForegroundColor Green
} else {
    python -m venv .venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created successfully!" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Create data directory if not exists
Write-Host ""
Write-Host "Setting up data directory..." -ForegroundColor Yellow
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data"
    Write-Host "Created data directory" -ForegroundColor Green
}

# Copy example contacts file if needed
if (-not (Test-Path "data\known_contacts.json")) {
    if (Test-Path "data\known_contacts.example.json") {
        Copy-Item "data\known_contacts.example.json" "data\known_contacts.json"
        Write-Host "Created known_contacts.json from example" -ForegroundColor Green
    }
}

# Setup complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Read QUICKSTART.md for configuration instructions" -ForegroundColor White
Write-Host "2. Get your Gmail App Password (see docs/IMAP-SETUP.md)" -ForegroundColor White
Write-Host "3. Get your Gemini API key from https://makersuite.google.com/app/apikey" -ForegroundColor White
Write-Host ""
Write-Host "To start MailBuddy, run:" -ForegroundColor Yellow
Write-Host "  streamlit run main.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Happy emailing! 📧" -ForegroundColor Green
