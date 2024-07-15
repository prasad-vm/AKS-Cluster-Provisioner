import os
import json
import requests

def main():
    json_spec_path = 'specs/Spec01.json'

    if not os.path.exists(json_spec_path):
        raise FileNotFoundError(f"file not found: {json_spec_path}")
    
    # Load JSON spec
    with open(json_spec_path, 'r') as file:
        json_spec = json.load(file)
    
    # Run the automation script
    os.system(f"python automation.py '{json.dumps(json_spec)}'")

if __name__ == "__main__":
    main()
