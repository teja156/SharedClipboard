#! /usr/bin/python3


import pyperclip as cb
import socket
import threading
import sys
import time
from rich import print
import argparse


# Parse arguments

parser = argparse.ArgumentParser(description='Share clipboard between two devices in a network')
parser.add_argument('-c',metavar='Connection',action='store',type=str,help='IPAddress/hostname of the other device',required=True)
parser.add_argument('-v','--verbose',action='store_true',help='enable verbose mode')
args = parser.parse_args()
IP = args.c
verbose = args.verbose

print("[yellow][*][/yellow]Remote host: ",IP)
print("[yellow][*][/yellow]Verbose: ",verbose)
print()


SERVER_PORT = 9898
client_connected = False
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_clipboard = ""


# Bi-directional channel to send and receive data
# Or a seperate port for sending and receiving

def sendClipboardData(data):
	global client,my_clipboard,verbose
	try:
		my_clipboard = data
		client.sendall(data.encode())
		if verbose:
			# print("Sent : ",data.encode())
			print("[blue][+][/blue]Sent clipboard data")
	except Exception as e:
		print("\n[red][-][/red]Exception while trying to send data :pile_of_poo: : [red]\n%s\n[/red]"%e)
		


# Start the server and listen on a different thread

def serverThread():
	global server, IP, SERVER_PORT, client_connected, my_clipboard, verbose
	try:
		
		server.bind(('',SERVER_PORT))
		print("[bold blue][*][/bold blue]Server up and waiting for connections. :thumbs_up:")
		server.listen()
		conn, addr = server.accept()
		with conn:
			print("[yellow][*][/yellow]Connection received from : ",addr[0])
			client_connected = True
			while True:
				data = conn.recv(1024)
				if verbose:
					print("[green][+][/green]Received clipboard data :smiley:")
					# print(addr[0]+": "+data.decode("utf-8"))

				# print("My clipboard: ",my_clipboard)
				if data.decode("utf-8").strip()!=my_clipboard:
					cb.copy(data.decode("utf-8"))
					my_clipboard = data.decode("utf-8").strip()
					# print("Copied recieved data to clipboard")
				if not data:
				    break

				if data.decode("utf-8")=="^^enD^^":
					client_connected = False
					print("\n[yellow][!][/yellow]Client left the channel :raccoon:\n")



	except Exception as e:
		print("\n[red][-][/red]Exception occured in server thread :pile_of_poo: - [red]\n%s\n[/red]"%e)




def main():
	global client, IP,SERVER_PORT,client_connected, my_clipboard, verbose
	server_thread = threading.Thread(target=serverThread,args=(),daemon=True)
	server_thread.start()

	# Try connecting as client
	while 1:
		try:
			client.connect((IP,SERVER_PORT))
			print("[bold blue][+][/bold blue]Connected as client. :smiley:")
			break
		except Exception as e:
			print("[yellow][!][/yellow]Couldn't connect as client, trying again in 5 secs..")
			time.sleep(5)

	while not client_connected:
		continue


	print("\n[bold magenta][*]OK. Clipboard is now shared. :thumbs_up:[/bold magenta]\n")
	while 1:
		data = "No data in clipboard"
		if cb.paste()=="" or cb.paste()==None:
			data = cb.waitForPaste()
		else:
			data = cb.waitForNewPaste()



		if not client_connected:
			print("[red][-][/red]No client to send data.")
			sys.exit(0)

		if client_connected and my_clipboard!=data and data!="":
			sendClipboardData(data)
			





if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Closing program..")
		sendClipboardData("^^enD^^")