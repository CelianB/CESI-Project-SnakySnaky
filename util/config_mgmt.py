# Auteur : Célian B & Florian H

#!/usr/bin/python3
import os
import configparser

class ConfigHandler:
	def __init__(self, node, debugg=False, fileName='core.ini', folder='conf'):
		self.configDir = folder
		if folder == '':
			self.configPath = fileName
		else:
			self.configPath = folder + '/' + fileName
		self.configNode = node
		self.debug = debugg
		self.config = configparser.ConfigParser()
		self.defaultConfig()

	def defaultConfig(self): #Void
		try:
			if not self.configDir == '':
				if not os.path.exists(self.configDir):
					os.mkdir(self.configDir)
			if(not os.path.exists(self.configPath)):
				f = open(self.configPath, 'w')
				f.close()
				self.config.read(self.configPath)
				self.config[self.configNode] = {}
				self.saveConfig()
			else:
				self.config.read(self.configPath)
				try:
					if self.config[self.configNode] != None:
						pass
				except:
					self.config[self.configNode] = {}
					self.saveConfig()
		except:
			if self.debug:
				print('Impossible d\'écrire la configuration par défaut dans '+self.configPath+' !')
			pass

	def saveConfig(self): #Bool
		try:
			with open(self.configPath, 'w') as configFile:
				self.config.write(configFile)
			return True
		except:
			if self.debug:
				print('Impossible de sauvegarder la configuration !')
			return False

	def getStr(self, key): #Str
		try:
			self.config.read(self.configPath)
			return self.config[self.configNode][str(key)]
		except:
			if self.debug:
				print('Impossible de lire la clé '+key+' dans '+self.configPath+' !')
			return ''

	def setValue(self, key, value): #Supporte les espaces et caractères spéciaux
		#Key will be save lower case
		try:
			self.config.read(self.configPath)
			if type(value) == bool:
				v = 0
				if value == True: v = 1
				self.config[self.configNode][str(key)] = str(v)
				if self.debug:
					print('Set boolean: ' + str(key) + ' -> ' + str(value) + ' with type: ' + str(type(value)))
			else:
				self.config[self.configNode][str(key)] = str(value)
				if self.debug:
					print('Set value: ' + str(key) + ' -> ' + str(value) + ' with type: ' + str(type(value)))
			self.saveConfig()
		except:
			if self.debug:
				print('Impossible d\'écrire la clé '+key+' avec la valeur '+value+' dans '+self.configPath+' !')
			pass

	def prepareArray(self, arr):
		return str(arr).strip('[]').replace('\'', '')
	def getArray(self, key):
		return self.getStr(key).split(', ')
	def getInt(self, key):
		return eval(self.getStr(key))
	def getFloat(self, key):
		return eval(self.getStr(key))
	def getList(self, key):
		return list(self.getStr(key))
	def getBoolean(self, key):
		if self.getInt(key) == 1:
			return True
		else:
			return False

	def isValueExists(self, s):
		try:
			if self.getStr(s) != '':
				return True
			else:
				return False
		except:
			return False
