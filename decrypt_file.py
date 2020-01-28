#!/usr/bin/env python3
from cryptography.fernet import Fernet
import sys
from datetime import datetime

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please specify the encryption key and the path to the file")
        exit(1)

    with open(sys.argv[2], 'r', encoding='utf-8') as file:
        data = file.read()
        fernet = Fernet(sys.argv[1].encode("utf8"))
        data = fernet.decrypt(data.encode("utf8"))
        data = data.decode("utf8")

        current_date_str = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        with open(f'backup_rebels_decrypt_{current_date_str}.json', 'w', encoding='utf-8') as output:
            output.write(data)
            output.close()
