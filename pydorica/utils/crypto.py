#!/usr/bin/env python
# coding: utf-8

import msgpack
import json


class MsgPack:
    """"""
    @staticmethod
    def load(file_path: str) -> dict:
        """Open and unpack Msgpack file"""
        f = open(file_path,'rb')
        try:
            msg = msgpack.load(f)
            return msg
        except msgpack.exceptions.ExtraData:
            pass

    @staticmethod
    def save(file_path: str, save_path: str):
        """Save unpacked file as json"""
        msg = MsgPack.load(file_path)
        data = json.dumps(msg,ensure_ascii=False)
        with open(save_path, 'w', encoding='utf8') as f:
            f.write(data)
            f.close()
        