from pathlib import Path
import os

DATA_DIR_EN = Path(__file__).parent / "resources" / "En"
DATA_DIR_CN = Path(__file__).parent / "resources" / "Cn"
ENGINE_CACHE_TTL_SECONDS = int(os.environ.get("ENGINE_CACHE_TTL_SECONDS", "0") or 0)
