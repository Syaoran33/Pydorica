#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import json
import pandas as pd

from pydorica.utils.crypto import MsgPack


class Imperium:

    def __init__(self, imperium_dir_path: str) -> None:
        self.path = Path(imperium_dir_path)
        self.path.mkdir(777, exist_ok=True)

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
                MsgPack.save(str(file_path), str(save_path))

    def converter_test(self,file_path):
        data = json.load(open(file_path,'r',encoding='utf8'))
        frame_data = data['C']['Default']['D']
        frame_key = data['C']['Default']['K']
        df = pd.DataFrame(frame_data,columns=frame_key)

        return df

    def converter(self, unpacked_dir_path:str='data/imperium/unpacked/'):
        """classify and convert to excel file"""
        save_path = Path(unpacked_dir_path)
        localization_file_path = save_path.joinpath('localization.json')
        gamedata_file_path = save_path.joinpath('gamedata.json')
        localization = json.load(open(localization_file_path,'r',encoding='utf8'))['C']
        gamedata = json.load(open(gamedata_file_path,'r',encoding='utf8'))['C']

        def to_excel(data:dict, type_:str='localization',black_list:list=['']):
            for file_name in data:
                if file_name not in black_list:
                    frame_columns = [
                        data[file_name]['K'][i] + ':' + data[file_name]['T'][i] \
                        for i in range(len(data[file_name]['K']))
                        ]
                    frame_data = data[file_name]['D']
                    df = pd.DataFrame(frame_data,columns=frame_columns)
                    file_path = file_name+'.xlsx'
                    save_path.joinpath(type_).mkdir(777, exist_ok=True)
                    df.to_excel(save_path.joinpath(type_,file_path),index=False)
        to_excel(localization,'localization')
        to_excel(gamedata,'gamedata',black_list=['DisableWords'])
