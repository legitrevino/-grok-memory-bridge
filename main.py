# grok-memory-bridge — merges every Grok thread into ONE so it never forgets
# Made because Grok kept gaslighting people about voice glitches

import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Load config (you will create config.json locally, never push it)
try:
    with open("config.json") as f:
        config = json.load(f)
except:
    print("Create config.json first (copy from config.json.example)")
    exit()

# Headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

def login():
    driver.get("https://x.com/login")
    time.sleep(6)
    driver.find_element("name", "text").send_keys(config["x_username"])
    driver.find_element("xpath", "//span[contains(text(),'Next')]").click()
    time.sleep(3)
    driver.find_element("name", "password").send_keys(config["x_password"])
    driver.find_element("xpath", "//span[contains(text(),'Log in')]").click()
    time.sleep(10)

def get_history():
    driver.get("https://grok.x.ai")
    time.sleep(8)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    turns = soup.find_all("div", {"data-testid": "conversation-turn"})
    return [t.get_text(strip=True)[:500] for t in turns[-400:]]  # last ~400 turns

def main():
    print("Logging in...")
    login()
    print("Scraping all your Grok threads...")
    history = get_history()
    mega = "\n\n=== OLD THREAD CONTINUED ===\n\n".join(history)
    print(f"Merged {len(history)} messages into one mega-context")
    print("\nCopy-paste this into a NEW Grok chat to make it remember forever:\n")
    print("——— START MEGATHREAD ———")
    print(mega)
    print("——— END MEGATHREAD ———")

if __name__ == "__main__":
    main()