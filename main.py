import time
import requests
import json
import os

# Fungsi untuk menampilkan logo
def echo_logo():
    print("\033[1;35m")
    print("/* ################################# */")
    print("/* # __    __   _____    __     __ # */")
    print("/* #/ / /\ \ \  \_   \  / /    / / # */")
    print("/* #\ \/  \/ /   / /\/ / /    / /  # */")
    print("/* # \  /\  / /\/ /_  / /___ / /___# */")
    print("/* #  \/  \/  \____/  \____/ \____/# */")
    print("/* ################################# */")
    print("\033[0m")
    print("    ++WILL++")  
    print("Hanya konsumsi pribadi")
    print("")

BASE_URL = "https://gateway-run.bls.dev/api/v1/nodes/"

# Fungsi untuk mengecek kesehatan
def check_health():
    health_url = "https://gateway-run.bls.dev/health"
    response = requests.get(health_url)
    if response.status_code == 200:
        print(f"✅ Health check successful")
    else:
        print(f"❌ Health check failed with status code: {response.status_code}")

# Fungsi untuk memulai sesi
def start_session(bearer_token, pubkey):
    start_session_url = f"{BASE_URL}{pubkey}/start-session"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0"
    }
    print(f"🚀 Starting session for pubkey {pubkey[-4:]}")
    response = requests.post(start_session_url, headers=headers)
    if response.status_code == 200:
        print(f"🟢 Session started successfully for pubkey {pubkey[-4:]}")
    else:
        print(f"❌ Failed to start session for pubkey {pubkey[-4:]} with status code: {response.status_code}")

# Fungsi untuk mengirimkan ping
def send_ping(bearer_token, pubkey):
    ping_url = f"{BASE_URL}{pubkey}/ping"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0"
    }
    print(f"📡 Sending ping for pubkey {pubkey[-4:]}")
    response = requests.post(ping_url, headers=headers)
    if response.status_code == 200:
        print(f"✅ Ping successful for pubkey {pubkey[-4:]}")
    else:
        print(f"❌ Ping failed for pubkey {pubkey[-4:]} with status code: {response.status_code}")

# Fungsi untuk mengambil informasi reward
def get_rewards(bearer_token, pubkey):
    rewards_url = f"{BASE_URL}{pubkey}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Mozilla/5.0"
    }
    print(f"⏲️ Fetching reward information for pubkey {pubkey[-4:]}")
    response = requests.get(rewards_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        total_reward = data.get("totalReward", "Not found")
        today_reward = data.get("todayReward", "Not found")
        print(f"🏅 Total Reward for pubkey {pubkey[-4:]}: {total_reward}")
        print(f"📅 Today's Reward for pubkey {pubkey[-4:]}: {today_reward}")
    else:
        print(f"❌ Failed to fetch reward for pubkey {pubkey[-4:]} with status code: {response.status_code}")

# Fungsi untuk memproses akun
def process_account(bearer_token, pubkey):
    print(f"\nProcessing account for pubkey {pubkey[-4:]}...\n")
    check_health()
    start_session(bearer_token, pubkey)
    send_ping(bearer_token, pubkey)
    get_rewards(bearer_token, pubkey)

# Fungsi untuk memproses semua akun
def process_all_accounts(accounts):
    for account in accounts:
        bearer_token = account["bearer"]
        pubkey = account["pubkey"]
        process_account(bearer_token, pubkey)
        time.sleep(5)

# Fungsi untuk memuat akun dari file JSON
def load_accounts_from_file():
    if not os.path.exists("account.json"):
        print("❌ File account.json tidak ditemukan. Membuat file baru.")
        return []
    with open("account.json", "r") as file:
        return json.load(file)

# Fungsi utama
def main():
    echo_logo()
    print("\nWelcome to the account processing script!")

    while True:
        accounts = load_accounts_from_file()
        if not accounts:
            print("\n❌ Tidak ada akun untuk diproses. Tambahkan akun di account.json dan jalankan ulang.")
            time.sleep(10)
            continue

        print(f"\n🔄 Processing {len(accounts)} account(s)...\n")
        process_all_accounts(accounts)

        print("🔄 Waiting 5 seconds before the next run...")
        time.sleep(5)

if __name__ == "__main__":
    main()
