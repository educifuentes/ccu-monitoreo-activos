import os
from pathlib import Path

# Replacements for import paths and function names globally
# We replace old modules with new modules
REPLACEMENTS = {
    # 1. Import paths (modules)
    "models.staging.base_normalizada._stg_base_normalizada__censo_2024_2": "models.staging.base_normalizada._stg_base_normalizada__censo_2024_2",
    "models.staging.base_normalizada._stg_base_normalizada__locales": "models.staging.base_normalizada._stg_base_normalizada__locales",
    "models.staging.base_normalizada._stg_base_normalizada__original": "models.staging.base_normalizada._stg_base_normalizada__original",

    "models.staging.bases_ccu._stg_bases_ccu__base_2024_q1": "models.staging.bases_ccu._stg_bases_ccu__base_2024_q1",
    "models.staging.bases_ccu._stg_bases_ccu__base_2026_q1": "models.staging.bases_ccu._stg_bases_ccu__base_2026_q1",

    "models.staging.censos._stg_censos__censo_2024_2": "models.staging.censos._stg_censos__censo_2024_2",
    "models.staging.censos._stg_censos__censo_2025_2": "models.staging.censos._stg_censos__censo_2025_2",
    "models.staging.censos._stg_censos__fne_listado_2026_1": "models.staging.censos._stg_censos__fne_listado_2026_1",
    
    # 2026_1 censos already converted to individual files, just correct the models.raw out
    "models.staging.censos._stg_censos__censo_2026_1_agencia_pk": "models.staging.censos._stg_censos__censo_2026_1_agencia_pk",
    "models.staging.censos._stg_censos__censo_2026_1_agencia_corpa": "models.staging.censos._stg_censos__censo_2026_1_agencia_corpa",
    "models.staging.censos._stg_censos__censo_2026_1_agencia_corpa_sistematizado": "models.staging.censos._stg_censos__censo_2026_1_agencia_corpa_sistematizado",
    "models.staging.censos._stg_censos__censo_2026_1_listado_marcas": "models.staging.censos._stg_censos__censo_2026_1_listado_marcas",
    # Catch any old imports that still used the monolithic file just in case
    "models.staging.censos._stg_censos__censo_2026_1": "models.staging.censos._stg_censos__censo_2026_1",

    "models.intermediate.base_normalizada._int_base_normalizada__locales": "models.intermediate.base_normalizada._int_base_normalizada__locales",
    "models.intermediate.bases_ccu._int_bases_ccu__base_2024_q1": "models.intermediate.bases_ccu._int_bases_ccu__base_2024_q1",
    "models.intermediate.bases_ccu._int_bases_ccu__base_2026_q1": "models.intermediate.bases_ccu._int_bases_ccu__base_2026_q1",
    "models.intermediate.censos._int_censos__censo_2024_2": "models.intermediate.censos._int_censos__censo_2024_2",
    "models.intermediate.censos._int_censos__censo_2025_2": "models.intermediate.censos._int_censos__censo_2025_2",
    "models.intermediate.censos._int_censos__censo_2026_1": "models.intermediate.censos._int_censos__censo_2026_1",
    "models.intermediate.censos._int_censos__fne_listado_2026_1": "models.intermediate.censos._int_censos__fne_listado_2026_1",

    "models.marts._dim_locales": "models.marts._dim_locales",
    "models.marts._fct_bases_ccu": "models.marts._fct_bases_ccu",
    "models.marts._fct_censos": "models.marts._fct_censos",
    "models.marts._fct_contratos": "models.marts._fct_contratos",
    "models.marts.metrics": "models.marts.metrics",
    "models.marts.reports": "models.marts.reports",

    # Remaining `models.raw` catch-all (sources, exposures)
    "models.sources": "models.sources",
    "models.exposures": "models.exposures",
    "models/sources": "models/sources",
    "models/exposures": "models/exposures",

    # 2. Function names
    "stg_base_normalizada__censo_2024_2": "stg_base_normalizada__censo_2024_2",
    "stg_base_normalizada__locales": "stg_base_normalizada__locales",
    "stg_base_normalizada__original": "stg_base_normalizada__original",
    "stg_bases_ccu__base_2024_q1": "stg_bases_ccu__base_2024_q1",
    "stg_bases_ccu__base_2026_q1": "stg_bases_ccu__base_2026_q1",
    "stg_censos__censo_2024_2": "stg_censos__censo_2024_2",
    "stg_censos__censo_2025_2": "stg_censos__censo_2025_2",
    "stg_censos__fne_listado_2026_1": "stg_censos__fne_listado_2026_1",

    "int_base_normalizada__locales": "int_base_normalizada__locales",
    # the 2024 functions have suffixes
    "int_bases_ccu__base_2024_q1_locales": "int_bases_ccu__base_2024_q1_locales",
    "int_bases_ccu__base_2024_q1_activos": "int_bases_ccu__base_2024_q1_activos",
    "int_bases_ccu__base_2024_q1_contratos": "int_bases_ccu__base_2024_q1_contratos",
    # the 2026 functions have suffixes
    "int_bases_ccu__base_2026_q1_locales": "int_bases_ccu__base_2026_q1_locales",
    "int_bases_ccu__base_2026_q1_activos": "int_bases_ccu__base_2026_q1_activos",
    "int_bases_ccu__base_2026_q1_contratos": "int_bases_ccu__base_2026_q1_contratos",

    "int_censos__censo_2024_2": "int_censos__censo_2024_2",
    "int_censos__censo_2025_2": "int_censos__censo_2025_2",
    "int_censos__censo_2026_1": "int_censos__censo_2026_1",
    "int_censos__fne_listado_2026_1": "int_censos__fne_listado_2026_1",
}

def update_files():
    root = Path(".")
    changed_files = 0
    # Process all py and md files but exclude venv, pycache, .gemini etc
    for ext in ["*.py", "*.md", "*.yml"]:
        for file in root.rglob(ext):
            if "venv" in file.parts or ".gemini" in file.parts or ".git" in file.parts:
                continue
            
            try:
                content = file.read_text("utf-8")
                new_content = content
                for old, new in REPLACEMENTS.items():
                    new_content = new_content.replace(old, new)
                
                if content != new_content:
                    file.write_text(new_content, "utf-8")
                    print(f"Updated {file}")
                    changed_files += 1
            except Exception as e:
                print(f"Error reading {file}: {e}")

    print(f"Done. Updated {changed_files} files.")

if __name__ == "__main__":
    update_files()
