import os
import json
from lxc_scanner.scanner import scan_all_lxc
from generators.terraform_generator import generate_terraform
from generators import ansible_generator

def main():
    containers = scan_all_lxc()
    print("Parsed LXC containers:")
    for c in containers:
        print(c)

    # Output 
    os.makedirs("output", exist_ok=True)

    # JSON save
    containers_json_path = "output/containers.json"
    with open(containers_json_path, "w") as f:
        json.dump(containers, f, indent=2)
    print(f"containers.json saved: {containers_json_path}")

    # Terraform generate
    generate_terraform(containers)
    print("Terraform files are generated")

    # Ansible generate
    ansible_generator.generate_inventory(containers, "output/ansible/inventory.ini")
    ansible_generator.generate_playbook(containers, "output/ansible/playbook.yml")
    print("Ansible inventory and playbook are generated")

if __name__ == "__main__":
    main()
