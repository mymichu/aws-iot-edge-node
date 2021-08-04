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
    path: str = ""

    def __repr__(self):
        rep_string = f"id: {self.id} -- size_mb: {self.size_mb} -- size_mb: {self.format} "
        rep_string += f" -- primary: {self.primary} -- path: {self.path}"
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
        print(sorted_partition[0])
