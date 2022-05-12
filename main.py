#!/usr/bin/env python
# coding: utf-8

from pydorica.utils.zipper import Zipper
from pydorica.plugins.imperium import Imperium
from pydorica.plugins.charAssets import CharAssets

# Unpack imperium
# ipm = Imperium('data/imperium/')
# ipm.unpack('data/imperium/unpacked/')

# Download CharAssets
# CharAssets.download('data/imperium/unpacked/charAssets.json','data/charAssets.zip')

# Unzip CharAssets
zp = Zipper('data/charAssets.zip')
# zp.unpack_all('data/charAssets/')
zp.unzip_c('data/charAssets/')
