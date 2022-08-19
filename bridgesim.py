from bridge import *
		
class Extended_LAN:
	def __init__(self,dictionary):
		self.bridge_network = dictionary				# dictionary a dict with Bridges as keys and LANs they are connected to as values 
		self.lan_network = {}
		for key in dictionary.keys():					# bridge network - info about which LANs it is connected to  { 1: ['A','B'], 2: ['C','D'] }
			for v in dictionary[key]:
				if v in self.lan_network.keys():		# lan network - info about which bridges the Lan is connected to { 'A':[1],'B':[1],'C':[2] ..}
					self.lan_network[v].append(key) 
				
				else:
					self.lan_network[v] = [key]
		

class bridgesim:
	def __init__(self,tr,n,data):
		self.graph  = Extended_LAN(data)
		self.bridges = []
		self.trace_flag = tr
		self.no_of_bridges = n

		obj = bridge(-1,[])
		list_obj = [obj.__class__ for i in range(n)]
		
		i=0
		for key in data.keys():
			self.bridges.append(list_obj[i](key,data[key]))
			i+=1

		self.timestamp = 0

	def transmission(self):
		# Which bridges to transmit the message
		
		for b in range(self.no_of_bridges):								# b is  a bridge
			self.bridges[b].empty_receive_buffer()						# empty receive buffer before new messages come

		for b in range(self.no_of_bridges):								# b is a bridge
			send_list = []
		
			for l in self.graph.bridge_network[b+1]:					# l is for LAN
				if self.bridges[b].connection_status[l] == 'DP':
					bridge_list = self.graph.lan_network[l]				# bridges LAN is connected to through RP and DP
					for i in bridge_list:  								
						if self.bridges[i-1].connection_status[l] != 'NP':	# Checking if LAN - bridge is NP or not
							send_list.append((i,l))  
							
			#send_list = list(set(send_list))
			send_list = [value for value in send_list if value[0]!=b+1] 										# list of bridges, b sends messages to
			
			for bridge in send_list:
				
				self.bridges[bridge[0]-1].receive_buffer.append((self.bridges[b].send_buffer,bridge[1]))    			# Transferring b's message in bridges recieve buffer which lan it came through
					

		
		# transmission over
	def display_output(self):

		for i in range(self.no_of_bridges):
			print('B'+str(self.bridges[i].bridge_id)+':',end=' ')
			for key in self.bridges[i].connection_status.keys():
				print(key+"-"+self.bridges[i].connection_status[key],end=" ")

			print()	

	def simulateSTP(self):
		# main loop
		
		while True:

			flag = 1													# determines if same messages are getting transmitted, helps in ending the loop 
			
			# display trace just before sending
			if self.trace_flag == 1:
				for bridge in self.bridges:
					print(self.timestamp,'s','B'+str(bridge.bridge_id),bridge.send_buffer.send_message())


			# transmission
			self.transmission()
			
			self.timestamp += 1

			# display trace just after receiving
			if self.trace_flag == 1:
				for bridge in self.bridges:
					for i in range(len(bridge.receive_buffer)):
						print(self.timestamp,'r','B'+str(bridge.bridge_id),bridge.receive_buffer[i][0].send_message())
				
			# Finding the best message out of all the received messages and the send buffer
			for bridge in self.bridges:
				msg = bridge.received_processing()
				#print(msg.send_message())
				#print(bridge.send_buffer.send_message())
				if msg.send_message() != bridge.send_buffer.send_message():
					flag = flag*0
					#print(flag)											# checking if the message is same as last one transmitted

				
				bridge.send_processing(msg)								# sending the best message to send buffer


			# if all messages are same then end the loop
			if flag ==1:
				break
		
			


# main program
tr = int(input())
n = int(input())
data = {}
for i in range(n):
	s = input().split()
	data[int(s[0][1:-1])] = sorted(s[1:])

tree = bridgesim(tr,n,data)

tree.simulateSTP()
tree.display_output()
