import serial
import time
import argparse
import auto_flash

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"auto_flash {auto_flash.__version__}")
    parser.add_argument("--device", type=str, required=True, help="Set tty device")
    return parser.parse_args()


def enter_uboot(tty):
    in_uboot = False
    timeout = time.time() + 60*5
    while not in_uboot:
        tty.write("m".encode())  # write a string
        in_uboot = wait_for_acknowledge(tty, 1, "Colibri iMX6 #")
        if time.time() > timeout:
            raise RuntimeError("Unable to enter u-boot console")
    print("u-boot console entered!")
    tty.close()


def wait_for_acknowledge(tty, timeout_sec, acknowldge_message):
    timeout = time.time() + timeout_sec
    while True:
        feedback = tty.readline().decode('UTF-8')
        if acknowldge_message in feedback:
            return True
        if time.time() > timeout:
            return False


def boot_ram(tty, serverip, ip, fit_binary):
    tty.write(f"setenv ipaddr {ip}".encode())
    tty.write(f"setenv serverip {serverip}".encode())
    tftpcmd = "tftp ${loadaddr}"+f" {fit_binary}"
    tty.write(tftpcmd.encode())
    wait_for_acknowledge(tty, 60, "done")
    tty.write("bootm ${loadaddr}".encode())
    wait_for_acknowledge(tty, 60, "done")

if __name__ == "__main__":
    args = get_args()
    serial = serial.Serial(args.device, timeout=2, baudrate=115200)
    print(serial.name)
    enter_uboot(serial)
    boot_ram(serial, "192.100.10.1", "192.100.10.2", "fitImage-image-initramfs-iot-edge--5.4.77+gitAUTOINC+a2e5dc8022-r0-iot-edge-20210730054435.bin")


