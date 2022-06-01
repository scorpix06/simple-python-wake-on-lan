from wakeonlan import send_magic_packet
import os 




class Wol():

	def __init__(self, Ip, Mac, Port=9):

		self.Ip = Ip
		self.Mac = Mac
		self.Port = Port

		self.WakeUp()

	def WakeUp(self):

		send_magic_packet(self.Mac, ip_address=self.Ip, port=int(self.Port))

		return True


