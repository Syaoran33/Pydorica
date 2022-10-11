#!/usr/bin/env python
# coding: utf-8

import httpx
import json
from pathlib import Path
import zipfile
import gzip
from pydorica.log import logger


class CharAssets:
    """Character Assets
    bundle_path: charAssets.zip file path, staticmethod@download_bundle support if not have one
    output_path: unpack output dir path"""
    def __init__(self, bundle_path, output_path) -> None:
        self.bundle_path = Path(bundle_path)
        self.output_path = Path(output_path).joinpath('charAssets')
        self.output_path.mkdir(parents=True,exist_ok=True)
        self.zfile = zipfile.ZipFile(bundle_path,'r')

    @staticmethod
    def download_bundle(json_file, save_path):
        """Download charAssets zipfile from unpacked imperium
        json_file: unpacked imperium json file path
        save_path: bundle save path"""
        json_file_path = Path(json_file)
        save_path = Path(save_path)
        save_path.parent.mkdir(exist_ok=True,parents=True)
        data = json.load(open(json_file_path, 'r'))
        url = data['A']['CharAssets.zip']['L']
        res = httpx.get(url,timeout=120)
        with open(save_path,'wb') as f:
            f.write(res.content)
            f.close()

    def list_item(self, keyword:str=None):
        """List item by keyword"""
        for item in self.zfile.infolist():
            if keyword:
                if keyword in item.filename:
                    print(item)
            else:
                print(item)

    def unpack_all(self, convert:bool=True, classify:bool=True):
        """Unzip all file
        convert: unzip to unpacked json file || to raw bson file
        classify: classify by filename"""

        def classify(filename,dir_path):
            filename_ls = filename.split('_')
            if 'battlecharacter' in filename_ls:
                extract_path = dir_path.joinpath('battlecharacter')
            elif 'buff' in filename_ls:
                extract_path = dir_path.joinpath('buff')
            elif 'condition' in filename_ls:
                extract_path = dir_path.joinpath('condition')
            else:
                extract_path = dir_path.resolve()
            extract_path.mkdir(parents=True,exist_ok=True)
            return extract_path

        if convert:
            dir_path = self.output_path.joinpath('json/')
            dir_path.mkdir(parents=True,exist_ok=True)
            for item in self.zfile.infolist():
                filename = item.filename
                extract_path = classify(filename,dir_path) if classify else dir_path.resolve()
                bson_data:bytes = self.zfile.read(item)
                json_data = gzip.decompress(bson_data)
                extract_path = str(extract_path.joinpath(filename)).replace('bson','json')
                json_file = open(extract_path,'wb')
                json_file.write(json_data)
                logger.debug(filename)
        else:
            raws_path = self.output_path.joinpath('raws/')
            if raws_path.exists():
                for path in raws_path.rglob('*'):
                    path.unlink()
            raws_path.mkdir(exist_ok=True, parents=True)
            self.zfile.extractall(raws_path)

