from notation import *
from scales import *

tuning = ['E', 'A', 'D', 'G', 'B', 'E']

def GetNoteAt(pair):
    '''gets the note on the fretboard at (string, fret) pair'''
    try:
        return INDEX_NOTE[(NOTE_INDEX[tuning[pair[0]]]+pair[1])%12]
    except: raise ValueError("GetNoteAt: String index out of range!")

def ProcessFretboard(board):
    '''using list of notes in order of low-high strings '''
    list = []
    for note in board:


