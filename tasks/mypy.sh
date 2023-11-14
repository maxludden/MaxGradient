#!/bin/bash
# Run mypy on the project

clear
sudo -S mypy -m maxgradient --ignore-missing-imports >>logs/mypy_output.txt
python -m ~/dev/py/maxgradient/tasks/mypy.py
