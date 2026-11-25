ok[app]

# (str) Title of your application
title = Sahibi Budget App

# (str) Package name
package.name = sahibibudget

# (str) Package domain
package.domain = sahibi.budget

# (str) Source code directory
source.dir = .

# (list) Source file extensions to include
source.include_exts = py,kv,png,jpg,at,txt,xml,json

# (str) Application version
version = 1.0.0

# (list) Application requirements - PINNED for buildozer compatibility
# python3==3.10.* required (3.11+ breaks buildozer)
# cython==0.29.36 required (newer breaks buildozer)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow
android.api = 33
android.archs = arm64-v8a
android.accept_sdk_license = True
# (str) Supported orientation
orientation = portrait

#
# Android specific
#

# (bool) Fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.build_tools_version = 33.0.2
# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (int) Android NDK API
android.ndk_api = 21

# (bool) Private storage
android.private_storage = True


#
# Python for android (p4a) specific
#
p4a.fork = kivy
p4a.branch = master

#
# Buildozer specific
#
log_level = 2
warn_on_root = 1
buildozer.spec_version = 1.0
