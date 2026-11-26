[app]

# (str) Title of your application
title = Sahibi Budget App

# (str) Package name
package.name = sahibibudget

# (str) Package domain (needed for android.permission.INTERNET etc.)
package.domain = sahibi.budget

# (str) Source code where the .p4a will look for your code (which export to python)
source.dir = .

# (list) Source files to be processed and to distribution
source.include_exts = py,kv,png,jpg,at,txt,xml,json

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements - PINNED for buildozer
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.10.*,kivy,kivymd,yt-dlp,ffmpeg

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source =

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

#
# Android specific

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE,FOREGROUND_SERVICE_TYPE_DOWNLOAD

# (int) Android API to use
android.api = 33

# (int) Minimum API required (8 = Android 2.2 devices)
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 21

# (bool) Use --private data storage (True) or dir public storage (False)
android.private_storage = True

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, e.g. libs/*.jar
# android.add_jars =

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
# android.add_src =

# (list) Android AAR archives to add (currently works only with sdl2_gradle
# bootstrap)
# android.add_aars =

# (list) Gradle dependencies to add (currently works only with sdl2_gradle
# bootstrap)
# android.gradle_dependencies =

# (list) add java compile options
# e.g. android.add_compile_options = "-source 1.8", "-target 1.8"
# android.add_compile_options =

# (list) Gradle repositories to add (please, avoid using this if possible,
# prefer letting gradle download them automatically from jcenter or google)
# android.gradle_repositories =

# (str) python-for-android branch to use, if not master, you can try
# p4a.branch = master

# (str) OUYA Console category
# Should be one of game, social, media, ... check OUYA documentation.
# android.ouya.category = game

# (str) Filename of OUYA Console icon
# android.ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filter in <activity> tag
# android.manifest.intent_filters =

# (str) launchMode to set for the main activity
# android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android/*.so
# android.add_libs_armeabi_v7a = libs/android-v7/*.so
# android.add_libs_arm64_v8a = libs/android-arm64/*.so
# android.add_libs_x86 = libs/android-x86/*.so
# android.add_libs_mips = libs/android-mips/*.so

# (bool) Whether to copy or symlink the libraries. When False (default), the
# libraries are symlinked. This is faster and uses less disk space.
# android.copy_libs = 1

# (str) The Android arch to build for, choices: arm64-v8a, armeabi-v7a, x86, x86_64
# In past, was android.arch but was renamed.
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic versionCode computation (used in build.gradle)
# android.numeric_version = 1

# (bool) enables Android app bundle support (AAB)
# android.enable_aab = False

# (str) The format of the package to build. Can be 'apk' or 'aab'.
# android.package_format = apk

# (str) Java or Kotlin file to add to the project as a native activity
# This is required if you want to extend a PythonActivity.
# android.activity_class_name = com.kivy.android.PythonActivity

# (str) xml file that defines the theme for the application
# android.theme = @style/Theme.KivyMD

#
# Python for android (p4a) specific

# (str) python-for-android fork to use, defaults to kivy (kivy/p4a)
# p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) python-for-android specific settings to pass to setup.py
# p4a.setup_args =

# (list) Extra arguments to pass to python-for-android toolchain
# p4a.extra_args =

#
# iOS specific

# (str) Path to a custom xcodebuild file
# ios.xcodebuild =

# (str) Name of the certificate to use for signing the debug version
# ios.codesign.debug = "iPhone Developer"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = "iPhone Distribution"

# (str) Path to the development team id
# ios.development_team =

# (str) Path to the provisioning profile to use
# ios.provisioning_profile =

# (str) Path to the certificate to use for signing
# ios.codesign =

#
# Buildozer specific

# (int) Log level (0 = debug, 1 = info, 2 = warning, 3 = error)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

# (list) List of files to exclude from the buildozer build
# buildozer.exclude_patterns =

# (list) List of files to include in the buildozer build
# buildozer.include_patterns =

# (list) Buildozer hooks, e.g. buildozer-hooks.py
# buildozer.hooks =

# (str) buildozer spec file version
buildozer.spec_version = 1.0