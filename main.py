import sys
import os

# Add the data directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from PyQt5.QtWidgets import QApplication
from interfaces import CarTrackerApp, Cli, run_flet_app

if __name__ == "__main__":
    print("Starting Car Tracker App")
    try:
        interface = 'flet'  # Default interface

        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg in ['--flet', '--cli', '--gui']:
                interface = arg[2:]
            else:
                print(f"Unknown argument: {arg}")
                print("Usage: python main.py [--flet|--gui|--cli]")
                sys.exit(1)

        if interface == 'cli':
            print("Starting Car Tracker App in CLI mode")
            print("Please enter the commands as per the instructions")
            print("Type '--help' to see the available commands")
            print("Type 'exit' to exit the program")
            cli = Cli()
            cli.run()
        elif interface == 'gui':
            print("Starting Car Tracker App in GUI mode")
            app = QApplication(sys.argv)
            window = CarTrackerApp()
            window.show()
            sys.exit(app.exec_())
        elif interface == 'flet':
            print("Starting Car Tracker App in Flet mode")
            run_flet_app()

    except KeyboardInterrupt:
        print("\nExiting application.")
        sys.exit(0)
