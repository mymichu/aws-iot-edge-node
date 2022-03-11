from time import time
from auto_flash.tty import TTY





class Utility:
    tty_interface: TTY

    def __init__(self, tty: TTY):
        self.tty_interface = tty

    def set_ip(self, ip: str, mask: str):
        print("Set IP on RAM Disk")
        self.tty_interface.write_command(f"ifconfig eth0 {ip} netmask {mask} up")
        self.tty_interface.wait_for_acknowledge(30, "link becomes ready")
        self.tty_interface.write_command("ifconfig")
        self.tty_interface.wait_for_acknowledge(10, f"{ip}")
        print("Ethernet is configured")

    def mount_device_force(self, device: str, target_folder: str) -> None:
        print(f"mount {device} to {target_folder}")
        self.tty_interface.write_command(f"rm -rf {target_folder}")
        self.tty_interface.write_command(f"mkdir -p {target_folder}")
        self.tty_interface.write_command(f'mount {device} {target_folder} && echo "DONE"')
        self.tty_interface.wait_for_acknowledge(60, "DONE")

    def change_director(self, directory: str) -> None:
        self.tty_interface.write_command(f'cd {directory} && echo "DONE"')
        self.tty_interface.wait_for_acknowledge(60, f"DONE")

    def tftp_download(self, server_ip: str, file):
        print(f"Download {file} over TFTP")
        self.tty_interface.write_command(f'tftp {server_ip} -c get {file} && echo "DONE"')
        self.tty_interface.wait_for_acknowledge(120, f"DONE")
        print(f"File downloaded {file}")
        print(f"Check if {file} was correctly downloaded")
        self.tty_interface.write_command(f"stat {file}")
        self.tty_interface.wait_for_acknowledge(60, "regular file")
        print(f"File {file} download was successful")

    def untar(self, file:str ):
        print(f"Untar {file}")
        self.tty_interface.write_command(f'tar -xf {file} && echo "DONE" ')
        self.tty_interface.wait_for_acknowledge(18000, "DONE")
        print(f"Unpacked {file}")
        self.tty_interface.write_command(f"rm -rf {file}")