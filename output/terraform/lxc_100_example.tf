resource "proxmox_lxc" "" {
  vmid = 100
  hostname = ""
  cores = 2
  memory = 4096
  

  network {
    type = "veth"
    bridge = "vmbr0"
    ip = "192.168.32.148/24"
  }
}