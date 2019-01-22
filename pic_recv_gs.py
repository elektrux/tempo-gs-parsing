import socket, re, io
from PIL import Image

datacount = 0
packetcount = 0
firstPacket = True
buildingData = False
readyToEnd = False
alldata = []

while True:
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serversocket.bind((socket.gethostname(), 4000))
	serversocket.listen(5)
	while True:
		connection, client_address = serversocket.accept()
		print('Connected')

		while True:
			IPData = bytes(connection.recv(36)).encode('hex') #bytearray?s
			CANData = re.findall('..', IPData[56:])
			print('can data')
			print(CANData)

			packet = []
			for byte in CANData:
				try:
					if not byte == "":
						packet.append(int(byte, 16))
						if (packet[0] == 0):
							buildingData = True
						if (packet[0] == 1 and buildingData):
							readyToEnd = True
						if (buildingData):
							print('Building data.')
							alldata.append(int(byte, 16))
							datacount += 1
						
				except ValueError as e:
					print("Error message: " + str(e))

			print("packet")
			print(packet)
			if (buildingData and readyToEnd):
				packetcount+=1

				if packet[0] == 0:
					print("Got " + str(packetcount) + " bytes of data")
					print("Should have sent: " + str(datacount) + " bytes of data")

					print("RECV: Listener stopped.")
					alldata = bytearray(alldata)
					image = Image.open(io.BytesIO(alldata))
					image.save("recvPic.jpg")

					connection.close()
					break
				if firstPacket:
					print("First Packet")
					print(packet)
					firstPacket = False



