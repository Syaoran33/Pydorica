#!/usr/bin/env python
# coding: utf-8

import json
from pathlib import Path
from pydorica.utils.skel2json import Handler
from PIL import Image


class Spine:

    @staticmethod
    def skel2json(skel_path: str, json_path: str):
        result = Handler(open(skel_path, 'rb')).handle()
        json.dump(result, open(json_path, 'w'))

    @staticmethod
    def resize(pic_path: str, size: tuple):
        img = Image.open(pic_path)
        img = img.resize(size)
        img.save(pic_path)

    @staticmethod
    def atlas_size(atlas_path: str):
        lines = open(atlas_path, 'r').readlines()
        size_line = lines[2].replace('size:', '').strip()
        size = tuple([int(x) for x in size_line.split(',')])
        return size

    @staticmethod
    def SpineChef(spinedata_dir_path: str):
        dir_path = Path(spinedata_dir_path)
        for spine_pic in dir_path.rglob('*.png'):
            def chef(spine_pic):
                index_html: str = open(
                    'pydorica/src/spine_web_player.html', 'r').read()
                spine_skel = Path(str(spine_pic).replace(
                    spine_pic.suffix, '.skel.bytes'))
                spine_atlas_txt = Path(str(spine_pic).replace(
                    spine_pic.suffix, '.atlas.txt'))
                spine_atlas = Path(str(spine_pic).replace(
                    spine_pic.suffix, '.atlas'))
                spine_json = Path(str(spine_pic).replace(
                    spine_pic.suffix, '.json'))
                spine_html = Path(str(spine_pic).replace(
                    spine_pic.name, 'index.html'))
                # Rename atlas
                if not spine_atlas.is_file():
                    spine_atlas_txt.rename(spine_atlas)
                # Resize pic
                size = Spine.atlas_size(spine_atlas)
                Spine.resize(str(spine_pic), size)
                # Convert config
                if not spine_json.is_file():
                    Spine.skel2json(str(spine_skel), str(spine_json))
                # Generate html
                if not spine_html.is_file():
                    index_html = index_html.replace(
                        '$jsonUrl$', f'./{spine_json.name}').replace('$atlasUrl$', f'./{spine_atlas.name}')
                    index_file = open(spine_html, 'w')
                    index_file.write(index_html)
                    index_file.close()
                print(spine_pic)
            try:
                chef(spine_pic)
            except Exception as ChefError:
                print(spine_pic, ChefError)
