# Environment setup script

# Move to the directory where this script is located
Set-Location $PSScriptRoot

# If config.yml does not exist, copy config.yml-template to create it
if (-not (Test-Path .\config.yml)) {
    Copy-Item .\etc\config.yml-template .\config.yml
}

# If .venv does not exist, create a virtual environment
if (-not (Test-Path .\.venv)) {
    py -m venv .venv
}

# Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# Install dependency packages
python -m pip install -r etc\requirements.txt
