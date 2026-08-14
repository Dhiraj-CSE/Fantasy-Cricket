import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar
)

from login import LoginWindow


class SplashScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fantasy Cricket")
        self.setFixedSize(500, 320)
        self.move(
            QApplication.desktop().screen().rect().center()
            - self.rect().center()
        )

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""
        QWidget{
            background:white;
        }
        """)

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo = QLabel()

        pixmap = QPixmap("icon.ico")

        if not pixmap.isNull():
            logo.setPixmap(
                pixmap.scaled(
                    80,
                    80,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        logo.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Fantasy Cricket")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        subtitle = QLabel("Team Builder System")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 11))

        self.progress = QProgressBar()

        self.progress.setMaximum(100)

        self.progress.setValue(0)

        self.progress.setTextVisible(True)
        self.progress.setFormat("Loading... %p%")
        self.progress.setStyleSheet("""
        QProgressBar{
            border:1px solid #999;
            border-radius:5px;
            background:#EEEEEE;
            height:15px;
        }

        QProgressBar::chunk{
            background:#1976D2;
        }
        """)

        developer = QLabel("Developed by Dhiraj Kumar")
        developer.setAlignment(Qt.AlignCenter)

        layout.addStretch()

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        layout.addWidget(self.progress)

        layout.addSpacing(15)

        layout.addWidget(developer)

        layout.addStretch()

        self.setLayout(layout)

        self.value = 0

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_progress)

        self.timer.start(30)

    def update_progress(self):

        self.value += 2

        self.progress.setValue(self.value)

        if self.value >= 100:

            self.timer.stop()

            self.login = LoginWindow()

            self.login.show()

            self.close()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    splash = SplashScreen()

    splash.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        print(e)
        input("Press Enter...")