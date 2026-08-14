import os
import sqlite3
from statistics import mean, median

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QMessageBox,
)


class DataAnalysisWindow(QWidget):

    def __init__(self):
        super().__init__()

        # -----------------------------------------
        # Database
        # -----------------------------------------

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DB_PATH = os.path.join(BASE_DIR, "cricket.db")

        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cursor = self.conn.cursor()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                f"Unable to open database:\n{e}"
            )
            return

        # -----------------------------------------
        # Window
        # -----------------------------------------

        self.setWindowTitle("Fantasy Cricket - Data Analysis")
        self.setGeometry(250, 100, 1100, 700)

        # -----------------------------------------
        # Main Layout
        # -----------------------------------------

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # -----------------------------------------
        # Default values
        # -----------------------------------------

        self.total_players = 0
        self.total_runs = 0
        self.average_runs = 0
        self.total_wickets = 0
        self.top_runs = None
        self.top_wickets = None

        # -----------------------------------------
        # Create UI FIRST
        # -----------------------------------------

        self.create_ui()

        # -----------------------------------------
        # Then load database data
        # -----------------------------------------

        self.load_analysis()
    # -------------------------------------------------
    # UI
    # -------------------------------------------------
    def create_ui(self):

        # =========================================
        # Title
        # =========================================

        title = QLabel("Fantasy Cricket Data Analysis")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))

        subtitle = QLabel(
            "Player and Team Performance Dashboard"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 11))

        self.main_layout.addWidget(title)
        self.main_layout.addWidget(subtitle)

        # =========================================
        # Summary Cards
        # =========================================

        cards_layout = QHBoxLayout()

        self.lblPlayers = QLabel(
            f"Players\n{self.total_players}"
        )

        self.lblRuns = QLabel(
            f"Total Runs\n{self.total_runs}"
        )

        self.lblWickets = QLabel(
            f"Total Wickets\n{self.total_wickets}"
        )

        self.lblAverage = QLabel(
    f"Average Runs\n{round(self.average_runs, 2)}"
)

        self.lblMatches = QLabel(
            "Total Matches\n0"
        )

        self.lblTeams = QLabel(
            "Saved Teams\n0"
        )

        cards = [
            self.lblPlayers,
            self.lblRuns,
            self.lblWickets,
            self.lblAverage,
            self.lblMatches,
            self.lblTeams
        ]

        for card in cards:

            card.setAlignment(Qt.AlignCenter)
            card.setMinimumHeight(75)

            card.setStyleSheet("""
                QLabel {
                    background: #E3F2FD;
                    border: 1px solid #90CAF9;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 12pt;
                    font-weight: bold;
                }
            """)

            cards_layout.addWidget(card)

        self.main_layout.addLayout(cards_layout)

        # =========================================
        # Top Performers
        # =========================================

        top_layout = QVBoxLayout()

        self.top_run_label = QLabel("🏏 Top Run Scorer: Loading...")
        self.top_wicket_label = QLabel("🎯 Top Wicket Taker: Loading...")

        self.top_run_label.setStyleSheet(
            "font-size: 14pt; font-weight: bold; padding: 5px;"
        )

        self.top_wicket_label.setStyleSheet(
            "font-size: 14pt; font-weight: bold; padding: 5px;"
        )

        top_layout.addWidget(self.top_run_label)
        top_layout.addWidget(self.top_wicket_label)

        self.main_layout.addLayout(top_layout)
        # =========================================
        # Analysis Selector
        # =========================================

        selector_layout = QHBoxLayout()

        selector_label = QLabel("Analyze by:")

        self.combo = QComboBox()

        self.combo.addItems([
            "Top Run Scorers",
            "Top Wicket Takers",
            "Highest Strike Rate",
            "Best Bowling Economy",
            "All Players"
        ])
        self.combo.currentIndexChanged.connect(
            self.load_analysis
        )

        refresh_button = QPushButton("Refresh")

        refresh_button.clicked.connect(
            self.load_analysis
        )

        selector_layout.addWidget(selector_label)
        selector_layout.addWidget(self.combo)
        selector_layout.addWidget(refresh_button)
        selector_layout.addStretch()

        self.main_layout.addLayout(selector_layout)

        # =========================================
        # Table
        # =========================================

        self.table = QTableWidget()

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.main_layout.addWidget(self.table)
        # =========================================
        # Performance Chart
        # =========================================

        self.chart = FigureCanvas(Figure(figsize=(8, 3)))

        self.main_layout.addWidget(self.chart)

        self.ax = self.chart.figure.add_subplot(111)

        # =========================================
        # Insights
        # =========================================

        self.insights = QLabel(
            "Analysis insights will appear here."
        )

        self.insights.setWordWrap(True)

        self.insights.setStyleSheet("""
            QLabel {
                background: #F5F5F5;
                border: 1px solid #DDDDDD;
                border-radius: 8px;
                padding: 12px;
                font-size: 11pt;
            }
        """)

        self.main_layout.addWidget(self.insights)
   
    def create_card(self, title, value):

        card = QFrame()

        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #DDDDDD;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 11pt;
                color: #666666;
            }
        """)

        value_label = QLabel(str(value))
        value_label.setStyleSheet("""
            QLabel {
                font-size: 20pt;
                font-weight: bold;
            }
        """)

        value_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card
    # -------------------------------------------------
    # Load analysis
    # -------------------------------------------------

    def load_analysis(self):

        try:

            # =========================================
            # Player statistics
            # =========================================

            stats = self.cursor.execute("""
                SELECT
                    player,
                    matches,
                    runs,
                    hundreds,
                    fifties,
                    value,
                    ctg
                FROM stats
            """).fetchall()

            # =========================================
            # Match statistics
            # =========================================

            match_stats = self.cursor.execute("""
                SELECT
                    player,
                    scored,
                    faced,
                    fours,
                    sixes,
                    bowled,
                    maidens,
                    givenruns,
                    wickets,
                    catches,
                    stumping,
                    runout
                FROM match
            """).fetchall()

            # =========================================
            # Teams
            # =========================================

            teams = self.cursor.execute("""
                SELECT
                    name,
                    players,
                    value,
                    points
                FROM teams
            """).fetchall()

            # =========================================
            # Summary
            # =========================================

            total_players = len(stats)

            total_runs = sum(
                row[2] or 0
                for row in stats
            )

            average_runs = (
                total_runs / total_players
                if total_players > 0
                else 0
            )

            total_matches = sum(
                row[1] or 0
                for row in stats
            )

            total_wickets = sum(
                row[8] or 0
                for row in match_stats
            )

            # Update summary cards

            self.lblPlayers.setText(
                f"Players\n{total_players}"
            )

            self.lblRuns.setText(
                f"Total Runs\n{total_runs}"
            )

            self.lblWickets.setText(
                f"Total Wickets\n{total_wickets}"
            )

            self.lblMatches.setText(
                f"Total Matches\n{total_matches}"
            )

            self.lblTeams.setText(
                f"Saved Teams\n{len(teams)}"
            )

            # =========================================
            # Top performers
            # =========================================

            if stats:

                top_runs = max(
                    stats,
                    key=lambda row: row[2] or 0
                )

                self.top_run_label.setText(
                    f"🏏 Top Run Scorer: "
                    f"{top_runs[0]} - {top_runs[2]} runs"
                )

            else:

                self.top_run_label.setText(
                    "🏏 Top Run Scorer: No data available"
                )

            if match_stats:

                top_wickets = max(
                    match_stats,
                    key=lambda row: row[8] or 0
                )

                self.top_wicket_label.setText(
                    f"🎯 Top Wicket Taker: "
                    f"{top_wickets[0]} - {top_wickets[8]} wickets"
                )

            else:

                self.top_wicket_label.setText(
                    "🎯 Top Wicket Taker: No data available"
                )

            # =========================================
            # Combine player data
            # =========================================

            match_dict = {}

            for row in match_stats:

                player = row[0]

                match_dict[player] = {
                    "scored": row[1] or 0,
                    "faced": row[2] or 0,
                    "fours": row[3] or 0,
                    "sixes": row[4] or 0,
                    "bowled": row[5] or 0,
                    "maidens": row[6] or 0,
                    "givenruns": row[7] or 0,
                    "wickets": row[8] or 0,
                    "catches": row[9] or 0,
                    "stumping": row[10] or 0,
                    "runout": row[11] or 0,
                }

            players = []

            for row in stats:

                player = row[0]

                m = match_dict.get(
                    player,
                    {
                        "scored": 0,
                        "faced": 0,
                        "fours": 0,
                        "sixes": 0,
                        "bowled": 0,
                        "maidens": 0,
                        "givenruns": 0,
                        "wickets": 0,
                        "catches": 0,
                        "stumping": 0,
                        "runout": 0,
                    }
                )

                # -----------------------------------------
                # Strike rate
                # -----------------------------------------

                faced = m["faced"]

                strike_rate = (
                    (m["scored"] / faced) * 100
                    if faced > 0
                    else 0
                )

                # -----------------------------------------
                # Bowling economy
                # -----------------------------------------

                bowled = m["bowled"]

                economy = (
                    (m["givenruns"] / bowled) * 6
                    if bowled > 0
                    else 0
                )

                players.append({
                    "player": player,
                    "matches": row[1] or 0,
                    "runs": row[2] or 0,
                    "hundreds": row[3] or 0,
                    "fifties": row[4] or 0,
                    "value": row[5] or 0,
                    "category": row[6] or "",

                    "scored": m["scored"],
                    "faced": faced,
                    "fours": m["fours"],
                    "sixes": m["sixes"],
                    "bowled": bowled,
                    "givenruns": m["givenruns"],
                    "wickets": m["wickets"],
                    "catches": m["catches"],

                    "strike_rate": strike_rate,
                    "economy": economy,
                })

            # =========================================
            # Selected analysis
            # =========================================

            option = self.combo.currentText()

            # =========================================
            # 1. Top Run Scorers
            # =========================================

            if option == "Top Run Scorers":

                players.sort(
                    key=lambda x: x["runs"],
                    reverse=True
                )

                players = players[:10]

                headers = [
                    "Player",
                    "Runs",
                    "Matches",
                    "100s",
                    "50s",
                    "Value"
                ]

                data = [
                    [
                        p["player"],
                        p["runs"],
                        p["matches"],
                        p["hundreds"],
                        p["fifties"],
                        f"{p['value']:.1f}"
                    ]
                    for p in players
                ]

                self.set_table(headers, data)

                self.create_run_insight(players)

                self.update_chart(
                    players,
                    option
                )

            # =========================================
            # 2. Top Wicket Takers
            # =========================================

            elif option == "Top Wicket Takers":

                players.sort(
                    key=lambda x: x["wickets"],
                    reverse=True
                )

                players = players[:10]

                headers = [
                    "Player",
                    "Wickets",
                    "Economy",
                    "Matches",
                    "Value"
                ]

                data = [
                    [
                        p["player"],
                        p["wickets"],
                        f"{p['economy']:.2f}",
                        p["matches"],
                        f"{p['value']:.1f}"
                    ]
                    for p in players
                ]

                self.set_table(headers, data)

                self.create_wicket_insight(players)

                self.update_chart(
                    players,
                    option
                )

            # =========================================
            # 3. Highest Strike Rate
            # =========================================

            elif option == "Highest Strike Rate":

                players = [
                    p for p in players
                    if p["faced"] > 0
                ]

                players.sort(
                    key=lambda x: x["strike_rate"],
                    reverse=True
                )

                players = players[:10]

                headers = [
                    "Player",
                    "Strike Rate",
                    "Runs",
                    "Balls",
                    "Fours",
                    "Sixes"
                ]

                data = [
                    [
                        p["player"],
                        f"{p['strike_rate']:.2f}",
                        p["scored"],
                        p["faced"],
                        p["fours"],
                        p["sixes"]
                    ]
                    for p in players
                ]

                self.set_table(headers, data)

                self.create_strike_rate_insight(players)

                self.update_chart(
                    players,
                    option
                )

            # =========================================
            # 4. Best Bowling Economy
            # =========================================

            elif option == "Best Bowling Economy":

                players = [
                    p for p in players
                    if p["bowled"] > 0
                ]

                players.sort(
                    key=lambda x: x["economy"]
                )

                players = players[:10]

                headers = [
                    "Player",
                    "Economy",
                    "Wickets",
                    "Runs Given",
                    "Balls"
                ]

                data = [
                    [
                        p["player"],
                        f"{p['economy']:.2f}",
                        p["wickets"],
                        p["givenruns"],
                        p["bowled"]
                    ]
                    for p in players
                ]

                self.set_table(headers, data)

                self.create_economy_insight(players)

                self.update_chart(
                    players,
                    option
                )

            # =========================================
            # 5. All Players
            # =========================================

            else:

                players.sort(
                    key=lambda x: x["runs"],
                    reverse=True
                )

                headers = [
                    "Player",
                    "Category",
                    "Runs",
                    "Wickets",
                    "Strike Rate",
                    "Economy",
                    "Value"
                ]

                data = [
                    [
                        p["player"],
                        p["category"],
                        p["runs"],
                        p["wickets"],
                        f"{p['strike_rate']:.2f}",
                        f"{p['economy']:.2f}",
                        f"{p['value']:.1f}"
                    ]
                    for p in players
                ]

                self.set_table(headers, data)

                self.create_general_insight(players)

                self.update_chart(
                    players,
                    option
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Analysis Error",
                str(e)
            )
    # -------------------------------------------------
    # Table
    # -------------------------------------------------

    def set_table(self, headers, data):

        self.table.clear()

        self.table.setColumnCount(len(headers))

        self.table.setRowCount(len(data))

        self.table.setHorizontalHeaderLabels(headers)

        for row_index, row in enumerate(data):

            for column_index, value in enumerate(row):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row_index,
                    column_index,
                    item
                )

    # -------------------------------------------------
    # Insights
    # -------------------------------------------------

    def create_run_insight(self, players):

        if not players:
            self.insights.setText(
                "No player data available."
            )
            return

        top = players[0]

        runs = [p["runs"] for p in players]

        self.insights.setText(
            f"🏏 Top Run Scorer: {top['player']} "
            f"with {top['runs']} runs.\n"
            f"Average runs among displayed players: "
            f"{mean(runs):.2f}\n"
            f"Median runs: {median(runs):.2f}"
        )

    def create_wicket_insight(self, players):

        if not players:
            self.insights.setText(
                "No bowling data available."
            )
            return

        top = players[0]

        self.insights.setText(
            f"🎯 Top Wicket Taker: {top['player']} "
            f"with {top['wickets']} wickets.\n"
            f"Best economy among displayed players: "
            f"{top['economy']:.2f}"
        )

    def create_strike_rate_insight(self, players):

        if not players:
            return

        top = players[0]

        self.insights.setText(
            f"⚡ Highest Strike Rate: {top['player']} "
            f"with {top['strike_rate']:.2f}.\n"
            f"Runs scored: {top['scored']} "
            f"from {top['faced']} balls."
        )

    def create_economy_insight(self, players):

        if not players:
            return

        top = players[0]

        self.insights.setText(
            f"🎯 Best Bowling Economy: {top['player']} "
            f"with {top['economy']:.2f} runs per over.\n"
            f"Wickets: {top['wickets']}"
        )

    def create_general_insight(self, players):

        if not players:
            self.insights.setText(
                "No player data available."
            )
            return

        run_values = [
            p["runs"] for p in players
        ]

        self.insights.setText(
            f"Player analysis loaded successfully.\n"
            f"Average runs: {mean(run_values):.2f}\n"
            f"Median runs: {median(run_values):.2f}\n"
            f"Highest runs: {max(run_values)}"
        )
    def update_chart(self, players, option):

        self.ax.clear()

        if not players:
            self.ax.set_title("No data available")
            self.chart.draw()
            return

        names = [p["player"] for p in players]

        # -----------------------------------------
        # Select chart data
        # -----------------------------------------

        if option == "Top Run Scorers":

            values = [p["runs"] for p in players]

            title = "Top 10 Run Scorers"
            ylabel = "Runs"

        elif option == "Top Wicket Takers":

            values = [p["wickets"] for p in players]

            title = "Top 10 Wicket Takers"
            ylabel = "Wickets"

        elif option == "Highest Strike Rate":

            values = [p["strike_rate"] for p in players]

            title = "Highest Strike Rate"
            ylabel = "Strike Rate"

        elif option == "Best Bowling Economy":

            values = [p["economy"] for p in players]

            title = "Best Bowling Economy"
            ylabel = "Economy"

        else:

            values = [p["runs"] for p in players]

            title = "Player Run Comparison"
            ylabel = "Runs"

        # -----------------------------------------
        # Draw chart
        # -----------------------------------------

        self.ax.bar(names, values)

        self.ax.set_title(
            title,
            fontsize=14,
            fontweight="bold",
            pad=12
        )

        self.ax.set_xlabel(
            "Players",
            fontsize=10
        )

        self.ax.set_ylabel(
            ylabel,
            fontsize=10
        )

        self.ax.tick_params(
            axis="x",
            rotation=45
        )

        # -----------------------------------------
        # Display values above bars
        # -----------------------------------------

        for i, value in enumerate(values):

            self.ax.text(
                i,
                value,
                f"{value:.1f}" if isinstance(value, float) else str(value),
                ha="center",
                va="bottom",
                fontsize=9
            )

        self.chart.figure.subplots_adjust(
            left=0.10,
            right=0.98,
            top=0.88,
            bottom=0.30
        )


        self.chart.draw()
    # -------------------------------------------------

    def closeEvent(self, event):

        try:
            self.conn.close()
        except Exception:
            pass

        event.accept()
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    window = DataAnalysisWindow()
    window.show()

    sys.exit(app.exec())