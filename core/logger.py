from colorama import Fore
from datetime import datetime

class Logger():
    def __init__(self, name: str) -> None:
        self.name: str = name

    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def debug(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] [{self.name}/DEBUG]: {message}")

    def info(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] [{self.name}/{Fore.BLUE}INFO{Fore.RESET}]: {message}")

    def warn(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] [{self.name}/{Fore.LIGHTYELLOW_EX}WARN{Fore.RESET}]: {message}")

    def error(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] [{self.name}/{Fore.LIGHTRED_EX}ERROR{Fore.RESET}]: {message}")

    def critical(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] [{self.name}/{Fore.RED}CRITICAL{Fore.RESET}]: {message}")