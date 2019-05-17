'''
Code for the automated cable cross machine by: Christopher Karam

Uses pygame for the interface. Pyfirmata is for the ardiuno connection.
'''


import pyfirmata, sys, pygame
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program

#Sets up serial connection with the arduino
board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)
it.start()

#call for the PNG for each excersize
back_row = pygame.image.load('back_row.png')
bicep_curl = pygame.image.load('bicep_curl.png')
tricep_extention = pygame.image.load('tricep_extention.png')
chest_fly = pygame.image.load('chest_fly.png')
chest_press = pygame.image.load('chest_press.png')
hip_extention = pygame.image.load('hip_extension.png')
lat_pulldown = pygame.image.load('lat_pulldown.png')
shoulder_cross = pygame.image.load('shoulder_cross.png')
shoulder_pull = pygame.image.load('shoulder_pull.png')

#loads the pngs into a list, and couresponding list for angle location
#and names.
exercises = [back_row,bicep_curl,tricep_extention,chest_fly,chest_press,hip_extention,lat_pulldown,shoulder_cross,shoulder_pull]
names = ['Back Row','Bicep Curl','Tricep Extention','Chest Fly','Chest Press','Hip Extention','Lat Pulldown','Shoulder Cross','Shoulder Pull']
angles = [(25.0,25.0),(25.0,25.0),(155.0,155.0),(135.0,135.0),(45.0,45.0),(25.0,25.0),(155.0,155.0),(135.0,135.0),(145.0,145.0)]

#sets servo connection for both arms and 
#the platforms
sArmLeft = board.get_pin('d:9:s')
sArmRight = board.get_pin('d:10:s')
sAngleLeft = board.get_pin('d:11:s')
sAngleRight = board.get_pin('d:12:s')

def main():
	
    global FPSCLOCK, DISPLAYSURF, buttonText, angleText
    pygame.init()
    buttonText = pygame.font.Font('freesansbold.ttf',45)
    angleText = pygame.font.Font('freesansbold.ttf',30)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    
    state = 1 #which muscle group section has been picked
    selection = 0 #excercise selected
    angleL , angleR = angles[selection] #initial angle for each arm
    lSide = 90 #anlge for left platform
    rSide = 90 #angle for right platform
    

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Automated Cable Cross')


    while True: #main game loop
        mouseClicked = False

        DISPLAYSURF.fill((255,255,255)) # drawing the window
        #sArmLeft.write(90)
        
        #Calls for drawing the GUI
        drawButtons()
        drawIcons(state)
        drawSelection(selection,angleL,angleR, lSide, rSide)
        
        #call to output to the servos
        controlServos(angleL, angleR, lSide, rSide)
        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                
		#decides which action to do for each button press
        if mouseClicked:
            toDo, val = getLocation(mousex,mousey)
            if toDo == 1:
                state = val
            if toDo == 2:
                selection = val
                angleL , angleR = angles[selection]
            if toDo == 4:
                if angleL > 15 and angleL < 175:
                   angleL += val
                else :
					angleL += (val * -1)
            if toDo == 3:
                if angleR >= 15 and angleR <= 175:
                   angleR += val
                else :
					angleR += (val * -1)
            if toDo == 5:
                if lSide >= 75 and lSide <= 175:
                    lSide += val
                else :
                    lSide += (val * -1)
            if toDo == 6:
                if rSide >= 75 and rSide <= 175:
                    rSide += val
                else :
                    rSide += (val * -1)

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


#method to output the correct angles to the motors
def controlServos(lArm, rArm, lSide, rSide):
    l = int((lArm) * 2.0 / 3.0)
    print(l)
    r = int(( 180.0 - rArm ) * 2.0 / 3.0)
    print(r)
    sArmLeft.write(l)
    sArmRight.write(r)
    rSide = 180 - rSide
    sAngleLeft.write(lSide)
    sAngleRight.write(rSide)

#draws every botton on the screen
def drawButtons():
	##############drawing the buttons#############
	pygame.draw.rect(DISPLAYSURF, (0,255,255), (12, 862, 250, 100))
	textSurf1, textRect1 = text_objects("All", buttonText)
	textRect1.center = ( (12 + (250/2)), (862 + (100/2)))
	DISPLAYSURF.blit(textSurf1, textRect1)
	
	pygame.draw.rect(DISPLAYSURF, (0,255,255), (269, 862, 250, 100))
	textSurf2, textRect2 = text_objects("Chest", buttonText)
	textRect2.center = ( (269 + (250/2)), (862 + (100/2)))
	DISPLAYSURF.blit(textSurf2, textRect2)
	
	pygame.draw.rect(DISPLAYSURF, (0,255,255), (526, 862, 250, 100))
	textSurf3, textRect3 = text_objects("Back", buttonText)
	textRect3.center = ( (526 + (250/2)), (862 + (100/2)))
	DISPLAYSURF.blit(textSurf3, textRect3)
	
	pygame.draw.rect(DISPLAYSURF, (0,255,255), (783, 862, 250, 100))
	textSurf4, textRect4 = text_objects("Biceps", buttonText)
	textRect4.center = ( (783 + (250/2)), (862 + (100/2)))
	DISPLAYSURF.blit(textSurf4, textRect4)
	
	pygame.draw.rect(DISPLAYSURF, (0,255,255), (1040, 862, 250, 100))
	textSurf5, textRect5 = text_objects("Triceps", buttonText)
	textRect5.center = ( (1040 + (250/2)), (862 + (100/2)))
	DISPLAYSURF.blit(textSurf5, textRect5)
	
	pygame.draw.rect(DISPLAYSURF, (0,255,255), (1297, 862, 250, 100))
	textSurf6, textRect6 = text_objects("Shoulders", buttonText)
	textRect6.center = ( (1297 + (250/2)), (862 + (100/2)))
	DISPLAYSURF.blit(textSurf6, textRect6)
	
	pygame.draw.rect(DISPLAYSURF, (0,255,255), (1554, 862, 250, 100))
	textSurf7, textRect7 = text_objects("Legs", buttonText)
	textRect7.center = ( (1554 + (250/2)), (862 + (100/2)))
	DISPLAYSURF.blit(textSurf7, textRect7)
	
	#left up arrow
	pygame.draw.rect(DISPLAYSURF, (0,0,0), (1055, 360, 75, -100))
	pygame.draw.polygon(DISPLAYSURF,(0,0,0),((1045,260),(1092,210),(1140,260)))
	
	#left down arrow
	pygame.draw.rect(DISPLAYSURF, (0,0,0), (1055, 480, 75, 100))
	pygame.draw.polygon(DISPLAYSURF,(0,0,0),((1045,580),(1092,630),(1140,580)))
	
	#left arm angle left arrow
	pygame.draw.rect(DISPLAYSURF, (0,0,0), (1055, 690, -50, 20))
	pygame.draw.polygon(DISPLAYSURF,(0,0,0),((1005,685),(985,700),(1005,715)))
	
	#left arm angle right arrow
	pygame.draw.rect(DISPLAYSURF, (0,0,0), (1130, 690, 50, 20))
	pygame.draw.polygon(DISPLAYSURF,(0,0,0),((1180,685),(1200,700),(1180,715)))
	
	#right up arrow
	pygame.draw.rect(DISPLAYSURF, (0,0,0), (1450, 360, 75, -100))
	pygame.draw.polygon(DISPLAYSURF,(0,0,0),((1440,260),(1488,210),(1535,260)))
	
	#right down arrow
	pygame.draw.rect(DISPLAYSURF, (0,0,0), (1450, 480, 75, 100))
	pygame.draw.polygon(DISPLAYSURF,(0,0,0),((1440,580),(1488,630),(1535,580)))
	
	#right arm angle left arrow
	pygame.draw.rect(DISPLAYSURF, (0,0,0), (1450, 690, -50, 20))
	pygame.draw.polygon(DISPLAYSURF,(0,0,0),((1400,685),(1380,700),(1400,715)))
	
	#right arm angle right arrow
	pygame.draw.rect(DISPLAYSURF, (0,0,0), (1525, 690, 50, 20))
	pygame.draw.polygon(DISPLAYSURF,(0,0,0),((1575,685),(1595,700),(1575,715)))

def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

#Draws which pngs should be displayed
def drawIcons(state):
	if state == 1 :
		DISPLAYSURF.blit(back_row,(0,0))
		DISPLAYSURF.blit(bicep_curl,(280,0))
		DISPLAYSURF.blit(tricep_extention,(560,0))
		DISPLAYSURF.blit(chest_fly,(0,280))
		DISPLAYSURF.blit(chest_press,(280,280))
		DISPLAYSURF.blit(hip_extention,(560,280))
		DISPLAYSURF.blit(lat_pulldown,(0,560))
		DISPLAYSURF.blit(shoulder_cross,(280,560))
		DISPLAYSURF.blit(shoulder_pull,(560,560))
		return
	
	elif state == 2 :
		DISPLAYSURF.blit(chest_fly,(0,280))
		DISPLAYSURF.blit(chest_press,(280,280))
		return
	
	elif state == 3 :
		DISPLAYSURF.blit(back_row,(0,0))
		DISPLAYSURF.blit(lat_pulldown,(0,560))
		return
	elif state == 4 :
		DISPLAYSURF.blit(bicep_curl,(280,0))
		return
	elif state == 5 :
		DISPLAYSURF.blit(tricep_extention,(560,0))
		return
	elif state == 6 :
		DISPLAYSURF.blit(shoulder_cross,(280,560))
		DISPLAYSURF.blit(shoulder_pull,(560,560))
		return
	else :
		DISPLAYSURF.blit(hip_extention,(560,280))
		return

#gets what button or icon was pressed
def getLocation(x,y):	
	if 262 > x > 12 and 962 > y > 862:
		return 1, 1
	elif 519 > x > 269 and 962 > y > 862:
		return 1, 2
	elif 776 > x > 526 and 962 > y > 862:
		return 1, 3
	elif 1033 > x > 783 and 962 > y > 862:
		return 1, 4
	elif 1290 > x > 1040 and 962 > y > 862:
		return 1, 5
	elif 1547 > x > 1297 and 962 > y > 862:
		return 1, 6
	elif 1804 > x > 1554 and 962 > y > 862:
		return 1, 7
	elif 280 > x > 0 and 280 > y > 0:
		return 2, 0
	elif 560 > x > 280 and 280 > y > 0:
		return 2, 1
	elif 840 > x > 560 and 280 > y > 0:
		return 2, 2
	elif 280 > x > 0 and 560 > y > 280:
		return 2, 3
	elif 560 > x > 280 and 560 > y > 280:
		return 2, 4
	elif 840 > x > 560 and 560 > y > 280:
		return 2, 5
	elif 280 > x > 0 and 840 > y > 560:
		return 2, 6
	elif 560 > x > 280 and 840 > y > 560:
		return 2, 7
	elif 840 > x > 560 and 840 > y > 560:
		return 2, 8
	elif 1140 > x > 1045 and 360 > y > 210:
		return 3, 1.0
	elif 1140 > x > 1045 and 630 > y > 480:
		return 3, -1.0
	elif 1535 > x > 1440 and 360 > y > 210:
		return 4, 1.0
	elif 1535 > x > 1440 and 630 > y > 480:
		return 4, -1.0
	elif 1055 > x > 985 and 715 > y > 685:
		return 5, 1
	elif 1200 > x > 1130 and 715 > y > 685:
		return 5, -1
	elif 1450 > x > 1380 and 715 > y > 685:
		return 6, -1
	elif 1595 > x > 1525 and 715 > y > 685:
		return 6, 1
	else :
		return None, None

#draws the excercise thats been picked in the 
#middle of the arrows and the current arm angles
def drawSelection(val, leftAngle,rightAngle, lSide, rSide):
	
	DISPLAYSURF.blit(exercises[val],(1150,280))
	textSurfTitle, textRectTitle = text_objects(names[val], buttonText)
	textRectTitle.center = (1290,105)
	DISPLAYSURF.blit(textSurfTitle,textRectTitle)
	
	textSurfLeftArm, textRectLeftArm = text_objects(str(int(rightAngle)), buttonText)
	textRectLeftArm.center = (1092,420)
	DISPLAYSURF.blit(textSurfLeftArm,textRectLeftArm)
	
	textSurfRightArm, textRectRightArm = text_objects(str(int(leftAngle)), buttonText)
	textRectRightArm.center = (1488,420)
	DISPLAYSURF.blit(textSurfRightArm,textRectRightArm)
	
	
	textSurfFL, textRectFL = text_objects(str(lSide - 90), angleText)
	textRectFL.center = (1092,700)
	DISPLAYSURF.blit(textSurfFL,textRectFL)
	
	textSurfFR, textRectFR = text_objects(str(rSide - 90), angleText)
	textRectFR.center = (1488,700)
	DISPLAYSURF.blit(textSurfFR,textRectFR)
    
def getBoxAtPixel(boxx, boxy):
    for x in boardX:
        if boxx >= x and boxx <= (x+50):
            for y in boardY:
                if boxy >= y and boxy <= (y+80):
                    return (x,y)       
    return (None, None)


if __name__ == '__main__':
    main()












                     
