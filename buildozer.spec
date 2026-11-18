[app]

# App Information
title = Edenshore
package.name = edenshore
package.domain = org.edencore

# Version
version = 1.0

# Source
source.dir = .
source.include_exts = py,png,jpg,jpeg,json,txt,kv,mp3,wav,ogg,md
source.exclude_dirs = tests,bin,.git,.github,__pycache__

# Requirements
requirements = python3==3.11.9,kivy,plyer

# Display
fullscreen = 1
orientation = portrait

# Android Permissions
android.permissions = INTERNET,VIBRATE

# Android SDK Settings
android.api = 33
android.minapi = 21
android.ndk = 25b

# SDK Management
android.skip_update = False
android.accept_sdk_license = True

# Python-for-Android
p4a.branch = develop

# Architectures
android.archs = arm64-v8a, armeabi-v7a

# Build Options
log_level = 2

# Presplash and Icon (uncomment when files exist)
# presplash.filename = assets/images/presplash.png
# icon.filename = assets/images/icon.png

# Android Behaviour
android.allow_backup = True

# Packaging
android.release_artifact = apk

[buildozer]

warn_on_root = 0
