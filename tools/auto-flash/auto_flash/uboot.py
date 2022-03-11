from auto_flash.tty import TTY

import time


class UBoot:
    tty_interface: TTY

    def __init__(self, tty: TTY):
        self.tty_interface = tty

    def enter_uboot(self):
        in_uboot = False
        timeout = time.time() + 60 * 5
        print("Wait for reset Board.")
        while not in_uboot:
            self.tty_interface.write_command("m", ignore_error=True) 
            self.tty_interface.write_command("", ignore_error=True)
            time.sleep(0.5)
            try:
                self.tty_interface.wait_for_acknowledge(0.01, "Colibri iMX6 #")
                in_uboot = True
            except:
                if time.time() > timeout:       
                    raise RuntimeError("Unable to enter U-Boot console")
        print("U-Boot console entered.")

    def boot_ram(self, serverip: str, ip: str, fit_binary: str):
        print("Download From TFTP & Boot from RAM.")
        self.tty_interface.write_command(f"setenv ipaddr {ip}")
        self.tty_interface.write_command(f"setenv serverip {serverip}")
        self.tty_interface.write_command("tftp ${loadaddr}" + f" {fit_binary}")
        self.tty_interface.wait_for_acknowledge(60, "done")
        print("FIT image downloaded from tftp.")
        self.tty_interface.write_command("bootm ${loadaddr}")
        self.tty_interface.wait_for_acknowledge(60, "Run /init as init process")
        time.sleep(5)
        print("FIT image started.")
