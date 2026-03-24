import os
import shutil
from pathlib import Path

# Paths to rename (Directories and Files)
RENAMES = {
    # Directories
    "models/staging/base_normalizada": "models/staging/bases_manuales",
    "models/intermediate/base_normalizada": "models/intermediate/bases_manuales",
    # Files
    "models/sources/_src_bases_manuales.yml": "models/sources/_src_bases_manuales.yml"
}

# String Replacements globally
STR_REPLACEMENTS = [
    # Schema name in yaml
    ("name: bases manuales", "name: bases manuales"),
    ("source_name=\"base normalizada\"", "source_name=\"bases manuales\""),
    
    # Imports / Paths
    ("models.staging.bases_manuales", "models.staging.bases_manuales"),
    ("models.intermediate.bases_manuales", "models.intermediate.bases_manuales"),
    ("models/sources/_src_bases_manuales.yml", "models/sources/_src_bases_manuales.yml"),
    
    # Function names and files
    ("stg_bases_manuales", "stg_bases_manuales"),
    ("int_bases_manuales", "int_bases_manuales"),
    
    # General string traces but avoiding modifying the raw CSV string paths since the user requested "leave the path names in src files the same"
    ("_src_bases_manuales", "_src_bases_manuales")
]

def refactor():
    root = Path("/Users/educifuentes/code/ccu-monitoreo-activos")
    
    # 1. Rename specific directories and files first
    for old_r, new_r in RENAMES.items():
        src = root / old_r
        dst = root / new_r
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"Moved {src.name} -> {dst.name}")
            
    # 2. Rename the python models residing inside the newly moved folders
    for layer in ["staging", "intermediate"]:
        dir_path = root / f"models/{layer}/bases_manuales"
        if dir_path.exists():
            for file in dir_path.glob("*.py"):
                if "base_normalizada" in file.name:
                    new_name = file.name.replace("base_normalizada", "bases_manuales")
                    new_file = dir_path / new_name
                    shutil.move(str(file), str(new_file))
                    print(f"Renamed file {file.name} -> {new_name}")

    # 3. Text Replacements
    changed = 0
    for ext in ["*.py", "*.md", "*.yml"]:
        for file in root.rglob(ext):
            if any(p in file.parts for p in ["venv", ".venv", ".gemini", ".git"]):
                continue
            
            try:
                original = file.read_text("utf-8")
                new_text = original
                for old_val, new_val in STR_REPLACEMENTS:
                    new_text = new_text.replace(old_val, new_val)
                    
                if new_text != original:
                    file.write_text(new_text, "utf-8")
                    changed += 1
                    print(f"Updated content in {file.relative_to(root)}")
            except Exception:
                pass
                
    print(f"Done. Modified {changed} files.")

if __name__ == "__main__":
    refactor()
