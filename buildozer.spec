[app]
title = Edenshore
package.name = edenshore
package.domain = org.edencore
version = 1.0

p4a.local_recipes = p4a-recipes

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,txt,kv,mp3,wav,ogg,md
source.exclude_dirs = tests, bin, .git, .github, __pycache__, .buildozer

requirements = python3==3.11.9,hostpython3==3.11.9,kivy,plyer

p4a.branch = develop
p4a.pip_no_upgrade = 1

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
