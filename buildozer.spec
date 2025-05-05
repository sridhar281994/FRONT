[app]
title = DateCha
package.name = datecha
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
version = 1.0
android.permissions = INTERNET,RECORD_AUDIO,CAMERA
icon.filename = assets/icons/app_icon.png
entrypoint = main.py
android.add_aars = ./libs/agora-rtc-sdk.aar
android.add_src = ./java
fullscreen = 1
orientation = portrait
requirements = python3,kivy,requests,pyjnius,hostpython3
android.api = 33
android.minapi = 24
android.ndk = 23b
android.ndk_api = 24
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0
android.enable_androidx = 1
android.clean_build = 1
[buildozer]
log_level = 2
warn_on_root = 1




