# lxc_scanner/scanner.py

import paramiko
import yaml
import json

def load_config():
    with open("config/settings.yaml", "r") as f:
        return yaml.safe_load(f)

def ssh_connect(config):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=config['proxmox']['host'],
        username=config['proxmox']['user'],
        key_filename=config['proxmox']['ssh_key_path']
    )
    return ssh

def get_lxc_list(ssh):
    stdin, stdout, stderr = ssh.exec_command("pct list")
    output = stdout.read().decode()
    lines = output.strip().split("\n")[1:]  # Skip header
    ids = [line.split()[0] for line in lines if line.strip()]
    return ids

def parse_lxc_config(lxc_id, config_str):
    result = {
        "vmid": int(lxc_id),
        "network": {}
    }
    lines = config_str.strip().split("\n")
    for line in lines:
        if not line.strip():
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        
        if key.startswith("net"):
            # net0: name=eth0,bridge=vmbr0,ip=192.168.1.50/24,tag=50,type=veth
            net_attrs = {}
            for part in value.split(","):
                if "=" in part:
                    k,v = part.split("=",1)
                    net_attrs[k.strip()] = v.strip()
            result["network"] = net_attrs
        elif key in ("cores", "memory"):
            result[key] = int(value)
        else:
            result[key] = value
    return result


def get_lxc_config(ssh, lxc_id):
    cmd = f"pct config {lxc_id}"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdout.read().decode()

def scan_all_lxc():
    config = load_config()
    ssh = ssh_connect(config)
    lxc_ids = get_lxc_list(ssh)
    
    results = []
    for lxc_id in lxc_ids:
        config_str = get_lxc_config(ssh, lxc_id)
        parsed = parse_lxc_config(lxc_id, config_str)
        results.append(parsed)

    ssh.close()
    return results


if __name__ == "__main__":
    lxc_configs = scan_all_lxc()
    with open("output/containers.json", "w") as f:
        json.dump(lxc_configs, f, indent=2)
    print(f"Containers saved: output/containers.json")

