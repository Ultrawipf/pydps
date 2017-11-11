import pydps,time

# dps Test Example

def main():
    dps = pydps.dps_psu('COM3', 1) # port name, slave address (in decimal)
    print(dps.getModel())
    print(dps.getFullData())
    dps.setVoltage(0)
    dps.setOutput(True)
    for v in range(0,1400,50):
        dps.setVoltage(v*0.01)
        time.sleep(0.25) #wait for stable voltage
        dat=dps.getFullData()
        print(str(dat["i-out"]) + 'A ' + str(dat['u-out']) + 'V')
    dps.setOutput(False)


if __name__ == "__main__":
    main()
