import os
import sys
import configparser

def read_config(key):
    config = configparser.ConfigParser()
    if getattr(sys, 'frozen', False):  # Check if running from PyInstaller bundle
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(__file__)  # Get the directory where the script is located

    config_file_path = os.path.join(exe_dir, 'config.ini')

    if os.path.exists(config_file_path):
        config.read(config_file_path)
        return config['Configuration'].get(key, None)
    else:
        raise FileNotFoundError("Config file config.ini not found.")

def main():
    try:
        terminal = read_config('TERMINAL')
        if terminal is not None:
            print("Terminal:", terminal)
        else:
            print("Terminal not specified in config.ini")
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
