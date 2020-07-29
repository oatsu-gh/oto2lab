REM reclsit2region.pyをexeにして配布用zipにするバッチ

mkdir USTのBPMと音域を取得するツール
copy /Y ust_bpm_and_range.py USTのBPMと音域を取得するツール\ust_bpm_and_range.py
copy /Y README.md USTのBPMと音域を取得するツール\readme.txt
cd USTのBPMと音域を取得するツール

pyinstaller.exe ust_bpm_and_range.py --onefile --clean --exclude-module readme.txt

move /Y dist\ust_bpm_and_range.exe ust_bpm_and_range.exe
rmdir /s /q dist, build, __pycache__
del /q ust_bpm_and_range.spec, ust_bpm_and_range.py
cd ..

powershell compress-archive -Force USTのBPMと音域を取得するツール USTのBPMと音域を取得するツール.zip
rmdir /s /q USTのBPMと音域を取得するツール
