from enum import Enum

from auto_flash.tty import TTY
from typing import List


class Format(Enum):
    FAT = 1
    EXT4 = 2


class Partition:
    start_mb: int = 0
    size_mb: int = 0
    fill: bool = False
    format: Format = None
    primary: bool = False


class Partitioner:
    tty_interface: TTY

    def __init__(self, tty: TTY):
        self.tty_interface = tty

    @staticmethod
    def convert_format_as_string(in_format: Format) -> str:
        if in_format == Format.FAT:
            return "fat32"
        if in_format == Format.EXT4:
            return "ext4"
        raise RuntimeError("Only FAT and EXT4 supported")

    def create_partition_table(self, partitions: List[Partition], device: str) -> None:
        print("Create Partition Table")
        self.tty_interface.write_command(f'parted  -a optimal {device} -s mklabel msdos && echo "DONE"')
        self.tty_interface.wait_for_acknowledge(60,"DONE")
        partition_id: int = 1
        for partition in partitions:
            format_string = self.convert_format_as_string(partition.format)
            partition_command = f"parted  -a optimal {device} -s mkpart primary {format_string} "
            if partition.start_mb == 0:
                partition_command += f" 0%"
            else:
                partition_command += f" {size_of_last_mb}MB"
            size_of_last_mb = partition.size_mb
            if partition.fill:
                partition_command += f" 100%"
            else:
                partition_command += f" {partition.size_mb}MB"
            self.tty_interface.write_command(f'{partition_command} && echo "DONE"')
            self.tty_interface.wait_for_acknowledge(60,"DONE")
            if partition.primary:
                self.tty_interface.write_command(f'parted -a optimal {device} -s set {partition_id} boot on && echo "DONE"')
                self.tty_interface.wait_for_acknowledge(60,"DONE")
            partition_id= partition_id + 1

    def format_device(self, device, to_format: Format):
        print(f"Format {device} to {to_format}")
        if to_format == Format.FAT:
            self.tty_interface.write_command(f'yes | mkfs.vfat {device} && echo "DONE"')
        if to_format == Format.EXT4:
            self.tty_interface.write_command(f'yes | mkfs.ext4 {device} && echo "DONE"')
        self.tty_interface.wait_for_acknowledge(60, "DONE")
        print("Formatted")
