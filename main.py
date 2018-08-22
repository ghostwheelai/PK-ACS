# -*- coding: utf-8 -*-
import signal
import time
import mysql.connector as mariadb
from module.NFC522 import Nfc522

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
##    GPIO.cleanup()

def test(id):
    
    mariadb_connection = mariadb.connect(user='user', password='ld3lsc', host='192.168.1.241', database='pacs_uids')

    cursor = mariadb_connection.cursor()

    try:
        cursor.execute("SELECT uid FROM uids WHERE uid=(%s)",(id,))
    except mariadb.Error as error:
        print ("Error: {}".format(error))

    results = cursor.fetchall()

    if cursor.rowcount > 0:
        for res in results:
            for uid in res:

                print "indatabase {}".format(uid)
        
        #        for uid in results:
#            print("В базе данных, код {}".format(uid)
    else:
        print ("Нет в базе данных");

    mariadb_connection.commit()
    mariadb_connection.close()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

nfc = Nfc522()

continue_reading = True
print "\nWaiting for Tag\n---------------"

while continue_reading:
    print_opt = 0
    
    gid1,gid2 = nfc.obtem_nfc_rfid()
    ##print "G Read TAG Number: " +str(id)

    if not gid1==0:
        print "ID of first Tag is:" + str(gid1)
        print_opt = 1
        #test(gid1)
    if not gid2==0:
        print "ID of SecondTag is:" + str(gid2)
        print_opt = 1
        #test(gid2)

    if print_opt==1:
        print "\nWaiting for Tag\n---------------"
    time.sleep(1)


