#!/usr/bin/env python3
# BIN LOOKUP + VBV CHECKER
# First run will ask for Stripe test key and save it.

import requests
import time
import json
import os
from pathlib import Path

CONFIG_FILE = Path.home() / ".stripe_key.json"

def save_key(key):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"key": key}, f)

def load_key():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("key")
    return None

def get_stripe_key():
    key = load_key()
    if not key:
        print("\n🔑 Stripe test key not found.")
        print("Get your free key from: https://dashboard.stripe.com/test/apikeys")
        key = input("Paste your Stripe test key (sk_test_... or pk_test_...): ").strip()
        if key.startswith(("sk_test_", "pk_test_")):
            save_key(key)
            print("✅ Key saved for future runs.\n")
        else:
            print("❌ Invalid key format. Must start with sk_test_ or pk_test_")
            exit(1)
    return key

STRIPE_TEST_KEY = get_stripe_key()

def bin_lookup(bin_num):
    try:
        resp = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "scheme": data.get("scheme", "N/A"),
                "type": data.get("type", "N/A"),
                "brand": data.get("brand", "N/A"),
                "prepaid": data.get("prepaid", "N/A"),
                "country": data.get("country", {}).get("name", "N/A"),
                "bank": data.get("bank", {}).get("name", "N/A"),
            }
        else:
            return {"error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def luhn_generate(bin_num):
    prefix = str(bin_num)[:6]
    partial = prefix + "000000000"
    digits = [int(d) for d in partial]
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    check_digit = (10 - (total % 10)) % 10
    return partial + str(check_digit)

def check_vbv(bin_num):
    card_number = luhn_generate(bin_num)
    url = "https://api.stripe.com/v1/tokens"
    auth = (STRIPE_TEST_KEY, "")
    payload = {
        "card[number]": card_number,
        "card[exp_month]": 12,
        "card[exp_year]": 2028,
        "card[cvc]": "123"
    }
    try:
        resp = requests.post(url, data=payload, auth=auth, timeout=10)
        data = resp.json()
        if resp.status_code == 200:
            if "three_d_secure" in str(data) or "authentication_required" in str(data):
                return "❌ VBV (3DS required)"
            else:
                return "✅ NON-VBV (token created)"
        elif resp.status_code == 402:
            if "authentication_required" in str(data).lower():
                return "❌ VBV (3DS challenge)"
            else:
                return "✅ NON-VBV (declined)"
        else:
            error_msg = data.get("error", {}).get("message", "Unknown error")
            return f"⚠️ Error: {error_msg}"
    except Exception as e:
        return f"⚠️ Exception: {e}"

def main():
    print("\n" + "="*50)
    print("   BIN LOOKUP + VBV CHECKER")
    print("="*50)
    print("Enter BIN (first 6 digits) or 'exit' to quit.\n")
    
    while True:
        bin_input = input("BIN: ").strip()
        if bin_input.lower() == 'exit':
            print("Goodbye!")
            break
        if not bin_input.isdigit() or len(bin_input) < 6:
            print("❌ Invalid BIN. Enter at least 6 digits.\n")
            continue
        
        bin_num = bin_input[:6]
        print(f"\n[*] Checking BIN {bin_num}...")
        
        lookup = bin_lookup(bin_num)
        if "error" in lookup:
            print(f"    BIN Lookup failed: {lookup['error']}")
        else:
            print(f"    💳 Card Type: {lookup.get('scheme', 'N/A')} ({lookup.get('type', 'N/A')})")
            print(f"    🏦 Bank: {lookup.get('bank', 'N/A')}")
            print(f"    🌍 Country: {lookup.get('country', 'N/A')}")
            if lookup.get('prepaid') is not None:
                print(f"    💰 Prepaid: {lookup['prepaid']}")
        
        vbv_status = check_vbv(bin_num)
        print(f"    🔐 VBV Status: {vbv_status}\n")
        time.sleep(0.5)

if __name__ == "__main__":
    main()