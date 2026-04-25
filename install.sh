#!/bin/bash
# WordForge Installer for Kali Linux

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  __        __            _ _____ "
echo "  \ \      / /__  _ __ __| |  ___|__  _ __ __ _  ___  "
echo "   \ \ /\ / / _ \| '__/ _\` | |_ / _ \| '__/ _\` |/ _ \ "
echo "    \ V  V / (_) | | | (_| |  _| (_) | | | (_| |  __/ "
echo "     \_/\_/ \___/|_|  \__,_|_|  \___/|_|  \__, |\___| "
echo "                                            |___/       "
echo -e "${NC}"
echo -e "${GREEN}[*] Installing WordForge on Kali Linux...${NC}"

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 not found. Install with: sudo apt install python3${NC}"
    exit 1
fi

echo -e "${GREEN}[✓] Python3 found: $(python3 --version)${NC}"

# Copy to /usr/local/bin
sudo cp wordforge.py /usr/local/bin/wordforge
sudo chmod +x /usr/local/bin/wordforge

echo -e "${GREEN}[✓] WordForge installed to /usr/local/bin/wordforge${NC}"
echo -e "${CYAN}[*] Usage: wordforge --help${NC}"
echo ""
echo -e "${GREEN}[*] Quick test:${NC}"
echo "    wordforge -m keyword --keywords test admin --leet -o test.txt"
