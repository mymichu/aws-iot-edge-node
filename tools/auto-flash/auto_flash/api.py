from codecs import ignore_errors
import time
import serial
import config
from typing import List

def enter_uboot(tty: serial):
    if not tty.is_open:
        tty.open()
    in_uboot = False
    timeout = time.time() + 60 * 5
    print("Wait for reset Board.")
    while not in_uboot:
        tty.write("m \n".encode())  # write a string
        tty.flush()
        in_uboot = _wait_for_acknowledge(tty, 0.01, "Colibri iMX6 #")
        if time.time() > timeout:
            raise RuntimeError("Unable to enter U-Boot console")
    print("U-Boot console entered.")
    tty.close()


def _wait_for_acknowledge(tty: serial, timeout_sec: float, acknowledge_message: str, only_ack: bool = False):
    inTime = time.time();
    timeout =  inTime + timeout_sec
    feedback_buffer=""
    acknowledge_message=acknowledge_message.strip();
    acknowledge_message=acknowledge_message.replace(" ", "")
    while True:    
        feedback_buffer +=  tty.readline().decode('UTF-8', errors="ignore").strip()
        feedback_buffer=feedback_buffer.replace(" ", "")
        current_time=time.time();
        if only_ack == True:
            if acknowledge_message == feedback_buffer:
                return True
        else:
            if acknowledge_message in feedback_buffer:
                return True
        if current_time > timeout:
            print(f"Timeout {inTime} vs {timeout} vs {timeout_sec}: {acknowledge_message} vs {feedback_buffer}")
            return False
        if len(feedback_buffer) > 200000000:
            print(f"blabal {feedback_buffer}")
            raise BufferError("Serial rx buffer to long")

def _write_command(tty: serial, command: str, ignore_check=False):
    command_enter=command+"\n"
    tty.write(command_enter.encode())
    tty.flush()
    if ignore_check ==False:
        if _wait_for_acknowledge(tty, 5.0, command, only_ack=False) == False:
            raise RuntimeError("Not able to write command to serial")


def boot_ram(tty: serial, serverip: str, ip: str, fit_binary: str):
    print("Download From TFTP & Boot from RAM.")
    if not tty.is_open:
        tty.open()
    tty.flush()
    tty.write("\n".encode())
    _write_command(tty, f"setenv ipaddr {ip}")
    _write_command(tty, f"setenv serverip {serverip}")
    tftpcmd = "tftp ${loadaddr}" + f" {fit_binary}" 
    _write_command(tty, tftpcmd)
    if _wait_for_acknowledge(tty, 60, "done") == True:
        print("FIT image downloaded from tftp.")
        _write_command(tty, "bootm ${loadaddr}")
        if _wait_for_acknowledge(tty, 60, "Run /init as init process") == True:
            time.sleep(5)
            print("FIT image started.")
        else:
            raise("Not able to start RAM Image!")
    else:
            raise("Not able to download RAM Image!")
    tty.close()

def partition_device(tty: serial, serverip: str, ip: str, mask: str, partitions: List[config.Partition]):
    if not tty.is_open:
        tty.open()
    tty.flush()
    print("Set IP on RAM Disk")
    _write_command(tty, f"ifconfig eth0 {ip} netmask {mask} up")
    _wait_for_acknowledge(tty, 30, "link becomes ready")
    _write_command(tty, f"ifconfig")
    if _wait_for_acknowledge(tty, 10, f"{ip}"):
        print("Ethernet is configured")
    _write_command(tty,f"parted  -a optimal /dev/mmcblk1 -s mklabel msdos")
    size_of_last_mb = 0
    sorted_partition = sorted(partitions)
    for partition in sorted_partition:
        partition_command=f"parted  -a optimal /dev/mmcblk1 -s mkpart primary {partition.format} "
        if size_of_last_mb == 0:
            partition_command+=f" 0%" 
        else:
            partition_command+=f" {size_of_last_mb}MB"
        size_of_last_mb = partition.size_mb
        if partition.fill:
            partition_command += f" 100%"
        else:
            partition_command += f" {partition.size_mb}MB"
        _write_command(tty,partition_command)
        if partition.primary:
            _write_command(tty,f"parted -a optimal /dev/mmcblk1 -s set {partition.id} boot on")
    for partition in sorted_partition:
        if "fat" in partition.format:
            _write_command(tty,f"yes | mkfs.vfat /dev/mmcblk1p{partition.id}")
            if _wait_for_acknowledge(tty,60,"mkfs.fat"):
                print("FAT Formatted")
        if "ext4" in partition.format:
            _write_command(tty,f"yes | mkfs.ext4 /dev/mmcblk1p{partition.id}")
            if _wait_for_acknowledge(tty,60,"done"):
                print("EXT4 Formatted")
    
    for partition in sorted_partition:
        if partition.files.count:
            _write_command(tty,f"mkdir -p /mnt/dir{partition.id}")
            _write_command(tty,f'mount /dev/mmcblk1p{partition.id} /mnt/dir{partition.id} && echo "DONE"')
            if _wait_for_acknowledge(tty,60,f"DONE")==False:
                raise "Not able to mount device"
            _write_command(tty,f'cd /mnt/dir{partition.id} && echo "DONE"')
            if _wait_for_acknowledge(tty,60,f"DONE")==False:
                raise "Change Directory"
            for file in partition.files:
                print(f"Download {file}")
                _write_command(tty,f'tftp {serverip} -c get {file} && echo "DONE"')
                time.sleep(1)
                if _wait_for_acknowledge(tty,120,f"DONE")==True:
                    print(f"File downloaded {file}")
                print(f"Check if file was correctly downladed {file}")
                _write_command(tty,f"stat {file}")
                if _wait_for_acknowledge(tty,60,"regular file") == True:
                    print(f"File was correctly downloaded {file}")
                else:
                    raise "Download was not succesfull"
                if partition.extract == True:
                    print(f"Unpacking {file}")
                    _write_command(tty,f'tar -xf {file} && echo "DONE" ')
                    if _wait_for_acknowledge(tty,18000,"DONE") == True:
                        print(f"Unpackecd {file}")
                        _write_command(tty,f"rm -rf {file}")
                    else:
                        raise f"Was not able to unpack {file}"
            _write_command(tty,f"cd /")
            
    print("Flashed reset the device")
    tty.close()
    