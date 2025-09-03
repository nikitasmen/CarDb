import os
import subprocess

def build_apk():
    """
    Builds the Flet app into an APK file.
    """
    # Ensure the Flet command is available
    try:
        subprocess.run(["flet", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Flet is not installed or not in the system's PATH.")
        print("Please install Flet with: pip install flet")
        return

    # Build the APK
    print("Building APK...")
    # The flet tool will automatically use main.py and flet.yml
    build_command = [
        "flet",
        "build",
        "apk",
        "--module-name",
        "mobile_app"
    ]

    try:
        # Using Popen to stream output in real-time
        process = subprocess.Popen(build_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)

        for line in iter(process.stdout.readline, ''):
            print(line, end='')

        process.wait()

        if process.returncode == 0:
            print("\nAPK build successful!")
            print("The APK file can be found in the 'build/apk' directory.")
        else:
            print(f"\nAPK build failed with exit code {process.returncode}.")

    except FileNotFoundError:
        print("Error: 'flet' command not found. Make sure Flet is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        print("APK build failed.")
        print(e)

if __name__ == "__main__":
    build_apk()
