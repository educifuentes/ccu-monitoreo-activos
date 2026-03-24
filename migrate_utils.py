import os
import shutil
from pathlib import Path
import re

def migrate_utilities():
    root = Path("/Users/educifuentes/code/ccu-monitoreo-activos")
    utils_dir = root / "utilities"
    helpers_dir = root / "helpers"
    
    # Target 1: Whole Subdirectories to move over directly
    direct_moves = ["assets", "charts", "constants", "transformations"]
    for d in direct_moves:
        src = utils_dir / d
        dst = helpers_dir / d
        if src.exists():
            shutil.move(str(src), str(dst))
            print(f"Moved directory {d}")
            
    # Target 2: Merge Widgets
    widgets_src = utils_dir / "widgets"
    widgets_dst = helpers_dir / "widgets"
    if widgets_src.exists():
        widgets_dst.mkdir(parents=True, exist_ok=True)
        for f in widgets_src.glob("*"):
            if f.is_file():
                tgt = widgets_dst / f.name
                if not tgt.exists():
                    shutil.move(str(f), str(tgt))
                    print(f"Moved widget {f.name}")
                else:
                    print(f"Skipped {f.name} into widgets (already exists)")
                    
    # Target 3: UI specific scripts
    ui_scripts = ["ui_components.py", "ui_config.py", "ui_icons.py", "render_docs.py"]
    ui_dst = helpers_dir / "ui_components"
    ui_dst.mkdir(parents=True, exist_ok=True)
    for s in ui_scripts:
        src = utils_dir / s
        dst = ui_dst / s
        if src.exists() and not dst.exists():
            shutil.move(str(src), str(dst))
            print(f"Moved UI script {s}")
            
    # Target 4: General scripts to helpers.utilities
    gen_scripts = ["app_version.py", "data_connection_config.py"]
    gen_dst = helpers_dir / "utilities"
    gen_dst.mkdir(parents=True, exist_ok=True)
    for s in gen_scripts:
        src = utils_dir / s
        dst = gen_dst / s
        if src.exists() and not dst.exists():
            shutil.move(str(src), str(dst))
            print(f"Moved General script {s}")
            
    # Remove yaml_loader if duplicate
    yaml_src = utils_dir / "yaml_loader.py"
    if yaml_src.exists():
        os.remove(str(yaml_src))
        print("Deleted legacy yaml_loader")
        
    # Flush __pycache__ and empty directories inside utilities
    if utils_dir.exists():
        shutil.rmtree(str(utils_dir), ignore_errors=True)
        print("Swept empty utilities source directory.")
        
    print("Files restructured. Starting codebase string replace...")

    # String mapping translation paths
    # Because imports are dot separated, we map explicitly
    str_mappings = [
        ("from helpers.utilities.yaml_loader", "from helpers.utilities.yaml_loader"),
        ("import helpers.utilities.yaml_loader", "import helpers.utilities.yaml_loader"),
        
        ("from helpers.utilities.app_version", "from helpers.utilities.app_version"),
        ("from helpers.utilities.data_connection_config", "from helpers.utilities.data_connection_config"),
        
        ("from helpers.ui_components.ui_components", "from helpers.ui_components.ui_components"),
        ("from helpers.ui_components.ui_config", "from helpers.ui_components.ui_config"),
        ("from helpers.ui_components.ui_icons", "from helpers.ui_components.ui_icons"),
        ("from helpers.ui_components.render_docs", "from helpers.ui_components.render_docs"),
        
        ("from helpers.assets", "from helpers.assets"),
        ("from helpers.charts", "from helpers.charts"),
        ("from helpers.constants", "from helpers.constants"),
        ("from helpers.transformations", "from helpers.transformations"),
        ("from helpers.widgets", "from helpers.widgets"),
        
        ("helpers.charts", "helpers.charts"),
        ("helpers.constants", "helpers.constants"),
        ("helpers.transformations", "helpers.transformations"),
        ("helpers.widgets", "helpers.widgets"),
        ("helpers.assets", "helpers.assets")
    ]
    
    # Iterate across python app files
    changed = 0
    for ext in ["*.py"]:
        for file in root.rglob(ext):
            if any(p in file.parts for p in ["venv", ".venv", ".gemini", ".git"]):
                continue
                
            try:
                original = file.read_text("utf-8")
                new_text = original
                for old_val, new_val in str_mappings:
                    new_text = new_text.replace(old_val, new_val)
                    
                if new_text != original:
                    file.write_text(new_text, "utf-8")
                    changed += 1
            except Exception:
                pass
                
    print(f"Successfully modified {changed} module imports!")

if __name__ == "__main__":
    migrate_utilities()
