import sqlite3
import sys
import os
import shutil
from PyQt5.QtWidgets import QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QColor, QIcon 
from analysis import DataAnalysisWindow
import csv
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QListWidget,
    QPushButton,
    QLineEdit,
    QRadioButton,
    QMessageBox,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QAction,
    QDialog,
    QHBoxLayout,
    QVBoxLayout,
    QHeaderView,
    QStyle,
)
def get_database_path():
    app_data = os.getenv("LOCALAPPDATA")
    data_folder = os.path.join(app_data, "FantasyCricket")

    os.makedirs(data_folder, exist_ok=True)

    user_db = os.path.join(data_folder, "cricket.db")

    if not os.path.exists(user_db):

        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        bundled_db = os.path.join(base_path, "cricket.db")

        shutil.copy2(bundled_db, user_db)

    return user_db

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)
class FantasyCricket(QMainWindow):
    def __init__(self):
        super().__init__()

    # -----------------------------
    # Database
    # -----------------------------
        import os
        import sqlite3

        DB_PATH = get_database_path()

        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        # -----------------------------
        # Team Information
        # -----------------------------
        self.points_left = 1500
        self.players_left = 11
        self.dark_mode = False

        # -----------------------------
        # Main Window
        # -----------------------------
        self.setWindowTitle("Fantasy Cricket Team Builder")
        self.setGeometry(200, 100, 900, 720)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setStyleSheet("""
        QMainWindow{
            background-color:#F4F6F8;
        }

        QGroupBox{
            font-size:13px;
            font-weight:bold;
            border:2px solid #BDBDBD;
            border-radius:8px;
            margin-top:12px;
        }

        QGroupBox::title{
            subcontrol-origin: margin;
            left:12px;
            padding:0 5px;
        }
        """)

        # -----------------------------
        # Fonts
        # -----------------------------
        title_font = QFont("Arial", 18, QFont.Bold)
        heading_font = QFont("Arial", 11, QFont.Bold)
        normal_font = QFont("Arial", 10)
        button_font = QFont("Segoe UI", 10, QFont.Bold)
        # ==========================
        # Menu Bar
        # ==========================
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        toolsMenu = menuBar.addMenu("Tools")
        helpMenu = menuBar.addMenu("Help")
        # ==========================
        # File Menu Actions
        # ==========================
        newAction = QAction("New Team", self)
        saveAction = QAction("Save Team", self)
        openAction = QAction("Open Team", self)
        exitAction = QAction("Exit", self)

        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # ==========================
        # Tools Menu Actions
        # ==========================
        leaderboardAction = QAction("Leaderboard", self)
        exportAction = QAction("Export CSV", self)

        toolsMenu.addAction(leaderboardAction)
        toolsMenu.addAction(exportAction)

        # ==========================
        # Help Menu Actions
        # ==========================
        aboutAction = QAction("About", self)

        helpMenu.addAction(aboutAction)
        newAction.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))

        saveAction.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))

        openAction.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))

        exitAction.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))

        leaderboardAction.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        exportAction.setIcon(self.style().standardIcon(QStyle.SP_DriveHDIcon))

        aboutAction.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        newAction.setStatusTip("Create a new team")
        saveAction.setStatusTip("Save the current team")
        openAction.setStatusTip("Open an existing team")
        exitAction.setStatusTip("Exit the application")

        leaderboardAction.setStatusTip("View team rankings")
        exportAction.setStatusTip("Export leaderboard to CSV")

        aboutAction.setStatusTip("About Fantasy Cricket Team Builder")
        # ==========================
        # Menu Connections
        # ==========================
        newAction.triggered.connect(self.reset_team)
        saveAction.triggered.connect(self.save_team)
        openAction.triggered.connect(self.open_team)
        exitAction.triggered.connect(self.close)
        # ==========================
        # Keyboard Shortcuts
        # ==========================
        newAction.setShortcut("Ctrl+N")
        saveAction.setShortcut("Ctrl+S")
        openAction.setShortcut("Ctrl+O")
        exitAction.setShortcut("Ctrl+Q")

        leaderboardAction.setShortcut("Ctrl+L")
        exportAction.setShortcut("Ctrl+E")

        leaderboardAction.triggered.connect(self.show_leaderboard)
        exportAction.triggered.connect(self.export_csv)
        aboutAction.triggered.connect(self.show_about)

        # -----------------------------
        # Main Title
        # -----------------------------
        self.lblTitle = QLabel("🏏 Fantasy Cricket Team Builder", self)
        self.lblTitle.setGeometry(230, 10, 500, 40)
        self.lblTitle.setFont(title_font)
        self.lblTitle.setStyleSheet("color:#0D47A1;")

        # -----------------------------
        # Team Information Box
        # -----------------------------
        self.teamBox = QGroupBox("Team Information", self)
        self.teamBox.setGeometry(20, 60, 340, 80)

        self.lblTeam = QLabel("Team Name", self.teamBox)
        self.lblTeam.setGeometry(15, 32, 90, 25)
        self.lblTeam.setFont(heading_font)

        self.txtTeam = QLineEdit(self.teamBox)
        self.txtTeam.setGeometry(110, 30, 200, 28)
        self.txtTeam.setFont(normal_font)
        self.txtTeam.setPlaceholderText("Enter Team Name")
# -----------------------------
# Available Players Box
# -----------------------------
        self.availableBox = QGroupBox("Available Players", self)
        self.availableBox.setGeometry(20, 160, 280, 450)

        self.listAvailable = QListWidget(self.availableBox)
        self.listAvailable.setGeometry(10, 30, 260, 410)
        self.listAvailable.setFont(normal_font)
        self.listAvailable.setSpacing(3)
        self.listAvailable.setAlternatingRowColors(True)

        # -----------------------------
        # Selected Players Box
        # -----------------------------
        self.selectedBox = QGroupBox("Selected Team", self)
        self.selectedBox.setGeometry(370, 160, 280, 450)

        self.listSelected = QListWidget(self.selectedBox)
        self.listSelected.setGeometry(10, 30, 260, 410)
        self.listSelected.setFont(normal_font)
        self.listSelected.setSpacing(3)
        self.listSelected.setAlternatingRowColors(True)

        # -----------------------------
        # Move Buttons
        # -----------------------------
        self.btnAdd = QPushButton(">>", self)
        self.btnAdd.setGeometry(315, 280, 40, 35)

        self.btnRemove = QPushButton("<<", self)
        self.btnRemove.setGeometry(315, 340, 40, 35)

        # -----------------------------
        # Category Box
        # -----------------------------
        self.categoryBox = QGroupBox("Category", self)
        self.categoryBox.setGeometry(680, 60, 130, 180)

        self.rbBAT = QRadioButton("BAT", self.categoryBox)
        self.rbBAT.setGeometry(20, 30, 80, 25)
        self.rbBAT.setFont(heading_font)

        self.rbBWL = QRadioButton("BWL", self.categoryBox)
        self.rbBWL.setGeometry(20, 60, 80, 25)
        self.rbBWL.setFont(heading_font)

        self.rbAR = QRadioButton("AR", self.categoryBox)
        self.rbAR.setGeometry(20, 90, 80, 25)
        self.rbAR.setFont(heading_font)

        self.rbWK = QRadioButton("WK", self.categoryBox)
        self.rbWK.setGeometry(20, 120, 80, 25)
        self.rbWK.setFont(heading_font)

        # -----------------------------
        # Statistics Box
        # -----------------------------
        self.statsBox = QGroupBox("Team Statistics", self)
        self.statsBox.setGeometry(780, 60, 180, 180)

        self.lblPoints = QLabel(f"Points Left : {self.points_left}", self.statsBox)
        self.lblPoints.setGeometry(10, 30, 160, 25)
        self.lblPoints.setFont(normal_font)

        self.lblPlayers = QLabel(f"Players Left : {self.players_left}", self.statsBox)
        self.lblPlayers.setGeometry(10, 70, 160, 25)
        self.lblPlayers.setFont(normal_font)

        self.lblScore = QLabel("Score : 0", self.statsBox)
        self.lblScore.setGeometry(10, 110, 160, 25)
        self.lblScore.setFont(normal_font)
# -----------------------------
# Action Buttons
# -----------------------------
        self.btnSave = QPushButton(self)
        self.btnSave.setGeometry(680, 270, 135, 42)
        icon = QIcon("icon/save.png")
        pixmap = QPixmap("icon/save.png")

        self.btnSave.setIcon(icon)
        self.btnSave.setIconSize(QSize(32,32))

        self.btnOpen = QPushButton("Open Team", self)
        self.btnOpen.setGeometry(825, 270, 135, 42)


        self.btnUpdate = QPushButton("Update Team", self)
        self.btnUpdate.setGeometry(680, 325, 135, 42)


        self.btnDelete = QPushButton("Delete Team", self)
        self.btnDelete.setGeometry(825, 325, 135, 42)


        self.btnScore = QPushButton("Calculate Score", self)
        self.btnScore.setGeometry(680, 380, 280, 42)

        self.btnReset = QPushButton("New Team", self)
        self.btnReset.setGeometry(680, 485, 280, 42)

        self.btnLeaderboard = QPushButton("Leaderboard", self)
        self.btnLeaderboard.setGeometry(680, 430, 280, 42)
        self.btnLeaderboard.clicked.connect(self.show_leaderboard)
        self.btnAbout = QPushButton("About", self)
        self.btnAbout.setGeometry(680, 540, 135, 42)

        self.btnAnalysis = QPushButton("📊 Analysis", self)
        self.btnAnalysis.setGeometry(825, 540, 135, 42)

        self.btnAnalysis.clicked.connect(self.open_analysis)
       
        blue_button = """
        QPushButton{
            background-color:#007BFF;
            color:white;
            ...
        }
        """
        self.btnAbout.setStyleSheet(blue_button)
        self.btnAbout.clicked.connect(self.show_about)
        self.btnAdd.setIcon(QIcon("icon/add.png"))
        self.btnRemove.setIcon(QIcon("icon/remove.png"))

        self.btnSave.setText(" Save Team")
        self.btnSave.setIcon(QIcon("icon/save.png"))
        self.btnSave.setIconSize(QSize(20, 20))
        self.btnOpen.setIcon(QIcon("icon/open.png"))

        self.btnUpdate.setIcon(QIcon("icon/update.png"))
        self.btnDelete.setIcon(QIcon("icon/delete.png"))

        self.btnScore.setIcon(QIcon("icon/score.png"))
        self.btnReset.setIcon(QIcon("icon/new.png"))

        self.btnLeaderboard.setIcon(QIcon("icon/leaderboard.png"))
        self.btnAbout.setIcon(QIcon(resource_path("icon/about.png")))
        self.btnAdd.setIconSize(QSize(20,20))
        self.btnRemove.setIconSize(QSize(20,20))

        
        self.btnOpen.setIconSize(QSize(20,20))

        self.btnUpdate.setIconSize(QSize(20,20))
        self.btnDelete.setIconSize(QSize(20,20))

        self.btnScore.setIconSize(QSize(20,20))
        self.btnReset.setIconSize(QSize(20,20))

        self.btnLeaderboard.setIconSize(QSize(20,20))
        self.btnAbout.setIconSize(QSize(20,20))
        self.btnAdd.setToolTip("Add selected player to your team")
        self.btnRemove.setToolTip("Remove selected player from your team")

        self.btnSave.setToolTip("Save the current team")
        self.btnOpen.setToolTip("Open a saved team")
        self.btnUpdate.setToolTip("Update the selected team")
        self.btnDelete.setToolTip("Delete the selected team")

        self.btnScore.setToolTip("Calculate fantasy score")
        self.btnReset.setToolTip("Create a new team")

        self.btnLeaderboard.setToolTip("View leaderboard")
        self.btnAbout.setToolTip("About this application")

        # -----------------------------
        # Button Styles
        # -----------------------------
        green_button = """
        QPushButton{
            background-color:#28A745;
            color:white;
            font-size:13px;
            font-weight:bold;
            border-radius:8px;
        }
        QPushButton:hover{
            background-color:#218838;
        }
        """

        red_button = """
        QPushButton{
            background-color:#DC3545;
            color:white;
            font-size:13px;
            font-weight:bold;
            border-radius:8px;
        }
        QPushButton:hover{
            background-color:#C82333;
        }
        """

        blue_button = """
        QPushButton{
            background-color:#007BFF;
            color:white;
            font-size:13px;
            font-weight:bold;
            border-radius:8px;
        }
        QPushButton:hover{
            background-color:#0069D9;
        }
        """

        orange_button = """
        QPushButton{
            background-color:#FD7E14;
            color:white;
            font-size:13px;
            font-weight:bold;
            border-radius:8px;
        }
        QPushButton:hover{
            background-color:#E96B00;
        }
        """

        gray_button = """
        QPushButton{
            background-color:#6C757D;
            color:white;
            font-size:13px;
            font-weight:bold;
            border-radius:8px;
        }
        QPushButton:hover{
            background-color:#5A6268;
        }
        """
        self.btnTheme = QPushButton("🌙 Dark Mode", self)
        self.btnTheme.setGeometry(680, 595, 280, 40)
        self.btnTheme.setFont(button_font)
        self.btnTheme.setStyleSheet(gray_button)

        self.btnTheme.clicked.connect(self.toggle_theme)
        # Apply Styles
        self.btnAdd.setStyleSheet(blue_button)
        self.btnRemove.setStyleSheet(gray_button)

        self.btnSave.setStyleSheet(green_button)
        self.btnOpen.setStyleSheet(blue_button)

        self.btnUpdate.setStyleSheet(orange_button)
        self.btnDelete.setStyleSheet(red_button)

        self.btnScore.setStyleSheet(blue_button)
        self.btnReset.setStyleSheet(gray_button)
        self.btnLeaderboard.setStyleSheet(blue_button)
        self.btnAbout.setStyleSheet(blue_button)
        self.btnAnalysis.setStyleSheet(blue_button)
        self.btnAbout.setIcon(QIcon("icon/about.png"))
        self.btnAbout.setIconSize(QSize(20,20))
        self.btnAnalysis.setIconSize(QSize(20,20))
        # Apply button font
        self.btnAdd.setFont(button_font)
        self.btnRemove.setFont(button_font)

        self.btnSave.setFont(button_font)
        self.btnOpen.setFont(button_font)

        self.btnUpdate.setFont(button_font)
        self.btnDelete.setFont(button_font)

        self.btnScore.setFont(button_font)
        self.btnReset.setFont(button_font)

        self.btnLeaderboard.setFont(button_font)
        self.btnAbout.setFont(button_font)

        # -----------------------------
        # Signal Connections
        # -----------------------------

        # Radio Buttons
        self.rbBAT.clicked.connect(lambda: self.load_players("BAT"))
        self.rbBWL.clicked.connect(lambda: self.load_players("BWL"))
        self.rbAR.clicked.connect(lambda: self.load_players("AR"))
        self.rbWK.clicked.connect(lambda: self.load_players("WK"))
        # Buttons
        self.btnAdd.clicked.connect(self.add_player)
        self.btnRemove.clicked.connect(self.remove_player)

        self.btnSave.clicked.connect(self.save_team)
        self.btnOpen.clicked.connect(self.open_team)
        self.btnUpdate.clicked.connect(self.update_team)
        self.btnDelete.clicked.connect(self.delete_team)
        self.btnScore.clicked.connect(self.calculate_score)
        self.btnReset.clicked.connect(self.reset_team)

# Player Information
        self.listAvailable.itemClicked.connect(self.show_player_info)
# -----------------------------
# Player Information Box
# -----------------------------
    
        self.infoBox = QGroupBox("Player Information", self)
        self.infoBox.setGeometry(20, 610, 940, 80)

        self.lblInfo = QLabel(self.infoBox)
        self.lblInfo.setGeometry(10, 20, 920, 50)
        self.lblInfo.setWordWrap(True)
        self.lblInfo.setFont(QFont("Arial", 11))

        self.lblInfo.setStyleSheet("""
        QLabel{
            background:white;
            border:1px solid #BDBDBD;
            border-radius:8px;
            padding:8px;
            color:#0D47A1;
            font-size:12pt;
            font-weight:bold;
        }
        """)

        self.lblInfo.setText("Select a player to view details.")
        # -----------------------------
        # Status Bar
        # -----------------------------
        self.statusBar().showMessage("Fantasy Cricket Team Builder Ready")

        # -----------------------------
        # Load Default Category
        # -----------------------------
        self.rbBAT.setChecked(True)
        self.load_players("BAT")
    # -----------------------------
    # Load Players by Category
    # -----------------------------
    def load_players(self, category):

        self.listAvailable.clear()

        self.cursor.execute(
            "SELECT player FROM stats WHERE ctg=?",
            (category,)
        )

        players = self.cursor.fetchall()

        for player in players:
            self.listAvailable.addItem(player[0])
    def show_player_info(self, item):

        player = item.text()

        self.cursor.execute(
            """
            SELECT player, ctg, value
            FROM stats
            WHERE player=?
            """,
            (player,)
        )

        data = self.cursor.fetchone()

        if data is None:
            self.lblInfo.setText("No information available.")
            return

        player, category, value = data

        self.lblInfo.setText(
            f"🏏 <b>Player:</b> {player} &nbsp;&nbsp;&nbsp;&nbsp;"
            f"📌 <b>Category:</b> {category} &nbsp;&nbsp;&nbsp;&nbsp;"
            f"💰 <b>Value:</b> {value} Points"
        )
        self.lblInfo.setStyleSheet("""
        QLabel{
            background:white;
            border:1px solid #BDBDBD;
            border-radius:8px;
            padding:10px;
            color:#0D47A1;
            font-size:8pt;
            font-weight:bold;
        }
        """)
    # -----------------------------
    # Add Player
    # -----------------------------
    def add_player(self):

        item = self.listAvailable.currentItem()

        if item is None:
            QMessageBox.warning(
                self,
                "Error",
                "Please select a player."
            )
            return

        player = item.text()

        self.cursor.execute(
            "SELECT value FROM stats WHERE player=?",
            (player,)
        )

        result = self.cursor.fetchone()

        if result is None:
            QMessageBox.warning(
                self,
                "Error",
                "Player not found."
            )
            return

        value = result[0]

        if self.points_left < value:
            QMessageBox.warning(
                self,
                "Error",
                "Not enough points."
            )
            return

        if self.players_left <= 0:
            QMessageBox.warning(
                self,
                "Error",
                "Team already has 11 players."
            )
            return

        self.points_left -= value
        self.players_left -= 1

        self.lblPoints.setText(
            f"Points Left : {self.points_left}"
        )

        self.lblPlayers.setText(
            f"Players Left : {self.players_left}"
        )

        self.listSelected.addItem(player)

        row = self.listAvailable.row(item)
        self.listAvailable.takeItem(row)

    # -----------------------------
    # Remove Player
    # -----------------------------
    def remove_player(self):

        item = self.listSelected.currentItem()

        if item is None:
            QMessageBox.warning(
                self,
                "Error",
                "Select a player to remove."
            )
            return

        player = item.text()

        self.cursor.execute(
        "SELECT value FROM stats WHERE player=?",
         (player,)
        )

        result = self.cursor.fetchone()

        if result is None:
            return

        value = result[0]

        self.points_left += value
        self.players_left += 1

        self.lblPoints.setText(
            f"Points Left : {self.points_left}"
        )

        self.lblPlayers.setText(
            f"Players Left : {self.players_left}"
        )

        self.listAvailable.addItem(player)

        row = self.listSelected.row(item)
        self.listSelected.takeItem(row)
    def validate_team(self):

        players = []

        for i in range(self.listSelected.count()):
            players.append(self.listSelected.item(i).text())

        if len(players) != 11:
            QMessageBox.warning(
                self,
                "Invalid Team",
                "Team must contain exactly 11 players."
            )
            return False

        if len(players) != len(set(players)):
            QMessageBox.warning(
                self,
                "Invalid Team",
                "Duplicate players are not allowed."
            )
            return False

        wk = bat = ar = bwl = 0

        for player in players:

            self.cursor.execute(
                "SELECT ctg FROM stats WHERE player=?",
                (player,)
            )

            result = self.cursor.fetchone()

            if result is None:
                continue

            category = result[0]

            if category == "WK":
                wk += 1
            elif category == "BAT":
                bat += 1
            elif category == "AR":
                ar += 1
            elif category == "BWL":
                bwl += 1

        if not (1 <= wk <= 4):
            QMessageBox.warning(
                self,
                "Invalid Team",
                "Team must contain 1–4 wicketkeepers."
            )
            return False

        if not (3 <= bat <= 6):
            QMessageBox.warning(
                self,
                "Invalid Team",
                "Team must contain 3–6 batsmen."
            )
            return False

        if not (1 <= ar <= 4):
            QMessageBox.warning(
                self,
                "Invalid Team",
                "Team must contain 1–4 all-rounders."
            )
            return False

        if not (3 <= bwl <= 6):
            QMessageBox.warning(
                self,
                "Invalid Team",
                "Team must contain 3–6 bowlers."
            )
            return False

        return True        
    # -----------------------------
    # Save Team
    # -----------------------------
    def save_team(self):
        team_name = self.txtTeam.text().strip()
        if team_name == "":
            QMessageBox.warning(
                self,
                "Error",
                "Enter Team Name"
            )
            return

        self.cursor.execute(
            "SELECT * FROM teams WHERE name=?",
            (team_name,)
        )

        if self.cursor.fetchone() is not None:
            QMessageBox.warning(
                self,
                "Error",
                "Team name already exists.\nUse Update Team instead."
            )
            return

        if not self.validate_team():
            return

        players = []

        for i in range(self.listSelected.count()):
            players.append(self.listSelected.item(i).text())

        players_string = ",".join(players)

        self.cursor.execute(
            """
            INSERT INTO teams(name, players, value, points)
            VALUES(?,?,?,?)
            """,
            (
                team_name,
                players_string,
                self.points_left,
                0
            )
        )

        self.conn.commit()

        QMessageBox.information(
            self,
            "Success",
            "Team Saved Successfully!"
        )
    def resource_path(relative_path):
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(base_path, relative_path)    
    # -----------------------------
    # Calculate Score
    # -----------------------------
    def calculate_score(self):

        score = 0

        for i in range(self.listSelected.count()):

            player = self.listSelected.item(i).text()

            self.cursor.execute(
                """
                SELECT
                    scored,
                    fours,
                    sixes,
                    wickets,
                    catches,
                    stumping,
                    runout
                FROM match
                WHERE player=?
                """,
                (player,)
            )

            data = self.cursor.fetchone()

            if data is None:
                continue

            (
                scored,
                fours,
                sixes,
                wickets,
                catches,
                stumping,
                runout
            ) = data

            score += scored
            score += fours
            score += sixes * 2
            score += wickets * 10
            score += catches * 10
            score += stumping * 10
            score += runout * 10

        self.lblScore.setText(
            f"Score : {score}"
        )
        team_name = self.txtTeam.text().strip()

        if team_name:
            self.cursor.execute(
                "UPDATE teams SET points=? WHERE name=?",
                (score, team_name)
            )
            self.conn.commit()
    def open_team(self):

        team_name = self.txtTeam.text().strip()

        if team_name == "":
            QMessageBox.warning(
                self,
                "Error",
                "Enter Team Name"
            )
            return

        self.cursor.execute(
            "SELECT players, value, points FROM teams WHERE name=?",
            (team_name,)
        )

        result = self.cursor.fetchone()

        if result is None:
            QMessageBox.warning(
                self,
                "Error",
                "Team not found"
            )
            return

        players_string, points_left, score = result

        self.points_left = points_left

        self.listSelected.clear()

        players = players_string.split(",")

        self.players_left = 11 - len(players)

        self.lblPoints.setText(
            f"Points Left : {self.points_left}"
        )

        self.lblPlayers.setText(
            f"Players Left : {self.players_left}"
        )

        self.lblScore.setText(
            f"Score : {score}"
        )

        self.listAvailable.clear()

        if self.rbBAT.isChecked():
            self.load_players("BAT")

        elif self.rbBWL.isChecked():
            self.load_players("BWL")

        elif self.rbAR.isChecked():
            self.load_players("AR")

        elif self.rbWK.isChecked():
            self.load_players("WK")

        # --------------------------------
        # Load saved players
        # --------------------------------

        for player in players:

            player = player.strip()

            if player == "":
                continue

            self.listSelected.addItem(player)

            items = self.listAvailable.findItems(
                player,
                Qt.MatchExactly
            )

            if items:
                row = self.listAvailable.row(items[0])
                self.listAvailable.takeItem(row)

        QMessageBox.information(
            self,
            "Success",
            "Team Loaded Successfully"
        )
    def delete_team(self):

        team_name = self.txtTeam.text().strip()

        if team_name == "":
            QMessageBox.warning(
                self,
                "Error",
                "Enter Team Name"
            )
            return
        reply = QMessageBox.question(
            self,
            "Delete Team",
            f"Are you sure you want to delete '{team_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            return
        self.cursor.execute(
            "SELECT * FROM teams WHERE name=?",
            (team_name,)
        )

        team = self.cursor.fetchone()

        if team is None:
            QMessageBox.warning(
                self,
                "Error",
                "Team not found"
            )
            return

        self.cursor.execute(
            "DELETE FROM teams WHERE name=?",
            (team_name,)
        )

        self.conn.commit()

        QMessageBox.information(
            self,
            "Success",
            "Team deleted successfully!"
        )

    # Clear the GUI
        self.txtTeam.clear()
        self.listSelected.clear()
        self.lblScore.setText("Score : 0")
    def update_team(self):

        team_name = self.txtTeam.text().strip()

        if team_name == "":
            QMessageBox.warning(
                self,
                "Error",
                "Enter Team Name"
            )
            return
        reply = QMessageBox.question(
            self,
            "Update Team",
            f"Update the team '{team_name}' with the current players?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            return
        if not self.validate_team():
            return

        players = []

        for i in range(self.listSelected.count()):
            players.append(
                self.listSelected.item(i).text()
            )
            players_string = ",".join(players)

    # Check whether the team exists
        self.cursor.execute(
            "SELECT * FROM teams WHERE name=?",
            (team_name,)
        )

        if self.cursor.fetchone() is None:
            QMessageBox.warning(
                self,
                "Error",
                "Team not found"
            )
            return

    # Calculate score again before updating
        score = 0

        for player in players:

            self.cursor.execute(
                """
                SELECT
                    scored,
                    fours,
                    sixes,
                    wickets,
                    catches,
                    stumping,
                    runout
                FROM match
                WHERE player=?
                """,
                (player,)
            )

            data = self.cursor.fetchone()

            if data is None:
                continue

            (
                scored,
                fours,
                sixes,
                wickets,
                catches,
                stumping,
                runout
            ) = data

            score += scored
            score += fours
            score += sixes * 2
            score += wickets * 10
            score += catches * 10
            score += stumping * 10
            score += runout * 10

    # Update database
        self.cursor.execute(
            """
            UPDATE teams
            SET
                players=?,
                value=?,
                points=?
            WHERE
                name=?
            """,
            (
                players_string,
                self.points_left,
                score,
                team_name
            )
        )

        self.conn.commit()

        self.lblScore.setText(
            f"Score : {score}"
        )

        QMessageBox.information(
            self,
            "Success",
            "Team Updated Successfully!"
        )
    def reset_team(self):
        reply = QMessageBox.question(
            self,
            "New Team",
            "Do you want to clear the current team and start a new one?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        self.txtTeam.clear()

        self.listAvailable.clear()
        self.listSelected.clear()

        self.points_left = 1500
        self.players_left = 11

        self.lblPoints.setText(f"Points Left : {self.points_left}")
        self.lblPlayers.setText(f"Players Left : {self.players_left}")
        self.lblScore.setText("Score : 0")

        self.rbBAT.setChecked(False)
        self.rbBWL.setChecked(False)
        self.rbAR.setChecked(False)
        self.rbWK.setChecked(False)

        QMessageBox.information(
            self,
            "Success",
            "Ready to create a new team!"
        )
    def show_leaderboard(self):

        dialog = QDialog(self)
        search_layout = QHBoxLayout()
        search_label = QLabel("Search Team :")

        search_box = QLineEdit()
        search_box.setPlaceholderText("Enter team name...")

        search_layout.addWidget(search_label)
        search_layout.addWidget(search_box)
        dialog.setWindowTitle("🏆 Fantasy Cricket Leaderboard")
        dialog.resize(700, 500)

        layout = QVBoxLayout()
        layout.addLayout(search_layout)

        table = QTableWidget()
        table.setStyleSheet("""
        QTableWidget{
            background-color:white;
            alternate-background-color:#F5F5F5;
            gridline-color:#D3D3D3;
            font-size:11px;
        }

        QHeaderView::section{
            background-color:#1976D2;
            color:white;
            font-weight:bold;
            padding:6px;
            border:1px solid #1565C0;
        }
        """)
        table.setMinimumHeight(350)
        table.setMinimumWidth(450)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setDefaultSectionSize(35)
        self.cursor.execute("""
            SELECT name, points
            FROM teams
            ORDER BY points DESC
        """)

        teams = self.cursor.fetchall()
        table.setRowCount(len(teams))
        table.setColumnCount(3)

        table.setHorizontalHeaderLabels([
            "Rank",
            "Team Name",
            "Score"
        ])
        # Auto-size columns
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        # Stretch last column
        table.horizontalHeader().setStretchLastSection(True)

        # Disable editing
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Select complete row
        table.setSelectionBehavior(QTableWidget.SelectRows)

        # Alternate row colors
        table.setAlternatingRowColors(True)

        # Hide row numbers
        table.verticalHeader().setVisible(False)

        for row, team in enumerate(teams):

            rank_item = QTableWidgetItem(str(row + 1))
            name_item = QTableWidgetItem(team[0])
            score_item = QTableWidgetItem(str(team[1]))
            rank_item.setTextAlignment(Qt.AlignCenter)
            name_item.setTextAlignment(Qt.AlignCenter)
            score_item.setTextAlignment(Qt.AlignCenter)

            # Highlight Top 3 Teams
            if row == 0:
                color = QColor(255, 215, 0)      # Gold
            elif row == 1:
                color = QColor(192, 192, 192)    # Silver
            elif row == 2:
                color = QColor(205, 127, 50)     # Bronze
            else:
                color = None

            if color:
                rank_item.setBackground(color)
                name_item.setBackground(color)
                score_item.setBackground(color)

                bold_font = QFont()
                bold_font.setBold(True)

                rank_item.setFont(bold_font)
                name_item.setFont(bold_font)
                score_item.setFont(bold_font)

            table.setItem(row, 0, rank_item)
            table.setItem(row, 1, name_item)
            table.setItem(row, 2, score_item)
        layout.addWidget(table)
        def search_team():
            text = search_box.text().strip().lower()

            for row in range(table.rowCount()):

                item = table.item(row, 1)

                if item is None:
                    continue

                team = item.text().lower()

                if text == "":
                    table.setRowHidden(row, False)
                elif text in team:
                    table.setRowHidden(row, False)
                else:
                    table.setRowHidden(row, True)

        search_box.textChanged.connect(search_team)
       # Export CSV Button
        btnExport = QPushButton("Export CSV")

        btnExport.setStyleSheet("""
        QPushButton{
            background-color:#28A745;
            color:white;
            font-size:13px;
            font-weight:bold;
            border-radius:8px;
        }
        QPushButton:hover{
            background-color:#218838;
        }
        """)

        btnExport.clicked.connect(self.export_csv)

        layout.addWidget(btnExport)

        dialog.setLayout(layout)

        dialog.exec_()
    def export_csv(self):

        # Ask where to save
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Leaderboard",
            "leaderboard.csv",
            "CSV Files (*.csv)"
        )

        if not file_name:
            return

        # Fetch leaderboard data
        self.cursor.execute("""
            SELECT name, points
            FROM teams
            ORDER BY points DESC
        """)

        teams = self.cursor.fetchall()

        # Write CSV
        with open(file_name, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Rank",
                "Team Name",
                "Score"
            ])

            for rank, team in enumerate(teams, start=1):

                writer.writerow([
                    rank,
                    team[0],
                    team[1]
                ])

        QMessageBox.information(
            self,
            "Success",
            "Leaderboard exported successfully!"
        )
    def show_about(self):

        QMessageBox.about(
            self,
            "About Fantasy Cricket",
            """
            <h2>🏏 Fantasy Cricket Team Builder</h2>

            <b>Version:</b> 1.0<br><br>

            <b>Developer:</b> Dhiraj Kumar<br><br>

            <b>Technology Used:</b><br>
            • Python<br>
            • PyQt5<br>
            • SQLite<br><br>

            <b>Features:</b><br>
            ✔ Create Team<br>
            ✔ Save / Open / Update / Delete Team<br>
            ✔ Calculate Score<br>
            ✔ Leaderboard<br>
            ✔ Export CSV<br>
            ✔ Player Information<br><br>

            © 2026 Fantasy Cricket
            """
        )
    def toggle_theme(self):

        if not self.dark_mode:

            self.setStyleSheet("""
            QMainWindow{
                background-color:#2B2B2B;
            }

            QLabel{
                color:white;
            }

            QGroupBox{
                color:white;
                border:2px solid gray;
                border-radius:8px;
                margin-top:12px;
            }
            QListWidget,
            QLineEdit,
            QTableWidget{
                background-color:#2E2E2E;
                color:white;
                border:1px solid gray;
            }

            QListWidget{
                alternate-background-color:#3A3A3A;
                selection-background-color:#1976D2;
                selection-color:white;
            }"""
            )

            self.btnTheme.setText("☀ Light Mode")
            self.dark_mode = True

        else:

            self.setStyleSheet("""
            QMainWindow{
                background-color:#F4F6F8;
            }

            QGroupBox{
                font-size:13px;
                font-weight:bold;
                border:2px solid #BDBDBD;
                border-radius:8px;
                margin-top:12px;
            }

            QGroupBox::title{
                subcontrol-origin: margin;
                left:12px;
                padding:0 5px;
            }
            """)

            self.btnTheme.setText("🌙 Dark Mode")
            self.dark_mode = False
    def open_analysis(self):
        self.analysis_window = DataAnalysisWindow()
        self.analysis_window.show()

    # -----------------------------
    # Close Database
    # -----------------------------
    def closeEvent(self, event):

        self.conn.close()
        event.accept()
# -----------------------------
# Main Program
# -----------------------------
if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))

    # Create Splash Screen
    pixmap = QPixmap(600, 300)
    pixmap.fill(QColor("#0D47A1"))

    splash = QSplashScreen(pixmap)
    splash.setStyleSheet("""
        color: white;
        font-size: 24px;
        font-weight: bold;
    """)

    splash.showMessage(
        "\n\n🏏 Fantasy Cricket Team Builder\n\nLoading...",
        Qt.AlignCenter,
        Qt.white
    )

    splash.show()

    app.processEvents()

    window = FantasyCricket()

    def start_app():
        splash.finish(window)
        window.show()

    QTimer.singleShot(2500, start_app)

    sys.exit(app.exec())