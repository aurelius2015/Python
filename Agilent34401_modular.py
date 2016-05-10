#Agilent 34401 instrument control program
#Author: DP (aurelius2015)
#Date: 2015-08-15

import visa
import re
import time
import datetime

# Functions
def visaResourceManager():
    rema = None
    try:
        rema = visa.ResourceManager()
        #print ("Found resources are: ", rema.list_resources())
    except:
        print ("Please make sure that VISA Resource Manager is installed on the PC")
        print ("Please turn on the instrument, check PC and RS232 connection.")
    else:
        return (rema)

def instrument_open(rm):
    DMM = None
    try:
        DMM = rm.open_resource(Serial_address)
        print ("Instrument detected: " + DMM.query("*IDN?").rstrip())
    except:
        print ("instrument_open not done")
        print ("Please turn on the instrument and check RS232 connection.")
    else:
        return (DMM)

def system_remote(DMM):
    try:
        DMM.write("syst:remote")
        time.sleep(1)
    except:
        print ("syst:remote not done")
        print ("Please turn on the instrument and check RS232 connection.")
    finally:
        return ("Exiting system_remote(DMM)...")

def error_buffer_clearing(DMM):
    try:
        Noerror = "+0,\"No error\"\r\n"
        while (DMM.query("system:error?") != Noerror):
            DMM.query("system:error?")
    except:
        print ("error_buffer_clearing not done")
        print ("Please turn on the instrument and check RS232 connection.")
    finally:
        return ("Exiting error_buffer_clearing(DMM)...")
              
#DMM.write("SYSTem:BEEPer:STATe OFF")
#time.sleep(1)
#DMM.write("SYSTem:BEEPer:STATe ON")

def create_logfile():
    filehandle = None
    try:
        filename = datetime.datetime.now().strftime("AG34401_Measure_%Y%m%d%H%M%S.csv")
        filehandle = open(filename, 'w')
        print ("The datalog file name created: " + filename)
    except:
        print ("Dead meat")
    else:
        return (filehandle)

def create_column_header(filehandle):
    try:
        cHeader = "Time,AG34401 DC Voltage"
        print (cHeader)
        filehandle.write (cHeader+"\n")
    except:
        print ("create_column_header not done")
        print ("Please check PC.")
    finally:
        return ("Exiting create_column_header(fhandle)...")

def data_acquisition(filehandle):
    try:
        for i in range(3):
            VDC = re.sub ("\r\n", "", DMM.query(SCPI_VDC))
            #today = datetime.datetime.now()
            #print(datetime.datetime.now().ctime() + "," + VDC)
            #print(strftime("%Y-%m-%d %H:%M:%S,") + VDC)
            results = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f,") + VDC
            print (results)
            filehandle.write (results+"\n")
    except:
        print ("data_acquisition not done")
        print ("Please check PC or the DMMrument or cable.")
    finally:
        return ("Exiting data_acquisition(fhandle)...")

def close_file(filehandle):
    try:
        filehandle.close()
    except:
        print ("close_file not done")
        print ("Please check PC.")
    finally:
        return ("Exiting close_file(fhandle)...")

def system_local(DMM):
    try:
        DMM.write("syst:local")
    except:
        print ("system_local not done")
        print ("Please check PC or the instrument or cable.")
    finally:
        return ("Exiting system_local(DMM)...")

def close_instrument(DMM):
    try:
        DMM.close()
    except:
        print ("close_instrument not done")
        print ("Please check PC or the instrument or cable.")
    finally:
        return ("Exiting close_instrument(DMM)...")

# Main Program
Serial_address = 'ASRL7::INSTR'
SCPI_VDC = 'measure:volt:dc?'
#SCPI_Res = 'measure:resistance?'
rema = visaResourceManager()
DMM = instrument_open(rema)
system_remote(DMM)
error_buffer_clearing(DMM)
filehandle = create_logfile()
create_column_header(filehandle)
data_acquisition(filehandle)
close_file(filehandle)
system_local(DMM)
close_instrument(DMM)
