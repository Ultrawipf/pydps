import minimalmodbus, serial

# Example Usage:
# import pydps
# dps = pydps.dps_psu('COM3', 1) # port name, slave address
# print(dps.getModel())
# print(dps.getVoltage())


class dps_psu(minimalmodbus.Instrument):

    def __init__(self, portname, slaveaddress):
            minimalmodbus.Instrument.__init__(self, portname, slaveaddress,mode='rtu')
            self.serial.baudrate = 9600
            self.serial.bytesize = 8
            self.serial.parity   = serial.PARITY_NONE
            self.serial.stopbits = 1
            self.serial.timeout  = 1
    def setVoltage(self,volt):
        self.write_register(0x0000,volt,2)
 
    def setCurrent(self,curr):
        self.write_register(0x0001,curr,3)

    def getVoltage(self):
        return self.read_register(0x0002,2)

    def getCurrent(self):
        return self.read_register(0x0003,2)

    def getPower(self):
        return self.read_register(0x0004,2)

    def getInputVoltage(self):
        return self.read_register(0x0005,2)

    def setKeyLock(self, lock):
        self.write_register(0x0006,(1 if lock else 0),0)
 
    def getProtection(self):
        return self.read_register(0x0007,2)

    def getCVCC(self):
        return self.read_register(0x0008,2)
 
    def setOutput(self,on):
        self.write_register(0x0009,(1 if on else 0),0)

    def setBackLight(self,level):
        self.write_register(0x000A,level,2)

    def getModel(self):
        return self.read_register(0x000B,2)

    def getFwVersion(self):
        return self.read_register(0x000C,2)

    def getOverVoltageProtection(self):
        return self.read_register(0x0052,2)

    def setOverVoltageProtection(self,level):
        self.write_register(0x0052,level,2)

    def getOverCurrentProtection(self):
        return self.read_register(0x0053,2)

    def setOverCurrentProtection(self,level):
        self.write_register(0x0053,level,3)

    def getOverPowerProtection(self):
        return self.read_register(0x0054,1)

    def setOverPowerProtection(self,level):
        self.write_register(0x0054,level,1)

    def setById(self, name, value):
        if name == 'u-set':
            self.setVoltage(value)
        elif name == 'i-set':
            self.setCurrent(value)
        elif name == 'on':
            self.setOutput(value)
        elif name == 'lock':
            self.setKeyLock(value)
        elif name == 'b-led':
            self.setBackLight(value)
        elif name == 's-ovp':
            self.setOverVoltageProtection(value)
        elif name == 's-ocp':
            self.setOverCurrentProtection(value)
        elif name == 's-opp':
            self.setOverPowerProtection(value)
        else:
            print("not a valid Id.")
            exit()

    # Read all interesting status registers at once
    def getFullData(self):
        buf = self.read_registers(0x00,87)
        dat = {"u-set" : buf[0]*0.01,
               "i-set": buf[1]*0.001,
               "u-out":round(buf[2]*0.01,2),
               "i-out":round(buf[3]*0.001,3),
               "power":round(buf[4]*0.01,2),
               "u-in":buf[5]*0.01,
               "lock":buf[6],
               "protect":buf[7],
               "cvcc":buf[8],
               "on":buf[9],
               "b-led":buf[10],
               "model":buf[11],
               "fw-version":str(buf[12] / 10.0),
               "s-ovp":buf[82]*0.01,
               "s-ocp":buf[83]*0.001,
               "s-opp":buf[84]}
        return dat
