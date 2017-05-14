import random 
from Tkinter import *
import time
import sys

def run():
    argCount = len(sys.argv)
    if argCount >= 3:
        rows = int(sys.argv[1])
        cols = int(sys.argv[2])
    else:
        # use standard Tetris game board size if args not provided
        rows = 20
        cols = 10
    
    # set delay between timed events in milliseconds
    # set number of delays to wait before moving a falling piece down
    if argCount == 5:
        delay = int(sys.argv[3])
        intervals = int(sys.argv[4])
    else:
        delay = 25
        intervals = 10

    # create the root and the canvas
    global canvas
    root = Tk()
    blockSideLength=30
    canvasHeight=rows*blockSideLength+60
    canvasWidth=cols*blockSideLength+60
    canvas = Canvas(root, height=canvasHeight, width=canvasWidth)
    canvas.pack()
    root.resizable(width=0, height=0)
    
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.delay = delay
    canvas.data.intervals = intervals
    canvas.data.master = root
    canvas.data.height=canvasHeight
    canvas.data.width=canvasWidth
    canvas.data.rows=rows
    canvas.data.cols=cols
    canvas.data.scoreY = 15
    canvas.data.blockSideLength=blockSideLength
    init()
    
    # set up events
    root.bind("<Key>", keyPressed)
    timerFired()
    
    root.mainloop() 

def init():
    # initialize canvas data values for game state
    canvas.data.isGameOver=False
    canvas.data.score=0
    cols=canvas.data.cols
    rows=canvas.data.rows
    
    canvas.data.board=[(["blue"]*cols) for row in xrange(rows)]
    canvas.data.emptyColor = "blue"
    
    canvas.data.tetrisPieces=tetrisPieces()
    tetrisPieceColors=[ "red", "yellow", "magenta", "pink", "cyan", "green",
                       "orange" ]
    canvas.data.tetrisPieceColors=tetrisPieceColors

    # now make the first piece fall and draw the game on the tk canvas
    newFallingPiece()
    redrawAll()

def timerFired(counter=0):
    # draw the game while moving the current piece downward periodically
    if (canvas.data.isGameOver==False and counter % canvas.data.intervals == 0):
        moveFallingPiece(1, 0)
        if not(fallingPieceIsLegal()):
            canvas.data.isGameOver=True
    
    redrawAll()
    delay=canvas.data.delay #milliseconds
    canvas.after(delay, lambda: timerFired(counter+1))
    
def redrawAll():
    # update the appearance of the game
    canvas.delete(ALL)
    drawGame()
    drawScore()
    if (canvas.data.isGameOver==True):
        canvasWidth=canvas.data.width
        canvasHeight=canvas.data.height
        canvas.create_text(canvasWidth/2, canvasHeight/3, text="Game Over!",
               font="Helvetica 24 bold")
    
def drawScore():
    #draw the current score in the upper right corner
    width=canvas.data.width
    height=canvas.data.height
    score=canvas.data.score
    canvas.create_text(.7*canvas.data.width, canvas.data.scoreY, 
      text="Score: "+str(score), font="Helvetica 20")

def drawGame():
    # draw the orange background, the board, and the current falling piece
    width=canvas.data.width
    height=canvas.data.height
    canvas.create_rectangle(0, 0, width, height, fill="orange")
    drawBoard()
    drawFallingPiece()
    
def drawFallingPiece():
    #draw the piece that is currently falling onto the game board
    if (canvas.data.isGameOver==True):
        return
    
    fallingPiece=canvas.data.fallingPiece
    fallingPieceRows=len(fallingPiece)
    fallingPieceCols=len(fallingPiece[0])
    fallingPieceRow=canvas.data.fallingPieceRow
    fallingPieceCol=canvas.data.fallingPieceCol
    
    for row in xrange(fallingPieceRows):
        for col in xrange(fallingPieceCols):
            if (fallingPiece[row][col]==True):
                cellRow=row+fallingPieceRow
                cellCol=col+fallingPieceCol
                color=canvas.data.fallingPieceColor
                drawCell(canvas, cellRow, cellCol, color)

def placeFallingPiece():
    # place a falling piece when another piece or the board edge stops it
    emptyColor="blue"
    fallingPiece=canvas.data.fallingPiece
    fallingPieceRows=len(fallingPiece)
    fallingPieceCols=len(fallingPiece[0])
    color=canvas.data.fallingPieceColor
    board=canvas.data.board
    fallingPieceRow=canvas.data.fallingPieceRow
    fallingPieceCol=canvas.data.fallingPieceCol
    
    for row in xrange(fallingPieceRows):
        for col in xrange(fallingPieceCols):
            if (fallingPiece[row][col]==True):
                board[row+fallingPieceRow][col+fallingPieceCol]=color

    # now check for and remove full rows, then make a new falling piece
    removeFullRows()
    newFallingPiece()

def drawBoard():
    #draw the board and all currently placed pieces
    cols=canvas.data.cols
    rows=canvas.data.rows
    board=canvas.data.board
    
    for row in xrange(rows):
        for col in xrange(cols):
            color=board[row][col]
            drawCell(canvas, row, col, color)

def drawCell(canvas, row, col, color):
    #draw an individual cell on the board in the proper position on canvas
    blockLength=canvas.data.blockSideLength
    margin=1
    boardMargin=30
    
    cornerX=boardMargin+col*blockLength
    cornerY=boardMargin+row*blockLength
    lowerX=cornerX+blockLength
    lowerY=cornerY+blockLength
    
    canvas.create_rectangle(cornerX, cornerY, lowerX, lowerY, fill="black")
    canvas.create_rectangle(cornerX+margin, cornerY+margin, lowerX-margin,
                            lowerY-margin, fill=color)
def tetrisPieces():
    #Seven "standard" pieces (tetrominoes)
    iPiece = [
    [True, True, True, True]]
    jPiece = [
    [True, False, False],
    [True, True, True]]
    lPiece = [
    [False, False, True],
    [True, True, True]]
    oPiece = [
    [True, True],
    [True, True]]
    sPiece = [
    [False, True, True],
    [True, True, False ]]
    tPiece = [
    [False, True, False],
    [True, True, True]]
    zPiece = [
    [True, True, False],
    [False, True, True]]
    
    return [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]

def newFallingPiece():
    # choose a random piece type to be the new falling piece and update
    # canvas data to track its position
    board=canvas.data.board
    cols=len(board[0])
    tetrisPieces=len(canvas.data.tetrisPieces)
    randomIndex=random.randint(0, tetrisPieces-1)
    
    canvas.data.fallingPiece=canvas.data.tetrisPieces[randomIndex]
    canvas.data.fallingPieceColor=canvas.data.tetrisPieceColors[randomIndex]
    canvas.data.fallingPieceRow=0
    fallingPieceCols=0
    
    for row in canvas.data.fallingPiece:
        if (len(row)>fallingPieceCols):
            fallingPieceCols=len(row)
    
    canvas.data.fallingPieceCol=cols/2-fallingPieceCols/2

def moveFallingPiece(drow, dcol):
    # move the falling piece down, right, or left in response to keypress 
    # or timer
    newFallingRow = canvas.data.fallingPieceRow + drow
    newFallingCol = canvas.data.fallingPieceCol + dcol
    
    if fallingPieceIsLegal(canvas.data.fallingPiece, newFallingRow, 
      newFallingCol):
        canvas.data.fallingPieceRow+=drow
        canvas.data.fallingPieceCol+=dcol
        return True
    
    if drow > 0 and dcol == 0:
        canvas.data.master.unbind("<Key>")
        placeFallingPiece()
        canvas.update()
        canvas.data.master.bind("<Key>", keyPressed)
    
    return False

def fallingPieceIsLegal(fallingPiece=None, fallingPieceRow=None, 
    fallingPieceCol=None):
    # check whether a given piece or the falling piece is legal on the current 
    # board, meaning it doesn't intersect other pieces or cross over the edge
    if not fallingPiece:
        fallingPiece = canvas.data.fallingPiece
        fallingPieceRow = canvas.data.fallingPieceRow
        fallingPieceCol = canvas.data.fallingPieceCol
    
    rowsInPiece=len(fallingPiece)
    colsInPiece=len(fallingPiece[0])
    emptyColor="blue"
    board=canvas.data.board
    rows=len(board)
    cols=len(board[0])
    
    for pieceRow in xrange(rowsInPiece):
        for pieceCol in xrange(colsInPiece):
            if (fallingPiece[pieceRow][pieceCol]==True):
                rowOnBoard=fallingPieceRow+pieceRow
                colOnBoard=fallingPieceCol+pieceCol
                if (rowOnBoard<0 or rowOnBoard>=rows or colOnBoard<0
                  or colOnBoard>=cols):
                    return False
                if (board[rowOnBoard][colOnBoard]!=emptyColor):
                    return False
    return True
                    
def keyPressed(event):
    # direct keypresses to appropriate handlers
    if (event.char=="r"):
        init()
    
    if (canvas.data.isGameOver==False):
        if (event.keysym=="Down"):
            moveFallingPiece(1, 0)
        elif (event.keysym=="Right"):
            moveFallingPiece(0, 1)
        elif (event.keysym=="Left"):
            moveFallingPiece(0, -1)
        elif (event.keysym=="Up"):
            rotateFallingPiece()

def fallingPieceCenter(fallingPiece=None):
    # get the center row and center column of a given piece or the falling 
    # piece - important because piece is rotated about this center
    if not fallingPiece:
        fallingPiece=canvas.data.fallingPiece
    
    fallingPieceRow=canvas.data.fallingPieceRow
    fallingPieceCol=canvas.data.fallingPieceCol
    fallingPieceRows=len(fallingPiece)
    fallingPieceCols=len(fallingPiece[0])
    
    fallingPieceCenterRow=fallingPieceRow+fallingPieceRows/2
    fallingPieceCenterCol=fallingPieceCol+fallingPieceCols/2

    return (fallingPieceCenterRow, fallingPieceCenterCol)

def rotateFallingPiece():
    # rotate the current falling piece if the rotated piece is legal on board
    (oldCenterRow, oldCenterCol)=fallingPieceCenter()
    fallingPiece=canvas.data.fallingPiece
    rowsInPiece=len(fallingPiece)
    colsInPiece=len(fallingPiece[0])
    fallingPieceRow=canvas.data.fallingPieceRow
    fallingPieceCol=canvas.data.fallingPieceCol
    
    rotatePiece=createRotatedPiece(rowsInPiece, colsInPiece)
    (newCenterRow, newCenterCol)=fallingPieceCenter(rotatePiece)

    if rowsInPiece == 4 and colsInPiece == 1:
        newFallingRow = fallingPieceRow+2
        newFallingCol = fallingPieceCol-2
    elif rowsInPiece == 1 and colsInPiece == 4:
        newFallingRow = fallingPieceRow-2
        newFallingCol = fallingPieceCol+2
    else:
        newFallingRow = fallingPieceRow + newCenterRow - oldCenterRow
        newFallingCol = fallingPieceCol + newCenterCol - oldCenterCol
    
    #translate the piece's row and col on the board if it is legal
    if fallingPieceIsLegal(rotatePiece, newFallingRow, newFallingCol):
        canvas.data.fallingPiece=rotatePiece
        canvas.data.fallingPieceRow = newFallingRow
        canvas.data.fallingPieceCol = newFallingCol

def createRotatedPiece(rowsInPiece, colsInPiece):
    # make a list representing the falling piece rotated once
    fallingPiece=canvas.data.fallingPiece
    rotatePiece=[]
    
    for col in xrange(colsInPiece-1, -1, -1):
        rotatePieceRow=[]
        for row in xrange(rowsInPiece):
            rotatePieceRow=rotatePieceRow+[fallingPiece[row][col]]
        rotatePiece=rotatePiece+[rotatePieceRow]
    
    return rotatePiece

def removeFullRows():
    # check for and remove full rows, then update score accordingly
    rowsFilled = 0
    board = [row[:] for row in canvas.data.board]
    
    for rowIdx in xrange(canvas.data.rows):
        if not isFullRow(board[rowIdx]):
            if rowsFilled > 0:
                canvas.data.board[rowIdx-rowsFilled] = board[rowIdx]
        else:
            emptyRow = [canvas.data.emptyColor]*canvas.data.cols
            canvas.data.board[rowIdx-rowsFilled] = emptyRow
            rowsFilled += 1

    canvas.data.score += rowsFilled**2

def isFullRow(row):
    # return whether the row is full
    for col in row:
        if (col==canvas.data.emptyColor):
            return False
    return True

if __name__ == '__main__':
    run()