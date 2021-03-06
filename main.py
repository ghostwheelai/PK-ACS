# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import signal
import time
import datetime
import requests
import mysql.connector as mariadb
from module.NFC522 import Nfc522

user='user'
password='password'
host='ip'
database='pacs_uids'

GPIO.setmode(GPIO.BCM)

class rfid_module:

    def __init__(self):
        self.turn_on()
    
    def turn_on(self):
        GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
        self.status = True

    def turn_off(self):
        GPIO.cleanup(14)
        self.status = False
        self.time = 2

    time = 1

def send_data(last_id, card_id, id_bitrix, card_number):

    url = "http://random.denko.me/test.php"
    data = { 'last_id': last_id,
             'card_id': card_id,
             'id_bitrix': id_bitrix,
             'card_number': card_number }
    
    req = requests.post(url, data=data)
    #print req.text

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    GPIO.cleanup();
    continue_reading = False

def put_traffic(id, id_read):

    query = "INSERT INTO traffic(id_card, date_time, id_read) VALUES(%s, %s, %s)"
    date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    args = (id, date, id_read)

    mariadb_connection = mariadb.connect(user=user, password=password, host=host, database=database)
    cursor = mariadb_connection.cursor()

    try:
        cursor.execute(query,args)
    except mariadb.Error as error:
        print ("Error: {}".format(error))

    mariadb_connection.commit()
    mariadb_connection.close()

    if cursor.lastrowid:
        return cursor.lastrowid
    else: return None

def get_card_id(id):
    
    query = "SELECT * FROM cards WHERE num_card=(%s)"

    mariadb_connection = mariadb.connect(user=user, password=password, host=host, database=database)
    cursor = mariadb_connection.cursor()

    try:
        cursor.execute(query,(id,))
    except mariadb.Error as error:
        print ("Error: {}".format(error))

    results = cursor.fetchall()

    mariadb_connection.commit()
    mariadb_connection.close()

    if cursor.rowcount > 0:
        for res in results:
            return res              
    else:
        return None

def test(id, id_read):

    res = get_card_id(id)

    if res:
        card_id, id_bitrix, card_number = res

        if id_read==0:
            enter="Вход,"
        else:
            enter="Выход,"
        
        print enter + " id карты {}, Битрикс id {}, номер карты {}".format(card_id, id_bitrix, card_number)
    else:
        print "Карты {} нет в базе данных".format(id)
        return None
    
    last_id = put_traffic(card_id, id_read)

    if last_id:
        send_data(last_id, card_id, id_bitrix, card_number)
    else:
        print "Что-то пошло не так"
    
    rfid.turn_off()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

nfc = Nfc522()
rfid = rfid_module()

continue_reading = True
print "\nWaiting for Tag\n---------------\n"

while continue_reading:
    print_opt = 0

    if rfid.time == 1:
        
        if not rfid.status:
            rfid.turn_on()

        gid1,gid2 = nfc.obtem_nfc_rfid()

        if not gid1==0:
            print_opt = 1
            test(gid1, 0)
        if not gid2==0:
            print_opt = 1
            test(gid2, 1)
    else:
        rfid.time -= 1

    if print_opt==1:
        print "\nWaiting for Tag\n---------------"
    
    time.sleep(1)
