# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
from pathlib import Path
from os import getenv

hiddenimports = []
hiddenimports += collect_submodules('config.py')
hiddenimports += collect_submodules('directinput.py')
hiddenimports += collect_submodules('ScanKeys.py')
hiddenimports += collect_submodules('ui_main.py')
hiddenimports += collect_submodules('captureloop.py')

block_cipher = None

a = Analysis(['main.py'],
             pathex=[f'{getenv("appdata")}\\Roaming\\Python\\Python38\\site-packages\\cv2', ''],
             binaries=[],
             datas=[("model\\gi_actions.weights", "model\\"), ("model\\yolov4-tiny.cfg", "model\\"), ("model\\classes.names", "model\\")],
             hiddenimports=hiddenimports,
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='GIAP',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , uac_admin=True)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='GIAP')
