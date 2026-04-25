# 🔥 WordForge — Advanced Wordlist Generator for Kali Linux

```
██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
██║ █╗ ██║██║   ██║██████╔╝██║  ██║█████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
██║███╗██║██║   ██║██╔══██╗██║  ██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
```

> **Advanced Wordlist Generator** for Penetration Testing — Built for Kali Linux

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Keyword Mode** | Generate from names, targets, topics |
| **Brute-Force Mode** | All combinations of a custom charset |
| **OSINT Mode** | Name + DOB + company + phone + city + pet |
| **Mutate Mode** | Supercharge any existing wordlist (rockyou, etc.) |
| **Pattern Mode** | Custom pattern-based generation |
| **Leet Speak** | Auto leet substitutions (a→@, e→3, o→0...) |
| **Year Injection** | Append/prepend years 1980–2025+ |
| **Hash Output** | MD5, SHA1, SHA256, SHA512, NTLM hash files |
| **Length Filter** | `--min-len` / `--max-len` filtering |
| **Random Order** | Shuffle output for stealth |

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/raj/WordForge.git
cd WordForge

# No external dependencies — pure Python 3
python3 wordforge.py --help
```

### Optional: Add to PATH (use from anywhere in Kali)

```bash
chmod +x wordforge.py
sudo cp wordforge.py /usr/local/bin/wordforge
wordforge --help
```

---

## 🛠️ Usage

### Mode 1 — Keyword Mode
Generate powerful wordlist from keywords:

```bash
python3 wordforge.py -m keyword \
  --keywords raj hacker admin secret \
  --leet --years \
  -o output.txt
```

### Mode 2 — OSINT Mode
Target-specific wordlist using personal info:

```bash
python3 wordforge.py -m osint \
  --name raj \
  --dob 19960101 \
  --city delhi \
  --company infosec \
  --pet rocky \
  --leet \
  -o target_raj.txt
```

### Mode 3 — Brute-Force Mode
Generate every combination:

```bash
# lowercase + digits, 6-8 chars
python3 wordforge.py -m brute \
  --lower --digits \
  --min-len 6 --max-len 8 \
  -o brute6-8.txt

# Custom charset
python3 wordforge.py -m brute \
  --charset "abc123!@#" \
  --min-len 4 --max-len 6 \
  -o custom_brute.txt
```

### Mode 4 — Mutate Existing Wordlist
Supercharge rockyou or any other wordlist:

```bash
python3 wordforge.py -m mutate \
  --wordlist /usr/share/wordlists/rockyou.txt \
  --leet \
  --min-len 6 --max-len 20 \
  -o rockyou_mutated.txt
```

### Mode 5 — Pattern Mode
Pattern chars: `@`=lowercase, `,`=uppercase, `%`=digit, `^`=special, `*`=any

```bash
# Pattern: 4 letters + 2 digits
python3 wordforge.py -m pattern \
  --pattern "@@@@%%" \
  -o pattern.txt

# Pattern: Capital + lowercase x3 + 2 digits + special
python3 wordforge.py -m pattern \
  --pattern ",@@@%%^" \
  -o strong_pattern.txt
```

### Hash Output
```bash
python3 wordforge.py -m keyword \
  --keywords admin password \
  --hash-type md5 \
  -o admin.txt
# Creates: admin.txt + admin_md5.txt (word:hash format)
```

---

## 🔢 Pattern Reference

| Char | Charset |
|------|---------|
| `@`  | a-z (lowercase) |
| `,`  | A-Z (uppercase) |
| `%`  | 0-9 (digits) |
| `^`  | Special chars (!@#$%^&*-_.) |
| `*`  | All printable |
| Anything else | Literal character |

---

## 💡 Combine with Other Tools

```bash
# Use with Hydra
hydra -l admin -P output.txt ssh://192.168.1.1

# Use with Hashcat
hashcat -m 0 hash.txt output.txt

# Use with John the Ripper
john --wordlist=output.txt hash.txt

# Use with Medusa
medusa -u admin -P output.txt -h 192.168.1.1 -M ssh
```

---

## ⚙️ All Options

```
usage: wordforge -m MODE [options]

Modes:
  keyword   Generate from keywords
  brute     Brute-force charset combinations
  osint     OSINT-based personal info wordlist
  mutate    Mutate an existing wordlist
  pattern   Pattern-based generation

Global Options:
  -o OUTPUT         Output file
  --leet            Add leet speak variants
  --years           Append/prepend years
  --min-len N       Minimum word length
  --max-len N       Maximum word length
  --limit N         Max number of words to output
  --random-order    Shuffle output
  --hash-type ALGO  Generate hash file (md5, sha1, sha256, sha512)
```

---

## ⚠️ Disclaimer

> WordForge is developed for **ethical hacking and penetration testing only**.  
> Use only on systems you have **explicit written permission** to test.  
> The author is not responsible for any misuse.

---

## 📄 License

MIT License — See [LICENSE](LICENSE)

---

## ✨ Author

**Raj** — Ethical Hacker  
GitHub: [@raj](https://github.com/raj)
