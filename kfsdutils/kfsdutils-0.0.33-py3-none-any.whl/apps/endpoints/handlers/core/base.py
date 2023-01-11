import netifaces, os, subprocess, socket, time, json, yaml
from os import path
import shlex
from subprocess import Popen, PIPE
from threading import Timer
class Base():
	def __init__(self):
		self.__isDebug = False

	def setDebug(self, val):
		self.__isDebug = val

	def log(self, t, msg):
		if t == "DEBUG":
			if not self.__isDebug:
				print("[{}] {}".format(t, msg))
		else:
			print("[{}] {}".format(t, msg))

	def sleep(self, seconds):
		time.sleep(seconds)

	def encryptKey(self):
		return self.cmdExec("head -c 32 /dev/urandom | base64")

	def getArch(self):
		return self.cmdExec("uname -m").lower()

	def jsonToYaml(self, json):
		return yaml.dump(json)

	def getHostIP(self):
		return netifaces.ifaddresses(self.getNIC())[netifaces.AF_INET][0]['addr']

	def readFileReplaceStrs(self, filePath, replaceKeys):
		self.log("DEBUG", "Replace keys to file: {}, replace keys: {}".format(filePath, replaceKeys))
		fileHandle = open(filePath, "rt")
		fileData = fileHandle.read()
		for k, v in replaceKeys.items():
			fileData = fileData.replace(k, v)
		fileHandle.close()
		return fileData

	def getNIC(self):
		nicPath = "/sys/class/net/{}/"
		if self.pathExists(nicPath.format("eth0")):
			return "eth0"
		elif self.pathExists(nicPath.format("enp5s0")):
			return "enp5s0"
		return "en0"

	def getHostName(self):
		return socket.gethostname()

	def getOS(self):
		return self.cmdExec("uname").lower()

	def changeFilePermission(self, permission, filePath):
		self.cmdExec("chmod {} {}".format(permission, filePath))

	def createDir(self, dirPath):
		if not self.pathExists(dirPath):
			os.makedirs(dirPath)

	def rmFile(self, filePath):
		if self.pathExists(filePath):
			os.remove(filePath)

	def writeFile(self, filePath, content, appendMode=False):
		self.log("DEBUG", "Writing to file: {}, content: {}".format(filePath, content))
		if content:
			self.createDir(self.getDirFromFilePath(filePath))
			writeMode = "a" if appendMode else "w"
			f = open(filePath, writeMode)
			f.write(content)
			f.close()
		else:
			self.log("ERROR", "Failed to write to file: {}, content is None".format(filePath))

	def readFileAsString(self, filePath, removeLineBreaks=True):
		if self.pathExists(filePath):
			fileStr = ""
			with open(filePath, 'r') as file:
				fileStr = file.read()
			return fileStr.replace("\n", " ") if removeLineBreaks else fileStr
		self.log("ERROR", "File: {} does not exist".format(filePath))
		return None

	def readJsonFromFile(self, filePath):
		if self.pathExists(filePath):
			with open(filePath) as json_file:
				return json.load(json_file)
		return {}

	def convertJsonFromStr(self, jsonStr):
		return json.loads(jsonStr)

	def getDirFromFilePath(self, filePath):
		return os.path.dirname(filePath)

	def convertDictToJson(self, content:dict):
		return json.dumps(content)

	def pathExists(self, destPath):
		if not os.path.exists(destPath):
			return False
		return True

	def runCmd(self, cmd):
		return subprocess.getoutput(cmd)

	def cmdsExec(self, cmds, returnOutput=True, shell=False):
		return [self.cmdExec(cmd, returnOutput, shell) if not type(cmd) == list else self.cmdsExec(cmd, returnOutput, shell) for cmd in cmds]

	def cmdExec(self, cmd, returnOutput=True, shell=False):
		if returnOutput:
			cmdOutput = subprocess.getstatusoutput(cmd)
			returnVal = cmdOutput[1] if cmdOutput[0]==0 else None
			self.log("INFO", "CMD: {}, Output: {}".format(cmd, returnVal))
			return returnVal
		else:
			self.log("INFO", "CMD: {}".format(cmd))
			proc = subprocess.Popen(shlex.split(cmd) if not shell else cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell, universal_newlines=True)
			for line in iter(proc.stdout.readline, ""):
				self.log("INFO", "{}".format(line.strip()))
			proc.stdout.close()
