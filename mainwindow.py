import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QListWidget,
    QPushButton,
    QLineEdit,
    QRadioButton
)


class FantasyCricket(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fantasy Cricket")
        self.setGeometry(200, 100, 900, 600)

        # Team Name
        self.lblTeam = QLabel("Team Name", self)
        self.lblTeam.move(20, 20)

        self.txtTeam = QLineEdit(self)
        self.txtTeam.setGeometry(110, 20, 200, 25)

        # Available Players
        self.lblAvailable = QLabel("Available Players", self)
        self.lblAvailable.move(20, 70)

        self.listAvailable = QListWidget(self)
        self.listAvailable.setGeometry(20, 100, 250, 300)

        # Selected Players
        self.lblSelected = QLabel("Selected Players", self)
        self.lblSelected.move(350, 70)

        self.listSelected = QListWidget(self)
        self.listSelected.setGeometry(350, 100, 250, 300)

        # Category Radio Buttons
        self.rbBAT = QRadioButton("BAT", self)
        self.rbBAT.move(650, 100)

        self.rbBWL = QRadioButton("BWL", self)
        self.rbBWL.move(650, 130)

        self.rbAR = QRadioButton("AR", self)
        self.rbAR.move(650, 160)

        self.rbWK = QRadioButton("WK", self)
        self.rbWK.move(650, 190)

        # Labels
        self.lblPoints = QLabel("Points Left : 100", self)
        self.lblPoints.move(650, 250)

        self.lblPlayers = QLabel("Players Left : 11", self)
        self.lblPlayers.move(650, 280)

        self.lblScore = QLabel("Score : 0", self)
        self.lblScore.move(650, 310)

        # Buttons
        self.btnAdd = QPushButton(">>", self)
        self.btnAdd.setGeometry(285, 180, 50, 30)

        self.btnRemove = QPushButton("<<", self)
        self.btnRemove.setGeometry(285, 230, 50, 30)

        self.btnSave = QPushButton("Save Team", self)
        self.btnSave.setGeometry(650, 380, 120, 35)

        self.btnScore = QPushButton("Calculate Score", self)
        self.btnScore.setGeometry(650, 430, 120, 35)


app = QApplication(sys.argv)

window = FantasyCricket()
window.show()

sys.exit(app.exec())