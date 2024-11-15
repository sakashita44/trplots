# To generate the graph, run this script.

# Move to the directory where this script is located
Set-Location $PSScriptRoot

# Execute init.ps1
./init.ps1

# Execute gen_graph.py
python .src/gen_graph.py
