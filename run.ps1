# To generate the graph, run this script.

# Move to the directory where this script is located
Set-Location $PSScriptRoot

# Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# Execute gen_graph.py
python .\src\gen_graph.py
