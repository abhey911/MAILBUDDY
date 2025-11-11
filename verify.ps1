# MailBuddy Installation Verification Script
# Run this to verify all files are in place

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MailBuddy Installation Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""
Write-Host "Checking project files..." -ForegroundColor Yellow

# Root files
$rootFiles = @(
    "main.py",
    "requirements.txt",
    "README.md",
    "QUICKSTART.md",
    "PROJECT-STRUCTURE.md",
    "DELIVERABLES.md",
    "setup.ps1",
    ".gitignore"
)

foreach ($file in $rootFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $allGood = $false
    }
}

# Agents
Write-Host ""
Write-Host "Checking agents/..." -ForegroundColor Yellow
$agentFiles = @("agents/__init__.py", "agents/email_agent.py")
foreach ($file in $agentFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $allGood = $false
    }
}

# Utils
Write-Host ""
Write-Host "Checking utils/..." -ForegroundColor Yellow
$utilFiles = @(
    "utils/__init__.py",
    "utils/contacts.py",
    "utils/email_folder_manager.py",
    "utils/inbox_monitor.py",
    "utils/email_sender.py",
    "utils/mailbuddy_triage.py"
)
foreach ($file in $utilFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $allGood = $false
    }
}

# Docs
Write-Host ""
Write-Host "Checking docs/..." -ForegroundColor Yellow
$docFiles = @(
    "docs/IMAP-SETUP.md",
    "docs/automation-guide.md",
    "docs/flowcharts.md"
)
foreach ($file in $docFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $allGood = $false
    }
}

# Data
Write-Host ""
Write-Host "Checking data/..." -ForegroundColor Yellow
if (Test-Path "data/known_contacts.example.json") {
    Write-Host "  ✓ data/known_contacts.example.json" -ForegroundColor Green
} else {
    Write-Host "  ✗ data/known_contacts.example.json MISSING" -ForegroundColor Red
    $allGood = $false
}

# Tests
Write-Host ""
Write-Host "Checking tests/..." -ForegroundColor Yellow
$testFiles = @(
    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_email_folder_manager.py",
    "tests/test_mailbuddy_triage.py"
)
foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $allGood = $false
    }
}

# Final result
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "  ✓ All files present!" -ForegroundColor Green
    Write-Host "  Ready to run setup.ps1" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Run: .\setup.ps1" -ForegroundColor White
    Write-Host "  2. Then: streamlit run main.py" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "  ✗ Some files are missing!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please check the missing files above." -ForegroundColor Yellow
    Write-Host ""
}

# Count files
Write-Host "File Statistics:" -ForegroundColor Cyan
$pyFiles = (Get-ChildItem -Recurse -Filter "*.py" -File | Measure-Object).Count
$mdFiles = (Get-ChildItem -Recurse -Filter "*.md" -File | Measure-Object).Count
$allFiles = (Get-ChildItem -Recurse -File | Measure-Object).Count

Write-Host "  Python files: $pyFiles" -ForegroundColor White
Write-Host "  Markdown docs: $mdFiles" -ForegroundColor White
Write-Host "  Total files: $allFiles" -ForegroundColor White
Write-Host ""
