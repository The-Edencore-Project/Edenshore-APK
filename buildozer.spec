[app]

title = Edenshore
package.name = edenshore
package.domain = org.edenshore

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,wav,ogg,ttf,json,txt

version = 0.1

requirements = python3,kivy,plyer

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

log_level = 2

[buildozer]

warn_on_root = 0
