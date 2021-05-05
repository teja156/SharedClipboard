import pyperclip as cb
import socket
import threading
import sys
import time


IP = sys.argv[1].strip()
SERVER_PORT = 9898


# Bi-directional channel to send and receive data
# Or a seperate port for sending and receiving

def sendClipboardData(data):
	global client
	client.sendall(data.encode())


# Start the server and listen on a different thread

def serverThread():
	global IP, SERVER_PORT
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(('',SERVER_PORT))
		print("Server up and waiting for connections.")
		server.listen()
		conn, addr = server.accept()
		with conn:
			print("Connection received from : ",addr)
			while True:
				data = conn.recv(1024)
				print(addr[0]+": "+data.decode("utf-8"))
				if not data:
				    break


	except Exception as e:
		print("Exception occured - %s"%e)



server_thread = threading.Thread(target=serverThread,args=(),daemon=True)
server_thread.start()




# Try connecting as client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while 1:
	try:
		client.connect((IP,SERVER_PORT))
		print("Connected as client.\n")
		break
	except Exception as e:
		print("Couldn't connect as client, trying again in 5 secs..")
		time.sleep(5)

print("Listening clipboard activity now.\n")
while 1:
	data = "No data in clipboard"
	if cb.paste()=="" or cb.paste()==None:
		data = cb.waitForPaste()
	else:
		data = cb.waitForNewPaste()


	if data=="clipboard":
		continue

	sendClipboardData(data)