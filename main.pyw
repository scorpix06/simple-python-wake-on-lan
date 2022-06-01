from wol import *
from tkinter import *
import time
import pickle
from tkinter import messagebox
import datetime

class WakeOnLanGraphical():

	def __init__(self):
		""" Fenetre principale"""

		self.Ip = ""
		self.Mac = ""
		self.Port = ""

		self.ListLog = []

		try:
			self.GetConf()

		except:

			pass

		try:
			self.GetLog()

		except:

			pass


		self.window = Tk()
		self.window.title('Wake On Lan')
		self.window.geometry("350x400")
		self.window.config(bg='white')

		self.window.iconbitmap(default='image/logo.ico')

		# Photo
		self.image = PhotoImage(file="image/logo.png")
		self.image_verte = PhotoImage(file='image/logo_vert2.png')

		self.canvas = Canvas(self.window, width=300, height=300, bg='white',  bd=0, highlightthickness=0,)
		self.click = self.canvas.create_image(150, 150, image=self.image, state=NORMAL)


		self.canvas.tag_bind(self.click, "<Button-1>", self.WakeUpButton)


		self.canvas.pack()

		# Menu
		menu_bar = Menu(self.window)

		menu_bar.add_command(label='Configuration', command = self.ConfWol)
		menu_bar.add_command(label='Log', command =self.Log)
		menu_bar.add_command(label='A propos', command = self.About)


		self.window.config(menu=menu_bar)


		self.window.mainloop()



	def Gif(self):

		#NbrImage = 29
		NbrImage = 25
		i = 1
		
		while i != NbrImage + 1:

			#img = PhotoImage(file="image/gif - copie/{}.png".format(i)) 
			img = PhotoImage(file="image/gif/{}.png".format(i)) 

			self.canvas.itemconfig(self.click, image=img)
			self.window.update()
			i += 1

	def WakeUpButton(self, arg):
		"""Fonction appeler au click du bouton de reveil"""

		self.Gif()
		time.sleep(0.2)
		self.canvas.itemconfig(self.click, image=self.image)

		Check = self.CheckData(self.Ip, self.Mac, self.Port)
		print('Resultat du check data : {}'.format(Check))
		
		#Check = True # A del une fois CheckData fonctionnel

		if Check == True:

			print('Juste avant d envoyer : {}, {}, {}'.format(self.Ip, self.Mac, self.Port))
			Wol(self.Ip, self.Mac, self.Port)


			self.AddLog(self.Ip, self.Mac, self.Port, True)

			print('Paquet magique envoyée')

		else:

			messagebox.showinfo("Impossible d'envoyée le paquet", "Error {} : {}".format(Check[1], Check[2]))
			print("Impossible d'envoyée le paquet veuillez verifiez les data (Error {} : {})".format(Check[1], Check[2]))

			self.AddLog(self.Ip, self.Mac, self.Port, False, [Check[1], Check[2]])

		print(self.Ip, self.Mac, self.Port)


	def CheckData(self, Ip, Mac='', Port=''):


		if Ip == '':

			return [False, 1, 'Champ adresse IP vide']

		if Mac == '':

			return [False, 2, 'Champ addresse Mac vide']

		if Port == '':

			return [False, 3, 'Champ port destination vide']


		else:
			# Check IP
			try:

				IpSplit = Ip.split('.')

				for element in IpSplit:

					IpSplit[IpSplit.index(element)] = int(element)
			

				if len(IpSplit) != 4:

					IpCheck = False

				elif IpSplit[0] > 254 or IpSplit[0] < 1:

					IpCheck = False

				elif IpSplit[1] > 254 or IpSplit[1] < 1:

					IpCheck = False

				elif IpSplit[2] > 254 or IpSplit[2] < 1:

					IpCheck = False

				elif IpSplit[3] > 254 or IpSplit[3] < 1:

					IpCheck = False

				else:

					IpCheck = True

			except:

				if '.' in Ip:

					IpCheck = True

				else:
					IpCheck = False

		

			# Check Mac

			Alphabet = ['A', 'B', 'C', 'D', 'E', 'F', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', '-']
			CheckerMac = []
			try:

				LenMac = len(Mac)

				if LenMac == 12 or LenMac == 17:

					for element in Mac:

						if element.upper() in Alphabet:

							CheckerMac.append(True)

						else:

							CheckerMac.append(False)

					if False in CheckerMac:

						MacCheck = False

					else:

						MacCheck = True

				else:

					MacCheck = False


			except:

				MacCheck = False

			# Check Port
			try:

				if int(Port) == 9 or int(port) == 7:

					PortCheck = True

				else:
					PortCheck = False

			except:

				PortCheck = False


			Check = [IpCheck, MacCheck, PortCheck]

			if False in Check:

				Error = Check.index(False)

				# Ip invalide
				if Error == 0:

					return [False, 4, 'Adresse IP incorrecte']

				# Mac invalide
				if Error == 1:

					return [False, 5, 'Adresse MAC incorrecte']

				# Port invalide
				if Error == 2:

					return [False, 6, 'Port incorrecte']


			else:

				return True




	def ConfWol(self):
		"""Fonction appeler au click de la configuration du logiciel"""

		def SaveParams(event=False):
			""" Fonction d'enregistrement des parametres de configuration"""

			self.Ip = IpEntry.get()
			self.Mac = MacEntry.get()
			self.Port = PortEntry.get()

			self.SetConf(self.Ip, self.Mac, self.Port)

			main.destroy()

			print(self.Ip, self.Mac, self.Port)

		def Destroy(event=False):

			main.destroy()



		main = Tk()
		main.title('Configuration Wake On Lan')
		main.geometry("230x230")
		main.config(bg='white')

		parametres = Frame(main, bg='white')

		# @IP
		IpText = Label(parametres, text="Adresse IP :", bg='white')
		IpText.grid(row=1, column=1)

		IpEntry = Entry(parametres)
		IpEntry.insert(END, self.Ip)
		IpEntry.grid(row=1, column=2)

		# @MAC
		MacText = Label(parametres, text="Adresse MAC :", bg='white')
		MacText.grid(row=2, column=1)

		MacEntry = Entry(parametres)
		MacEntry.insert(END, self.Mac)
		MacEntry.grid(row=2, column=2)

		# Port
		PortText = Label(parametres, text="Port :", bg='white')
		PortText.grid(row=3, column=1)

		PortEntry = Entry(parametres)
		PortEntry.insert(END, self.Port)
		PortEntry.grid(row=3, column=2)

		# Touche clavier
		main.bind('<Return>', SaveParams) # Entrer enregistre les parametres
		main.bind('<Escape>', Destroy) # Echappe quitte la fenetre sans enregistrer les modification

		parametres.pack()

		# Valider
		SubmitButton = Button(main, text='Valider', command=SaveParams)
		SubmitButton.pack()

		


	
	def GetConf(self):

		with open('data', 'rb') as Fichier:

			mon_depickler = pickle.Unpickler(Fichier)
			data = mon_depickler.load()

		print("Element récuperer dans le fichier data : {}".format(data))

		self.Ip = data[0]
		self.Mac = data[1]
		self.Port = data[2]


	def SetConf(self, Ip, Mac, Port):


		conf = [Ip, Mac, Port]

		with open('data', 'wb') as Fichier:

			mon_pickle = pickle.Pickler(Fichier)
			mon_pickle.dump(conf)


	def About(self):

		main = Tk()
		main.title('A propos')
		main.geometry("300x300")
		main.config(bg='white')

		Text = Label(main, text="Logiciel libre de droit, crée par Alban Cipre en 2020")
		Text.grid()

		Version = Label(main, text="Version : 1")
		Version.grid()

		Contact = Label(main, text="Contact : alban@cipre.com")
		Contact.grid()

	def Log(self):

		main = Tk()
		main.title('Log')
		main.geometry("300x300")
		main.config(bg='white')

		for element in self.ListLog:

			Text = Label(main, text=element)
			Text.grid()

	def AddLog(self, Ip, Mac, Port, state, CodeError=False):

		heure = datetime.datetime.now()

		if state == True:

			self.ListLog.append(["[{}/{}/{} {}:{}] : Paquet envoyer : Ip : {}, Mac : {}, Port : {}".format(heure.day, heure.month, heure.year, heure.hour, heure.minute, Ip, Mac, Port)])

		else:

			self.ListLog.append(["[{}/{}/{} {}:{}] : Tentative d'envoi avec erreur : Ip : {}, Mac : {}, Port : {} [Error : {} {}]".format(heure.day, heure.month, heure.year, heure.hour, heure.minute, Ip, Mac, Port, CodeError[0], CodeError[1])])

		self.SetLog(self.ListLog)

	def GetLog(self):

		with open('log', 'rb') as Fichier:

			mon_depickler = pickle.Unpickler(Fichier)
			data = mon_depickler.load()

		print("Element récuperer dans le fichier log : {}".format(data))

		self.ListLog = data


	def SetLog(self, log):


		with open('log', 'wb') as Fichier:

			mon_pickle = pickle.Pickler(Fichier)
			mon_pickle.dump(log)



if __name__ == '__main__':

	main = WakeOnLanGraphical()

