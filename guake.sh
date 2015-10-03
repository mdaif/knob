#!/bin/sh
notify-send "Guake will re-open when Knob is ready !"
guake

guake -n $(pwd)
guake -r "Server" -e "source env/bin/activate;source set_env.sh"
guake -e "python manage.py runserver 1111"

guake -n $(pwd)
guake -r "Terminal" -e "source env/bin/activate;source set_env.sh"

guake -n $(pwd)
guake -r "Shell" -e "source env/bin/activate;source set_env.sh"
guake -e "python manage.py shell"

guake -n $(pwd)
guake -r "Email" -e "source env/bin/activate;source set_env.sh"
guake -e "python -m smtpd -n -c DebuggingServer localhost:1025"

sleep 5
guake
