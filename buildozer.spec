[app]
title = Edenshore
package.name = edenshore
package.domain = org.edencore

version = 1.0.0

source.dir = .
# We include all file types your app uses
source.include_exts = py,png,jpg,kv,atlas,ogg,json,md

# Required for Kivy, vibration, and Android native calls
requirements = python3,kivy,plyer,pyjnius

# App permissions
android.permissions = VIBRATE, INTERNET

# Universal compatibility (64-bit for your MatePad, 32-bit for older phones)
android.archs = arm64-v8a, armeabi-v7a

# Modern Android target
android.api = 33
android.minapi = 21

# Hide the Android status bar for full immersion
fullscreen = 1
