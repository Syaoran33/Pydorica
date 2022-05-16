#!/usr/bin/env python
# coding: utf-8

from pydorica.utils.zipper import Zipper
from pydorica.plugins.imperium import Imperium
from pydorica.plugins.charAssets import CharAssets
from pydorica.plugins.assetsbundle import AssetsBundle
from pydorica.plugins.assetsbundle import Extractor

# Imperium
# IMPERIUM DIR NEEDED, OR A EMPTY EXPORT
# imp = Imperium('data/imperium/')
# imp.unpack('data/imperium/unpacked/')
# imp.converter()

# CharAssets
# CharAssets.download('data/imperium/unpacked/charAssets.json','data/charAssets.zip')

# Unzip CharAssets
# zipper = Zipper('data/charAssets.zip')
# zipper.unpack_all('data/charAssets/')
# zipper.unzip_c('data/charAssets/')

# AssetsBundle
# ab = AssetsBundle('data/AssetsBundle')
# ab.checkUpdate('data/imperium/unpacked/')
# ab.download_all()

# AssetsBundle Extractor
# Extractor.extract('data/AssetsBundle/')
