# Courses Management System
no description at the moment

Delete the build:
rm -rf build dist *.spec

Build App:
pyinstaller --windowed \
  --name "Courses Management" \
  --icon "assets/app_icon.icns" \
  --add-data "assets/.env:assets" \
  --add-data "assets/database.db:assets" \
  --add-data "assets/student_profile:assets/student_profile" \
  main.py

DMG:
rm NileAcademy.dmg
create-dmg \
  --volname "Nile Academy Installer" \
  --window-pos 200 120 \
  --window-size 1000 600 \
  --icon-size 100 \
  --icon "NileAcademy.app" 250 250 \
  --app-drop-link 750 250 \
  "NileAcademy.dmg" \
  "dmgbuild/"

Signing:
codesign --force --deep --sign "Developer ID Application: Omar Khalifa" NileAcademy.app
