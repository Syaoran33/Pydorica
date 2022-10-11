#!/usr/bin/env python
# coding: utf-8

import httpx
import UnityPy

import asyncio
import json
from pathlib import Path


class Extractor:

    def __init__(self):
        pass
    
    @staticmethod
    def ls(raw_dir_path):
        dir_path = Path(raw_dir_path)
        for ab_path in dir_path.rglob('*'):
            print(ab_path)

    @staticmethod
    def extract(ab_dir_path):
        dir_path = Path(ab_dir_path)
        raw_path = dir_path.joinpath('raw')
        save_path = dir_path.joinpath('extracted')
        for ab_path in raw_path.rglob('*'):
            # File type
            file_extention = ab_path.suffix
            if file_extention == '.ab':
                
                env = UnityPy.load(str(ab_path))
                for path,obj in env.container.items():
                    try:
                        # Image Object
                        if obj.type.name in ["Texture2D", "Sprite"]:
                            data = obj.read()
                            # create dest based on original path
                            dest = save_path.joinpath(*path.split("/"))
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            extracted_path = Path(str(dest).replace(dest.suffix,'.png'))
                            if extracted_path.is_file():
                                extracted_path =str(extracted_path) + f'@{str(data.path_id)}'
                            data.image.save(str(extracted_path))
                            print('Sucessful: ',obj, obj.type.name, path)
                        
                        elif obj.type.name == 'TextAsset':
                            data = obj.read()
                            # create dest based on original path
                            dest = save_path.joinpath(*path.split("/"))
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            extracted_path = dest
                            if extracted_path.is_file():
                                extracted_path =str(extracted_path) + f'@{str(data.path_id)}'
                            text_asset = open(extracted_path,'wb')
                            text_asset.write(bytes(data.script))
                            text_asset.close()             
                            print('Sucessful: ',obj, obj.type.name, path)        

                        elif obj.type.name == "MonoBehaviour":
                            dest = save_path.joinpath(*path.split("/"))
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            # export
                            if obj.serialized_type.nodes:
                                #save decoded data
                                tree = obj.read_typetree()
                                extracted_path = Path(str(dest).replace(dest.suffix,'.json'))
                                if extracted_path.is_file():
                                    extracted_path += f'@{str(tree["m_Script"]["m_PathID"])}'
                                with open(extracted_path, "wt", encoding = "utf8") as f:
                                    json.dump(tree, f, ensure_ascii = False, indent = 4)
                            else:
                                # save raw relevant data (without Unity MonoBehaviour header)
                                data = obj.read()
                                extracted_path = Path(str(dest).replace(dest.suffix,'.bin'))
                                if extracted_path.is_file():
                                    extracted_path =str(extracted_path) + f'@{str(data.path_id)}'
                                with open(extracted_path, "wb") as f:
                                    f.write(data.raw_data)
                            print('Sucessful: ',obj, obj.type.name, path)

                        elif obj.type.name == "AudioClip":
                            clip = obj.read()
                            items = clip.samples.items()
                            for name, data in items:
                                dest = save_path.joinpath(*path.split("/"))
                                dest.parent.mkdir(parents=True, exist_ok=True)
                                extracted_path = Path(str(dest).replace(dest.suffix,'.wav'))
                                if extracted_path.is_file():
                                    extracted_path =str(extracted_path) + f'@{str(data.path_id)}'
                                audio_clip = open(extracted_path,'wb')
                                audio_clip.write(data)
                                audio_clip.close()
                                print('Sucessful: ',obj, obj.type.name, path)
                                
                        elif obj.type.name in ["AssetBundleManifest","GameObject","Material","UnknownType"]:
                            print('Unsupported: ',obj, obj.type.name, path)

                        elif obj.type.name == "Font":
                            data = obj.read()
                            # create dest based on original path
                            dest = save_path.joinpath(*path.split("/"))
                            dest.parent.mkdir(parents=True, exist_ok=True)

                            if data.m_FontData:
                                extracted_path = Path(str(dest).replace(dest.suffix,'.ttf'))
                                if font.m_FontData[0:4] == b"OTTO":
                                    extracted_path = Path(str(dest).replace(dest.suffix,'.otf'))
                            
                            if extracted_path.is_file():
                                extracted_path =str(extracted_path) + f'@{str(data.path_id)}'

                            font = open(extracted_path,'wb')
                            font.write(data.m_FontData)
                            font.close()
                            print('Sucessful: ',obj, obj.type.name, path)
                        
                        elif obj.type.name in ["Shader","Mesh"]:
                            data = obj.read()
                            # create dest based on original path
                            dest = save_path.joinpath(*path.split("/"))
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            extracted_path = Path(str(dest).replace(dest.suffix,'.txt'))

                            if extracted_path.is_file():
                                extracted_path =str(extracted_path) + f'@{str(data.path_id)}'

                            mesh = open(extracted_path, "wt", newline = "")
                            try:
                                w_data = data.export()
                                mesh.write(w_data)
                                mesh.close()
                            except IndexError:
                                print('Fail:',obj, obj.type.name, path)

                        else:
                            print('Undefine: ',obj, obj.type.name, path)
                    except Exception as ABEtractError:
                        print('Error: ',obj, obj.type.name, path)
                        print(ABEtractError)


class AssetsBundle:

    def __init__(self, ab_dir_path: str) -> None:
        self.dir_path = Path(ab_dir_path)
        self.client = httpx.AsyncClient()

    def checkUpdate(self, unpacked_dir_path: str):
        dir_path = Path(unpacked_dir_path)
        android_data = json.load(
            open(str(dir_path.joinpath('android.json')), 'r')
        )
        androidExp_data = json.load(
            open(str(dir_path.joinpath('androidExp.json')), 'r')
        )
        manifest_path = self.dir_path.joinpath('Manifest.json')

        if manifest_path.is_file():
            manifest = json.load(open(manifest_path, 'r'))

            def check(data):
                unmatched_ls = [x for x in data]
                update_ls = []
                for d_ab in data:
                    for m_ab in manifest:
                        # Compare ab name
                        if d_ab == m_ab:
                            unmatched_ls.pop(d_ab)
                            # Compare hash
                            if data[d_ab]['H'] != manifest[m_ab]['H']:
                                manifest[m_ab] = data[d_ab]
                                update_ls.update(d_ab)
                return unmatched_ls, update_ls
            android_data_tuple = check(android_data)
            androidExp_data_tuple = check(android_data)
            newly_ls = android_data_tuple[0] + androidExp_data_tuple[0]
            update_ls = androidExp_data_tuple[1] + androidExp_data_tuple[1]
            update = {
                'newly': newly_ls,
                'update': update_ls
            }

        else:
            manifest = {}
            manifest.update(android_data['A'])
            manifest.update(androidExp_data['A'])
            update = {}

        manifest_file = open(manifest_path, 'w')
        manifest_file.write(json.dumps(manifest))
        manifest_file.close()
        self.manifest = manifest
        return update

    async def download(self, ab: str, manifest: dict, save_dir_path: str):
        dir_path = Path(save_dir_path)
        dir_path.mkdir(exist_ok=True, parents=True)
        url = manifest.get(ab)['L']
        res = await self.client.get(url, timeout=3000)
        with open(dir_path.joinpath(ab), 'wb') as save_file:
            save_file.write(res.content)
            save_file.close()
        print(f'Download AB file sucessfully: {ab}')

    def download_all(self, save_dir_path='data/AssetsBundle/raw'):
        tasks = [self.download(ab, self.manifest, save_dir_path)
                 for ab in self.manifest]
        asyncio.run(asyncio.wait(tasks))
