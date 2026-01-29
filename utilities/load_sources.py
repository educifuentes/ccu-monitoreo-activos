import yaml
import os
from pprint import pprint

def read_yaml_config(yaml_path):
    """
    Reads a YAML file and returns the parsed content.
    """
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
        # The path/url might be at the source level
        source_path = source.get('path') or source.get('google_sheet_url')
        
        for table in source.get('tables', []):
            if table.get('name') == table_name:
                # Return table specific path/url if exists, otherwise fallback to source level
                return table.get('path') or table.get('google_sheet_url') or source_path
                
    return None

if __name__ == "__main__":
    # Test cases
    target_table = read_yaml_config("models/staging/_src_censos.yml")
    pprint(target_table)
  
