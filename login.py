import sys
from PyQt5.QtCore import Qt,  QSettings
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QCheckBox
)

from main import FantasyCricket


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.settings = QSettings("FantasyCricket", "Login")

        self.setWindowTitle("Fantasy Cricket Login")
        self.setGeometry(500, 200, 450, 330)
        self.setWindowIcon(QIcon("icon.ico"))

        # Background
        self.setStyleSheet("""
        QWidget{
            background:#F4F6F8;
        }
        """)

        # Title
        title = QLabel("Fantasy Cricket", self)
        title.setGeometry(70, 20, 310, 35)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Team Builder Login", self)
        subtitle.setGeometry(90, 55, 280, 25)
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setAlignment(Qt.AlignCenter)

        # Username
        lblUser = QLabel("Username", self)
        lblUser.setGeometry(40, 100, 80, 25)

        self.txtUser = QLineEdit(self)
        self.txtUser.setGeometry(130, 95, 220, 35)
        self.txtUser.setPlaceholderText("Enter username")

        # Password
        lblPass = QLabel("Password", self)
        lblPass.setGeometry(40, 150, 80, 25)

        self.txtPass = QLineEdit(self)
        self.txtPass.setGeometry(130, 145, 220, 35)
        self.txtPass.setPlaceholderText("Enter password")
        self.txtPass.setEchoMode(QLineEdit.Password)

        # Textbox Style
        textbox_style = """
        QLineEdit{
            border:2px solid #B0BEC5;
            border-radius:8px;
            padding:6px;
            font-size:11pt;
            background:white;
        }

        QLineEdit:focus{
            border:2px solid #1976D2;
        }
        """

        self.txtUser.setStyleSheet(textbox_style)
        self.txtPass.setStyleSheet(textbox_style)

        # Show Password
        self.chkShow = QCheckBox("Show Password", self)
        self.chkShow.setGeometry(130, 190, 150, 25)
        self.chkShow.toggled.connect(self.show_password)

        # Remember Me
        self.chkRemember = QCheckBox("Remember Me", self)
        self.chkRemember.setGeometry(130, 215, 150, 25)

        # Login Button
        self.btnLogin = QPushButton("Login", self)
        self.btnLogin.setGeometry(130, 255, 180, 42)

        self.btnLogin.setStyleSheet("""
        QPushButton{
            background:#1976D2;
            color:white;
            font-size:12pt;
            font-weight:bold;
            border-radius:8px;
        }

        QPushButton:hover{
            background:#1565C0;
        }

        QPushButton:pressed{
            background:#0D47A1;
        }
        """)

        self.btnLogin.clicked.connect(self.check_login)
        saved_user = self.settings.value("username", "")
        remember = self.settings.value("remember", "false")

        self.txtUser.setText(saved_user)

        if remember == "true":
            self.chkRemember.setChecked(True)

    # ------------------------
    # Show Password
    # ------------------------
    def show_password(self, checked):

        if checked:
            self.txtPass.setEchoMode(QLineEdit.Normal)
        else:
            self.txtPass.setEchoMode(QLineEdit.Password)

    # ------------------------
    # Login
    # ------------------------
    def check_login(self):

        username = self.txtUser.text().strip()
        password = self.txtPass.text().strip()

        if username == "admin" and password == "admin123":

            QMessageBox.information(
                self,
                "Success",
                "Login Successful!"
            )
            if self.chkRemember.isChecked():
                self.settings.setValue("username", username)
                self.settings.setValue("remember", "true")
            else:
                self.settings.setValue("username", "")
                self.settings.setValue("remember", "false")

            self.main_window = FantasyCricket()
            self.main_window.show()

            self.close()

        else:

            QMessageBox.warning(
                self,
                "Login Failed",
                "Invalid Username or Password"
            )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())