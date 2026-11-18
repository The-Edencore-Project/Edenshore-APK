[app]

title = Edenshore
package.name = edenshore
package.domain = org.edencore

version = 1.0

source.dir = .
source.include_exts = py,png,jpg,jpeg,json,txt,kv,mp3,wav,ogg,md
source.exclude_dirs = tests,bin,.git,.github,__pycache__

requirements = python3,kivy,plyer

fullscreen = 1
orientation = portrait

android.permissions = INTERNET,VIBRATE

android.api = 33
android.minapi = 21
android.ndk = 25b

android.skip_update = False
android.accept_sdk_license = True

android.archs = arm64-v8a,armeabi-v7a

log_level = 2

android.allow_backup = True
android.release_artifact = apk

[buildozer]

warn_on_root = 0
