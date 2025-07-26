from jinja2 import Environment, FileSystemLoader
import os

def generate_terraform(containers, output_dir="output/terraform"):
    env = Environment(
        loader=FileSystemLoader(searchpath="templates")
    )
    template = env.get_template("proxmox_lxc.tf.j2")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for container in containers:
        filename = f"{output_dir}/lxc_{container['vmid']}.tf"
        with open(filename, "w") as f:
            tf_content = template.render(container=container)
            f.write(tf_content)
