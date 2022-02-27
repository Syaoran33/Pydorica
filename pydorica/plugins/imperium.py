#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
from pydorica.utils.crypto import MsgPack


class Imperium:

    def __init__(self, imperium_dir_path: str) -> None:
        self.path = Path(imperium_dir_path)
        
    def ls(self):
        """Just list item"""
        for item in self.path.rglob('*'):
            if item.is_file():
                print(item.parent.name+': '+item.name)

    def unpack(self, output_path: str):
        """Unpack all file to json"""
        output_path = Path(output_path)
        output_path.mkdir(777, exist_ok=True)
        for item in self.path.rglob('*'):
            if item.is_file():
                file_name = item.parent.name + '.json'
                save_path = output_path.joinpath(file_name)
                file_path = item.absolute()
                MsgPack.save(file_path, save_path)
