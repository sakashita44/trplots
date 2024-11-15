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

# If Input directory does not exist, create it
if (-not (Test-Path .\Inputs)) {
    New-Item -ItemType Directory -Name Inputs
}

# If Output directory does not exist, create it
if (-not (Test-Path .\Outputs)) {
    New-Item -ItemType Directory -Name Outputs
}

# If Inputs\instructions.csv does not exist, copy etc\instructions.csv-template to create it
if (-not (Test-Path .\Inputs\instructions.csv)) {
    Copy-Item .\etc\instructions.csv-template .\Inputs\instructions.csv
}
