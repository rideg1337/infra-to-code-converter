import json
import os

ANSIBLE_OUTPUT_DIR = "output/ansible"
CONTAINERS_JSON_PATH = "output/containers.json"


def load_containers(json_path):
    with open(json_path, "r") as f:
        return json.load(f)


def generate_inventory(containers, output_path):
    with open(output_path, "w") as f:
        f.write("[lxc_containers]\n")
        for c in containers:
            vmid = c["vmid"]
            ip = c.get("network",{}).get("ip", "")
            if not ip:
                print(f"⚠️  Skipping VMID {vmid} — No IP defined.")
                continue
            ip = ip.split ("/")[0]
            f.write(f"{vmid} ansible_host={ip}\n")


def generate_playbook(containers, output_path):
    playbook = """- name: basic playbook
  hosts: lxc_containers
  become: yes
  tasks:
    - name: Ensure htop is installed
      apt:
        name: htop
        state: present
"""
    with open(output_path, "w") as f:
        f.write(playbook)


def main():
    if not os.path.exists(CONTAINERS_JSON_PATH):
        print(f"Missing {CONTAINERS_JSON_PATH} file.")
        return

    containers = load_containers(CONTAINERS_JSON_PATH)

    if not os.path.exists(ANSIBLE_OUTPUT_DIR):
        os.makedirs(ANSIBLE_OUTPUT_DIR)

    inventory_path = os.path.join(ANSIBLE_OUTPUT_DIR, "inventory.ini")
    playbook_path = os.path.join(ANSIBLE_OUTPUT_DIR, "playbook.yml")

    generate_inventory(containers, inventory_path)
    generate_playbook(playbook_path)

    print(f"inventory.ini saved: {inventory_path}")
    print(f"playbook.yml saved: {playbook_path}")


if __name__ == "__main__":
    main()
