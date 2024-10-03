@echo off
title Build Tool - Build TsukiNotes
echo Start Build The TsukiNotes
echo 必须保持py在当前文件夹，tsuki文件夹在当前文件夹

REM 检查是否存在 TsukiNotes.py 文件
if not exist "TsukiNotes.py" (
    echo Error: TsukiNotes.py 文件不存在！
    pause
    exit /b
)

REM 检查 tsuki 目录是否存在
if not exist "tsuki" (
    echo Error: tsuki 文件夹不存在！
    pause
    exit /b
)

REM 检查 tsuki/assets/kernel 目录是否存在
if not exist "tsuki/assets/kernel" (
    echo Error: tsuki/assets/kernel 文件夹不存在！
    pause
    exit /b
)

REM 检查 logo.ico 文件是否存在
if not exist "tsuki/assets/GUI/ico/logo.ico" (
    echo Error: logo.ico 文件不存在！
    pause
    exit /b
)

REM 安装 pip 和 pyinstaller
pip install --upgrade pip
pip install pyinstaller

REM 执行 pyinstaller 命令
pyinstaller --add-data "tsuki/assets/kernel/*.pyd;tsuki/assets/kernel" "TsukiNotes.py" -i "tsuki/assets/GUI/ico/logo.ico" -w

pause
