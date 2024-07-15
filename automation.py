import os
import sys
import json
import yaml

def load_template(env):
    template_file = f"{env}-general-purpose-spec.yaml"
    template_path = os.path.join('../AKS-Cluster-Specs/templates', template_file)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")
    with open(template_path, 'r') as file:
        template = yaml.safe_load(file)
    return template

def merge_spec_with_template(spec, template):
    template['metadata']['name'] = spec['clusterName']
    template['metadata']['labels']['env'] = spec['env']
    template['spec']['controlPlane']['count'] = spec['controlPlaneCount']
    template['spec']['controlPlane']['nodeType'] = spec['nodeType']
    template['spec']['workerNodes']['count'] = spec['workerNodeCount']
    template['spec']['workerNodes']['nodeType'] = spec['nodeType']
    template['spec']['network']['policy'] = spec['networkPolicy']
    template['spec']['storage']['class'] = spec['storageClass']
    template['spec']['version'] = spec['kubernetesVersion']
    template['spec']['region'] = spec['region']
    return template

def save_to_iac_repo(merged_spec):
    output_path = '../AKS-Cluster-IaC/output/cluster-definition.yaml'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        yaml.dump(merged_spec, file)
    print(f"Cluster definition saved to: {output_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python automation.py '<json_spec>'")
        sys.exit(1)

    json_spec = json.loads(sys.argv[1])

    env = json_spec.get('env', 'dev')
    template = load_template(env)
    merged_spec = merge_spec_with_template(json_spec, template)
    save_to_iac_repo(merged_spec)

if __name__ == "__main__":
    main()