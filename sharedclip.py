import pyperclip as cb
import socket
import threading
import sys
import time


IP = sys.argv[1].strip()
SERVER_PORT = 9898
client_connected = False

# Bi-directional channel to send and receive data
# Or a seperate port for sending and receiving

def sendClipboardData(data):
	global client
	try:
		client.sendall(data.encode())
		print("Sent clipboard data")
	except Exception as e:
		print("Exception while trying to send data: \n%d\n"%e)
		


# Start the server and listen on a different thread

def serverThread():
	global IP, SERVER_PORT, client_connected
	try:
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind(('',SERVER_PORT))
		print("Server up and waiting for connections.")
		server.listen()
		conn, addr = server.accept()
		with conn:
			print("Connection received from : ",addr)
			client_connected = True
			while True:
				data = conn.recv(1024)
				print(addr[0]+": "+data.decode("utf-8"))
				if not data:
				    break

				if data.decode("utf-8")=="^^enD^^":
					client_connected = False
					print("Client left the channel")



	except Exception as e:
		print("Exception occured - %s"%e)




def main():
	global IP,SERVER_PORT,client_connected
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



	while not client_connected:
		continue


	print("Listening clipboard activity now.\n")
	while 1:
		data = "No data in clipboard"
		if cb.paste()=="" or cb.paste()==None:
			data = cb.waitForPaste()
		else:
			data = cb.waitForNewPaste()


		if data=="clipboard":
			continue

		if client_connected:
			sendClipboardData(data)
		else:
			print("No client to send data.")
			sys.exit(0)





if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Closing program..")
		sendClipboardData("^^enD^^")