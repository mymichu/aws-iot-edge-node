import json
from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True, repr=True)
class Partition:
    id: int
    format: str
    size_mb: int = 0
    fill: bool = False
    primary: bool = False
    extract: bool = False
    files: str = ""

    def __repr__(self):
        rep_string = f"id: {self.id} -- format: {self.format} "
        rep_string += f" -- primary: {self.primary} "
        if self.fill:
            rep_string += f" -- size_mb: 100%"
        else:
            rep_string += f" -- size_mb: {self.size_mb}"
        if self.files :
            rep_string += f" -- files: {self.files}"
        if self.extract:
            rep_string += f" -- extract: {self.extract}"
        return rep_string

    def __gt__(self, other):
        return self.id > other.id

    def __eq__(self, other):
        return self.id == other.id


@dataclass_json
@dataclass(frozen=True)
class Config:
    partitions: List[Partition]


class Settings:
    config: Config
    config_file: str = field(repr=False)

    def __init__(self, file: str = "config.json"):
        self.config_file = file
        self.read_config()

    def read_config(self):
        with open(self.config_file) as json_file:
            raw_data = json_file.read()
        self.config = Config.from_json(raw_data)

    def print_part(self):
        sorted_partition = sorted(self.config.partitions)
        for partition in sorted_partition:
            print(partition)