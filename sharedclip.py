import pyperclip as cb
import socket
import threading
import sys
import time
from rich import print

IP = sys.argv[1].strip()
SERVER_PORT = 9898
client_connected = False
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_clipboard = ""


# Bi-directional channel to send and receive data
# Or a seperate port for sending and receiving

def sendClipboardData(data):
	global client,my_clipboard
	try:
		my_clipboard = data
		client.sendall(data.encode())
		print("[bold blue]Sent clipboard data[/bold blue]")
	except Exception as e:
		print("[red]Exception while trying to send data :pile_of_poo: : \n%s\n[/red]"%e)
		


# Start the server and listen on a different thread

def serverThread():
	global server, IP, SERVER_PORT, client_connected, my_clipboard
	try:
		
		server.bind(('',SERVER_PORT))
		print("[yellow]Server up and waiting for connections. :thumbs_up:[/yellow]")
		server.listen()
		conn, addr = server.accept()
		with conn:
			print("[yellow]Connection received from : [/yellow]",addr)
			client_connected = True
			while True:
				data = conn.recv(1024)
				print(data)
				# print(addr[0]+": "+data.decode("utf-8"))
				print("[green]Received :smiley:[/green]")
				# data = data.decode("utf-8")
				if data.decode("utf-8")!=my_clipboard:
					cb.copy(data.decode("utf-8"))
				if not data:
				    break

				if data.decode("utf-8")=="^^enD^^":
					client_connected = False
					print("[yellow]Client left the channel :raccoon:[/yellow]")



	except Exception as e:
		print("[red]Exception occured in server thread :pile_of_poo: - \n%s\n[/red]"%e)




def main():
	global client, IP,SERVER_PORT,client_connected
	server_thread = threading.Thread(target=serverThread,args=(),daemon=True)
	server_thread.start()

	# Try connecting as client
	while 1:
		try:
			client.connect((IP,SERVER_PORT))
			print("[yellow]Connected as client. :smiley:[/yellow]\n")
			break
		except Exception as e:
			print("[yellow]Couldn't connect as client, trying again in 5 secs..[/yellow]")
			time.sleep(5)



	while not client_connected:
		continue


	print("[magenta]Listening clipboard activity now. :thumbs_up:[/magenta]\n")
	while 1:
		data = "No data in clipboard"
		if cb.paste()=="" or cb.paste()==None:
			data = cb.waitForPaste()
		else:
			data = cb.waitForNewPaste()

		if client_connected:
			sendClipboardData(data)
		else:
			print("[red]No client to send data.[/red]")
			sys.exit(0)





if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Closing program..")
		sendClipboardData("^^enD^^")