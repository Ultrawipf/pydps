import pydps,time

# dps Test Example
dps = pydps.dps_psu('COM11', 1) # port name, slave address (in decimal)

#make a csv like measurement
def measureSteps(start,stop,step):

    with open('results.csv', 'a') as csv: # open csv file and append
        for v in range(int(start*1000),int((step+stop)*1000),int(step*1000)):
            dps.setVoltage(v*0.001)
            time.sleep(0.5) #wait for stable voltage
            dat=dps.getFullData()
            print(str(dat['u-out'])+"V, "+str(dat['i-out'])+"A")
            csv.write(str(dat['u-out']) + ',' + str(dat['i-out'])+"\n")


def main():
    with open('results.csv', 'w') as csv:
        csv.write("u-out,i-out\n")

    dps.setKeyLock(True)
    print(dps.getModel())

    dps.setVoltage(0)
    dps.setOutput(True)
    measureSteps(start=0,stop=15,step=0.25)

    dps.setOutput(False)
    dps.setKeyLock(False)

    print("Finished")

if __name__ == "__main__":
    main()
