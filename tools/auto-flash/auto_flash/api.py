import time
import serial


def enter_uboot(tty: serial):
    if not tty.is_open:
        tty.open()
    in_uboot = False
    timeout = time.time() + 60 * 5
    print("Wait for reset Board.")
    while not in_uboot:
        tty.write("m".encode())  # write a string
        in_uboot = _wait_for_acknowledge(tty, 0.01, "Colibri iMX6 #")
        if time.time() > timeout:
            raise RuntimeError("Unable to enter U-Boot console")
    print("U-Boot console entered.")
    tty.close()


def _wait_for_acknowledge(tty: serial, timeout_sec: float, acknowledge_message: str, only_ack: bool = False):
    timeout = time.time() + timeout_sec
    feedback_buffer = ""
    while True:
        feedback_buffer += tty.read(1).decode('UTF-8')
        if only_ack:
            if acknowledge_message == feedback_buffer:
                return True
        else:
            if acknowledge_message in feedback_buffer:
                return True
        if time.time() > timeout:
            return False
        if len(feedback_buffer) > 200000000:
            raise BufferError("Serial rx buffer to long")


def _write_command(tty: serial, command: str):
    tty.write(command.encode())
    if _wait_for_acknowledge(tty, 0.5, command, only_ack=True):
        raise RuntimeError("Not able to write command to serial")


def boot_ram(tty: serial, serverip: str, ip: str, fit_binary: str):
    print("Download From TFTP & Boot from RAM.")
    if not tty.is_open:
        tty.open()
    tty.flush()
    tty.write("\n".encode())
    _write_command(tty, f"setenv ipaddr {ip} \n")
    _write_command(tty, f"setenv serverip {serverip} \n")
    tftpcmd = "tftp ${loadaddr}" + f" {fit_binary}" + "\n"
    _write_command(tty, tftpcmd)
    if _wait_for_acknowledge(tty, 60, "done"):
        print("FIT image downloaded from tftp.")
        _write_command(tty, "bootm ${loadaddr} \n")
        if _wait_for_acknowledge(tty, 60, "Run /init as init process"):
            print("FIT image started.")
    tty.close()
