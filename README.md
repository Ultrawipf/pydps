# pydps
A small helper library using minimalmodbus for the popular dps5005 power supply modules

Dependencies:
minimalmodbus and serial

Example Usage:

  import pydps

  dps = pydps.dps_psu('COM3', 1) # port name, slave address

  print(dps.getModel()) #Should show 5005 for dps5005
  print(dps.getVoltage()) #returns the measured output voltage
  print(dps.getCurrent()) #Prints measured output current in A

  #or get the full dataset at once:
  dat = dps.getFullData()
  #Contained values: u-set, i-set, u-out, i-out, power, u-in, lock, protect, cvcc, on
  print(dat["power"]) #Prints measured power in W
  print(dat["i-out"]) #Prints measured output current in A
