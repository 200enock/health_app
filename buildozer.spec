[app]

# (str) Title of your app
title = Mosquito Net Distribution App

# (str) Package name
package.name = mosquito_net_app

# (str) Package domain (needed for android/ios packaging)
package.domain = org.test

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported android version
#android.arch = armeabi-v7a

# (list) Permissions
android.permissions = INTERNET

# (int) API to use
#android.api = 30

# (int) Android min API to use
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 30

# (str) Android NDK version to use
#android.ndk = 21b

# (str) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (list) Android additionnal libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android/*.so

# (bool) Indicate whether the screen should always be illuminated
#android.wakelock = False

# (bool) If True, then the status bar will be hidden during execution.
#android.hide_statusbar = False

# (bool) If True, then the title will be hidden during execution.
#android.hide_title = False

# (list) List of shared libraries
#osx.python_version = 3
#osx.arch = x86_64
#android.archs = armeabi-v7a, arm64-v8a, x86, x86_64

# (str) python-for-android branch to use, defaults to stable
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
#p4a.bootstrap = sdl2

# (int) port number to specify an explicit --port= value and allow the API to respond
#android.port = 5000

# (str) Log level (info, warn, error)
log_level = 2

# (str) Requirements
requirements = python3,kivy,requests,plyer

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Whether the app is fullscreen or not
fullscreen = 0
