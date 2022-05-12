#!/usr/bin/env python
# coding: utf-8

import httpx
import json

class CharAssets:

    def __init__(self) -> None:
        pass

    @staticmethod
    def download(json_file, save_path):
        data = json.load(open(json_file, 'r'))
        url = data['A']['CharAssets.zip']['L']
        res = httpx.get(url,timeout=120)
        with open(save_path,'wb') as f:
            f.write(res.content)
            f.close()
