import os
import shutil
from pathlib import Path
import re

# File moves
FILES_TO_MOVE = {
    "models/marts/_dim_clientes.py": "models/marts/_dim_clientes.py",
    "models/staging/base_normalizada/_stg_base_normalizada__clientes.py": "models/staging/base_normalizada/_stg_base_normalizada__clientes.py",
    "models/intermediate/base_normalizada/_int_base_normalizada__clientes.py": "models/intermediate/base_normalizada/_int_base_normalizada__clientes.py",
    "models/exposures/_exp_clientes.py": "models/exposures/_exp_clientes.py",
}

# String Replacements
# We use regex or strict strings. Ordered to avoid overlapping replacements.
# Note: we do NOT want to replace standard python or library variables if they conflict, but here the domain names are unique enough.
STR_REPLACEMENTS = [
    # 1. Explicit Module Paths
    ("models.marts._dim_clientes", "models.marts._dim_clientes"),
    ("models.staging.base_normalizada._stg_base_normalizada__clientes", "models.staging.base_normalizada._stg_base_normalizada__clientes"),
    ("models.intermediate.base_normalizada._int_base_normalizada__clientes", "models.intermediate.base_normalizada._int_base_normalizada__clientes"),
    ("models.exposures._exp_clientes", "models.exposures._exp_clientes"),

    # 2. Function Names
    ("dim_clientes", "dim_clientes"),
    ("stg_base_normalizada__clientes", "stg_base_normalizada__clientes"),
    ("int_base_normalizada__clientes", "int_base_normalizada__clientes"),
    ("exp_clientes", "exp_clientes"),
    ("clientes_options", "clientes_options"),
    ("unique_clientes_master", "unique_clientes_master"),
    ("cliente_assets_history", "cliente_assets_history"),
    ("cliente_contract", "cliente_contract"),

    # 3. Variable Names
    ("cliente_id", "cliente_id"),
    ("cliente_master", "cliente_master"),
    ("selected_cliente_id", "selected_cliente_id"),
    ("clientes_df", "clientes_df"),
    ("total_clientes", "total_clientes"),
    
    # 4. Text Display (We use regex boundary or exact casing for safe text replacements)
    (r"\bLocales\b", "Clientes"),
    (r"\bLocal\b", "Cliente"),
    (r"\blocal\b", "cliente"),
    (r"\blocales\b", "clientes"),
]

def migrate_and_replace():
    root = Path("/Users/educifuentes/code/ccu-monitoreo-activos")
    
    # Move files
    for src, dst in FILES_TO_MOVE.items():
        src_path = root / src
        dst_path = root / dst
        if src_path.exists():
            shutil.move(str(src_path), str(dst_path))
            print(f"Moved {src_path.name} -> {dst_path.name}")
    
    # Replace content
    changed_files = 0
    for ext in ["*.py", "*.md", "*.yml"]:
        for file in root.rglob(ext):
            if any(p in file.parts for p in ["venv", ".venv", ".gemini", ".git"]):
                continue
            
            try:
                original_content = file.read_text("utf-8")
                new_content = original_content
                
                for old, new in STR_REPLACEMENTS:
                    # if old is regex
                    if "\\b" in old:
                        new_content = re.sub(old, new, new_content)
                    else:
                        new_content = new_content.replace(old, new)
                        
                if new_content != original_content:
                    file.write_text(new_content, "utf-8")
                    changed_files += 1
                    print(f"Updated content in {file.relative_to(root)}")
            except Exception as e:
                # ignore binary or weird text errors
                pass
                
    print(f"Update complete. Changed {changed_files} files.")

if __name__ == "__main__":
    migrate_and_replace()
