from colorama import Fore, Style

def red(string):
	return f"{Fore.RED}{string}{Style.RESET_ALL}"

def yellow(string):
	return f"{Fore.YELLOW}{string}{Style.RESET_ALL}"

def green(string):
	return f"{Fore.GREEN}{string}{Style.RESET_ALL}"

def blue(string):
	return f"{Fore.BLUE}{string}{Style.RESET_ALL}"