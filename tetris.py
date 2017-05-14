#tetris.py
#Andrew Zadravec azadrave Section C

import random 
from Tkinter import *

def run(rows, cols):
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
    canvas.data.height=canvasHeight
    canvas.data.width=canvasWidth
    canvas.data.rows=rows
    canvas.data.cols=cols
    canvas.data.blockSideLength=blockSideLength
    init()
    # set up events
    #root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop() 

def init():
    canvas.data.isGameOver=False
    canvas.data.score=0
    cols=canvas.data.cols
    rows=canvas.data.rows
    canvas.data.board=[(["blue"]*cols) for row in xrange(rows)]
    board=canvas.data.board
    canvas.data.tetrisPieces=tetrisPieces()
    tetrisPieceColors=[ "red", "yellow", "magenta", "pink", "cyan", "green",
                       "orange" ]
    canvas.data.tetrisPieceColors=tetrisPieceColors
    newFallingPiece()
    redrawAll()

def timerFired():
    if (canvas.data.isGameOver==False):
	moveFallingPiece(canvas, +1, 0)
	if not(moveFallingPiece(canvas, +1, 0)):
	    placeFallingPiece()
	    newFallingPiece()
	    if not(fallingPieceIsLegal()):
	        canvas.data.isGameOver=True
	else:
	    moveFallingPiece(canvas, +1, 0)
    redrawAll()
    delay=500 #milliseconds
    canvas.after(delay, timerFired)
    
def redrawAll():
    canvas.delete(ALL)
    drawGame()
    drawScore()
    if (canvas.data.isGameOver==True):
	canvasWidth=canvas.data.width
	canvasHeight=canvas.data.height
	canvas.create_text(canvasWidth/2, canvasHeight/2, text="Game Over!",
			   font="Helvetica 48 bold")
	
def drawScore():
    width=canvas.data.width
    height=canvas.data.height
    score=canvas.data.score
    canvas.create_text(.8*width,.03*height, text="Score: "+str(score), font="Helvetica 20")

def drawGame():
    width=canvas.data.width
    height=canvas.data.height
    canvas.create_rectangle(0, 0, width, height, fill="orange")
    drawBoard()
    drawFallingPiece()
    
def drawFallingPiece():
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
    removeFullRows()

def drawBoard():
    cols=canvas.data.cols
    rows=canvas.data.rows
    board=canvas.data.board
    for row in xrange(rows):
        for col in xrange(cols):
            color=board[row][col]
            drawCell(canvas, row, col, color)

def drawCell(canvas, row, col, color):
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
    [ True,  True,  True,  True]]
  jPiece = [
    [ True, False, False ],
    [ True, True,  True]]
  lPiece = [
    [ False, False, True],
    [ True,  True,  True]]
  oPiece = [
    [ True, True],
    [ True, True]]
  sPiece = [
    [ False, True, True],
    [ True,  True, False ]]
  tPiece = [
    [ False, True, False ],
    [ True,  True, True]]
  zPiece = [
    [ True,  True, False ],
    [ False, True, True]]
  return [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]

def newFallingPiece():
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

def moveFallingPiece(canvas, drow, dcol):
    canvas.data.fallingPieceRow+=drow
    canvas.data.fallingPieceCol+=dcol
    if not fallingPieceIsLegal():
        canvas.data.fallingPieceRow-=drow
        canvas.data.fallingPieceCol-=dcol
        return False
    return True

def fallingPieceIsLegal():
    fallingPiece=canvas.data.fallingPiece
    rowsInPiece=len(fallingPiece)
    colsInPiece=len(fallingPiece[0])
    emptyColor="blue"
    board=canvas.data.board
    rows=len(board)
    cols=len(board[0])
    for pieceRow in xrange(rowsInPiece):
        for pieceCol in xrange(colsInPiece):
	    if (fallingPiece[pieceRow][pieceCol]==True):
	        rowOnBoard=canvas.data.fallingPieceRow+pieceRow
		colOnBoard=canvas.data.fallingPieceCol+pieceCol
		if (rowOnBoard<0 or rowOnBoard>=rows or colOnBoard<0
		    or colOnBoard>=cols):
		    return False
		if (board[rowOnBoard][colOnBoard]!=emptyColor):
		    return False
    return True
                    
def keyPressed(event):
    if (event.char=="r"):
        init()
    if (canvas.data.isGameOver==False):
	if (event.keysym=="Down"):
	    moveFallingPiece(canvas, 1, 0)
	elif (event.keysym=="Right"):
	    moveFallingPiece(canvas, 0, 1)
	elif (event.keysym=="Left"):
	    moveFallingPiece(canvas, 0, -1)
	elif (event.keysym=="Up"):
	    rotateFallingPiece()

def fallingPieceCenter(canvas):
    fallingPiece=canvas.data.fallingPiece
    fallingPieceRow=canvas.data.fallingPieceRow
    fallingPieceCol=canvas.data.fallingPieceCol
    fallingPieceRows=len(fallingPiece)
    fallingPieceCols=len(fallingPiece[0])
    fallingPieceCenterRow=fallingPieceRow+fallingPieceRows/2
    fallingPieceCenterCol=fallingPieceCol+fallingPieceCols/2
    return (fallingPieceCenterRow, fallingPieceCenterCol)
    
def rotateFallingPiece():
    oldPiece=canvas.data.fallingPiece
    (oldCenterRow, oldCenterCol)=fallingPieceCenter(canvas)
    fallingPiece=canvas.data.fallingPiece
    rowsInPiece=len(fallingPiece)
    colsInPiece=len(fallingPiece[0])
    fallingPieceRow=canvas.data.fallingPieceRow
    fallingPieceCol=canvas.data.fallingPieceCol
    rotateRows=colsInPiece
    rotateCols=rowsInPiece
    rotatePiece=createRotatedPiece(rowsInPiece, colsInPiece)
    canvas.data.fallingPiece=rotatePiece
    (newCenterRow, newCenterCol)=fallingPieceCenter(canvas)
    #translate the piece's row and col on the board
    canvas.data.fallingPieceRow+=(oldCenterRow-newCenterRow)
    canvas.data.fallingPieceCol+=(oldCenterCol-newCenterCol)
    if (not fallingPieceIsLegal()):
        canvas.data.fallingPiece=oldPiece
        canvas.data.fallingPieceRow-=(oldCenterRow-newCenterRow)
        canvas.data.fallingPieceCol-=(oldCenterRow-newCenterRow)

def createRotatedPiece(rowsInPiece, colsInPiece):
    fallingPiece=canvas.data.fallingPiece
    rotatePiece=[]
    for col in xrange(colsInPiece-1, -1, -1):
	rotatePieceRow=[]
	for row in xrange(rowsInPiece):
	    rotatePieceRow=rotatePieceRow+[fallingPiece[row][col]]
	rotatePiece=rotatePiece+[rotatePieceRow]
    return rotatePiece

def removeFullRows():
    board=canvas.data.board
    emptyColor="blue"
    rows=len(board)
    cols=len(board[0])
    rowsFilled=0
    newRow=rows-1
    for oldRow in xrange(rows-1, -1, -1):
	if not(isFullRow(board[oldRow], emptyColor)):
	    for col in xrange(cols):
		board[newRow][col]=board[oldRow][col]
	    newRow-=1
	else:
	    rowsFilled+=1
    if (rowsFilled>0):
	for row in xrange(newRow):
	    for col in xrange(cols):
		board[row][col]=emptyColor
    scoreIncrease=rowsFilled**2
    canvas.data.score+=scoreIncrease

def isFullRow(row, emptyColor):
    cols=len(row)
    for col in xrange(cols):
	if (row[col]==emptyColor):
	    return False
        return True
run(15, 10)