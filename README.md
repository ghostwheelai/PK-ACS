22.08.2018
------------

This is based on the code provided by Erivando Sena @ https://github.com/erivandoramos/TwoRC522RPi

I have modified it. 


Two RFID readers with Raspberry Pi

Assuming the python-dev and SPI-Py libraries are already correctly installed, configured, and tested on Raspberry Pi.

Otherwise, here is a brief help:
```{r, engine='bash', count_lines}
$ sudo apt-get install python-dev
$ git clone https://github.com/lthiery/SPI-Py.git
$ cd SPI-Py
$ sudo python setup.py install
```

Also install pip if it's not installed then
```{r, engine='bash', count_lines}
$ sudo pip install pyYaml
$ sudo pip install mysql-connector
```
Use: 
```
run the command "sudo python main.py" in the root folder of the extracted files
```
Press Ctrl + C to finish.
-------------

Denis Kolesnikov
