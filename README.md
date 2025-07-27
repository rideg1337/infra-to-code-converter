# Infra-to-Code Converter

An automated tool to fetch Proxmox LXC container configurations via SSH and convert them into infrastructure-as-code formats (Terraform and Ansible). The goal is to make your existing Proxmox LXC environment version-controlled, manageable, and deployable as code.

> ⚠️ **Note:** This project was created with a strong learning intention to deepen understanding of infrastructure as code, Proxmox, Terraform, Ansible, and automation. It serves as both a practical tool and an educational resource.

---

## Features

- Connects to a Proxmox server via SSH and retrieves LXC container configurations  
- Parses configurations into structured Python objects  
- Generates Terraform `.tf` files for LXC containers using Jinja2 templates  
- Generates Ansible inventory and playbook files for container management  
- Easily extendable to support other platforms  

---

## Installation & Usage

```bash
# 1. Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the converter
python main.py
```
