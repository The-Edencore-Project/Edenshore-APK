[app]
title = Edenshore
package.name = edenshore
package.domain = org.edencore
version = 1.0

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,txt,kv,mp3,wav,ogg,md
source.exclude_dirs = tests, bin, .git, .github, __pycache__, .buildozer

# (list) Application requirements
# FORCE Python 3.11.9 for BOTH target and host to avoid the 3.14 pip crash
requirements = python3==3.11.9,hostpython3==3.11.9,kivy,plyer

# (str) python-for-android branch (master is stable for Python <=3.12)
p4a.branch = master

fullscreen = 1
orientation = portrait

android.permissions = INTERNET, VIBRATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 24
android.accept_sdk_license = True

[buildozer]
warn_on_root = 0