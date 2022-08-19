from notation import *
from scales import *
from functools import reduce

tuning = ['E', 'A', 'D', 'G', 'B', 'E']
maxReach = 3
maxChordFret = 20

def getNoteAt(string, fret):
    '''gets the note on the fretboard at string, fret'''
    return INDEX_NOTE[(NOTE_INDEX[tuning[string]]+fret)%12]

def processFretboard(board):
    '''using list of frets in order of low-high strings, return list of notes played. '''
    list = []
    string = 0
    for fret in board:
        if(fret != -1):
            note = getNoteAt(string, fret)
            list.append(note)
        string+=1
    return list

def checkStr(s):
    if(s == 'N'): return -1
    return int(s)

def getBoardInput():
    board = list(map(checkStr, input("Input fret numbers from low to high with - in between, N for not played: ").split('-')))
    if(len(board) > 6  or len(board) < 6):
        print("invalid input! try again")
        return getBoardInput()
    return board

def checkMatch(notes, match):
    off = []
    for note in notes:
        if(note not in match):
            off.append(note)
    return off

def checkRange(f, board):
    for n in board:
        if(f > 0 and n > 0 and abs(f-n) > maxReach):
            return False
    return True

def getPositions(chordNotes, s=0, board=[]):
    open = tuning[s]
    possibleFrets = []
    if(board.count(-1) < len(tuning)-len(chordNotes)): possibleFrets = [-1]
    
    for note in chordNotes:
        mod = noteDistanceFwd(open, note)
        possibleFrets += [i+mod for i in range(0, maxChordFret, 12) if i+mod <= maxChordFret]
    possibleFrets = set(filter(lambda f: checkRange(f, board), possibleFrets))
    
    if(s == 5):
        return [board+[f] for f in possibleFrets]

    ls = [getPositions(chordNotes, s=s+1, board=board+[f]) for f in possibleFrets]
    if(len(ls) == 0): return []
    return list(reduce(lambda x,y: x+y, ls))

def getPositionsByName(root, name):
    return getPositions(CHORD_TYPES[name](root))

def getPositionsFiltered(root, name, maxStringsPlayed=6, minStringsPlayed=1):
    positions = getPositionsByName(root, name)
    npop = 0
    for chordi in range(len(positions)):
        chord = positions[chordi-npop]
        if(chord.count(-1) < len(tuning)-maxStringsPlayed or chord.count(-1) > len(tuning)-minStringsPlayed): 
            positions.pop(chordi-npop)
            npop += 1
            continue
        chunkstart = -1
        chunkend = -1
        for freti in range(len(chord)):
            if(chord[freti] == -1 and chunkstart == -1):
                chunkstart = freti
            elif(chord[freti] != -1 and chunkstart != -1 and chunkend == -1):
                chunkend = freti
                if(chunkstart != 0):
                    positions.pop(chordi-npop)
                    npop += 1
                    break
                chunkstart = -1
                chunkend = -1
    return positions
            

'''while True:
    notes = processFretboard(getBoardInput())
    chords = findChords(list(dict.fromkeys(notes)))
    closestMatch = max(chords, key=lambda c: len(c[2]))
    print("NOTES: " + str(notes))
    print("CLOSEST CHORD: " + str(closestMatch))
    match = checkMatch(notes, closestMatch[2])
    print("OFF BY: " + str(match))
'''
print(getPositionsFiltered('C', 'm6', 6, 6))
    


