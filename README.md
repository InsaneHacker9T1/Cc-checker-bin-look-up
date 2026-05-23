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
## 💻 How to Run on Windows (PC)

### 🔧 Prerequisites

1. **Install Python** – Download from [python.org](https://www.python.org/downloads/).  
   **Important:** During installation, check ✅ **"Add Python to PATH"**.

2. **Install Git** (optional, for cloning) – Download from [git-scm.com](https://git-scm.com/downloads/win).  
   *If you don't want Git, you can download the ZIP file from GitHub and extract it.*

---

### 🚀 Steps to Run (Command Prompt or PowerShell)

1. **Clone the repository** (or download ZIP and extract):
   ```bash
   git clone https://github.com/InsaneHacker9T1/Cc-checker-bin-look-up.git
   cd Cc-checker-bin-look-up
