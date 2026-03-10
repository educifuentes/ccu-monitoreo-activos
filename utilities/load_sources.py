import yaml
import os
import sys
import pandas as pd

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def read_yaml_config(yaml_path):
    """
    Reads a YAML file and returns the parsed content.
    """
    if not os.path.exists(yaml_path):
        # Try absolute path from project root if relative fails
        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        yaml_path = os.path.join(root_path, yaml_path)
        
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"YAML file not found: {yaml_path}")
    
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)

def get_source_path(table_name, yaml_path='models/staging/_src_censos.yml'):
    """
    Reads the sources from a YAML file and returns the path or URL
    for the specified table_name.
    """
    config = read_yaml_config(yaml_path)
    
    for source in config.get('sources', []):
        source_path = source.get('path') or source.get('google_sheet_url')
        
        for table in source.get('tables', []):
            if table.get('name') == table_name:
                return table.get('path') or table.get('google_sheet_url') or source_path
                
    return None

def load_source(name: str, src_yaml_path: str) -> pd.DataFrame:
    """
    Looks up a source by `name` in the given YAML file, resolves its `path`,
    and returns the CSV loaded as a pandas DataFrame.

    Args:
        name: The source name to look for (matches the top-level `name` field
              under `sources` in the YAML).
        src_yaml_path: Path to the YAML source file (absolute or relative to
                       project root).

    Returns:
        A pandas DataFrame with the CSV contents.

    Raises:
        ValueError: If no source with the given name is found.
        FileNotFoundError: If the resolved CSV path does not exist.
    """
    config = read_yaml_config(src_yaml_path)
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    for source in config.get('sources', []):
        if source.get('name') == name:
            csv_path = source.get('path')
            if csv_path is None:
                raise ValueError(f"Source '{name}' has no 'path' defined in {src_yaml_path}")
            # Resolve relative paths from the project root
            if not os.path.isabs(csv_path):
                csv_path = os.path.join(root_path, csv_path)
            return pd.read_csv(csv_path)

    raise ValueError(f"Source '{name}' not found in {src_yaml_path}")


if __name__ == "__main__":
    # Test cases
    target_table = "censo_2025_2"
    path = get_source_path(target_table)
    print(f"Path for '{target_table}': {path}")
