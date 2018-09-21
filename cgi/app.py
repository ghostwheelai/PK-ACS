#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import cgitb
import os
import psutil
from datetime import datetime
from datetime import timedelta

cgitb.enable()

header = """<!DOCTYPE html>
<html>
<head>
    <title>СКУД РП</title>
    <meta charset='utf-8'>
</head>
<body>"""

style = """<style>

div.center {
    width: 600px; /* Ширина элемента в пикселах */
    margin: auto; /* Выравниваем по центру */
    padding: 0px;
    background: #000000;
}

div.info {
    width: 100%; /* Ширина элемента в пикселах */
    padding: 10px; /* Поля вокруг текста */
    background: #FFDAB9; /* Цвет фона */
}

div.form {
    width: 100%; /* Ширина элемента в пикселах */
    padding: 10px; /* Поля вокруг текста */
    margin: 0px;
    background: #FFA500; /* Цвет фона */
    text-align: right;
}

div.post {
    width: 100%;
    padding: 10px;
    color: white;
    background: #000000;
}

</style>"""

footer = "</body></html>"

def get_temp():
    
    fd1 = open("/sys/class/thermal/thermal_zone0/temp", "r")
    temp_cpu=float(fd1.read())
    fd1.close()

    return float(round((temp_cpu/1000), 1))

def get_uptime():

    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(timedelta(seconds = uptime_seconds))
        uptime_string = uptime_string[:-7]

    return uptime_string

def get_time():
    return datetime.strftime(datetime.now(), "%H:%M:%S")

def get_cpu():
    return  int(psutil.cpu_freq().current) #(interval=None, percpu=False)

def get_mem():
    
    memory = psutil.virtual_memory()
    return (memory.total >> 20, memory.available >> 20)

print "Content-Type: text/html\n"
print header
print style
print "<div class='center'><div class='info'>"
print "<h3>Состояние Raspberry Pi</h3>"
print "<b>Температура процессора - {} C&deg;</b><br />".format(get_temp())
print "<b>Время работы {}</b><br />".format(get_uptime())
print "<b>Местное время {}</b><br />".format(get_time())
print "<b>Частота процессора {} MHz</b><br />".format(get_cpu())
print "<b>Всего памяти {} Мб</b><b><br />Доступно памяти {} Мб</b>".format(get_mem()[0], get_mem()[1])
print "</div>"
print "<div class='form'><form action='http://192.168.1.63/cgi/app.py' method='post'><input type='submit' name='test' value='test post'></form>"
print "</div>"

form = cgi.FieldStorage();
if form.has_key("test"):
    print "<div class='post'>This is POST request</div>"

print "</div>"
print footer