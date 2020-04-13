from colorama import Fore, Style, init
from termcolor import colored

init()
def red(string):
	return colored(f"{Fore.RED}{string}{Style.RESET_ALL}")

def yellow(string):
	return colored(f"{Fore.YELLOW}{string}{Style.RESET_ALL}")

def green(string):
	return colored(f"{Fore.GREEN}{string}{Style.RESET_ALL}")

def blue(string):
	return colored(f"{Fore.BLUE}{string}{Style.RESET_ALL}")