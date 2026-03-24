import os
import shutil
from pathlib import Path

# Mapping of current file path -> new file path
# All paths are relative to models/raw
MAPPINGS = {
    # Staging - base_normalizada
    "staging/base_normalizada/_stg_bases_manuales__censo_2024_2.py": "../staging/base_normalizada/_stg_bases_manuales__censo_2024_2.py",
    "staging/base_normalizada/_stg_bases_manuales__clientes.py": "../staging/base_normalizada/_stg_bases_manuales__clientes.py",
    "staging/base_normalizada/_stg_bases_manuales__original.py": "../staging/base_normalizada/_stg_bases_manuales__original.py",

    # Staging - bases_ccu
    "staging/bases_ccu/_stg_bases_ccu__base_2024_q1.py": "../staging/bases_ccu/_stg_bases_ccu__base_2024_q1.py",
    "staging/bases_ccu/_stg_bases_ccu__base_2026_q1.py": "../staging/bases_ccu/_stg_bases_ccu__base_2026_q1.py",

    # Staging - censos
    "staging/censos/_stg_censos__censo_2024_2.py": "../staging/censos/_stg_censos__censo_2024_2.py",
    "staging/censos/_stg_censos__censo_2025_2.py": "../staging/censos/_stg_censos__censo_2025_2.py",
    "staging/censos/_stg_censos__fne_listado_2026_1.py": "../staging/censos/_stg_censos__fne_listado_2026_1.py",
    "staging/censos/_stg_censos__censo_2026_1_agencia_pk.py": "../staging/censos/_stg_censos__censo_2026_1_agencia_pk.py",
    "staging/censos/_stg_censos__censo_2026_1_agencia_corpa.py": "../staging/censos/_stg_censos__censo_2026_1_agencia_corpa.py",
    "staging/censos/_stg_censos__censo_2026_1_agencia_corpa_sistematizado.py": "../staging/censos/_stg_censos__censo_2026_1_agencia_corpa_sistematizado.py",
    "staging/censos/_stg_censos__censo_2026_1_listado_marcas.py": "../staging/censos/_stg_censos__censo_2026_1_listado_marcas.py",

    # Intermediate - base_normalizada
    "intermediate/_int_bases_manuales__clientes.py": "../intermediate/base_normalizada/_int_bases_manuales__clientes.py",

    # Intermediate - bases_ccu
    "intermediate/_int_reportes_ccu_base_2024_q1.py": "../intermediate/bases_ccu/_int_bases_ccu__base_2024_q1.py",
    "intermediate/_int_reportes_ccu_base_2026_q1.py": "../intermediate/bases_ccu/_int_bases_ccu__base_2026_q1.py",

    # Intermediate - censos
    "intermediate/_int_censos__censo_2024_2.py": "../intermediate/censos/_int_censos__censo_2024_2.py",
    "intermediate/_int_censos__censo_2025_2.py": "../intermediate/censos/_int_censos__censo_2025_2.py",
    "intermediate/_int_censos__censo_2026_1.py": "../intermediate/censos/_int_censos__censo_2026_1.py",
    "intermediate/_int_censos__fne_listado_2026_1.py": "../intermediate/censos/_int_censos__fne_listado_2026_1.py",

    # Marts (just move, no rename)
    "marts/_dim_clientes.py": "../marts/_dim_clientes.py",
    "marts/_fct_bases_ccu.py": "../marts/_fct_bases_ccu.py",
    "marts/_fct_censos.py": "../marts/_fct_censos.py",
    "marts/_fct_contratos.py": "../marts/_fct_contratos.py",
}

def migrate():
    base_dir = Path("/Users/educifuentes/code/ccu-monitoreo-activos/models/raw")
    
    for src, dst in MAPPINGS.items():
        src_path = base_dir / src
        if not src_path.exists():
            # If the staging censos 2026 files have exact slightly different names, handle them
            if 'listado_marcas' in src and not src_path.exists():
                 src_path = base_dir / "staging/censos/_stg_censos__censo_2026_1_agencia_corpa_listado_marcas.py"
                 if not src_path.exists():
                     print(f"File not found: {src_path}")
                     continue

        dst_path = base_dir / dst
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src_path), str(dst_path))
        print(f"Moved {src_path.name} -> {dst_path.parent.name}/{dst_path.name}")

    # Move folders wholesale
    for folder in ['sources', 'exposures']:
        src_folder = base_dir / folder
        dst_folder = base_dir.parent / folder
        if src_folder.exists():
            if not dst_folder.exists():
                shutil.move(str(src_folder), str(dst_folder))
                print(f"Moved folder {folder}")

    # Move marts/metrics and marts/reports
    for sub in ['metrics', 'reports']:
        src_sub = base_dir / 'marts' / sub
        dst_sub = base_dir.parent / 'marts' / sub
        if src_sub.exists():
            dst_sub.parent.mkdir(parents=True, exist_ok=True)
            if not dst_sub.exists():
                shutil.move(str(src_sub), str(dst_sub))
                print(f"Moved marts config {sub}")

if __name__ == "__main__":
    migrate()
    print("Migration script completed.")
