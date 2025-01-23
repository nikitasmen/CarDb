from PyQt5.QtWidgets import QApplication
from gui import CarTrackerApp
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarTrackerApp()
    window.show()
    sys.exit(app.exec_())
