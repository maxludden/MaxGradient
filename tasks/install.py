"""Install dependencies for the project."""
from pathlib import Path
from sh import Command, ErrorReturnCode
pdm = Command('pdm')
cd = Command('cd')

CWD = Path.cwd()
