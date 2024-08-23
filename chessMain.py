# Driver file will handle user input and displaying the current gameState object
import pygame as p
import chessEngine,menu,itertools,pickle,time,copy,platform

GWIDTH = 960 #global width
GHEIGHT = 600 #global height
WIDTH = HEIGHT = 512
DIMENSION = 8  # dimensions of a chess board is 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
ospath =  '' if platform.system() == 'Darwin' else '.' #added to fix os relative path issue
def macToWindowPath(path : str):
    return path.replace('/',chr(92)) if ospath == '.' else path #can't use '\' as literal error occurs 
#Flag variables
specialMove = False
gameOver = False


#button class
class Button(): #creates a button from an image.
    def __init__(self,x,y,image,scale):
        width,height = image.get_width(),image.get_height()
        self.image = p.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self): #will be main function called in event loop
        pos = p.mouse.get_pos()
        action = False
        #check mouseover and clicked
        if self.rect.collidepoint(pos): #if we are hovering over the button
            if p.mouse.get_pressed()[0] == 1 and not self.clicked: #allows action to only be peformed once
                self.clicked = True
                action = True
        if p.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action #returns true or false which can then trigger the action via  if else statement
 
#UI Elements
statBoxLoc = p.Rect(550,20,360,225) #location of boxes
logBoxLoc = p.Rect(550,270,360,242)
exitImg = saveImg = playImg = pauseImg = None #initalising variables

#timer class
class Timer():
    def __init__(self,time : int):
        self.wtimeRemains = time #in seconds
        self.btimeRemains = copy.copy(time) #prevent linkage of variable due to assign by obj ref
        self.paused = False
        self.gameStarted = False


    def playTime(self,whiteToMove : bool):
        if (not self.paused) and self.gameStarted:
            if whiteToMove and self.wtimeRemains>0:
                self.wtimeRemains -= 1
            elif self.btimeRemains> 0: #tp22 | now stops decrementing when 0 is reached
                self.btimeRemains -= 1
        self.getTimes()
        return (self.wtimeRemains<=0,self.btimeRemains<=0) #return 2 bool flags to stop the game and output a winner by timeout

    def setPaused(self):
        self.paused = True #simply toggles the paused state.

    def setUnpaused(self):
        self.paused = False
    
    def startGame(self):
        self.gameStarted = True
    def getTimes(self): #return times in min:sec format
        return (f'{self.wtimeRemains//60}:{self.wtimeRemains%60}',f'{self.btimeRemains//60}:{self.btimeRemains%60}')
'''
initialise global dictionary of images. This will be called once in the main
'''


def loadImages(skinIndex):
    indextoSkin = {0:'default',1:'Pixel',2:'Madware'} #correct skin path
    global exitImg,saveImg,playImg,pauseImg
    pieces = ["bR", "bN", 'bB', 'bQ', 'bK',
              'bp', "wR", "wN", 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load( macToWindowPath(macToWindowPath(f'./Skins/{indextoSkin[skinIndex]}/{piece}.png'))), (SQ_SIZE, SQ_SIZE)) #folder parameter now included to change skin
    exitImg = p.image.load( macToWindowPath('./ReqImgs/exitButton.png'))
    saveImg = p.image.load( macToWindowPath('./ReqImgs/saveButton.png'))
    playImg = p.image.load( macToWindowPath('./ReqImgs/playButton.png'))
    pauseImg = p.image.load( macToWindowPath('./ReqImgs/pauseButton.png'))
# main driver and handle user input and update the graphics




def main(timerFlag : bool,logFlag :bool ,skinIndex: int,Loadedgs = None,trueActive = None,trueCool = None,uses = None,ready = None,timer = None,time1 = None): #rearranged so subroutine works for new and loaded games
    #inital setup before event loop
    p.init()
    global gameOver,screen,playerClick,sqSelected,specialMove,statBoxLoc,logBoxLoc,timeOn,gs,atimerFlag,alogFlag,turn,timerRun,timerObj,timeOut,st
    alogFlag = logFlag
    atimerFlag = timerFlag
    gameOver = False #not reset when a new game is made. |fixed during post development testing
    timerObj = object() #if disabled 
    timeOut = (False,False) #used to determine when time is up.
    timeOn = True#button variable
    screen = p.display.set_mode((GWIDTH, GHEIGHT)) #sets screen dimensions 
    clock = p.time.Clock() 
    gs = chessEngine.GameState(ready,trueActive,trueCool,uses) if Loadedgs == None else Loadedgs#calling the board from the engine to start a game. | loaded or new game
    turn = gs.whiteToMove
    timeUpdated = None #initialise
    if timerFlag: #initialise timer
        timerObj = Timer(600) if timer is None else timer #create new timer obj for new game or load pickled obj |500 seconds for now
        timeUpdated = True
        timeElapsed = 0
        st = 0
    screen.fill(p.Color('white') if gs.whiteToMove else p.Color('black'))
    validMoves = gs.getValidMoves() #generate the first set of valid moves
    moveMade = False  # flag variable to let the program know a move is made
    loadImages(skinIndex) #initialising images
    running = True 
    sqSelected = ()  # tracks last click of user (tuple)
    playerClick = []  # keeps track of player clicks (two tuples)
    #Initialising graphics
    initaliseGraphics(screen,gs)
    while running: #event loop
        if timerFlag: #backround of timer |needs to execute before buttons draw on
            timerGraphics(screen)
        for e in p.event.get(): #if user clicks red x then game should close
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN: #register the click location when the mouse is clicked
                if not gameOver:  
                    location = p.mouse.get_pos()  # (x,y) location of mouse
                    col = location[0]//SQ_SIZE #depending on the location, use the dimensions of each square on the board to 
                    row = location[1]//SQ_SIZE #determine where the user clicked in relation to the chess board,
                    if sqSelected == (row, col) and not specialMove:  #if the same square is clicked again it should reset UNLESS an apply move
                        sqSelected = ()
                        playerClick = []
                    else:
                        # append for both first and second clicks
                        sqSelected = (row, col)
                        playerClick.append(sqSelected)
                    if len(playerClick) == 2: #once two valid clicks have been registered the chess engine takes over.
                        if specialMove: #special moves are treated differently
                            if playerClick[0] == playerClick[1]: #an apply move type
                                for i in range(len(validMoves)):
                                    if validMoves[i].type in ['imp','teth','rein']: #all apply moves
                                        if playerClick[0] == (validMoves[i].startRow,validMoves[i].startCol): #validating move
                                            gs.makeMove(validMoves[i])
                                            print(validMoves[i].getChessNotation())
                                            moveMade = True
                                            specialMove = False
                                            playerClick = [] #reset player clicks for next move
                                            sqSelected = () 
                                            break
                            else: #interchange and relocate
                                for i in range(len(validMoves)):
                                    if validMoves[i].type in ['rel','int']: #defensive design (crashed here as apply move was compared here)
                                        if playerClick[0] == (validMoves[i].startRow,validMoves[i].startCol) and playerClick[1] == (validMoves[i].endRow,validMoves[i].endCol):         
                                            gs.makeMove(validMoves[i])
                                            print(validMoves[i].getChessNotation())
                                            moveMade = True #flag to allow the game to update the graphics
                                            specialMove = False
                                            playerClick = [] #reset player clicks for next move
                                            sqSelected = () 
                                            break

                        else:
                            for i in range(len(validMoves)):
                                if validMoves[i].type == 'standard':
                                    if playerClick[0] == (validMoves[i].startRow,validMoves[i].startCol) and playerClick[1] == (validMoves[i].endRow,validMoves[i].endCol):         
                                        gs.makeMove(validMoves[i])
                                        print(validMoves[i].getChessNotation())
                                        moveMade = True #flag to allow the game to update the graphics
                                        playerClick = [] #reset player clicks for next move
                                        sqSelected = () 
                                        break
                        if not moveMade: #no move is made and player will have to click again.
                            playerClick = [sqSelected] #takes the previous square clicked as the new first location click for QoL
            elif e.type == p.KEYDOWN: #undo move bind.
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                elif e.key == p.K_c: #pressing c switches between special moves and standard moves
                    specialMove = not specialMove
                    print(specialMove)

            if moveMade: 
                validMoves = gs.getValidMoves()
                moveMade = False
                screen.fill('white') if gs.whiteToMove else screen.fill('black') #dynamically switch bc to show players turn
                if timerFlag: #if timer is enabled
                    timerObj.startGame() #when first move is played | wont execute if timer wasn't initialised
                turn = gs.whiteToMove #flip for timer
                if logFlag: #if user wants moveLog on or off
                    drawMoveLogText(screen,gs)
                drawStatusText(screen,gs)
        drawGameState(screen, gs,sqSelected,validMoves,skinIndex)
        #checking for mate or stalemate | or timeout
        if gs.checkMate or gs.staleMate:
            gameOver = True
            
            text = 'Stalemate'if gs.staleMate else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate' #assign text to be printed
            print('text')
            drawText(screen,text)
        elif True in timeOut:
            text = 'Black wins due to Time Out' if timeOut[0] else 'White wins due to Time out' #text to be printed if timer runs out
            drawText(screen,text) #draws text if text is availible
            gameOver = True #ends game
        drawSpecialIndicator(screen,specialMove) #draws the text for the special indicator element

        #buttons
        if exitButton.draw():
            running = False #stop game
            p.quit()
            return 0
        if saveButton.draw(): #if button is pressed then peform action inside
            savePressed() #save file
        if timeOn and timerFlag: #timerFlag prevents button from being shown
            if pauseButton.draw(): #if button is pressed
                timeOn = False #timeOn draws the correct button
                timerObj.setPaused() #set timer object to pause
        elif timerFlag:
            if playButton.draw(): #set timer to unpause
                timeOn = True
                timerObj.setUnpaused() #now pauses and unpauses timer
        

        #timer updates
        if timerFlag: 
            if timeUpdated: #when a second has passed reset start time for the next second.
                st = time.time()
                timeUpdated = False
            if timeUpdated is None:
                pass
            else:
                timeElapsed = time.time() - st #measure elapsaed time since start time was updated
                # print(timeElapsed)
                if int(timeElapsed) == 1: #if one second has passed
                    timeOut = timerObj.playTime(turn) #make sure the correct turn decrements
                    timeUpdated = True #reset start time

        #updating graphics
        clock.tick(MAX_FPS) 
        p.display.flip() #


def drawBoard(screen,skinIndex): #draws the chequered design of the chess board
    indexTocolours = {0:[p.Color(238,238,213), p.Color(124,149,93)],1:[p.Color(230,234,216),p.Color(68,77,94)],2:[p.Color(201,219,250),p.Color(254,255,239)]} #board square colours
    colours = indexTocolours[skinIndex] 
    for r, c in itertools.product(range(DIMENSION), range(DIMENSION)): #creates an 8*8 matrix with each square containg a tuple representing its index
        color = colours[((r+c) % 2)] #alternates between white and grey for each square
        p.draw.rect(screen, color, p.Rect(
            c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) #draws a rectangle at the location specified by first 2 parameters with side lengths of the last 2 parameters


def drawPieces(screen, board): #draws the images onto the window using the image dictionary.
    colors = {'+' : p.Color('yellow'),'-' : p.Color('purple')} #colours for imp and tether
    colour = None
    s = p.Surface((SQ_SIZE,SQ_SIZE))
    s.set_alpha(100)
    for r, c in itertools.product(range(DIMENSION), range(DIMENSION)):
        piece = board[r][c][:2] #the third charatcer is not revelevant for this stage.
        if piece != '--':  # not empty square
            colour = colors.get(board[r][c][2]) 
            if colour != None:
                s.fill(colour) #highlight tether/impervious
                screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
                
            screen.blit(IMAGES[piece], p.Rect( #draws image onto the board
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def drawStatusText(screen,gs):
    global statBoxLoc
    indexToType = {0 : 'Impervious', 1:'Tether',2:'Triumvirate',3:'Interchange'}
    aM = gs.wAM if gs.whiteToMove else gs.bAM #pick out correct ability manager
    #convert from aM data to understandable text
    statusList = [] #append text to this list to then display
    data = aM.getStatusData()
    ready,cool,uses,active = data[0],data[1],data[2],data[3]
    for i in range(4):
        if ready[i]: #organise data into user friendly text
            statusList.append(f'{indexToType[i]} : ready! | {uses[i]} use(s) remain')
        else:
            if cool[i] > 0:
                statusList.append(f'{indexToType[i]} : {cool[i]} turns until ready | {uses[i]} use(s) remain')
        try:# try except statement as last 2 do not have active durations
            if active[i] != 0:
                statusList.append(f'{indexToType[i]} is active for {active[i]} turns')
        except IndexError:
            pass
    drawStatusBox(screen) #override old messages
    #rendering messages
    yLoc = 50
    font = p.font.SysFont("Connection II", 21 , False,False)
    colour = p.Color(229,250,252) 
    for message in statusList:
        screen.blit(font.render(message,5,colour),statBoxLoc.move(5,yLoc))
        yLoc += 25

def drawStatusBox(screen): #draws the main box
    global statBoxLoc
    p.draw.rect(screen,p.Color(27,67,150),statBoxLoc) #draw rectangle 
    font = p.font.SysFont("Connection II", 25 , False,False) 
    statTitle = font.render('Ability Status',5,p.Color(160,192,215)) #title text
    screen.blit(statTitle,statBoxLoc.move(180-statTitle.get_width()/2,0)) #applying title text | numbers inside move centre title
    

def drawGameState(screen, gs,sqSelected,validMoves,skinIndex):  # all board graphics in current game state
    drawBoard(screen,skinIndex)  # draw squares
    # add in piece highlighting or move suggestions
    highlightSquares(screen,gs,sqSelected,validMoves) #highlight squares
    drawPieces(screen, gs.board) #draws pieces onto board
    

def drawText(screen,txt): #draws all the text
    font = p.font.SysFont("Connection II", 54 , True,False) #set font
    textObj = font.render(txt,5,p.Color('Gray')) #render text
    textLoc = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObj.get_width()/2,HEIGHT/2 - textObj.get_height()/2) #place text in centre of board
    screen.blit(textObj,textLoc) #place onto screen
    textObj = font.render(txt,5,p.Color('Black')) #shadow effect double render
    screen.blit(textObj,textLoc.move(2,2))

def drawMoveLogBox(screen): 
    global logBoxLoc
    p.draw.rect(screen,p.Color(27,67,150),logBoxLoc)
    font = p.font.SysFont("Connection II", 25 , False,False) 
    logTitle = font.render('Move Log',5,p.Color(229,250,252))
    screen.blit(logTitle,logBoxLoc.move(180-logTitle.get_width()/2,0))
def drawMoveLogText(screen,gs):
    drawMoveLogBox(screen) #draw box
    font = p.font.SysFont("Connection II", 25 , False,False)
    colours = {True:p.Color('white'),False:p.Color('black')}
    moveLog = gs.moveLog 
    length = len(moveLog)
    if length == 0:  #no text to display
        return None
    moves = moveLog if length<8 else moveLog[-8:] #now displays last 8 moves
    i = 0 #go through list backwards to display them
    col = length%2 == 1 #if true then white is last element else black
    yLoc = 25
    for i in range(len(moves)-1,-1,-1): #go through list backwards to print moves in correct order
        screen.blit(font.render(moves[i].getChessNotation(),5,colours[col]),logBoxLoc.move(30,yLoc))
        yLoc+=25 #move down for next move
        col = not col #alternate colours


def drawSpecialIndicator(screen,specialMove):
    font = p.font.SysFont("Connection II", 25 , False,False)
    if specialMove:
        txt = 'Looking For Special Moves (Press C to Switch to Standard Moves)'
        txtObj = font.render(txt,5,p.Color("black"),p.Color(209,241,164))
    else:
        txt = 'Looking For Standard Moves (Press C to Switch to Special Moves)'
        txtObj = font.render(txt,5,p.Color("black"),p.Color('grey'))
    loc = p.Rect(200,580,txtObj.get_width(),txtObj.get_height())

    screen.blit(txtObj,loc)

def highlightSquares(screen,gs,sqSelected,validMoves):
    s = p.Surface((SQ_SIZE,SQ_SIZE))
    if sqSelected != ():
        r,c = sqSelected
        limits = range(8)
        if r in limits and c in limits:
            if not specialMove: #standard square highlighting
                if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
                    #highlight selected square blue
                    s.set_alpha(100) #transparency Val
                    s.fill(p.Color('blue')) #highlight square blue
                    screen.blit(s, (c*SQ_SIZE,r*SQ_SIZE))
                    #highlight possible standard moves
                    for move in validMoves:
                        s.fill(p.Color(53,32,201)) 
                        if move.startRow == r and move.startCol == c and move.type == 'standard': #highlight only standard moves availible
                            if move.pieceCaptured != '-- ': #if capture move then highlight red
                                s.fill(p.Color('red'))
                            screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE)) #using r*SqSize to place correctly.
            else:#special moves
                #highlight selected square green
                s.set_alpha(100) #transparency Val
                s.fill(p.Color('green'))
                screen.blit(s, (c*SQ_SIZE,r*SQ_SIZE))
                #highlight possible special moves
                for move in validMoves:
                    match gs.board[r][c][1]:
                        case 'K': #rein moves have no connection to piece selected
                            if move.type == 'rein': # if king selected the rein moves should be highlighted
                                screen.blit(s, (move.startCol*SQ_SIZE,move.startRow*SQ_SIZE)) 
                        case 'B':#teth moves also have no connection to the piece selected (will show all tether moves for both bishops | can be considered a bug or feature)
                                if move.type == 'teth': # if king selected the rein moves should be highlighted
                                    screen.blit(s, (move.startCol*SQ_SIZE,move.startRow*SQ_SIZE)) 

                    if move.startRow == r and move.startCol == c and move.type != 'standard': 
                        try:
                            screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE)) #non apply moves
                        except AttributeError: #apply moves do not have an endRow attribute
                            pass
    #highlight king if in check
    s.fill(p.Color('red'))
    if gs.whiteToMove: #so we know which king to highlight
        if gs.inCheck():
            screen.blit(s,(gs.whiteKingLocation[1]*SQ_SIZE,gs.whiteKingLocation[0]*SQ_SIZE))
    elif gs.inCheck():
        screen.blit(s,(gs.blackKingLocation[1]*SQ_SIZE,gs.blackKingLocation[0]*SQ_SIZE))
            

def initaliseGraphics(screen,gs):
    global exitButton,saveButton,playButton,pauseButton
    drawMoveLogText(screen,gs)
    drawStatusText(screen,gs)
    #creating button instances
    exitButton = Button(20,516,exitImg,0.5)
    saveButton = Button(104,516,saveImg,1)
    playButton = Button(705,520,playImg,0.5)
    pauseButton = Button(705,520,pauseImg,0.5)

#savefile
def savePressed(): 
    global timerObj,st,saveQuad
    if atimerFlag: #if timer enabled
        timerObj.gameStarted = False #ready for when game resumes
    else:
        timerObj = None
    saveQuad = [gs,atimerFlag,alogFlag,timerObj]
    savePath = menu.openFolder() #get path from pyqt file explorer
    if savePath is None: #if cancel is pressed
        return 0
    savePath += '.savefile' #add extension
    with open(savePath, 'wb') as file: #save gameState object
        pickle.dump(saveQuad,file)
    file.close()
    if atimerFlag: #if timer enabled
        timerObj.gameStarted = True #dont affect current game as it continues
        st = time.time() #resetting st

#timer graphics
def timerGraphics(screen): #draws the timer graphics onto the screen
    global timerObj #uses the time object to get the time remaning
    timerBoxLoc = p.Rect(660-70,525,100,40)
    timerBc = p.Rect(650-70,520,300,50)
    p.draw.rect(screen,p.Color(172,70,64),timerBc,border_radius=5)
    p.draw.rect(screen,p.Color('white'),timerBoxLoc,3,5)
    p.draw.rect(screen,p.Color('black'),timerBoxLoc.move(180,0),3,5)
    font = p.font.SysFont("Connection II", 30 , False,False)
    wtxt,btxt = timerObj.getTimes()
    wtxtRender = font.render(wtxt,5,p.Color('white'))
    btxtRender = font.render(btxt,5,p.Color('black'))
    screen.blit(wtxtRender,timerBoxLoc.move(30,10))
    screen.blit(btxtRender,timerBoxLoc.move(210,10))

    





