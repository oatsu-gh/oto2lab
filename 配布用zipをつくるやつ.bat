rem oto2labをexeにして配布用フォルダを作るバッチ

rmdir /s /q exe\oto2lab--exe

mkdir exe\oto2lab--exe\
copy /Y oto2lab.py exe\oto2lab--exe\oto2lab.py
copy /Y README.md exe\oto2lab--exe\readme.txt
copy /Y README_English.md exe\oto2lab--exe\readme_english.txt
xcopy /Y /q dic exe\oto2lab--exe\dic\
ren exe\oto2lab--exe\dic\README.md readme.txt
copy /Y exe\oto2labGUI.exe exe\oto2lab--exe\oto2labGUI.exe

cd exe\oto2lab--exe
pyinstaller --onefile oto2lab.py

move /Y dist\oto2lab.exe oto2lab.exe
rmdir /s /q dist, build, __pycache__
del /q oto2lab.spec, oto2lab.py
cd ..

explorer.exe .

PAUSE
