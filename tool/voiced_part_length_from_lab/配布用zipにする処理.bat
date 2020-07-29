REM reclsit2region.pyをexeにして配布用zipにするバッチ

mkdir 歌唱DBの有音部時間を調べるツール
copy /Y voiced_part_length_from_lab.py 歌唱DBの有音部時間を調べるツール\voiced_part_length_from_lab.py
copy /Y README.md 歌唱DBの有音部時間を調べるツール\readme.txt
cd 歌唱DBの有音部時間を調べるツール

pyinstaller.exe voiced_part_length_from_lab.py --onefile --clean --exclude-module readme.txt

move /Y dist\voiced_part_length_from_lab.exe voiced_part_length_from_lab.exe
rmdir /s /q dist, build, __pycache__
del /q voiced_part_length_from_lab.spec, voiced_part_length_from_lab.py
cd ..

powershell compress-archive -Force 歌唱DBの有音部時間を調べるツール 歌唱DBの有音部時間を調べるツール.zip
rmdir /s /q 歌唱DBの有音部時間を調べるツール
