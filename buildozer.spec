[app]
# (str) Title of your application
title = Edenshore

# (str) Package name
package.name = edenshore

# (str) Package domain
package.domain = org.edencore

# (str) Version of the app
version = 1.0

# (str) Source code where the main.py is located
source.dir = .

# (list) List of inclusions
source.include_exts = py,png,jpg,jpeg,json,txt,kv,mp3,wav,ogg,md

# (list) List of exclusions
source.exclude_dirs = tests, bin, .git, .github, __pycache__

# (list) Application requirements
# REMOVED pyjnius to prevent compilation errors.
requirements = python3,kivy,plyer

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Supported orientation
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, VIBRATE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 24

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) Automatically accept Android SDK licenses
android.accept_sdk_license = True

[buildozer]
warn_on_root = 0
