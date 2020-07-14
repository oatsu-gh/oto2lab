REM reclsit2region.pyをexeにして配布用zipにするバッチ

mkdir 録音リストからリージョンCSVを生成するツール
copy /Y reclist2region.py 録音リストからリージョンCSVを生成するツール\reclist2region.py
copy /Y README.md 録音リストからリージョンCSVを生成するツール\readme.txt
cd 録音リストからリージョンCSVを生成するツール

pyinstaller.exe reclist2region.py --onefile --clean --exclude-module readme.txt

move /Y dist\reclist2region.exe reclist2region.exe
rmdir /s /q dist, build, __pycache__
del /q reclist2region.spec, reclist2region.py
cd ..

powershell compress-archive -Force 録音リストからリージョンCSVを生成するツール 録音リストからリージョンCSVを生成するツール.zip
rmdir /s /q 録音リストからリージョンCSVを生成するツール
