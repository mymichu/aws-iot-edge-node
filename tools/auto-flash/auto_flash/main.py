import serial

import argparse
import api
import config
import auto_flash


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"auto_flash {auto_flash.__version__}")
    parser.add_argument("--device", type=str, required=True, help="Set tty device")
    parser.add_argument("--config", type=str, required=True, help="Config file path")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    serial = serial.Serial(args.device, timeout=5, baudrate=115200, writeTimeout=1)
    print(serial.name)
    api.enter_uboot(serial)
    api.boot_ram(serial, "192.100.10.1", "192.100.10.2", "fitImage-image-initramfs-iot-edge.bin")
    cfg = config.Settings(args.config)
    cfg.print_part()
    api.partition_device(serial,"192.100.10.1", "192.100.10.2","255.255.255.0",cfg.config.partitions)
