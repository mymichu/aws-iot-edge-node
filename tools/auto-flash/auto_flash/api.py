import configuration
import serial
from typing import List

from auto_flash.partition import Partition, Format, Partitioner
from auto_flash.utility import Utility
from auto_flash.tty import TTY
from auto_flash.uboot import UBoot
from auto_flash.configuration import Settings as Json_Settings


class API:
    tty_interface: TTY
    configuration: Json_Settings
    linux_utility = Utility

    def __init__(self, device: str, baudrate: int, configuration_path: str):
        self.tty_interface = TTY(device, baudrate)
        self.configuration = Json_Settings(configuration_path)
        self.linux_utility = Utility(self.tty_interface)

    def _start_ram_image(self):
        uboot = UBoot(self.tty_interface)
        uboot.enter_uboot()
        uboot.boot_ram(self.configuration.config.serverip, self.configuration.config.ip, self.configuration.config.ramimage)

    def _configure_device(self):
        self.linux_utility.set_ip(self.configuration.config.ip, self.configuration.config.mask)

    def _flash_image(self):
        sorted_partition = sorted(self.configuration.config.partitions)
        part_partitions: List[Partition] = API.convert_partition_type(sorted_partition)
        partitioner = Partitioner(self.tty_interface)
        partitioner.create_partition_table(part_partitions, "/dev/mmcblk1")
        partition_id: int = 1
        for partition in sorted_partition:
            mounted_device = f"/dev/mmcblk1p{partition_id}"
            mounted_folder = f"/mnt/dir{partition_id}"
            partitioner.format_device(mounted_device, self._convert_format(partition.format))
            self.linux_utility.mount_device_force(mounted_device, mounted_folder)
            partition_id = partition_id + 1
            self.linux_utility.change_director(mounted_folder)
            for file in partition.files:
                self.linux_utility.tftp_download(self.configuration.config.serverip, file.name)
                if file.extract:
                    self.linux_utility.untar(file.name)
        print("Flashed reset the device")

    def run(self):
        self._start_ram_image()
        self._configure_device()
        self._flash_image()

    @staticmethod
    def convert_partition_type(in_partitions: List[configuration.Partition]) -> List[Partition]:
        part_partitions: List[Partition]=[]
        size_of_last_mb = 0
        for config_partition in in_partitions:
            part_partition: Partition = Partition()
            part_partition.fill = config_partition.fill
            part_partition.start_mb = size_of_last_mb
            part_partition.size_mb = config_partition.size_mb
            part_partition.primary = config_partition.primary
            part_partition.format = API._convert_format(config_partition.format)
            part_partitions.append(part_partition)
            size_of_last_mb = config_partition.size_mb
        return part_partitions

    @staticmethod
    def _convert_format(format_str: str) -> Format:
        if "fat32" == format_str:
            return Format.FAT
        elif "ext4" == format_str:
            return Format.EXT4
        else:
            raise "ONLY ext4 and fat32 format is supported"

