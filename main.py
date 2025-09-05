import sys
import os

# Add the data directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from interfaces import Cli, run_flet_app

if __name__ == "__main__":
    try:
        interface = 'flet'  # Default interface for mobile

        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg in ['--flet', '--cli']:
                interface = arg[2:]
            else:
                print(f"Unknown argument: {arg}")
                print("Usage: python main.py [--flet|--cli]")
                sys.exit(1)

        if interface == 'cli':
            print("Starting CarDb in CLI mode")
            print("Please enter the commands as per the instructions")
            print("Type '--help' to see the available commands")
            print("Type 'exit' to exit the program")
            cli = Cli()
            cli.run()
        else:  # Default to flet for mobile
            print("Starting CarDb Mobile App")
            run_flet_app()

    except KeyboardInterrupt:
        print("\nExiting application.")
        sys.exit(0)
