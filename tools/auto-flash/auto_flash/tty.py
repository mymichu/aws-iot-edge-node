import time

import serial


class TTY:
    interface: serial

    def __init__(self, device: str, baudrate: int):
        self.interface = serial.Serial(device, timeout=5, baudrate=baudrate, writeTimeout=1)
        print(f"Serial device {self.interface.name} is used")
        if self.interface.is_open == False:
            self.interface.open()

    def __del__(self):
        self.interface.close()

    def wait_for_acknowledge(self, timeout_sec: float, acknowledge_message: str) -> None:
        in_time = time.time()
        timeout = in_time + timeout_sec
        feedback_buffer = ""
        acknowledge_message_stripped = self._strip_message(acknowledge_message)
        while True:
            current_time = time.time()
            feedback_buffer += self.interface.readline().decode('UTF-8', errors="ignore").strip()
            feedback_buffer_stripped = self._strip_message(feedback_buffer)
            #print(f"DATA {acknowledge_message_stripped} vs {feedback_buffer_stripped}")
            if acknowledge_message_stripped in feedback_buffer_stripped:
                return
            if current_time > timeout:
                raise RuntimeError(f"Timeout wait for ACK on waiting {acknowledge_message}")
            if len(feedback_buffer) > 200000000:
                raise BufferError("Serial rx buffer to long")
            

    @staticmethod
    def _strip_message(message: str) -> str:
        message = message.strip()
        return message.replace(" ", "")

    def write_command(self, command: str, ignore_error: bool = False) -> None:
        command_enter = command + "\n"
        self.interface.write(command_enter.encode())
        self.interface.flush()
        if ignore_error:
            return
        self.wait_for_acknowledge(5.0, command)
