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
    if not tty.is_open:
        tty.open()
    in_uboot = False
    timeout = time.time() + 60 * 5
    while not in_uboot:
        tty.write("m".encode())  # write a string
        in_uboot = wait_for_acknowledge(tty, 0.01, "Colibri iMX6 #")
        if time.time() > timeout:
            raise RuntimeError("Unable to enter u-boot console")
    print("u-boot console entered!")
    tty.close()


def wait_for_acknowledge(tty, timeout_sec, acknowldge_message, only_ack=False):
    timeout = time.time() + timeout_sec
    feedback_buffer = ""
    while True:
        feedback_buffer += tty.read(1).decode('UTF-8')
        print(feedback_buffer)
        if only_ack:
            if acknowldge_message == feedback_buffer:
                return True
        else:
            if acknowldge_message in feedback_buffer:
                return True
        if time.time() > timeout:
            return False
        if len(feedback_buffer) > 200000000:
            raise BufferError("Serial rx buffer to long")


def write_command(tty, command):
    tty.write(command.encode())
    if wait_for_acknowledge(tty, 0.5, command, only_ack=True):
        raise RuntimeError("Not able to write command to serial")


def boot_ram(tty, serverip, ip, fit_binary):
    if not tty.is_open:
        tty.open()
    tty.flush()
    tty.write("\n".encode())
    write_command(tty, f"setenv ipaddr {ip} \n")
    write_command(tty, f"setenv serverip {serverip} \n")
    tftpcmd = "tftp ${loadaddr}" + f" {fit_binary}" + "\n"
    write_command(tty, tftpcmd)
    if wait_for_acknowledge(tty, 60, "done"):
        print("FIT image downloaded from tftp!")
        write_command(tty,"bootm ${loadaddr} \n")
        if wait_for_acknowledge(tty, 60, "poky"):
            print("FIT image started!")
    tty.close()


if __name__ == "__main__":
    args = get_args()
    serial = serial.Serial(args.device, timeout=5, baudrate=115200, writeTimeout=1)
    print(serial.name)
    enter_uboot(serial)
    boot_ram(serial, "192.100.10.1", "192.100.10.2", "fitImage-image-initramfs-iot-edge.bin")
