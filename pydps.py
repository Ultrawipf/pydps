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
            self.serial.timeout  = 0.5

    def getVoltage(self):
        return self.read_register(0x0002,2)

    def getCurrent(self):
        return self.read_register(0x0003,3)

    def getPower(self):
        return self.read_register(0x0004,2)

    def setVoltage(self,volt):
        self.write_register(0x0000,volt,2)

    def setCurrent(self,curr):
        self.write_register(0x0001,curr,3)

    def setOutput(self,on):
        self.write_register(0x0009,(1 if on else 0),0)

    def getInputVoltage(self):
        return self.read_register(0x0005,2)

    def getFwVersion(self):
        return self.read_register(0x000C,0)

    def getModel(self):
        return self.read_register(0x000B,0)

    def setKeyLock(self, lock):
        self.write_register(0x0006,(1 if lock else 0),0)

    # Read all interesting status registers at once
    def getFullData(self):
        buf = self.read_registers(0x00,10)
        dat = {"u-set" : buf[0]*0.01, "i-set": buf[1]*0.001, "u-out":round(buf[2]*0.01,2), "i-out":round(buf[3]*0.001,3), "power":round(buf[4]*0.01,2), "u-in":buf[5]*0.01, "lock":buf[6], "protect":buf[7], "cvcc":buf[8],"on":buf[9]}
        return dat
