#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from pathlib import Path
import zipfile
import gzip


class Zipper:

    def __init__(self, zip_file_path) -> None:
        self.zfile = zipfile.ZipFile(zip_file_path,'r')
    
    def ls(self):
        """Just list file"""
        for item in self.zfile.infolist():
            print(item)

    def unpack_all(self,save_dir_path:str):
        dir_path = Path(save_dir_path)
        dir_path.mkdir(777,exist_ok=True, parents=True)
        raws_path = dir_path.joinpath('raws')
        if raws_path.exists():
            for path in raws_path.rglob('*'):
                path.unlink()
        raws_path.mkdir(777,exist_ok=True, parents=True)
        self.zfile.extractall(raws_path)


    def unzip_c(self, save_dir_path:str):
        # path
        dir_path = Path(save_dir_path)
        dir_path.mkdir(777,exist_ok=True, parents=True)

        # Update
        def update(classify):
            dir_path_c = dir_path.joinpath(classify)
            if dir_path_c.exists:
                for path in dir_path_c.rglob('*'):
                    path.unlink()
            dir_path_c.mkdir(777,exist_ok=True, parents=True)
        update('battlecharacter')
        update('buff')
        update('condition')

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
            return extract_path

        for item in self.zfile.infolist():
            filename = item.filename
            extract_path = classify(filename,dir_path)
            bson_data:bytes = self.zfile.read(item)
            json_data = gzip.decompress(bson_data)
            extract_path = str(extract_path.joinpath(filename)).replace('bson','json')
            print(extract_path)
            json_file = open(extract_path,'wb')
            json_file.write(json_data)
