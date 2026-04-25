#!/usr/bin/env python3
"""
██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
██║ █╗ ██║██║   ██║██████╔╝██║  ██║█████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
██║███╗██║██║   ██║██╔══██╗██║  ██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

WordForge - Advanced Wordlist Generator for Kali Linux
Author  : Raj (Ethical Hacker)
GitHub  : https://github.com/raj/WordForge
License : MIT
"""

import argparse
import itertools
import os
import sys
import string
import hashlib
import random
from datetime import datetime

# ─────────────────────────────────────────────
#  COLOR CODES
# ─────────────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

BANNER = f"""
{CYAN}{BOLD}
██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
██║ █╗ ██║██║   ██║██████╔╝██║  ██║█████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
██║███╗██║██║   ██║██╔══██╗██║  ██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{RESET}
{YELLOW}  Advanced Wordlist Generator for Penetration Testing | Kali Linux{RESET}
{GREEN}  Author: Raj | GitHub: https://github.com/raj/WordForge{RESET}
"""

# ─────────────────────────────────────────────
#  COMMON LEET SPEAK SUBSTITUTIONS
# ─────────────────────────────────────────────
LEET_MAP = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7'],
    'b': ['b', '8'],
    'g': ['g', '9'],
    'l': ['l', '1'],
    'z': ['z', '2'],
}

COMMON_SUFFIXES = [
    '123', '1234', '12345', '123456',
    '!', '@', '#', '$', '!!', '@@',
    '1', '2', '01', '69', '99',
    '2020', '2021', '2022', '2023', '2024', '2025',
    '_123', '_1', '786', '007', '000', '111', '777', '888', '999',
]

COMMON_PREFIXES = [
    '123', 'the', 'my', 'super', 'mega', 'Mr', 'Mrs', 'miss',
    '@', '#',
]

SPECIAL_CHARS = ['!', '@', '#', '$', '%', '^', '&', '*', '-', '_', '.', '+']


# ─────────────────────────────────────────────
#  CORE WORDLIST ENGINE
# ─────────────────────────────────────────────

class WordForge:
    def __init__(self, args):
        self.args = args
        self.words = set()
        self.output_file = args.output
        self.count = 0

    def log(self, msg, color=GREEN):
        print(f"{color}[*] {msg}{RESET}")

    def error(self, msg):
        print(f"{RED}[!] {msg}{RESET}")
        sys.exit(1)

    # ── Mode 1: Custom keyword-based ──────────────────────────────────────
    def generate_from_keywords(self):
        keywords = self.args.keywords or []
        if not keywords:
            self.error("--keywords required for -m keyword mode")

        self.log(f"Generating from {len(keywords)} keyword(s): {keywords}")
        base_forms = set()

        for word in keywords:
            w = word.strip()
            base_forms.update([
                w,
                w.lower(),
                w.upper(),
                w.capitalize(),
                w[::-1],              # reverse
                w.title(),
            ])

        # Case variations + suffixes + prefixes
        for base in list(base_forms):
            self.words.add(base)
            # Suffixes
            for suf in COMMON_SUFFIXES:
                self.words.add(base + suf)
                self.words.add(base.lower() + suf)
                self.words.add(base.capitalize() + suf)
            # Prefixes
            for pre in COMMON_PREFIXES:
                self.words.add(pre + base)
                self.words.add(pre + base.capitalize())
            # Special chars at end
            for sc in SPECIAL_CHARS:
                self.words.add(base + sc)
                self.words.add(base + sc + sc)

        # Leet speak
        if self.args.leet:
            leet_words = set()
            for base in list(base_forms):
                leet_words.update(self._leet_variants(base))
            self.words.update(leet_words)
            self.log(f"Leet speak variants added.")

        # Year combinations
        if self.args.years:
            year_words = set()
            current_year = datetime.now().year
            years = [str(y) for y in range(1980, current_year + 2)]
            for base in list(base_forms):
                for yr in years:
                    year_words.add(base + yr)
                    year_words.add(yr + base)
                    year_words.add(base.capitalize() + yr)
            self.words.update(year_words)
            self.log("Year combinations added.")

        # Keyword combinations with each other
        if len(keywords) > 1:
            for combo in itertools.permutations(keywords, 2):
                self.words.add(''.join(combo))
                self.words.add('_'.join(combo))
                self.words.add('.'.join(combo))

    # ── Mode 2: Brute-force charset ───────────────────────────────────────
    def generate_bruteforce(self):
        charset = ''
        if self.args.charset:
            charset = self.args.charset
        else:
            if self.args.lower:  charset += string.ascii_lowercase
            if self.args.upper:  charset += string.ascii_uppercase
            if self.args.digits: charset += string.digits
            if self.args.special: charset += ''.join(SPECIAL_CHARS)
            if not charset:
                charset = string.ascii_lowercase + string.digits

        min_len = self.args.min_len or 4
        max_len = self.args.max_len or 6

        self.log(f"Brute-force: charset='{charset}' len={min_len}-{max_len}")
        self.log(f"Estimated size: {sum(len(charset)**l for l in range(min_len, max_len+1)):,} words")

        for length in range(min_len, max_len + 1):
            for combo in itertools.product(charset, repeat=length):
                self.words.add(''.join(combo))

    # ── Mode 3: OSINT-based (Name + DOB + keyword) ────────────────────────
    def generate_osint(self):
        name    = self.args.name    or ''
        dob     = self.args.dob     or ''       # format: DDMMYYYY or YYYY
        company = self.args.company or ''
        phone   = self.args.phone   or ''
        city    = self.args.city    or ''
        pet     = self.args.pet     or ''

        targets = [x for x in [name, dob, company, phone, city, pet] if x]
        if not targets:
            self.error("Provide at least one OSINT field (--name, --dob, --company, etc.)")

        self.log(f"OSINT mode: {targets}")

        base_forms = set()
        for t in targets:
            base_forms.update([t, t.lower(), t.upper(), t.capitalize()])
            base_forms.add(t[::-1])

        # All combinations of OSINT fields
        for r in range(1, len(targets) + 1):
            for perm in itertools.permutations(targets, r):
                joined = ''.join(perm)
                base_forms.add(joined)
                base_forms.add('_'.join(perm))
                base_forms.add('.'.join(perm))
                base_forms.add('-'.join(perm))

        # Suffixes + prefixes
        for base in list(base_forms):
            self.words.add(base)
            for suf in COMMON_SUFFIXES:
                self.words.add(base + suf)
                self.words.add(base.capitalize() + suf)
            for sc in SPECIAL_CHARS:
                self.words.add(base + sc)

        if self.args.leet:
            for base in list(base_forms):
                self.words.update(self._leet_variants(base))

    # ── Mode 4: Mutate an existing wordlist ───────────────────────────────
    def mutate_wordlist(self):
        if not self.args.wordlist or not os.path.exists(self.args.wordlist):
            self.error("--wordlist <file> required for mutate mode")

        self.log(f"Loading wordlist: {self.args.wordlist}")
        base_words = []
        with open(self.args.wordlist, 'r', errors='ignore') as f:
            base_words = [line.strip() for line in f if line.strip()]

        self.log(f"Loaded {len(base_words):,} words. Mutating...")

        for w in base_words:
            self.words.add(w)
            self.words.add(w.lower())
            self.words.add(w.upper())
            self.words.add(w.capitalize())
            self.words.add(w[::-1])
            for suf in COMMON_SUFFIXES:
                self.words.add(w + suf)
            for sc in SPECIAL_CHARS[:4]:
                self.words.add(w + sc)
            if self.args.leet:
                self.words.update(self._leet_variants(w))

    # ── Mode 5: Pattern-based ─────────────────────────────────────────────
    def generate_pattern(self):
        """
        Pattern chars:
          @ = lowercase letter
          , = uppercase letter
          % = digit
          ^ = special char
          * = any printable
        Example: --pattern "@@%%!!" -> ab12!!
        """
        pattern = self.args.pattern
        if not pattern:
            self.error("--pattern required for pattern mode")

        self.log(f"Pattern: {pattern}")

        charset_map = {
            '@': string.ascii_lowercase,
            ',': string.ascii_uppercase,
            '%': string.digits,
            '^': ''.join(SPECIAL_CHARS),
            '*': string.ascii_letters + string.digits + ''.join(SPECIAL_CHARS),
        }

        pools = []
        for ch in pattern:
            if ch in charset_map:
                pools.append(charset_map[ch])
            else:
                pools.append([ch])  # literal character

        for combo in itertools.product(*pools):
            self.words.add(''.join(combo))

    # ── Leet speak helper ─────────────────────────────────────────────────
    def _leet_variants(self, word):
        variants = ['']
        for ch in word.lower():
            subs = LEET_MAP.get(ch, [ch])
            variants = [v + s for v in variants for s in subs]
        return variants

    # ── Apply global filters ──────────────────────────────────────────────
    def apply_filters(self):
        filtered = set()
        min_l = self.args.min_len or 0
        max_l = self.args.max_len or 99999

        for w in self.words:
            if len(w) < min_l or len(w) > max_l:
                continue
            filtered.add(w)

        self.words = filtered

    # ── Write output ──────────────────────────────────────────────────────
    def write_output(self):
        if not self.output_file:
            self.output_file = "wordforge_output.txt"

        wordlist = sorted(self.words) if not self.args.random_order else list(self.words)
        if self.args.random_order:
            random.shuffle(wordlist)

        # Limit
        if self.args.limit and self.args.limit > 0:
            wordlist = wordlist[:self.args.limit]

        # Hash mode
        if self.args.hash_type:
            self.log(f"Computing {self.args.hash_type} hashes...")
            hash_file = self.output_file.replace('.txt', '') + f'_{self.args.hash_type}.txt'
            with open(hash_file, 'w') as hf:
                for w in wordlist:
                    h = self._hash_word(w, self.args.hash_type)
                    hf.write(f"{w}:{h}\n")
            self.log(f"Hash file saved: {hash_file}", CYAN)

        with open(self.output_file, 'w') as f:
            for w in wordlist:
                f.write(w + '\n')

        size_kb = os.path.getsize(self.output_file) / 1024
        self.log(f"Total words generated : {GREEN}{len(wordlist):,}{RESET}", CYAN)
        self.log(f"Output file           : {GREEN}{self.output_file}{RESET}", CYAN)
        self.log(f"File size             : {GREEN}{size_kb:.1f} KB{RESET}", CYAN)

    def _hash_word(self, word, hash_type):
        h = hashlib.new(hash_type)
        h.update(word.encode())
        return h.hexdigest()

    # ── Main run ──────────────────────────────────────────────────────────
    def run(self):
        mode = self.args.mode

        if   mode == 'keyword':   self.generate_from_keywords()
        elif mode == 'brute':     self.generate_bruteforce()
        elif mode == 'osint':     self.generate_osint()
        elif mode == 'mutate':    self.mutate_wordlist()
        elif mode == 'pattern':   self.generate_pattern()
        else:
            self.error(f"Unknown mode: {mode}. Use keyword | brute | osint | mutate | pattern")

        self.apply_filters()
        self.write_output()


# ─────────────────────────────────────────────
#  CLI ARGUMENT PARSER
# ─────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        prog='wordforge',
        description=f'{BOLD}WordForge{RESET} - Advanced Wordlist Generator',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
{CYAN}Modes:{RESET}
  keyword   Generate from keywords (names, targets, topics)
  brute     Brute-force all combinations of a charset
  osint     OSINT-based: name, DOB, company, phone, city, pet
  mutate    Mutate an existing wordlist with transformations
  pattern   Pattern-based generation (@@%% = letters+digits)

{CYAN}Examples:{RESET}
  {GREEN}# Keyword mode{RESET}
  python3 wordforge.py -m keyword --keywords raj hacker admin --leet --years -o raj.txt

  {GREEN}# OSINT mode{RESET}
  python3 wordforge.py -m osint --name raj --dob 19960101 --city delhi --pet rocky -o osint.txt

  {GREEN}# Brute-force mode{RESET}
  python3 wordforge.py -m brute --lower --digits --min-len 6 --max-len 8 -o brute.txt

  {GREEN}# Mutate an existing wordlist{RESET}
  python3 wordforge.py -m mutate --wordlist /usr/share/wordlists/rockyou.txt --leet -o mutated.txt

  {GREEN}# Pattern mode{RESET}
  python3 wordforge.py -m pattern --pattern "@@@@%%" -o pattern.txt

  {GREEN}# With MD5 hash output{RESET}
  python3 wordforge.py -m keyword --keywords admin --hash-type md5 -o admin.txt
"""
    )

    # Required
    parser.add_argument('-m', '--mode', required=True,
        choices=['keyword', 'brute', 'osint', 'mutate', 'pattern'],
        help='Generation mode')

    # Output
    parser.add_argument('-o', '--output', default='wordforge_output.txt',
        help='Output file (default: wordforge_output.txt)')

    # Keyword mode
    kg = parser.add_argument_group('Keyword Mode')
    kg.add_argument('--keywords', nargs='+', metavar='WORD',
        help='Keywords to generate from')

    # Brute mode
    bg = parser.add_argument_group('Brute-Force Mode')
    bg.add_argument('--charset', metavar='CHARS',
        help='Custom charset string')
    bg.add_argument('--lower',   action='store_true', help='Use lowercase letters')
    bg.add_argument('--upper',   action='store_true', help='Use uppercase letters')
    bg.add_argument('--digits',  action='store_true', help='Use digits')
    bg.add_argument('--special', action='store_true', help='Use special characters')

    # OSINT mode
    og = parser.add_argument_group('OSINT Mode')
    og.add_argument('--name',    help='Target name')
    og.add_argument('--dob',     help='Date of birth (e.g. 19960101)')
    og.add_argument('--company', help='Company name')
    og.add_argument('--phone',   help='Phone number')
    og.add_argument('--city',    help='City')
    og.add_argument('--pet',     help='Pet name')

    # Mutate mode
    mg = parser.add_argument_group('Mutate Mode')
    mg.add_argument('--wordlist', metavar='FILE',
        help='Existing wordlist to mutate')

    # Pattern mode
    pg = parser.add_argument_group('Pattern Mode')
    pg.add_argument('--pattern', metavar='PATTERN',
        help='Pattern: @=lower ,=upper %%=digit ^=special *=any')

    # Global options
    gl = parser.add_argument_group('Global Options')
    gl.add_argument('--leet',         action='store_true', help='Add leet speak variants')
    gl.add_argument('--years',        action='store_true', help='Append/prepend years (keyword/osint)')
    gl.add_argument('--min-len',      type=int, metavar='N', help='Minimum password length')
    gl.add_argument('--max-len',      type=int, metavar='N', help='Maximum password length')
    gl.add_argument('--limit',        type=int, metavar='N', help='Limit number of output words')
    gl.add_argument('--random-order', action='store_true',   help='Randomize output order')
    gl.add_argument('--hash-type',    metavar='ALGO',
        help='Also output hash file (md5, sha1, sha256, sha512, ntlm)')

    return parser.parse_args()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

def main():
    print(BANNER)
    args = parse_args()
    wf = WordForge(args)
    wf.run()


if __name__ == '__main__':
    main()
