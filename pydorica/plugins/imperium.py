#!/usr/bin/env python
# coding: utf-8


from pathlib import Path
import json
import pandas as pd
from time import time
from pydorica.utils.crypto import MsgPack
from pydorica.log import logger


class Imperium:

    def __init__(self, imperium_dir_path: str, output_path: str) -> None:
        self.path = Path(imperium_dir_path)
        self.path.mkdir(exist_ok=True, parents=True)
        self.output_path = Path(output_path).joinpath('imperium/')
        self.output_path.mkdir(exist_ok=True, parents=True)
        self.BLACKLIST = ['ChinaBlacklist','GlobalBlacklist']
 
    def list(self):
        """Just list item"""
        for item in self.path.rglob('*'):
            if item.is_file():
                logger.info(item.parent.name+'@'+item.name)

    def unpack(self, overwrite:bool=False):
        """Unpack all file to json 
        overwrite: force to cover already unpacked file"""

        output_path = self.output_path.joinpath('unpacked')
        manifest_path = output_path.joinpath('manifest.json')

        if not overwrite:
            if manifest_path.is_file():
                logger.warning('Unpacked dir exists, try use overwrite param if you want a new one')
                return

        output_path.mkdir(exist_ok=True, parents=True)

        manifest = {}
        for item in self.path.rglob('*'):
            if item.is_file():
                dir_name = item.parent.name
                if 'unpacked' not in dir_name:
                    file_name = dir_name + '.json'
                    
                    save_path = output_path.joinpath(file_name)
                    file_path = item.absolute()
                    MsgPack.save(str(file_path), str(save_path))
                    manifest[dir_name] = item.name
                    logger.info(f'Unpack successfuly: {dir_name}@{item.name}')
        data = {
            'time': int(time()),
            'data': manifest
        }
        json.dump(data,open(manifest_path,'w'))

    def convert(self, to_excel:bool=False,  to_json:bool=False, overwrite:bool=True):
        """Convert and classify unpacked raw Json file, to Excel sheet or easy-to-read Json file"""
        # path
        unpacked_path = self.output_path.joinpath('unpacked')
        manifest_path = unpacked_path.joinpath('manifest.json')
        sheet_path = self.output_path.joinpath('sheet')
        json_path = self.output_path.joinpath('json')

        # cover and overwrite
        if overwrite:
            if not manifest_path.is_file():
                self.unpack(overwrite=True)
        else:
            if manifest_path.is_file():
                logger.warning('Unpacked manifest exists, try use overwrite param if you want a new one')
                return
            if sheet_path.is_dir():
                logger.warning('Unpacked excel dir exists, try use overwrite param if you want a new one')
                return
            if json_path.is_dir():
                logger.warning('Unpacked json dir exists, try use overwrite param if you want a new one')
                return                

        manifest = json.load(open(manifest_path,'r'))
        manifest_data = manifest['data']
        manifest_ls = [m for m in manifest_data]

        def _writer(to_excel:bool, to_json:bool, file_name:str, sheetlike_data:dict):

            if to_excel:
                sheet_path.mkdir(exist_ok=True, parents=True)
                writer = pd.ExcelWriter(sheet_path.joinpath(f'{file_name}.xlsx'))
            if to_json:
                json_path.mkdir(exist_ok=True, parents=True)
                to_json_data = {}
                to_json_path = json_path.joinpath(f'{file_name}.json')

            for sub_sheet_name in sheetlike_data:
                if sub_sheet_name not in self.BLACKLIST:
                    sub_sheet = sheetlike_data[sub_sheet_name]
                    sub_sheet_columns = sub_sheet['K']
                    sub_sheet_data = sub_sheet['D']
                    sub_sheet_df = pd.DataFrame(sub_sheet_data,columns=sub_sheet_columns)
                    if to_excel:
                        sub_sheet_df.to_excel(writer, sheet_name=sub_sheet_name)
                        logger.debug(f'Write to sheet: {file_name}#{sub_sheet_name}')
                    if to_json:
                        sub_sheet_dict = sub_sheet_df.to_dict(orient='records')
                        to_json_data.update({
                            sub_sheet_name: sub_sheet_dict
                        })
                        logger.debug(f'Write to json: {file_name}#{sub_sheet_name}')
            if to_excel:
                writer.close()
            if to_json:
                json.dump(to_json_data,open(to_json_path,'w',encoding='utf8'),ensure_ascii=False)
        
        for file_name in manifest_ls:
            file_path = unpacked_path.joinpath(f'{file_name}.json')
            data = json.load(open(file_path,'r',encoding='utf8'))
            sheetlike_data = data.get('C')
            if sheetlike_data:
                _writer(to_excel,to_json,file_name,sheetlike_data)

