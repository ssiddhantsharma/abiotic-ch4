# make_figure.py sits at the repo root rather than in the package.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
