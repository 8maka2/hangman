from bluepy.btle import Scanner, Peripheral
import signal
import struct
import time

scanner = Scanner()
devices = scanner.scan(3)
addr = None

for d in devices:
		for (adtype, desc, value) in d.getScanData():
			if adtype == 9 and value == 'CC2650 SensorTag':
				print('SensorTag: {}, RSSI: {}db'.format(d.addr, d.rssi))
				addr = d.addr

tag = Peripheral(addr)
service = tag.getServiceByUUID('F000AA20-0451-4000-B000-000000000000')
data = service.getCharacteristics('F000AA21-0451-4000-B000-000000000000')[0]
conf = service.getCharacteristics('F000AA22-0451-4000-B000-000000000000')[0]

conf.write(b'\x01', withResponse=True)
time.sleep(1)

raw_data = data.read()
print(raw_data)
raw_temp, raw_humid = struct.unpack('<HH', raw_data)
temp = -40.0 + 165.0 * (raw_temp / 65336.0)
print(temp)
