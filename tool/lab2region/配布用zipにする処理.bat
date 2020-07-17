REM reclsit2region.pyをexeにして配布用zipにするバッチ

mkdir 音素ラベルからリージョンCSVを生成するツール
copy /Y lab2region.py 音素ラベルからリージョンCSVを生成するツール\lab2region.py
copy /Y README.md 音素ラベルからリージョンCSVを生成するツール\readme.txt
cd 音素ラベルからリージョンCSVを生成するツール

pyinstaller.exe lab2region.py --onefile --clean --exclude-module readme.txt

move /Y dist\lab2region.exe lab2region.exe
rmdir /s /q dist, build, __pycache__
del /q lab2region.spec, lab2region.py
cd ..

powershell compress-archive -Force 音素ラベルからリージョンCSVを生成するツール 音素ラベルからリージョンCSVを生成するツール.zip
rmdir /s /q 音素ラベルからリージョンCSVを生成するツール
