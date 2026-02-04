
# GitHub Push Helper Script

Write-Host "Checking Git Configuration..." -ForegroundColor Cyan

# 1. Check/Set User Config
$currentEmail = git config user.email
if ([string]::IsNullOrWhiteSpace($currentEmail)) {
    $email = Read-Host "Please enter your GitHub Email"
    if (-not [string]::IsNullOrWhiteSpace($email)) {
        git config --global user.email $email
    }
}
else {
    Write-Host "Git Email: $currentEmail" -ForegroundColor Gray
}

$currentName = git config user.name
if ([string]::IsNullOrWhiteSpace($currentName)) {
    $name = Read-Host "Please enter your Name"
    if (-not [string]::IsNullOrWhiteSpace($name)) {
        git config --global user.name $name
    }
}
else {
    Write-Host "Git Name: $currentName" -ForegroundColor Gray
}

# 2. Check/Set Remote
try {
    $currentRemote = git remote get-url origin 2>$null
}
catch {
    $currentRemote = $null
}

if ([string]::IsNullOrWhiteSpace($currentRemote)) {
    Write-Host "`nYou need to create a repository on GitHub first." -ForegroundColor Yellow
    Write-Host "Go to: https://github.com/new"
    Write-Host "Create a repo named 'quran-reel-generator'"
    $repoUrl = Read-Host "`nPaste the HTTPS Repository URL here"
    
    if (-not [string]::IsNullOrWhiteSpace($repoUrl)) {
        git remote add origin $repoUrl
        Write-Host "Remote set to: $repoUrl" -ForegroundColor Green
    }
}
else {
    Write-Host "Remote Origin: $currentRemote" -ForegroundColor Gray
}

# 3. Push
Write-Host "`nPushing to GitHub..." -ForegroundColor Cyan
git push -u origin master

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSuccessfully pushed to GitHub!" -ForegroundColor Green
}
else {
    Write-Host "`nPush failed. Check errors above." -ForegroundColor Red
}
Read-Host "Press Enter to exit"
