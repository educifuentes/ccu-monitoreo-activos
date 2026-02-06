import yaml
import os

with open('models/sources/_src_reportes_ccu.yml', 'r') as f:
    config = yaml.safe_load(f)

print(f"Type: {type(config)}")
if isinstance(config, list):
    for i, source in enumerate(config):
        print(f"Source {i} name: '{source.get('name')}'")
        for j, table in enumerate(source.get('tables', [])):
            print(f"  Table {j} name: '{table.get('name')}'")
            print(f"  Table {j} path: '{table.get('path')}'")
            print(f"  Table {j} filename: '{table.get('filename')}'")
