import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
MAX_DEPTH = 2

'''
Picks and returns a random valid move
'''
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

'''
Find the best move based on material alone
Greedy
'''
def findBestMoveGreedily(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkMate:
            score = turnMultiplier * CHECKMATE
        elif gs.staleMate:
            score = STALEMATE
        else:
            score = -turnMultiplier * scoreMaterial(gs.board)
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove

'''
Looking two moves into the future
'''
def findBestMove2(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    oppMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        oppMoves = gs.getValidMoves()
        oppMaxScore = -CHECKMATE
        if gs.staleMate:
            oppMaxScore = STALEMATE
        elif gs.checkMate:
            oppMaxScore = -CHECKMATE
        else:
            oppMaxScore = -CHECKMATE
            for oppMove in oppMoves:
                gs.makeMove(oppMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > oppMaxScore:
                    oppMaxScore = score
                gs.undoMove()
        if oppMinMaxScore > oppMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

'''
Helper method to make first recursive call
'''
def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    random.shuffle(validMoves)
    # findMoveNegaMax(gs, validMoves, MAX_DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, MAX_DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

'''
Recursive method with depth to calculate the best possible moves for a given depth value
'''
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove         # global because recursive function, so cannot just simply declare best move to keep track
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextValidMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextValidMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == MAX_DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextValidMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextValidMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == MAX_DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

'''
Simplifying the MinMax function usign NegaMax logic
'''
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore =  -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == MAX_DEPTH:
                nextMove = move
        gs.undoMove()

    return maxScore

'''
Applying alpha-beta pruning the function to minimize redundant calculations 
'''
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # move ordering - implement later
    maxScore =  -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == MAX_DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:    #pruning to cutoff redundant branches
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


'''
A positive score from this is good for white, a negative score is good for black.
'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE   # black wins
        else:
            return CHECKMATE    # white wins
    elif gs.staleMate:
        return 0    # neither side wins

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score

'''
Score the board based on material
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
