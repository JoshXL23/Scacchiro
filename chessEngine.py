# This class is responsible for storing all the information about the current state of a chess game. will also be responsible for determining the valid moves. also going to have a move log.


# move classes


class ApplyMove():  # used for moves which inflict something like impervious, tether and reincarnation
    def __init__(self, startSq, board, atype):
        self.startRow = startSq[0]  # only use a start square
        self.startCol = startSq[1]
        # know what piece is being moved
        self.pieceMoved = board[self.startRow][self.startCol]
        self.type = atype  # know the type of move
        self.ranksToRows = {'1': 7, "2": 6, '3': 5, '4': 4,  # dictionary helps get chess notation
                            '5': 3, '6': 2, '7': 1, '8': 0}
        self.rowsToRanks = {v: k for k, v in self.ranksToRows.items()}
        self.filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                            'e': 4, 'f': 5, 'g': 6, 'h': 7, }
        self.colsToFiles = {v: k for k, v in self.filesToCols.items()}

    def getChessNotation(self):  # used for printing out moves in movelog
        return f'{self.getRankFile(self.startRow, self.startCol)}, {self.pieceMoved} ({self.type})'

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


class basicMove(ApplyMove):
    # requires an endsquare like all basic moves in chess
    def __init__(self, startSq, board, atype, endSq):
        super().__init__(startSq, board, atype)
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):  # method overriding
        return f'{self.getRankFile(self.startRow, self.startCol)},{self.pieceMoved} --> {self.getRankFile(self.endRow, self.endCol)}, {self.pieceCaptured} ({self.type})'


class Move(basicMove):  # takes into consideration specail types of standard moves
    def __init__(self, startSq, board, atype, endSq, isEnpassantMove=False, isCastlingMove=None):
        super().__init__(startSq, board, atype, endSq)
        # flagged moves
        self.isPawnPromotion = (self.pieceMoved == 'wp ' and self.endRow == 0) or (
            self.pieceMoved == 'bp ' and self.endRow == 7)  # pawn promotion
        self.isEnpassantMove = isEnpassantMove
        self.isCastlingMove = isCastlingMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp ' if self.pieceMoved == 'bp ' else 'bp '


class AbilityManager():  # manages abilities for each player and regulates when they can be used
    def __init__(self, aready, acool, auses, aactive, trueCool, trueAct):
        self.ready = aready
        self.cooldown = acool
        self.uses = auses
        self.active = aactive
        self.trueActive = trueAct
        self.trueCool = trueCool
        self.typeToIndex = {'imp': 0, 'teth': 1,
                            'rel': 2, 'rec': 2, 'rein': 2, 'int': 3}
        self.nUsesAt = {}  # added in v3
        self.coolHitZeroAt = {}  # added in v3
        self.activeHitZeroAt = {}  # added in v3

    def getStatusData(self):
        return (self.ready, self.cooldown, self.uses, self.active)

    def setReady(self, i):  # when a cooldown has finished
        if self.uses[i] > 0:  # is now greater than 0 rather than not equal to for robustness
            self.ready[i] = True

    def setActive(self, type, nMoves):  # ver 3 when an ability is casted
        deactivateAt = None
        i = self.typeToIndex[type]
        # decrements uses and returns a bool if the ability can refresh or not
        refresh = self.decrementUses(i, nMoves)
        if i > 1:
            if refresh:
                self.cooldown[i] = self.trueCool[i]
        else:  # moves with active durations
            self.active[i] = self.trueActive[i]  # make active
            # predicting deactivation turn
            deactivateAt = nMoves + (self.trueActive[i]*2)
            # predicting when active hits 0
            self.activeHitZeroAt[i] = deactivateAt
        self.ready[i] = False
        return deactivateAt  # appending to deActOrder

    def updateCooldowns(self, nMoves):
        for x in range(len(self.cooldown)):
            match self.cooldown[x]:  # ver 3 using match case
                case 1:  # ability is ready (hitting 0)
                    self.cooldown[x] = 0
                    # update the dict so if undoing we know when cooldown hit 0
                    self.coolHitZeroAt[x] = nMoves
                    self.setReady(x)
                case 0:  # nothing happens (cooldown has been at 0 for some time)
                    pass
                case _:
                    # every other case cooldown decreases by 1
                    self.cooldown[x] -= 1

    # ver 2 | now a procedure, no longer helps game state determine deactivations
    def updateActive(self):
        for x in range(len(self.active)):
            match self.active[x]:
                case 1:  # move deactivating on this turn
                    self.active[x] = 0  # set = 0
                    if self.uses[x] > 0:  # refresh if uses availible
                        self.cooldown[x] = self.trueCool[x]
                    else:  # required due to strange bug
                        pass
                case 0:  # do nothing if already at 0
                    pass
                case _:  # decrement for all other cases
                    self.active[x] -= 1

    def decrementUses(self, i, nMoves):  # new to v3 more robust method of decrementing uses
        match self.uses[i]:
            case 1:  # last use
                self.uses[i] = 0
                # add to dict to help undo moves at correct stage in game.
                self.nUsesAt[i] = nMoves
                return True
            case 0:  # return False to prevent cooldown refresh
                return False
            case _:  # default case reduce number of uses by 1
                self.uses[i] -= 1
                return True

    # new to v3 more robust method of incrementning uses
    def incrementUses(self, i, nMoves):
        if self.uses[i] == 0:
            if self.nUsesAt.get(i) == nMoves + 1:  # uses hit zero on this turn
                self.nUsesAt.pop(i)
                self.uses[i] += 1  # increment
                return True
            return False  # if on 0 for a second turn do not increment.
        else:  # all other cases
            self.uses[i] += 1
            return True


   def undoCooldowns(self, nMoves):
        for i in range(len(self.cooldown)):
            class Vars:  # required due to match case syntax error
                h = self.trueCool[i]
            match self.cooldown[i]:
                case 0:
                    # ability was just made ready |adding 1 to fix error in tp20
                    if self.coolHitZeroAt.get(i) == nMoves+1:
                        self.ready[i] = False
                        self.coolHitZeroAt.pop(i)
                        self.cooldown[i] = 1
                    else:
                        pass

                case Vars.h:  # ability just finished duration or was casted
                    self.cooldown[i] = 0  # reset to 0
                    if i > 1:  # if not a duraiton based move
                        self.ready[i] = True  # reset stats to pre special move
                        if not self.incrementUses(i, nMoves):
                            # should not return false otherwise error
                            raise BaseException('Uses Error')
                    else:
                        pass
                case _:
                    # all other cases just add 1 to cooldown
                    self.cooldown[i] += 1

    def undoActive(self, nMoves):
        for i in range(len(self.active)):
            class Vars:
                trueAct = self.trueActive[i]

            match self.active[i]:
                case 0:
                    # if move was deactivated on this turn | +1 to fix error in tp20
                    if self.activeHitZeroAt.get(i) == nMoves+1:
                        # removed pop state from here as it is neccessary to prevent bug| tp20
                        self.active[i] += 1
                    else:
                        pass
                case Vars.trueAct:  # move was casted and needs to be deactivated on this turn
                    self.active[i] = 0
                    self.activeHitZeroAt.pop(i)
                    self.incrementUses(i, nMoves)
                    self.ready[i] = True
                case _:
                    # all other cases add 1 to active state
                    self.active[i] += 1

    def moveMade(self, nMoves):
        self.updateCooldowns(nMoves)
        self.updateActive()  # does not require nMoves

    def undoMoveMade(self, nMoves):
        self.undoCooldowns(nMoves)
        self.undoActive(nMoves)


class GameState():  # houses all the game logic

    def __init__(self, ready, trueActive, trueCool, uses):
        # board is a 8*8 2D list with each element of the list having 2 characters, first character represents colour with b or w and the second represents type. '-- ' represents empty space
        # fix pass by reference error in tp21
        bUses = uses.copy()
        bReady = ready.copy()
        self.board = [
            ['bR ', 'bN ', 'bB ', 'bQ ', 'bK ', 'bB ', 'bN ', 'bR '],
            ['bp ', 'bp ', 'bp ', 'bp ', 'bp ', 'bp ', 'bp ', 'bp '],
            ['-- ', '-- ', '-- ', '-- ', '-- ', '-- ', '-- ', '-- '],
            ['-- ', '-- ', '-- ', '-- ', '-- ', '-- ', '-- ', '-- '],
            ['-- ', '-- ', '-- ', '-- ', '-- ', '-- ', '-- ', '-- '],
            ['-- ', '-- ', '-- ', '-- ', '-- ', '-- ', '-- ', '-- '],
            ['wp ', 'wp ', 'wp ', 'wp ', 'wp ', 'wp ', 'wp ', 'wp '],
            ["wR ", "wN ", 'wB ', 'wQ ', 'wK ', 'wB ', 'wN ', 'wR ']]
        # self.moveFunctions = {'p' :lambda a,b,c:self.getPawnMoves(a,b,c), 'R': lambda a,b,c:self.getRookMoves(a,b,c), 'N':lambda a,b,c:self.getKnightMoves(a,b,c),
        #                       'B': lambda a,b,c:self.getBishopMoves(a,b,c), 'Q': lambda a,b,c:self.getQueenMoves(a,b,c), 'K': lambda a,b,c,d:self.getKingMoves(a,b,c,d)}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()  # co-ords of the square where it is possible
        self.bKMoved = self.wkMoved = self.wRRMoved = self.wRLMoved = self.bRRMoved = self.bRLMoved = False
        self.firstMoved = []
        # added in tp13 to fix reactivation issue |ver 2 addition | ver 3 - changed to a dict
        self.deActOrder = {}
        self.recolBuffer = []
        self.wAM = AbilityManager(ready, [0, 0, 0, 0], uses, [0, 0], tuple(
            trueCool), tuple(trueActive))  # added for smoother integration
        self.bAM = AbilityManager(bReady, [0, 0, 0, 0], bUses, [0, 0], tuple(
            trueCool), tuple(trueActive))  # added for smoother integration
# move handlers

    def makeMove(self, move):

        if move.type != 'standard':
            self.makeSpMove(move)
            return None
        # fixed in tp13 strings updated to new convention
        # remove the piece from its starting square
        self.board[move.startRow][move.startCol] = '-- '
        # place the piece at its ending square
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # tracking all moves made in game so far
        # update the locations of the kings so the checkmate algortihm doesn't have to find it everytime
        # update the Moved variables so castling can no longer be generated
        if move.pieceMoved == 'bK ':
            self.blackKingLocation = (move.endRow, move.endCol)
            if self.bKMoved == False:  # fixed flaw in design
                self.bKMoved = True
                self.firstMoved.append(len(self.moveLog))

        elif move.pieceMoved == 'wK ':
            self.whiteKingLocation = (move.endRow, move.endCol)
            if self.wkMoved == False:  # potential flaw in design amended
                self.wkMoved = True
                self.firstMoved.append(len(self.moveLog))
        elif move.pieceMoved == 'wR ':
            if move.startCol == 0 and not self.wRLMoved:  # potential flaw in design amended
                self.wRLMoved = True
                self.firstMoved.append(len(self.moveLog))
            elif move.startCol == 7 and not self.wRRMoved:  # treat each case separately
                self.wRRMoved = True
                self.firstMoved.append(len(self.moveLog))
        elif move.pieceMoved == 'bR ':
            if move.startCol == 0 and not self.bRLMoved:
                self.bRLMoved = True
                self.firstMoved.append(len(self.moveLog))
            elif move.startCol == 7 and not self.bRRMoved:
                self.bRRMoved = True
                self.firstMoved.append(len(self.moveLog))
        # special moves
        if move.isPawnPromotion:  # pawn promotion
            self.board[move.endRow][move.endCol] = f'{
                move.pieceMoved[0]}Q '  # change the pawn into a queen
        # enpassant move
        if move.isEnpassantMove:
            # capture pawn which is one square under or above the landing the square
            self.board[move.startRow][move.endCol] = '-- '
            # update enpassantPossible
        # only on 2 square pawn advances is an en passant possible
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            # lets the engine know that if this square is landed on by a pawn enpassant can be executed
            self.enpassantPossible = (
                ((move.startRow+move.endRow)//2), move.startCol)
        else:
            self.enpassantPossible = ()
        # castling
        if move.isCastlingMove == 'right':  # move object moves the king, this moves rook
            if self.whiteToMove:
                self.board[7][7] = '-- '  # fixed in tp13
                self.board[7][5] = 'wR '
            else:
                self.board[0][7] = '-- '
                self.board[0][5] = 'bR '
        elif move.isCastlingMove == 'left':
            if self.whiteToMove:
                self.board[7][0] = '-- '
                self.board[7][3] = 'wR '
            else:
                self.board[0][0] = '-- '
                self.board[0][3] = 'bR '
        # ver 3 changes
        self.deActivate2()
        self.wAM.moveMade(len(self.moveLog)) if self.whiteToMove else self.bAM.moveMade(
            len(self.moveLog))
        # no move here will require a prediciton as to when it deactivates
        # change the turn so the opponent can play
        self.whiteToMove = not self.whiteToMove

    def undoMove(self, move=None):
        length = 0
        if move is None:
            length = len(self.moveLog)
            if length == 0:
                return None
            else:
                move = self.moveLog.pop()
        if move.type != 'standard':
            self.undoSpMove(move, length)
            return None
        # inverse of move made
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        # undoing first time king or rook moves should reset the Moved variables
        if move.pieceMoved == 'bK ':
            self.blackKingLocation = (move.startRow, move.startCol)
            if length == self.firstMoved[-1]:
                # change from original design (Flipped booleans)
                self.bKMoved = False
                self.firstMoved.pop()
        elif move.pieceMoved == 'wK ':
            self.whiteKingLocation = (move.startRow, move.startCol)
            if length == self.firstMoved[-1]:
                self.wkMoved = False
                self.firstMoved.pop()
        elif move.pieceMoved == 'wR ':
            # statement determines if it is the first time that piece has moved
            if length == self.firstMoved[-1]:
                if move.startCol == 0:  # figures out if its the right or left rook
                    self.wRLMoved = False
                else:
                    self.wRRMoved = False
                self.firstMoved.pop()  # forgot to add resolved with test plan 10
        elif move.pieceMoved == 'bR ':
            if length == self.firstMoved[-1]:
                if move.startCol == 0:
                    self.bRLMoved = False
                else:
                    self.bRRMoved = False
                self.firstMoved.pop()  # forgot to add
        # undo en passant
        if move.isEnpassantMove:
            # leave landing square blank
            self.board[move.endRow][move.endCol] = '-- '
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endCol)
        # undo 2 sq pawn advance
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            # if 2 square advance is undone then enpassant is no longer possible at this square
            self.enpassantPossible = ()
        # undo castle move
        if move.isCastlingMove == 'left':
            if move.pieceMoved[0] == 'w':
                # updated string to new convention fixed in tp13
                self.board[7][3] = '-- '
                self.board[7][0] = 'wR '
            else:
                self.board[0][3] = '-- '
                self.board[0][0] = 'bR '
        elif move.isCastlingMove == 'right':
            # fixed attribute error (was self.PieceMoved[0])
            if move.pieceMoved[0] == 'w':
                self.board[7][5] = '-- '
                self.board[7][7] = 'wR '
            else:
                self.board[0][5] = '-- '
                self.board[0][7] = 'bR '
        # ver 3 changes | similar to undoSpMove
        self.reActivate2()
        self.bAM.undoMoveMade(len(
            self.moveLog)) if self.whiteToMove else self.wAM.undoMoveMade(len(self.moveLog))
        # flip move before to get turn of previous player as reActive relies on players turn.
        self.whiteToMove = not self.whiteToMove

        # self.reActivate(reAct) #reactivate any abilities that qere active in the previous round

    def makeSpMove(self, move):  # ver 2 (using replace)
        deactivateAt = None
        if move.type == 'rec':
            # save the last 12 moves in case recollection was to be undone
            self.recolBuffer = self.moveLog[-12:]
            for _ in range(12):  # undo the board 12 moves
                self.undoMove()
        elif move.type == 'imp':
            self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                ' ', '+')  # indicates this piece has impervious active
        elif move.type == 'teth':
            self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                ' ', '-')  # indicates this piece has tether active
        elif move.type == 'rel':
            move.type = 'standard'  # peform the move like an ordrinariy move
            self.makeMove(move)
            self.whiteToMove = not self.whiteToMove  # fixed in tp12
            self.moveLog.pop()  # fixed in tp 12
            self.wAM.undoMoveMade(len(self.moveLog)-1) if self.whiteToMove else self.bAM.undoMoveMade(
                len(self.moveLog)-1)  # added when resolving ver 3 issues
            move.type = 'rel'  # makes sure the ability manager knows what move it is
        elif move.type == 'rein':
            self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                'p', 'N')
        elif move.type == 'int':
            self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                'Q', 'p')
            self.board[move.endRow][move.endCol] = self.board[move.endRow][move.endCol].replace(
                'p', 'Q')
        else:
            print('moveType error')
        self.wAM.moveMade(len(self.moveLog)+1) if self.whiteToMove else self.bAM.moveMade(
            len(self.moveLog)+1)  # ver 1.1 changes
        # self.deActivate(deAct)
        # ver 2 changes
        if self.whiteToMove:
            # +1 as current move has not been appended yet
            deactivateAt = self.wAM.setActive(move.type, len(self.moveLog)+1)
        else:
            # pass length of moveLog to predict when ability will deactivate
            deactivateAt = self.bAM.setActive(move.type, len(self.moveLog)+1)
        self.moveLog.append(move)
        self.deActivate2()  # deactivates any move that runs out on this turn
        # self.deActOrder.append((deactivateAt,move)) if deactivateAt != None else None #appends predicted deactivation of ability
        if deactivateAt != None:
            self.deActOrder[deactivateAt] = move
        # if a special move is played then en passant can never be possible on next turn so reset en passant square
        self.enpassantPossible = ()  # fixed after debugging version 3
        self.whiteToMove = not self.whiteToMove  # flip to enemy turn

    def undoSpMove(self, move, length):
        match move.type:  # ver 3
            case 'imp' | 'teth':
                # reverse dictionary to use move object as key
                inv_map = {v: k for k, v in self.deActOrder.items()}
                self.deActOrder.clear()  # clear dictionary for no overlaps
                if move.type == 'imp':  # perform board action to undo move
                    self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                        '+', ' ')
                else:
                    self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                        '-', ' ')
                inv_map.pop(move)  # pop move as it has been undone
                # remap dictionary back
                self.deActOrder = {v: k for k, v in inv_map.items()}
            case 'int':
                self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                    'p', 'Q')  # reverses substitution
                self.board[move.endRow][move.endCol] = self.board[move.endRow][move.endCol].replace(
                    'Q', 'p')
            case 'rein':
                self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                    'N', 'p')  # reverse piece back to a pawn
            case 'rel':
                move.type = 'standard'
                self.undoMove(move)
                move.type = 'rel'
                if move.pieceMoved == 'wK ':  # undo king moved need to add 1 since movelog has not been undone
                    try:
                        if length == self.firstMoved[-1]:
                            self.wkMoved = False
                            self.firstMoved.pop()
                        elif move.pieceMoved == 'bK ':
                            if length == self.firstMoved[-1]:
                                self.bkMoved = False
                                self.firstMoved.pop()
                    # first moved is empty (should not adjust any variables)
                    except IndexError:
                        pass
                self.wAM.moveMade(len(self.moveLog)) if self.whiteToMove else self.bAM.moveMade(
                    len(self.moveLog))  # added when resolving ver 3 issues
                self.whiteToMove = not self.whiteToMove
            case _:
                raise BaseException('Move Type Error!')
        # ver 3 changes
        self.reActivate2()  # find out what ability is going to reactivate
        self.bAM.undoMoveMade(len(
            self.moveLog)) if self.whiteToMove else self.wAM.undoMoveMade(len(self.moveLog))
        # flip the move at the end due to deactivation not relying on the ability manager anymore
        self.whiteToMove = not self.whiteToMove

    def deActivate2(self):

        # load move #add 1 to fix bug in tp13
        move = self.deActOrder.get(len(self.moveLog))
        if move != None:
            if move.type == 'imp':
                self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                    '+', ' ')  # removes effect
            elif move.type == 'teth':
                self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                    '-', ' ')  # removes effect

    # new ver |if undoing ability just casted then remove from dictionary else do not

    def reActivate2(self):
        move = self.deActOrder.get(len(self.moveLog)+1)  # load move
        if move != None:
            if move.type == 'imp':
                self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                    ' ', '+')  # readds effect
            elif move.type == 'teth':
                self.board[move.startRow][move.startCol] = self.board[move.startRow][move.startCol].replace(
                    ' ', '-')  # readds effect
            return move.type


# general move generators

    def getAllPossibleMoves(self, sqUnderAttack=False):
        moves = []
        for r in range(len(self.board)):
            # iterate through the board and generate moves for the piece found
            for c in range(len(self.board[r])):
                # matches with the gamestate whether it's to move or not
                turn = self.board[r][c][0]
                # piece must not be tethered or imprevious to move
                if self.board[r][c][2] not in ['+', '-']:
                    if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                        piece = self.board[r][c][1]  # stores the type of piece
                        # new method of calling the correct function (dictionary with lambda had issues with pickle)
                        match piece:
                            case 'p':
                                self.getPawnMoves(r, c, moves)
                            case 'R':
                                self.getRookMoves(r, c, moves)
                            case 'B':
                                self.getBishopMoves(r, c, moves)
                            case 'N':
                                self.getKnightMoves(r, c, moves)
                            case 'Q':
                                self.getQueenMoves(r, c, moves)
                            case 'K':
                                self.getKingMoves(r, c, moves, sqUnderAttack)
        return moves


# checkmate governors


    def getValidMoves(self):
        removed = False
        # when generating possible moves enpassant possible can change
        tempEnpassantPossible = self.enpassantPossible
        moves = self.getAllPossibleMoves()
        # avoid bugs by removing elements by iterating through the list backwards.
        for i in range((len(moves)-1), -1, -1):
            removed = False
            self.makeMove(moves[i])  # make the potential move
            self.whiteToMove = not self.whiteToMove  # change turn back to who is playing
            if self.inCheck():  # after the move is made check if that move made causes a check
                moves.remove(moves[i])  # move is not valid if a check is found
                removed = True
            # make sure the turn is reverted so the same player can still play
            self.whiteToMove = not self.whiteToMove
            # once found out if in check or not undo the move so no changes would've occured
            self.undoMove()
            if not removed:
                try:  # remove moves which attack impervious (failsafe)
                    if moves[i].pieceCaptured[2] == '+':
                        moves.remove(moves[i]) if not removed else None
                except AttributeError:  # some moves will not have a pieceCaptured which we can ignore
                    pass
            # final check if all moves are apply moves
            onlyApplyMovesLeft = True
            for move in moves:
                if move.type not in ['teth', 'imp', 'rein']:
                    onlyApplyMovesLeft = False
                    break
        # no moves availible means checkmate or stalemate
        if len(moves) == 0 or onlyApplyMovesLeft:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        # retain the orgiginal enpassant possible before the check
        self.enpassantPossible = tempEnpassantPossible
        print('ready for next move')
        return moves

    def inCheck(self):
        if self.whiteToMove:  # check what king would be under attack
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # generate opponent moves
        oppMoves = self.getAllPossibleMoves(True)
        # balance out to make sure the game isn't changed
        self.whiteToMove = not self.whiteToMove
        # fixed in tp14 remove apply moves to prevent error
        for move in oppMoves:
            try:
                if move.endRow == r:
                    if move.endCol == c:
                        return True
            except AttributeError:  # appy moves can be passed
                pass
        return False
# specific move generators
# append move object to a list moves when verified it can be made

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # moving white pawns
            if self.board[r-1][c] == '-- ':  # move 1 square
                moves.append(Move((r, c), self.board, 'standard', (r-1, c)))
                # move 2 squares if the pawn hasn't moved yet
                if r == 6 and self.board[r-2][c] == '-- ':
                    moves.append(
                        Move((r, c), self.board, 'standard', (r-2, c)))
            # capture piece to the left unless impervious piece
            if c >= 1 and self.board[r - 1][c - 1][0] == 'b' and self.board[r - 1][c - 1][2] != '+':
                moves.append(Move((r, c), self.board, 'standard', (r-1, c-1)))
            elif c >= 1 and (r - 1, c - 1) == self.enpassantPossible:
                moves.append(Move((r, c), self.board, 'standard',
                             (r-1, c-1), isEnpassantMove=True))  # enpassant
            # capture to the right unless impervious piece
            if c + 1 < len(self.board) and self.board[r - 1][c + 1][0] == 'b' and self.board[r - 1][c + 1][2] != '+':
                moves.append(Move((r, c), self.board, 'standard', (r-1, c+1)))
            elif c <= 6 and (r - 1, c + 1) == self.enpassantPossible:  # enpassant
                moves.append(Move((r, c), self.board, 'standard',
                             (r-1, c+1),  isEnpassantMove=True))
        else:  # same but for black pawns
            if self.board[r+1][c] == '-- ':  # 1 sq
                moves.append(Move((r, c), self.board, 'standard', (r+1, c)))
                if r == 1 and self.board[r+2][c] == '-- ':  # 2 square advance
                    moves.append(
                        Move((r, c), self.board, 'standard', (r+2, c)))
            # left capture unless impervious piece
            if c >= 1 and self.board[r + 1][c - 1][0] == 'w' and self.board[r + 1][c - 1][2] != '+':
                moves.append(Move((r, c), self.board, 'standard', (r+1, c-1)))
            elif c >= 1 and (r+1, c-1) == self.enpassantPossible:  # enpassant
                moves.append(Move((r, c), self.board, 'standard',
                             (r+1, c-1), isEnpassantMove=True))
            # right capture unless impervious piece
            if c + 1 < len(self.board) and self.board[r + 1][c + 1][0] == 'w' and self.board[r + 1][c + 1][2] != '+':
                moves.append(Move((r, c), self.board, 'standard', (r+1, c+1)))
            elif c+1 < len(self.board) and (r+1, c+1) == self.enpassantPossible:  # enpassant
                moves.append(Move((r, c), self.board, 'standard',
                             (r+1, c+1), isEnpassantMove=True))

    def getRookMoves(self, r, c, moves, qMove=False, atype=False):  # ver 2
        # determines if subroutine is called for a king relocate move or queen/rook normal move
        atype = 'rel' if atype else 'standard'
        nr, nc = 0, 0
        # the orthogonal directions which a rook can travel in
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            # with no pieces in the way the max distance a rook can travel is 7 and min is 1
            for i in range(1, 8):
                nr = r+d[0]*i
                nc = c+d[1]*i
                if nr not in range(8) or nc not in range(8):
                    break  # board limits reached
                if self.board[(nr)][(nc)] == '-- ':  # empty space move
                    moves.append(Move((r, c), self.board, atype, (nr, nc)))
                elif self.board[(nr)][(nc)][2] != '+' and (self.whiteToMove and self.board[(nr)][(nc)][0] == 'b') or (not self.whiteToMove and self.board[(nr)][(nc)][0] == 'w'):
                    # capture move
                    moves.append(Move((r, c), self.board, atype, (nr, nc)))
                    break  # piece cannot move any further
                else:
                    break  # stopped by ally piece blocking
            # piece ability | ver 2
        condition1 = (self.whiteToMove and self.wAM.ready[0]) or (
            not self.whiteToMove and self.bAM.ready[0])
        condition2 = not qMove
        if condition1 and condition2:
            moves.append((ApplyMove((r, c), self.board, 'imp')))

    # same algorithm as rook with different directions to check
    def getBishopMoves(self, r, c, moves, qMove=False, atype=False):
        atype = 'rel' if atype else 'standard'
        # diagonal directions which a bishop moves in
        for d in [(1, 1), (1, -1), (-1, -1), (-1, 1)]:
            for i in range(1, 8):  # similar to the rook.
                nr = r+d[0]*i
                nc = c+d[1]*i
                if nr not in range(8) or nc not in range(8):
                    break  # board limits reached
                if self.board[(nr)][(nc)] == '-- ':  # empty space move
                    moves.append(Move((r, c), self.board, atype, (nr, nc)))
                elif self.board[(nr)][(nc)][2] != '+' and (self.whiteToMove and self.board[(nr)][(nc)][0] == 'b') or (not self.whiteToMove and self.board[(nr)][(nc)][0] == 'w'):
                    # capture move
                    moves.append(Move((r, c), self.board, atype, (nr, nc)))
                    break  # piece cannot move any further
                else:
                    break  # stopped by ally piece blocking
        # piece ability  | ver 2
        condition1 = (self.whiteToMove and self.wAM.ready[1]) or (
            not self.whiteToMove and self.bAM.ready[1])
        condition2 = not qMove
        if condition1 and condition2:
            for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # tether move scan directions
                nr = r+d[0]
                nc = c+d[1]
                if (
                    0 <= nr <= 7
                    and 0 <= nc <= 7
                    and (
                        self.board[nr][nc][1] != 'K'  # cant tether a king
                        and (
                            self.whiteToMove and self.board[nr][nc][0] == 'b'
                        )  # enempy piece
                        or (
                            not self.whiteToMove and self.board[nr][nc][0] == 'w'
                        )  # enemy piece
                    )
                ):
                    moves.append(ApplyMove((nr, nc), self.board, 'teth'))

    def getQueenMoves(self, r, c, moves, rel=False):  # ver 2
        # pass in True so subroutines know it is a queen move and tether moves are not generated
        self.getBishopMoves(r, c, moves, True, rel)
        self.getRookMoves(r, c, moves, True, rel)
        if not rel:  # prevents relocate moves from also generating interchange
            found = 0
            # ability is ready for white
            if self.whiteToMove and self.wAM.ready[3]:
                # interchange
                for row in range(r+1):  # search possible squares for interchange
                    if found == 8:  # max of 8 pawns on board at time
                        break
                    for col in range(len(self.board[row])):  # search board
                        if self.board[row][col] == 'wp ':
                            moves.append(
                                basicMove((r, c), self.board, 'int', (row, col)))
                            found += 1
            # ability is ready for black
            elif not self.whiteToMove and self.bAM.ready[3]:
                # search possible squares for interchange
                for row in range(len(self.board)-1, r-1, -1):
                    if found == 8:  # max of 8 pawns on board at time
                        break
                    for col in range(len(self.board[row])):  # search board
                        # pawns with tether cannot be interchanged with.
                        if self.board[row][col] == 'bp ':
                            moves.append(
                                basicMove((r, c), self.board, 'int', (row, col)))
                            found += 1

    # moves like a queen but only 1square
    def getKingMoves(self, r, c, moves, sqUnderAttack=False):
        abReady = (self.whiteToMove and self.wAM.ready[2]) or (  # ability ready
            # changed from 1 -> 2 (error)
            not self.whiteToMove and self.bAM.ready[2])
        if abReady:
            self.getQueenMoves(r, c, moves, True)  # relocate
        ally = 'w' if self.whiteToMove else 'b'

        # recollection not working as of now
        # standard moves
        # all possible directions which the king can move
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            if (r+d[0]) in range(8) and (c+d[1]) in range(8):  # checking board limits
                if self.board[r+d[0]][c+d[1]] == '-- ':  # empty space move
                    moves.append(
                        Move((r, c), self.board, 'standard', (r+d[0], c+d[1])))
                # capture move
                elif self.board[r+d[0]][c+d[1]][2] != '+' and (self.board[r+d[0]][c+d[1]][0] == 'b' and self.whiteToMove) or (self.board[r+d[0]][c+d[1]][0] == 'w' and not self.whiteToMove):
                    moves.append(
                        Move((r, c), self.board, 'standard', (r+d[0], c+d[1])))
            if abReady:
                for i in (1, 2):  # reincarnation
                    nr = r+d[0]*i
                    nc = c+d[1]*i

                    if (0 <= nc <= 7) and (0 <= nr <= 7):  # board limits
                        if self.board[nr][nc] == f'{ally}p ':
                            self.board[nr][nc] = self.board[nr][nc].replace(
                                'p', 'N')
                            # make sure this move does not make a discovered check
                            self.whiteToMove = not self.whiteToMove
                            if not self.inCheck():
                                moves.append(
                                    ApplyMove((nr, nc), self.board, 'rein'))
                            self.board[nr][nc] = self.board[nr][nc].replace(
                                'N', 'p')
                            self.whiteToMove = not self.whiteToMove
        if not sqUnderAttack:  # prevent infinite recursive loop
            a = 0
            passed = True
            if not self.inCheck():  # cant castle in check
                if self.whiteToMove:  # white castling
                    if not self.wkMoved:
                        if not self.wRLMoved:  # both pieces can not have moved
                            # scan all squares to the left until edge of board | c -> c-1 fixed in tp14 & stops -1 -> 0
                            for a in range(c-1, 0, -1):
                                # reworked condition | if any square is not empty or a check is crossed prevent castling
                                if self.board[r][a] != '-- ' or self.squareUnderAttack(r, a):
                                    passed = False
                                    break
                            if passed:
                                # append the king move (move handler does rook)
                                moves.append(
                                    Move((r, c), self.board, 'standard', (r, c-2), isCastlingMove='left'))
                            passed = True  # reset vars for right side check
                            a = 0
                        if not self.wRRMoved:
                            # scan all squares to the right until edge of board | c -> c+1 fixed in tp14 & upper 8 -> 7
                            for a in range(c+1, 7):
                                # reworked condition
                                if self.board[r][a] != '-- ' or self.squareUnderAttack(r, a):
                                    passed = False
                                    break
                            if passed:
                                moves.append(
                                    Move((r, c), self.board, 'standard', (r, c+2), isCastlingMove='right'))
                elif not self.bKMoved:  # same code but with black moved boolean variables
                    if not self.bRLMoved:
                        for a in range(c-1, 0, -1):
                            if self.board[r][a] != '-- ' or self.squareUnderAttack(r, a):
                                passed = False
                                break
                        if passed:
                            moves.append(
                                Move((r, c), self.board, 'standard', (r, c-2), isCastlingMove='left'))
                        passed = True
                        a = 0
                    if not self.bRRMoved:
                        for a in range(c+1, 7):
                            if self.board[r][a] != '-- ' or self.squareUnderAttack(r, a):
                                passed = False
                                break
                        if passed:
                            moves.append(
                                Move((r, c), self.board, 'standard', (r, c+2), isCastlingMove='right'))

    def getKnightMoves(self, r, c, moves):
        # rotating the L shape which a knight can take
        for op in [('', ''), ('-', '-'), ('', '-'), ('-', '')]:
            for d in [('2', '1'), ('1', '2')]:  # the two main L shapes which a knight can peform
                newr = r+int(op[0]+d[0])  # end row
                newc = c+int(op[1]+d[1])  # end col
                # checking if the move complies with board limits
                if (newr in range(8)) and (newc in range(8)):
                    if self.board[newr][newc] == '-- ':  # empty space move
                        moves.append(
                            Move((r, c), self.board, 'standard', (newr, newc)))
                    # capture move
                    elif (self.whiteToMove and self.board[newr][newc][0] == 'b') or (not self.whiteToMove and self.board[newr][newc][0] == 'w'):
                        moves.append(
                            Move((r, c), self.board, 'standard', (newr, newc)))
