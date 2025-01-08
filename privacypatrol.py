import os
import subprocess
import logging
from datetime import datetime

class PrivacyPatrol:
    def __init__(self):
        logging.basicConfig(filename='privacy_patrol.log', level=logging.INFO)
        self.privacy_checks = [
            self.check_firewall_status,
            self.check_antivirus_status,
            self.check_os_updates,
            self.check_privacy_settings
        ]

    def check_firewall_status(self):
        try:
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'],
                                    capture_output=True, text=True)
            if "State ON" not in result.stdout:
                logging.warning("Firewall is not enabled on all profiles.")
                return "Firewall is not enabled on all profiles."
            return "Firewall is active."
        except Exception as e:
            logging.error(f"Error checking firewall status: {e}")
            return f"Error checking firewall status: {e}"

    def check_antivirus_status(self):
        try:
            result = subprocess.run(['powershell', 'Get-MpComputerStatus'],
                                    capture_output=True, text=True)
            if "AMServiceEnabled : True" not in result.stdout:
                logging.warning("Antivirus is not active.")
                return "Antivirus is not active."
            return "Antivirus is active."
        except Exception as e:
            logging.error(f"Error checking antivirus status: {e}")
            return f"Error checking antivirus status: {e}"

    def check_os_updates(self):
        try:
            result = subprocess.run(['powershell', '(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search("IsInstalled=0")'],
                                    capture_output=True, text=True)
            if "Updates" in result.stdout:
                logging.warning("There are pending OS updates.")
                return "There are pending OS updates."
            return "OS is up to date."
        except Exception as e:
            logging.error(f"Error checking OS updates: {e}")
            return f"Error checking OS updates: {e}"

    def check_privacy_settings(self):
        # Example: Check if location services are enabled
        try:
            result = subprocess.run(['powershell', 'Get-ItemProperty', 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location', '-Name', 'Value'],
                                    capture_output=True, text=True)
            if "Deny" not in result.stdout:
                logging.warning("Location services are enabled.")
                return "Location services are enabled."
            return "Location services are disabled."
        except Exception as e:
            logging.error(f"Error checking privacy settings: {e}")
            return f"Error checking privacy settings: {e}"

    def run_checks(self):
        logging.info(f"Privacy checks started at {datetime.now()}")
        results = []
        for check in self.privacy_checks:
            result = check()
            results.append(result)
        logging.info(f"Privacy checks completed at {datetime.now()}")
        return results

if __name__ == '__main__':
    patrol = PrivacyPatrol()
    alerts = patrol.run_checks()
    for alert in alerts:
        print(alert)