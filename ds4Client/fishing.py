# backend use tkAgg
import matplotlib
matplotlib.use('tkAgg')

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from PIL import Image
import sqlite3
import kmeans
import cv2
import time
import math

# initialize GPIO
DS4_L1 = 16
DS4_L2 = 36
DS4_R1 = 18
DS4_R2 = 38
DS4_UP = 40
DS4_SQUARE = 33
DS4_TRIANGLE = 35
DS4_CIRCLE = 37
DS4_CROSS = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setup(DS4_L1, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_L2, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_R1, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_R2, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_UP, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_SQUARE, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_TRIANGLE, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_CIRCLE, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(DS4_CROSS, GPIO.OUT, initial = GPIO.HIGH)

loopList = [DS4_L2, DS4_UP, DS4_R2, DS4_UP]
loopIndex = 0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera)

def handle_close(evt):
    GPIO.cleanup()
    sqlConn.close()
    camera.close()

# initialize the figure
plt.rcParams['toolbar'] = 'None'
fig = plt.figure()
fig.subplots_adjust(left=0, bottom=0, right=0.5, top=1)
fig.canvas.mpl_connect('close_event', handle_close)
thismanager = plt.get_current_fig_manager()
thismanager.window.wm_geometry("640x240+0+0")

# allow the camera to warmup
time.sleep(2)

# initialize the frame
frameStartX = 0
frameStartY = 0
frameScale = 1

# initialize the db
sqlConn = sqlite3.connect("database.db")
sqlCur = sqlConn.cursor()
try:
    cursor = sqlCur.execute("SELECT frameStartX, frameStartY, frameScale FROM framePos")
    for row in cursor:
        frameStartX = row[0]
        frameStartY = row[1]
        frameScale = row[2]
except sqlite3.OperationalError:
    sqlCur.execute("CREATE TABLE framePos (frameStartX INTEGER, frameStartY INTEGER, frameScale REAL)")
    sqlCur.execute("INSERT INTO framePos VALUES (0, 0, 1)")
    sqlConn.commit()


framePos = [] # top-left corner and bottom-right corner
def calcFramePos():
    global framePos
    frameWidth = math.floor(50 * frameScale)
    frameSpace = math.floor(11 * frameScale)
    frameDiffHeight = math.floor(30 * frameScale)
    framePos = []
    framePos.append([])
    framePos[0].append([frameStartX, frameStartY + frameDiffHeight])
    framePos[0].append([framePos[0][0][0] + frameWidth, framePos[0][0][1] + frameWidth])
    framePos.append([])
    framePos[1].append([framePos[0][1][0] + frameSpace, frameStartY])
    framePos[1].append([framePos[1][0][0] + frameWidth, framePos[1][0][1] + frameWidth])
    framePos.append([])
    framePos[2].append([framePos[1][1][0] + frameSpace, frameStartY + frameDiffHeight])
    framePos[2].append([framePos[2][0][0] + frameWidth, framePos[2][0][1] + frameWidth])

calcFramePos()

startFishingFlag = True
refreshTime = time.time()
def loopButton():
    global loopIndex
    global startFishingFlag
    global refreshTime

    if startFishingFlag == False:
        return
    # print(1/(time.time()-refreshTime), (time.time()-refreshTime), loopIndex)
    # refreshTime = time.time()

    for i in range(len(loopList)):
        if i == loopIndex:
            GPIO.output(loopList[i], GPIO.LOW)
        else:
            GPIO.output(loopList[i], GPIO.HIGH)
    loopIndex = loopIndex + 1
    if loopIndex >= len(loopList):
        loopIndex = 0


def pressButton(index):
    global startFishingFlag
    if startFishingFlag == False:
        return
    if index == -1:
        GPIO.output(DS4_SQUARE, GPIO.HIGH)
        GPIO.output(DS4_TRIANGLE, GPIO.HIGH)
        GPIO.output(DS4_CIRCLE, GPIO.HIGH)
    if index == 0:
        GPIO.output(DS4_SQUARE, GPIO.LOW)
        GPIO.output(DS4_TRIANGLE, GPIO.HIGH)
        GPIO.output(DS4_CIRCLE, GPIO.HIGH)
    if index == 1:
        GPIO.output(DS4_SQUARE, GPIO.HIGH)
        GPIO.output(DS4_TRIANGLE, GPIO.LOW)
        GPIO.output(DS4_CIRCLE, GPIO.HIGH)
    if index == 2:
        GPIO.output(DS4_SQUARE, GPIO.HIGH)
        GPIO.output(DS4_TRIANGLE, GPIO.HIGH)
        GPIO.output(DS4_CIRCLE, GPIO.LOW)


def getMainColor(arrowImg):
    blueFlag = False
    arrowImg.thumbnail((50, 50))
    pixels = [] # [(r,g,b), count]
    for count, (r, g, b) in arrowImg.getcolors(arrowImg.size[0] * arrowImg.size[1]):
        pixels.append([(r, g, b), count])
    colors = kmeans.kmeans(pixels, 3)
    for (r, g, b) in colors:
        if b > 100:
            blueFlag = True
    return blueFlag


# grab an image from the camera
imgShowFlag = True
def getCameraPic():
    global imgShowFlag
    camera.capture(rawCapture, use_video_port=True, format="rgb")
    image = rawCapture.array
    loopButton()
    pressButtonIndex = -1
    for i in range(len(framePos)):
        arrowImg = image[framePos[i][0][1]:framePos[i][1][1], framePos[i][0][0]:framePos[i][1][0]]
        if getMainColor(Image.fromarray(arrowImg, 'RGB')):
            pressButtonIndex = i
            if imgShowFlag:
                image = cv2.rectangle(image, tuple(framePos[i][0]), tuple(framePos[i][1]), (0,0,255), 10)
        else:
            if imgShowFlag:
                image = cv2.rectangle(image, tuple(framePos[i][0]), tuple(framePos[i][1]), (0,255,0), 3)

    pressButton(pressButtonIndex)

    rawCapture.truncate(0)
    if imgShowFlag:
        return image
    else:
        return [[0,0,0]]

im = plt.imshow(getCameraPic(), animated=True)


def updatefig(*args):
    im.set_array(getCameraPic())
    return im,

ani = animation.FuncAnimation(fig, updatefig, blit=True)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis


def framePosUp(event):
    global frameStartY
    frameStartY -= 10
    sqlCur.execute("UPDATE framePos SET frameStartY = ?", (frameStartY,))
    sqlConn.commit()
    calcFramePos()
def framePosDown(event):
    global frameStartY
    frameStartY += 10
    sqlCur.execute("UPDATE framePos SET frameStartY = ?", (frameStartY,))
    sqlConn.commit()
    calcFramePos()
def framePosLeft(event):
    global frameStartX
    frameStartX -= 10
    sqlCur.execute("UPDATE framePos SET frameStartX = ?", (frameStartX,))
    sqlConn.commit()
    calcFramePos()
def framePosRight(event):
    global frameStartX
    frameStartX += 10
    sqlCur.execute("UPDATE framePos SET frameStartX = ?", (frameStartX,))
    sqlConn.commit()
    calcFramePos()
def framePosZoomOut(event):
    global frameScale
    if frameScale == 1:
        return
    frameScale -= 0.2
    sqlCur.execute("UPDATE framePos SET frameScale = ?", (frameScale,))
    sqlConn.commit()
    calcFramePos()
def framePosZoomIn(event):
    global frameScale
    frameScale += 0.2
    sqlCur.execute("UPDATE framePos SET frameScale = ?", (frameScale,))
    sqlConn.commit()
    calcFramePos()
def framePosImgShow(event):
    global imgShowFlag
    if imgShowFlag:
        bImgShow.label.set_text('Open')
        imgShowFlag = False
    else:
        bImgShow.label.set_text('Close')
        imgShowFlag = True
def startFishing(event):
    global startFishingFlag
    if startFishingFlag:
        bStart.label.set_text('Start')
        startFishingFlag = False
    else:
        bStart.label.set_text('Stop')
        startFishingFlag = True


btnWidth = 0.1
btnHeight = 0.2

# left, bottom, width, height
axUp = plt.axes([0.55, 0.7, btnWidth, btnHeight])
axDown = plt.axes([0.7, 0.7, btnWidth, btnHeight])
axImgShow = plt.axes([0.85, 0.7, btnWidth, btnHeight])
axLeft = plt.axes([0.55, 0.4, btnWidth, btnHeight])
axRight = plt.axes([0.7, 0.4, btnWidth, btnHeight])
axStart = plt.axes([0.85, 0.4, btnWidth, btnHeight])
axZoomOut = plt.axes([0.55, 0.1, btnWidth, btnHeight])
axZoomIn = plt.axes([0.7, 0.1, btnWidth, btnHeight])
bUp = Button(axUp, 'Up')
bDown = Button(axDown, 'Down')
bImgShow = Button(axImgShow, 'Close')
bLeft = Button(axLeft, 'Left')
bRight = Button(axRight, 'Right')
bStart = Button(axStart, 'Stop')
bZoomOut = Button(axZoomOut, 'ZoomOut')
bZoomIn = Button(axZoomIn, 'ZoomIn')
bUp.on_clicked(framePosUp)
bDown.on_clicked(framePosDown)
bImgShow.on_clicked(framePosImgShow)
bLeft.on_clicked(framePosLeft)
bRight.on_clicked(framePosRight)
bStart.on_clicked(startFishing)
bZoomOut.on_clicked(framePosZoomOut)
bZoomIn.on_clicked(framePosZoomIn)


plt.show()
