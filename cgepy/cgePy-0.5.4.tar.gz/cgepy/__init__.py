__version__ = '0.5.4'
try:
	from cgePy.cgepy.codes import *
	from cgePy.cgepy import cust
except ModuleNotFoundError:
	try:
		from cgepy.cgepy.codes import *
		from cgepy.cgepy import cust
	except ModuleNotFoundError:
		from cgepy.codes import *
		from cgepy import cust
def cs():
	print("\033[2J")
	print("\033[H")
SPRITECOLOR = cust.SC
BACKGROUND = cust.BG
GRIDSIZE_EX = cust.GS
currentlyin = 0
gridinfo = {}
pr = int(GRIDSIZE_EX**0.5)
class cge:
	ctx = []
	class Exceptions:
		class OutOfRangeError(Exception):
			pass
		class MapError(Exception):
			pass
	class legacy:
		def cleargrid():
			counter=0
			newmap=[]
			for i in range(GRIDSIZE_EX):
				newmap.append(BACKGROUND+"  ")
			return newmap
			
		def creategrid():
			counter=0
			newmap=[]
			for i in range(GRIDSIZE_EX):
				newmap.append(BACKGROUND+"  ")
			return newmap
		def updategrid(grid=""):
			global currentlyin
			global cm
			cs()
			if grid != "":
				cm = grid
				grid=cm
			if grid == "":
				grid = cm
			grid[currentlyin%GRIDSIZE_EX]=SPRITECOLOR+"  "
			counter=-1
			refr=-1
			cs()
			for i in range(0,GRIDSIZE_EX):
				counter+=1
				refr+=1
				if refr == pr:
					if refr == GRIDSIZE_EX-pr:
						refr = 1
						print("")
					else:
						print("")
						refr=0
				print(grid[counter], end="")
			print(white+"")
		def updatepos(newpos):
			global currentlyin
			cm[currentlyin%GRIDSIZE_EX] = BACKGROUND+"  "
			currentlyin = newpos
		def movepos(direction):
			global currentlyin
			cm[currentlyin%GRIDSIZE_EX] = BACKGROUND+"  "
			if direction == "up":
				currentlyin-=pr
			if direction == "down":
				currentlyin+=pr
			if direction == "left":
				currentlyin-=1
			if direction == "right":
				currentlyin+=1
		def paint(map):
			global paintedlist
			counter = -1
			paintedlist = []
			map = list(map)
			#remove spacing
			for i in map:
				counter+=1
				if map[counter] == " ":
					map[counter] = RESET+""
			map = "".join(map)
			counter=-1
			odd = 0
			for i in map:
				counter+=1
				odd +=1
				if odd == 0:
					continue
				if odd == 1:
					odd = 0
					pass
				if counter+1 != len(map):
					if map[counter]+map[counter+1]=="BG":
							paintedlist+=[BACKGROUND+"  "]
					elif map[counter]+map[counter+1]=="RE":
							paintedlist+=[RED+"  "]
					elif map[counter]+map[counter+1]=="YE":
							paintedlist+=[YELLOW+"  "]
					elif map[counter]+map[counter+1]=="GR":
							paintedlist+=[GREEN+"  "]
					elif map[counter]+map[counter+1]=="BL":
							paintedlist+=[BLUE+"  "]
					elif map[counter]+map[counter+1]=="CY":
							paintedlist+=[CYAN+"  "]
					elif map[counter]+map[counter+1]=="MA":
							paintedlist+=[MAGENTA+"  "]
					elif map[counter]+map[counter+1]=="BB":
							paintedlist+=[BLACK+"  "]
					elif map[counter]+map[counter+1]=="WH":
							paintedlist+=[WHITE+"  "]
					elif map[counter]+map[counter+1]=="RR":
						paintedlist+=[RESET+"  "]
					return paintedlist
class Grid:
	def __init__(self, new=True):
		if new == True:
			self.ctx = cge.legacy.creategrid()
		else:
			if new == list():
				self.ctx = new
			elif new == str():
				self.ctx = new
				def Paint(self):
					self.ctx = cge.legacy.paint(self.ctx)
			elif new == Grid:
				self.ctx = new.ctx
	def clear(self):
		self.ctx = cge.legacy.creategrid()
	def write(self, pos, new):
		try:
			self.ctx[pos] = new
		except IndexError:
			raise cge.Exceptions.OutOfRangeError
	def swap(self, new):
		self.ctx = new
	def Update(self):
		cge.legacy.updategrid(self.ctx)
		cge.ctx = self.ctx
	def Self(self):
		return self.ctx
class Map:
	def __init__(self, map=False):
		if map==False:
			self.main = '''undefined'''
		else:
			self.main = map
	def Paint(self):
		if self.main == '''undefined''':
			raise cge.Exceptions.MapError("Cannot paint an undefined map.")
		else:
			self.ctx = cge.legacy.paint(self.main)
			self.__class__ = Grid
class Sprite:
	def __init__(self,pos=0,color=RED):
		self.pos = pos
		self.color = color
		self.sprite = color+"  "
	def Color(self,color):
		self.color = color
		self.sprite = color+"  "
	def Move(self,dir):
		if dir.lower() == "up":
			self.pos -= pr
		if dir.lower() == "down":
			self.pos += pr
		if dir.lower() == "left":
			self.pos -= 1
		if dir.lower() == "right":
			self.pos += 1

class MainSprite:
	def __init__(self):
		SPRITECOLOR = RED
	def Color(self,color):
		SPRITECOLOR = color
	def Move(self,dir):
		if dir.lower() == "up":
			cge.legacy.movepos("up")
		if dir.lower() == "down":
			cge.legacy.movepos("down")
		if dir.lower() == "left":
			cge.legacy.movepos("left")
		if dir.lower() == "right":
			cge.legacy.movepos("right")
MainSprite1 = MainSprite()
del MainSprite
MainSprite = MainSprite1
del MainSprite1