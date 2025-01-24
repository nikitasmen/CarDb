from PyQt5.QtWidgets import QApplication
from gui import CarTrackerApp
from cli import Cli
import sys

if __name__ == "__main__":
    print ("Starting Car Tracker App") 
    load = input("Load ui or cli? (Gui/Cli): (Enter default is Gui) ")
    if load == "cli":
        print ("Starting Car Tracker App in CLI mode")
        print ("Please enter the commands as per the instructions")
        print ("Type '--help' to see the available commands")
        print ("Type 'exit' to exit the program")
        cli = Cli()
        cli.run()  
    else:
        print("Starting Car Tracker App in GUI mode")
        app = QApplication(sys.argv)
        window = CarTrackerApp()
        window.show()
        sys.exit(app.exec_())
