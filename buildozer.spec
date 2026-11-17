[app]

# (str) Title of your application
title = EdenShore

# (str) Package name
package.name = edenshore

# (str) Package domain (needed for android/ios packaging)
package.domain = org.edenshore

# (str) Source code where the main.py is located
source.dir = .

# (list) List of inclusions (patterns are relative to source.dir)
source.include_exts = py,png,jpg,jpeg,json,txt,kv,mp3,wav,ogg

# (list) List of exclusions
source.exclude_dirs = tests, bin, .git, .github

# (list) Application requirements
requirements = python3,kivy

# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/data/icon.png

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (str) Supported orientation (landscape, portrait, all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET

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

# ──────────────────────────────
# ✅ THIS PART FIXES THE ROOT PROMPT
# ──────────────────────────────

[buildozer]
warn_on_root = 0
android.accept_sdk_license = True

