# Courses Management System
no description at the moment

Delete the build:
rm -rf build dist *.spec

Build App:
rm -rf build dist *.dmg
pyinstaller NileAcademy.spec --clean


DMG:
rm -rf dmgbuild
mkdir dmgbuild
cp -R "dist/NileAcademy.app" dmgbuild/
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
