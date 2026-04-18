[app]
title = Samsung Calculator
package.name = samcalc
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# ملف الأيقونة
icon.filename = %(source.dir)s/icon.png

# المتطلبات: أضفنا tcl و tk لضمان عمل tkinter
requirements = python3,hostpython3,tcl,tk

orientation = portrait
fullscreen = 1
android.accept_sdk_license = True
android.api = 31
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
