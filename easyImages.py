#!/usr/bin/python

'''
@author: michael.molien
@version: 1.1.1
Create Date: 06.05.2013
'''

__author__ = "Michael Molien"
__version__ = "1.1.1"
__license__ = "New-style BSD"

import PIL.Image        as Image
import PIL.ImageFont    as ImageFont
import PIL.ImageDraw    as ImageDraw
import StringIO


'''
#=============================
# easyImages Class
#=============================
# Dynamically Create Images for Testing.
# Verify that image is valid.
#=============================
'''


class easyImages:
    def __init__(self, savePath='./temp'):

        self._tempDir = savePath
        self._fileName = 'tempImage.png'
        self._size = [320, 50]
        self._textColor = 'white'
        self._shadColor = 'gray'
        self._mattColor = 'white'
        self._bordColor = 'orange'
        self._backColor = 'green'
        self._color = 'black'
        self._ColorWheel = {
            'black':  (0, 0, 0),
            'gray':   (80, 80, 80),
            'grey':   (144, 144, 144),
            'red':    (255, 0, 0),
            'green':  (0, 255, 0),
            'blue':   (0, 0, 255),
            'purple': (255, 0, 255),
            'yellow': (255, 255, 0),
            'orange': (255, 104, 0),
            'white':  (255, 255, 255),
        }

    def FontColor(self, value=None):
        if str(value) in self._ColorWheel.keys():
            self._textColor = str(value)
        return self._ColorWheel[self._textColor]

    def DropShadowColor(self, value=None):
        if str(value) in self._ColorWheel.keys():
            self._shadColor = str(value)
        return self._ColorWheel[self._shadColor]

    def MatteColor(self, value=None):
        if str(value) in self._ColorWheel.keys():
            self._mattColor = str(value)
        return self._ColorWheel[self._mattColor]

    def BorderColor(self, value=None):
        if str(value) in self._ColorWheel.keys():
            self._bordColor = str(value)
        return self._ColorWheel[self._bordColor]

    def BackgroundColor(self, value=None):
        if str(value) in self._ColorWheel.keys():
            self._backColor = str(value)
        return self._ColorWheel[self._backColor]

    def setColor(self, value=None):
        if str(value) in self._ColorWheel.keys():
            self._color = str(value)
        return self._ColorWheel[self._color]

    def getColor(self, value=None):
        if str(value) in self._ColorWheel.keys():
            return self._ColorWheel[value]
        return self._ColorWheel[self._color]

    def SavePath(self, filePath=None):
        if filePath is not None:
            self._tempDir = filePath
        return self._tempDir

    def FileName(self, fileName=None):
        if fileName is not None:
            self._fileName = fileName
        return self._fileName

    def Size(self, x=None, y=None):
        if type(x) == type(1):
            self._size[0] = x
        if type(y) == type(1):
            self._size[1] = y
        return self._size

    def rgbBoundCheck(self, color=0):
        if color > 255:
            color = 255
        if color < 0:
            color = 0
        return int(color)

    def CreateImage(self, border=None):
        im = Image.new('RGBA', self._size, 'White')
        draw = ImageDraw.Draw(im)

        a = (self.Size()[0] + 1) / 2
        highend = a
        b = (self.Size()[1] + 1) / 2
        if (b > a):
            highend = b
        n = float(float(255) / float(highend))

        color = self.BackgroundColor(border)

        for i in range(0, highend):
            y = self.Size()[1] - i
            if  y <= 0:
                y = (self.Size()[1] - (i % self.Size()[1]))
            x = self.Size()[0] - i
            if  x <= 0:
                x = (self.Size()[0] - (i % self.Size()[0]))

            R = self.rgbBoundCheck(color[0] - int(i * n))
            G = self.rgbBoundCheck(color[1] - int(i * n))
            B = self.rgbBoundCheck(color[2] - int(i * n))

            try:
                draw.rectangle([(i, i,), (x, y)], outline=(R, G, B))
            except( Exception, e ):
                print( "Draw Failed: %s" % (e) )

        color = self.BorderColor()
        x = self.Size()[0]
        y = self.Size()[1]
        r = 5
        n = float(float(255) / float(r))
        for i in range(0, r):
            y = self.Size()[1] - i
            x = self.Size()[0] - i

            R = self.rgbBoundCheck(color[0] - int(i * n))
            G = self.rgbBoundCheck(color[1] - int(i * n))
            B = self.rgbBoundCheck(color[2] - int(i * n))

            draw.rectangle([(i, i,), (x - 1, y - 1)], outline=(R, G, B))
        draw.rectangle([(r, r,), (x - 2, y - 2)], outline=self.MatteColor())

        a = (self.Size()[0] + 1) / 2
        b = (self.Size()[1] + 1) / 2
        ifo = ImageFont.load_default()
#        offSet = 10
        _fileName = self.FileName()
        (_width, _height) = draw.textsize(_fileName)
        fontPosX = (a) - (_width / 2)
        fontPosY = (b) - (_height)
        draw.text((fontPosX, fontPosY + 1), _fileName, self.DropShadowColor(), font=ifo)
        draw.text((fontPosX + 1, fontPosY), _fileName, self.DropShadowColor(), font=ifo)
        draw.text((fontPosX + 1, fontPosY + 1), _fileName, self.DropShadowColor(), font=ifo)
        draw.text((fontPosX, fontPosY), _fileName, self.FontColor(), font=ifo)
        _filePath = '%s/%s' % (self.SavePath(), self.FileName())
        im.save(_filePath)
        return _filePath


def verifyImage(image_buffer, label=''):
# -- Verify an Image
    status = False
    message = ''
    try:
        im = Image.open(StringIO.StringIO(image_buffer))
        status = im.verify()
    except( Exception, e ):
        message = e
        print( "Verify Image: %s %s: %s" % (label, status, message) )
    return status
