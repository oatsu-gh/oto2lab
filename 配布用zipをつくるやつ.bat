rmdir /s /q exe\oto2lab-exe

mkdir exe\oto2lab-exe\
copy /Y oto2lab.py exe\oto2lab-exe\oto2lab.py
copy /Y README.md exe\oto2lab-exe\readme.md
xcopy /Y /q table exe\oto2lab-exe\table\

cd exe\oto2lab-exe
pyinstaller --onefile oto2lab.py --exclude-module read

move /Y dist\oto2lab.exe oto2lab.exe
rmdir /s /q dist, build, __pycache__
del /q oto2lab.spec, oto2lab.py
cd ..

explorer.exe .
