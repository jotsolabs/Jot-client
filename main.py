import os
import socket
import getpass
import requests
import argparse
import win32security
import time
from windows_tools.installed_software import get_installed_software


SERVER_URL = "http://127.0.0.1:8000"

def register_startup():
    import winreg as reg
    key = reg.HKEY_CURRENT_USER
    subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "Jot-client v0.0.1 DEBUG"

    try:
        reg.OpenKey(key, subkey, 0, reg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        reg.CreateKey(key, subkey)

    with reg.OpenKey(key, subkey, 0, reg.KEY_ALL_ACCESS) as reg_key:
        current_path = os.path.abspath(__file__)
        reg.SetValueEx(reg_key, app_name, 0, reg.REG_SZ, current_path)

def get_user_sid():
    user_name = getpass.getuser()
    domain = os.environ['USERDOMAIN']
    sid, _, _ = win32security.LookupAccountName(domain, user_name)
    return str(sid).split(":")[1]

def send_report(debug=False):
    hostname = socket.gethostname()
    username = getpass.getuser()
    ip_address = socket.gethostbyname(hostname)
    user_sid = get_user_sid()
    installed_programs = get_installed_software()

    payload = {
        "sid": user_sid,
        "hostname": hostname,
        "username": username,
        "ip_address": ip_address,
        "installed_programs": installed_programs
    }

    print("Payload:", payload)

    if not debug:
        try:
            response = requests.post(f"{SERVER_URL}/report", json=payload)
            response.raise_for_status()
            print("Report sent successfully.")
        except Exception as e:
            print(f"Failed to send report: {e}")
    else:
        print("Skipping sending report in debug mode.")

def main(debug=False):
    if not debug:
        register_startup()

    while True:
        send_report(debug)
        time.sleep(3600)  # repeat every hour

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jot-client")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode (do not add to startup and skip sending requests)")
    args = parser.parse_args()

    main(args.debug)
