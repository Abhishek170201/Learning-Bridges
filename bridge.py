class config_message:
	def __init__(self,root,d,sender):
		
		self.root_bridge = root
		self.dist = d
		self.sender_bridge = sender

	def send_root_bridge(self):
		return self.root_bridge

	def send_dist(self):
		return self.dist

	def send_sender_bridge(self):
		return self.sender_bridge

	def send_message(self):
		return ('B'+str(self.root_bridge),self.dist,'B'+str(self.sender_bridge))


class bridge:

	def __init__(self,bridge_number,connection):
		self.bridge_id = bridge_number									# bridge id is a number  B1 - 1, B2 - 2 ...
		self.connected_LANs = connection 										# connection is an array having names of LANs the bridge is connected to
		self.connection_status = {} 											# stores the info about port status
		self.send_buffer = config_message(self.bridge_id,0,self.bridge_id)		# initialisation message in send buffer
		self.receive_buffer = []												# receive buffer is an array of config message objects
		self.generate_config_message = True										# indicates if the bridge is root or not

		for lan in connection:
			self.connection_status[lan] = 'DP'									# initializing all ports as DP

	def empty_receive_buffer(self):
		self.receive_buffer = []												# required after every time-step

	def received_processing(self):
		# Implementation of finding the best message

		best_msg = self.send_buffer



		for i in range(len(self.receive_buffer)):  
			# i represents a LAN connection
			# Determining best message among all the messages and changing the status

			msg = self.receive_buffer[i][0]
			msg_change_flag = 1
			# Rule 1
			if msg.send_root_bridge() < best_msg.send_root_bridge():
				best_msg = msg
				msg_change_flag = 0


			# Rule 2
			elif msg.send_root_bridge() == best_msg.send_root_bridge() :
				if msg.send_dist() < best_msg.send_dist():
					best_msg = msg
					msg_change_flag = 0

				# Rule 3
				elif msg.send_dist() == best_msg.send_dist():
					if msg.send_sender_bridge() < best_msg.send_sender_bridge():
						best_msg = msg
						msg_change_flag = 0

			if msg_change_flag==0:
				for key in self.connection_status.keys():
					if self.connection_status[key]== 'RP':
						self.connection_status[key]='DP'
				self.connection_status[self.receive_buffer[i][1]] = 'RP'
			

			# Rule 5
			if msg_change_flag == 1:
				
				if msg.send_root_bridge() == best_msg.send_root_bridge():
					if msg.send_dist() < best_msg.send_dist():
						self.connection_status[self.receive_buffer[i][1]] = 'NP'
					elif msg.send_dist() == self.send_buffer.send_dist():
						if msg.sender_bridge <= self.bridge_id:
							self.connection_status[self.receive_buffer[i][1]] = 'NP'
			
		# Rule 4
		if len(self.receive_buffer) != 0:	
			if best_msg.send_root_bridge() != self.bridge_id:
				self.generate_config_message = False
				best_msg = config_message(best_msg.send_root_bridge(),best_msg.send_dist()+1,self.bridge_id)
	
		
		
		count = 0
		for key in self.connection_status.keys():
			if self.connection_status[key] == 'DP':
				count+=1													# Checking if there is No DP present

		if count == 0:
			for key in self.connection_status.keys():
				self.connection_status[key] = 'NP'

		return best_msg


	def send_processing(self,best_msg):										# transferring best message to send buffer
		self.send_buffer = best_msg

