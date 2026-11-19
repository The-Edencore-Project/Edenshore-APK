[app]

title = Edenshore
package.name = edenshore
package.domain = org.edencore

version = 1.0

source.dir = .

source.include_exts = py,png,jpg,jpeg,json,txt,kv,mp3,wav,ogg,md
source.exclude_dirs = tests,bin,.git,.github,__pycache__,.buildozer

requirements = python3,kivy,plyer

fullscreen = 1
orientation = portrait

android.permissions = INTERNET,VIBRATE

android.api = 33
android.minapi = 21
android.ndk = 25b

android.accept_sdk_license = True

log_level = 2

p4a.url = https://github.com/kivy/python-for-android.git

# Remove p4a.branch line and add:

p4a.tag = v2026.05.09

[buildozer]

warn_on_root = 0
