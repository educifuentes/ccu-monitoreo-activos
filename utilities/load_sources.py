import yaml
import os
import sys

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

if __name__ == "__main__":
    # Test cases
    target_table = "censo_2"
    path = get_source_path(target_table)
    print(f"Path for '{target_table}': {path}")
