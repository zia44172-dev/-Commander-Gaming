[app]

title = Commander Gaming
package.name = commandergaming
package.domain = org.commander

source.dir = .
source.include_exts = py,png,jpg,kv,json,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.minapi = 24
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
p4a.branch = master
