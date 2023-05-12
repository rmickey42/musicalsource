import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGroupBox, QPushButton, QGridLayout, QButtonGroup, QComboBox
from PyQt5.QtGui import QFont
import GuitarCalculator as gc

NUM_FRETS = 21
selection = [0, 0, 0, 0, 0, 0]

class FretButton(QPushButton):
    def __init__(self, string, fret, parent, onChange, enabled=False):
        super(FretButton, self).__init__(parent)
        self.setCheckable(True)
        self.setChecked(enabled)
        self.setAutoExclusive(True)
        self.setStyleSheet("QPushButton:checked {background-color: red;}")
        self.setStyleSheet("QPushButton:unchecked {background-color: white;}")
        self.setStyleSheet("")
        self.fret = fret
        self.string = string
        self.setFixedHeight(60)
        if(fret > -1):
            self.setFixedWidth(60)
            self.setText(str(fret) + ": " + gc.getNoteAt(string, fret))
        else:
            self.setFixedWidth(20)
            self.setText("X")
        self.clicked.connect(self.setSelection(onChange))

    def setSelection(self, sidechain):
        def setfunc():
            selection[self.string] = self.fret
            sidechain()
        return setfunc

def generateButtonGroups(cancelbtns, fretbtns, parent=None):
    btns = []
    for string in range(6):
        btns.append(QButtonGroup(parent))
        btns[string].addButton(cancelbtns[string], id=0)
        for fret in range(NUM_FRETS):
            btns[string].addButton(fretbtns[string][fret], id=fret+1)
    return btns

class GuitarBoard(QGroupBox):
    def __init__(self, onChange, parent=None):
        super(GuitarBoard, self).__init__(parent)
        self.cancelbtns = list(map(lambda s: FretButton(s, -1, self, onChange), [sx for sx in range(6)]))
        self.fretbtns = list(map(lambda s: (list(map(lambda f: FretButton(s, f, self, onChange, True if f==0 else False), [fx for fx in range(NUM_FRETS)]))), [sx for sx in range(6)]))
        self.btngrps = generateButtonGroups(self.cancelbtns, self.fretbtns, self)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.layout.setColumnMinimumWidth(0, 20)
        for fret in self.cancelbtns:
            self.layout.addWidget(fret, 5-fret.string, 0)
        for string in self.fretbtns:
            for fret in string:
                self.layout.setColumnMinimumWidth(fret.string+1, 40)
                self.layout.addWidget(fret, 5-fret.string, fret.fret+1)

class ChordSelector(QGroupBox):
    def __init__(self, applyChord, parent=None):
        super(ChordSelector, self).__init__(parent)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.fingerings = []
        self.chordidx = 0

        self.desiredChordRoot = QComboBox(self)
        self.desiredChordRoot.addItems(gc.NOTES)

        self.desiredChordType = QComboBox(self)
        self.desiredChordType.addItems(gc.CHORD_TYPES.keys())

        self.applyChordButton = QPushButton("Get Chords", self)

        def apply():
            self.fingerings = gc.getPositionsFiltered(self.desiredChordRoot.currentText(), self.desiredChordType.currentText())
            self.chordidx = 0
            if(len(self.fingerings) > 0):
                applyChord(self.fingerings[self.chordidx])

        self.applyChordButton.clicked.connect(apply)

        def nxchd():
            if(len(self.fingerings) > 0):
                self.chordidx = (self.chordidx + 1) % len(self.fingerings)
                applyChord(self.fingerings[self.chordidx])
        def pvchd():
            if(len(self.fingerings) > 0):
                self.chordidx = (self.chordidx - 1) % len(self.fingerings)
                applyChord(self.fingerings[self.chordidx])

        self.prevChordBtn = QPushButton("<<", self)
        self.nextChordBtn = QPushButton(">>", self)
        self.prevChordBtn.clicked.connect(pvchd)
        self.nextChordBtn.clicked.connect(nxchd)

        self.layout.addWidget(self.desiredChordRoot, 0, 0)
        self.layout.addWidget(self.desiredChordType, 0, 1)
        self.layout.addWidget(self.applyChordButton, 1, 0, 1, 2)
        self.layout.addWidget(self.prevChordBtn, 2, 0)
        self.layout.addWidget(self.nextChordBtn, 2, 1)

def getChords():
    return gc.getBestMatchesOfFretboard(selection)

def run():
    app = QApplication(sys.argv)
    win = QWidget()
    win.setStyleSheet("font-size: 12px;")
    
    chordLbl = QLabel(f"Selected Chord: ???", win)
    chordLbl.alignment = Qt.AlignCenter
    chordLbl.setFont(QFont(win.font().family(), 20, QFont.Bold))
    
    def updateChordLbl():
        chds = getChords()
        chdstr = None
        if(len(chds) > 0):
            chdstr = ''
            for i,chd in enumerate(chds):
                chdstr += chd[0] + chd[1]
                if(i < len(chds)):
                    chdstr += ', '
                break
        else:
            chdstr = '???'
        chordLbl.setText(f"Selected Chord(s): {chdstr}")
    board = GuitarBoard(updateChordLbl, win)

    def applyChord(chord):
        global selection
        selection = chord
        for string in range(6):
            board.btngrps[string].button(selection[string]+1).setChecked(True)
        updateChordLbl()

    selector = ChordSelector(applyChord, win)
    
    win.layout = QGridLayout(win)
    win.layout.addWidget(board, 0, 0)
    win.layout.addWidget(chordLbl, 1, 0, 1, 2, Qt.AlignCenter)
    win.layout.addWidget(selector, 2, 0)
    win.setFixedSize(win.layout.sizeHint())

    win.setWindowTitle("Guitar Calculator")
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
   run()