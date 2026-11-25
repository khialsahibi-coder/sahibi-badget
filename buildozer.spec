[app]

# App info
title = Sahibi Budget
package.name = sahibibudget
package.domain = org.sahibi

# Source
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,txt
version = 0.1

# Requirements (no wildcards in versions)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow

# Display
orientation = portrait
fullscreen = 0

# Android
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
