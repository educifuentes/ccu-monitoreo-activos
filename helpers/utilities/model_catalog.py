import os
import pandas as pd

def build_global_model_registry(root_path="models"):
    """
    Recursively scans a multi-schema directory structure and produces a Pandas DataFrame
    acting as a searchable catalog of all models.
    """
    records = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Ignore Python cache directories
        if "__pycache__" in dirnames:
            dirnames.remove("__pycache__")
            
        rel_path = os.path.relpath(dirpath, root_path)
        if rel_path == ".":
            continue
            
        path_parts = rel_path.split(os.sep)
        
        # Ensure we are inside at least a Schema and Stage
        if len(path_parts) >= 2:
            schema = path_parts[0]
            stage = path_parts[1]
            
            for file in filenames:
                if file == "__init__.py" or not file.endswith(".py"):
                    continue
                    
                model_name_full = file[:-3] # Strip .py
                
                # If you want to use st.page_link("pages/others/view_model.py", query_params={"model": model_name_full})
                # or native LinkColumn URL:
                # The url points to the root of the app, handled by app.py query params intercept via st.switch_page
                link = f"/?model={model_name_full}"
                
                records.append({
                    "schema": schema,
                    "stage": stage,
                    "model": model_name_full,
                    "link": link
                })
                
    # Return empty DataFrame with columns if no records
    if not records:
        return pd.DataFrame(columns=["schema", "stage", "model", "link"])
        
    return pd.DataFrame(records)
