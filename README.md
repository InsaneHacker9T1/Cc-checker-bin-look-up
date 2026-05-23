# 🔍 BIN Lookup + VBV Checker (Termux)

Check any credit/debit card BIN (first 6 digits) to get:
- 💳 Card type (Visa, Mastercard, etc.)
- 🏦 Issuing bank name
- 🌍 Country of origin
- 🔐 VBV (3D Secure) status – Non-VBV or VBV

No code editing required. First run will ask for your Stripe test key and save it locally.

---

## 📦 Installation (Termux)

```bash
pkg update && pkg upgrade
pkg install python git -y
pip install requests
git clone https://github.com/InsaneHacker9T1/Cc-checker-bin-look-up.git
cd Cc-checker-bin-look-up
