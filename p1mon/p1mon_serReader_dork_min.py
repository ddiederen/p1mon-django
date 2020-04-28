#!/usr/bin/python3
# libraries
import os
import serial as srl
from datetime import datetime, timezone
# import systemid
from PyCRC.CRC16 import CRC16
import time
import sqlite3
import re

# django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','p1mon.settings')
django.setup()
from serialdata.models import SerialLive

# functions
# def funCommitRecord(record,db,cur,table):
#     columns = ', '.join(record.keys())
#     placeholders = ':'+', :'.join(record.keys())
#     query = 'INSERT INTO '+table+' (%s) VALUES (%s)' % (columns, placeholders)
#     print(query)
#     cur.execute(query, record)
#     db.commit()

def funCommitRecord(record):
    # convert dictionary to django model instance
    recordInstance = SerialLive(
        verbr_kwh_181 = record['VERBR_KWH_181'],
        verbr_kwh_182 = record['VERBR_KWH_182'],
        gelvr_kwh_281 = record['GELVR_KWH_281'],
        gelvr_kwh_282 = record['GELVR_KWH_282'],
        tariefcode = record['TARIEFCODE'],
        act_verbr_kw_170 = record['ACT_VERBR_KW_170'],
        act_gelvr_kw_270 = record['ACT_GELVR_KW_270'],
        verbr_gas_2421 = record['VERBR_GAS_2421']
    )

    # save
    recordInstance.save()

def funGetUtcTime():
	now = datetime.utcnow()
	return int((now - datetime(2000, 1, 1)).total_seconds()) # the number of seconds since 2000-01-01

def funCleanDigitStr(str_in):
    str_out = re.sub(r'[^-.0-9]', '', str_in)
    if len(str_out) == 0:
        return const.NOT_SET
    else:
        return str_out

def funOpenSerial():
    global ser1
    while True:
        try:
            ser1.open()
            break
        except Exception as e:
            print(": serial port niet te openen ("+ser1.port+") is de USB serial kabel aangesloten? melding:"+str(e.args)+"  retry in 60 seconden.")
            time.sleep(60)

def funRecordSanityCheck(record):
    verbr_kwh_181 = record['VERBR_KWH_181']
    verbr_kwh_182 = record['VERBR_KWH_182']
    gelvr_kwh_281 = record['GELVR_KWH_281']
    gelvr_kwh_282 = record['GELVR_KWH_282']
    tarief_code = record['TARIEFCODE']
    act_verbr_kw_170 = record['ACT_VERBR_KW_170']
    act_gelvr_kw_270 = record['ACT_GELVR_KW_270']
    verbr_gas_2421 = record['VERBR_GAS_2421']

    recordIsOk = True

    if gas_present_in_serial_data == True:
        if verbr_gas_2421 == -999:
            print(": Gefaald op gas verbruikt (24.2.1), waarde was "+str(verbr_gas_2421))
            recordIsOk = False

    if verbr_kwh_181 == -999:
        print(": Gefaald op dal/nacht voor verbruikte energie(1.8.1), waarde was "+str(verbr_kwh_181))
        recordIsOk = False

    if verbr_kwh_182 == -999:
        print(": Gefaald op piek/dag voor verbruikte energie(1.8.2), waarde was "+str(verbr_kwh_182))
        recordIsOk = False

    if gelvr_kwh_281 == -999:
        print(": Gefaald op dal/nacht  voor geleverde energie(2.8.1), waarde was "+str(gelvr_kwh_281))
        recordIsOk = False

    if gelvr_kwh_282 == -999:
        print(": Gefaald op piek/dag voor geleverde energie(2.8.2), waarde was "+str(gelvr_kwh_282))
        recordIsOk = False

    if tarief_code  != 'P' and tarief_code  != 'D':
        print(": Gefaald op tariefcode, verwachte P of D, waarde was "+str(tarief_code))
        recordIsOk = False

    if act_verbr_kw_170 == -999:
        print(": Gefaald op actueel verbruikt vermogen, waarde was "+str(act_verbr_kw_170))
        recordIsOk = False

    if act_gelvr_kw_270 == -999:
        print(": Gefaald op actueel geleverd vermogen, waarde was "+str(act_gelvr_kw_270))
        recordIsOk = False

    # expected format of fields
    if gas_present_in_serial_data == True:
        if len(str(verbr_gas_2421)) < 8 or len(str(verbr_gas_2421)) > 12:
            print(": Gefaald op gas verbruikt (24.2.1) (lengte), waarde was "+str(verbr_gas_2421))
            recordIsOk = False

    if len(str(verbr_kwh_181)) < 9 or len(str(verbr_kwh_181)) > 10:
        print(": Gefaald op dal/nacht format (1.8.1) (lengte), waarde was "+str(verbr_kwh_181))
        recordIsOk = False

    if len(str(verbr_kwh_182)) < 9  or len(str(verbr_kwh_182)) > 10:
        print(": Gefaald op piek/dag format (1.8.2) (lengte), waarde was "+str(verbr_kwh_182))
        recordIsOk = False

    if len(str(gelvr_kwh_281)) < 9  or len(str(gelvr_kwh_281)) > 10:
        print(": Gefaald op dal/nacht format (2.8.1) (lengte), waarde was "+str(gelvr_kwh_281))
        recordIsOk = False

    if len(str(gelvr_kwh_282)) < 9 or len(str(gelvr_kwh_282)) > 10:
        print(": Gefaald op piek/dag format (2.8.2) (lengte), waarde was "+str(gelvr_kwh_282))
        recordIsOk = False

    if len(str(act_verbr_kw_170)) < 6 or len(str(act_verbr_kw_170)) > 7:
        print(": Gefaald op actueel verbruikt vermogen format (1.7.0) (lengte), waarde was "+str(act_verbr_kw_170))
        recordIsOk = False
    
    if len(str(act_gelvr_kw_270)) < 6 or len(str(act_gelvr_kw_270)) > 7:
        print(": Gefaald op actueel geleverd vermogen format (2.7.0) (lengte), waarde was "+str(act_gelvr_kw_270))
        recordIsOk = False

    return recordIsOk    

def parseSerBuffer():
    global serial_buffer
    global gas_present_in_serial_data
    gas_present_in_serial_data = False 

    # preallocate record
    record = {}
    record['TIMESTAMP'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record['VERBR_KWH_181'] = -999
    record['VERBR_KWH_182'] = -999
    record['GELVR_KWH_281'] = -999
    record['GELVR_KWH_282'] = -999
    record['TARIEFCODE'] = -999
    record['ACT_VERBR_KW_170'] = -999
    record['ACT_GELVR_KW_270'] = -999
    record['VERBR_GAS_2421'] = -999

    # loop through serial buffer
    while len(serial_buffer) > 0:
        # pop line (take line out of buffer list)
        line = serial_buffer.pop(0)

        # we don't do empty lines
        if len(line) < 1: 
            continue
        try:
            # split line
            lineSplit = line.split('(')

            # parse
            if len(lineSplit) < 2: # verwijder velden die niet interessant zijn
                continue 
            elif lineSplit[0] == '0-0:96.1.1': # verwijder slimme meter header 
                continue
            elif lineSplit[0] == '0-'+str(gas_record_prefix_number)+':24.2.1':
                content = lineSplit[2].split(')')
                content = content[0].split('*')
                record['VERBR_GAS_2421'] = funCleanDigitStr(content[0])
            elif lineSplit[0] == '0-'+str(gas_record_prefix_number)+':24.3.0':
                line_tmp = serial_buffer.pop(0)
                buf_tmp =  line_tmp.split('(')
                record['VERBR_GAS_2421'] = funCleanDigitStr(buf_tmp[1])
            elif lineSplit[0] == '1-0:1.8.1': 
                content = lineSplit[1].split('*') 
                record['VERBR_KWH_181'] = funCleanDigitStr(content[0])
            elif lineSplit[0] == '1-0:1.8.2': 
                content = lineSplit[1].split('*') 
                record['VERBR_KWH_182'] = funCleanDigitStr(content[0])
            elif lineSplit[0] == '1-0:2.8.1': 
                content = lineSplit[1].split('*') 
                record['GELVR_KWH_281'] = funCleanDigitStr(content[0])
            elif lineSplit[0] == '1-0:2.8.2': 
                content = lineSplit[1].split('*') 
                record['GELVR_KWH_282'] = funCleanDigitStr(content[0])
            elif lineSplit[0] == '1-0:1.7.0':
                content = lineSplit[1].split('*') 
                record['ACT_VERBR_KW_170'] = funCleanDigitStr(content[0])
            elif lineSplit[0] == '1-0:2.7.0':
                content = lineSplit[1].split('*')
                record['ACT_GELVR_KW_270'] = funCleanDigitStr(content[0])
            elif lineSplit[0] == '0-0:96.14.0':    
                content = lineSplit[1].split(')')
                record['TARIEFCODE']=funCleanDigitStr(content[0])

            # overwrite tarief_code
            if record['TARIEFCODE'] == '0002':
                record['TARIEFCODE'] = 'P'
            if record['TARIEFCODE'] == '0001':
                record['TARIEFCODE'] = 'D'
            
        except Exception as e:
            print(": fout in P1 data. Regel="+\
            line+" melding:"+str(e.args[0]))
    
    # return
    return record
        

# preallocate
serial_interval = 9         # sec # 9 or 10 sec interval is ok.
serial_buffer = []
gas_present_in_serial_data = False 
timestamp_last_insert = funGetUtcTime()
p1_record_is_ok = 1
gas_record_prefix_number = '1'
p1_crc_check_is_on = True
# system_id = systemid.getSystemId()
last_crc_check_timestamp = 0
crc_error_cnt = 0

# serial port config
ser1 = srl.Serial()
ser1.baudrate = 115200
ser1.bytesize=srl.EIGHTBITS
ser1.parity=srl.PARITY_NONE
ser1.stopbits=srl.STOPBITS_ONE
ser1.xonxoff = 0
ser1.rtscts = 0 
ser1.timeout = 1 
ser1.port="/dev/ttyUSB0"

# try to open serial connection (with loop)
funOpenSerial()

# open sqlite data base
db_serial = sqlite3.connect('/home/p1mon/p1mon/serialdata/serialdata.db')
cur_serial = db_serial.cursor()

# loop read serial connection
while True:
    # if data is waiting to be read
    try:
        if ser1.in_waiting > 1:
            # read serial port
            try:
                line = ser1.readline().decode('utf-8')
                serial_buffer.append(line)
            except:
                print(": lezen van serieele poort mislukt.")
            
            #the benthouse BUG has 78 lines
            if len(serial_buffer) > 250: # normal size less then a 100 lines
                print(": serieele buffer te groot, gewist! Buffer lengte was "+str(len(serial_buffer)))
                del serial_buffer[:]

            # the last line of a record starts with '!'
            if line[:1] == '!':
                # rate limitingen of inserts, some smart meters send more then every 10 sec. a telegram.
                if abs(timestamp_last_insert - funGetUtcTime()) < serial_interval: 
                    del serial_buffer[:]
                    continue

                # check for meters that supply a crc value.
                if len(serial_buffer[len(serial_buffer)-1]) > 3 and p1_crc_check_is_on == True: # crc telegrams are 7 chars minimal (5+ cr\lf)

                    # check for telegrams with a CRC attached 
                    crc_read = str(serial_buffer[len(serial_buffer)-1][1:5])
                    save_crc = serial_buffer[len(serial_buffer)-1]
                    serial_buffer[len(serial_buffer)-1] = '!' # only process to ! not the crc itself
                    strvar = ''.join(serial_buffer)
                    calc_crc = str('{0:0{1}X}'.format(CRC16().calculate(strvar),4))

                    if (crc_read==calc_crc):
                        #restore CRC to received data
                        serial_buffer[len(serial_buffer)-1] = save_crc
                    else:
                        crc_error_cnt = crc_error_cnt+1
                        #flog.debug("CRC van telegram komt niet overeen. CRC telegram ("+crc_read+"), berekende CRC ("+calc_crc+") niet verwerkt.")
                        del serial_buffer[:]
                        continue
                
                # get record, i.e. parse serial buffer
                record = parseSerBuffer()

                # make sure the buffer is clean after parsing
                del serial_buffer[:]

                # check sanity of record
                recordSanity = funRecordSanityCheck(record)

                # if sane, commit
                if recordSanity == True:
                    # recordText = "%s" % str(record)
                    # print(recordText)
                    # funCommitRecord(record=record,db=db_serial,cur=cur_serial,table='serialdata_seriallive')
                    funCommitRecord(record=record)
                    timestamp_last_insert = funGetUtcTime()

        else:
            time.sleep(1)

            # serial check
            # serCheckCnt = serCheckCnt+1
            # if serCheckCnt > 30: 
            #      # do check
            #     print("serial interval check")
            #     checkSerSettings()
            #     checkGasTelgramPrefix()

            #     # read crc check settings from config
            #     checkCRCsettings()

            #     # reset counter
            #     serCheckCnt=0
            
            # set p1 connection working/not working on website
            if abs(timestamp_last_insert - funGetUtcTime()) > 51: # 51 secs (are 5 telegrams)
                #print "P1 data to late!"
                if p1_record_is_ok == 1:
                    print(": geen P1 record te lezen.")
                p1_record_is_ok = 0
            
            #crc error messages, if any.
            if p1_crc_check_is_on == True:
                if abs(last_crc_check_timestamp - funGetUtcTime()) > 900:  #check every 15 minutes, to limit log entries.
                    last_crc_check_timestamp = funGetUtcTime()
                    if crc_error_cnt > 0:
                        print("aantal P1 telegram crc fouten gevonden in de afgelopen minuut = " + str(crc_error_cnt))
                        crc_error_cnt = 0
            
    except Exception as inst:
        print(": fout bij het wachten op seriele gegevens. Error="+str(inst))
        time.sleep(1)
