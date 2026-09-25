#!/usr/bin/env python3
"""Rebuild ranked + directory outputs. Requires openpyxl."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name("expand_build.py")), run_name="__main__")
