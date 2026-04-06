[app]

# ── App info ─────────────────────────────────────────────────
title           = HabitFlow
package.name    = habitflow
package.domain  = com.habitflow
version         = 1.0.0

# ── Source ───────────────────────────────────────────────────
source.dir      = .
source.include_exts     = py,png,jpg,kv,atlas,html,json,js
source.include_patterns = assets/*

# ── Requirements ─────────────────────────────────────────────
# jnius lets Python call Android Java APIs (WebView etc.)
requirements = python3,kivy==2.3.0,android,jnius

# ── Orientation ──────────────────────────────────────────────
orientation     = portrait
fullscreen       = 0

# ── Android settings ─────────────────────────────────────────
android.api         = 33
android.minapi      = 24
android.ndk         = 25b
android.archs       = arm64-v8a

# Permissions
android.permissions = \
    INTERNET,\
    ACCESS_NETWORK_STATE

# Hardware acceleration (required for smooth WebView)
android.manifest.application_attributes = android:hardwareAccelerated="true"

# Allow cleartext for local file:// loading
android.add_aars             =
android.gradle_dependencies  =

# Accept SDK license
android.accept_sdk_license   = True

# Log level for build output
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
