#!/bin/bash
export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
notify-send "Reminder" "Submit your assignments today!"

#Add sound Effect
paplay /usr/share/sounds/freedesktop/stereo/complete.oga

#file open
xdg-open /home/aushtmi-deb/Downloads/sample.pdf
