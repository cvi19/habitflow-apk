[app]

# ── Basic info ──────────────────────────────────────────────
title           = HabitFlow
package.name    = habitflow
package.domain  = com.habitflow

source.dir      = .
source.include_exts = py,png,jpg,kv,atlas,html,json,js,css
source.include_patterns = assets/*

# ── Version ─────────────────────────────────────────────────
version         = 1.0.0

# ── Requirements ────────────────────────────────────────────
# jnius lets Python call Java (Android WebView)
requirements    = python3,kivy==2.3.0,jnius,android

# ── Orientation ─────────────────────────────────────────────
orientation     = portrait

# ── Icons (Buildozer will use these if present) ──────────────
# icon.filename   = %(source.dir)s/assets/icon-192.png
# presplash.filename = %(source.dir)s/assets/presplash.png

# ── Android ─────────────────────────────────────────────────
[buildozer]
log_level       = 2
warn_on_root    = 1

[app:android]
android.api                  = 33
android.minapi               = 21
android.ndk                  = 25b
android.sdk                  = 33
android.accept_sdk_license   = True

# Permissions
android.permissions = \
    INTERNET, \
    ACCESS_NETWORK_STATE, \
    WRITE_EXTERNAL_STORAGE, \
    READ_EXTERNAL_STORAGE

# Architecture — arm64-v8a covers 99% of modern Android devices
android.archs                = arm64-v8a, armeabi-v7a

# Release / debug
android.release_artifact     = apk
android.debug_artifact       = apk

# Entry point
android.entrypoint           = org.kivy.android.PythonActivity

# Enable hardware acceleration (needed for smooth WebView)
android.meta_data            = android:hardwareAccelerated=true

# Allow cleartext (for loading local file:// assets)
android.add_aars             =
android.gradle_dependencies  =

android.add_compile_options  = "android { \
    defaultConfig { \
        minSdk 21 \
    } \
}"

[app:ios]
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
