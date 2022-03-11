import serial

import argparse
import api
import configuration
import auto_flash


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"auto_flash {auto_flash.__version__}")
    parser.add_argument("--device", type=str, required=True, help="Set tty device")
    parser.add_argument("--baudrate", default=115200,type=int, required=False, help="Set tty device baudrate")
    parser.add_argument("--config", type=str, required=True, help="Config file path")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    api = api.API(device=args.device, baudrate=args.baudrate, configuration_path=args.config)
    api.run()
