import wx, os
from random import randint

RANDFACTOR = 10
HEX = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f")

def getNumber(inputText):
	while True:
		try:
			inp = int(input(inputText))
			if inp > 0:
				return inp
		except:
			pass
		print("Please input a positive integer")

def getPixelSize(width, height):
	while True:
		pixelSize = getNumber("Pixel size: ")
		if pixelSize > 0 and width%pixelSize == 0 and height%pixelSize==0:
			return pixelSize
		print("Please input a positive integer that divides width {0} and height {1}".format(width, height))

def getRGB():
	while True:
		startingColour = input("Starting colour - #RRGGBB or (R, G, B): ")
		try:
			if startingColour[0] == "#" and len(startingColour) == 7:
				r, g, b = [int(startingColour[i:i+2], 16) if startingColour[i].lower() in HEX and startingColour[i+1].lower() in HEX else 0/0 for i in range(1, 7, 2)]
				# if r.lower() in HEX and g.lower() in HEX and b.lower() in HEX:
					# r, g, b = map(lambda it: int(it, 16), (r, g, b))
					# r = int(startingColour[1:3], 16)
					# g = int(startingColour[3:5], 16)
					# b = int(startingColour[5:7], 16)
				return (r, g, b)
			elif startingColour[0] == "(" and startingColour[-1] == ")":
				r, g, b = map(int, startingColour[1:-1].split(", "))
				if r >=0 and r < 256 and g >= 0 and g < 256 and b >= 0 and b < 256:
					return (r, g, b)
		except:
			pass
		print("Please enter a proper RGB value - #RRGGBB or (R, G, B)")

def stepColour(r, g, b):
	rng = randint(1, 3)
	dir = randint(-1, 1)
	scale = randint(1, RANDFACTOR)
	if rng == 1:
		r += dir*scale
		if r >= 256:
			r = 510-r
		elif r < 0:
			r = -r
	elif rng == 2:
		g += dir*scale
		if g >= 256:
			g = 510-g
		elif g < 0:
			g = -g
	else:
		b += dir*scale
		if b >= 256:
			b = 510-b
		elif b < 0:
			b = -b
	return (r, g, b)
			
def generateImage(width, height, pixelSize, startingColour):
	img = wx.Image(width, height)
		
	cr, cg, cb = startingColour
	for x in range(0, width, pixelSize):
		r, g, b = (cr, cg, cb)
		for y in range(0, height, pixelSize):
			img.SetRGB(wx.Rect(x, y, pixelSize, pixelSize), r, g, b)
			r, g, b = stepColour(r, g, b)
		cr, cg, cb = stepColour(cr, cg, cb)
		
	return img

class MainFrame(wx.Frame):    
	def __init__(self):
		super().__init__(parent=None)
		
		width = getNumber("Width: ")
		height = getNumber("Height: ")
		pixelSize = getPixelSize(width, height)
		startingColour = getRGB()
		
		img = generateImage(width, height, pixelSize, startingColour)
		img.SaveFile("image.png", wx.BITMAP_TYPE_PNG)
		
		print("Image successfully generated")
		input("Press enter to continue")
		

def main():
	app = wx.App()
	frame = MainFrame()
	
if __name__ == "__main__":
	main()