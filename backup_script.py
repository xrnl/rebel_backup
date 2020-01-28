#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from rebel_management_utilities import get_all_members
from os import path
from cryptography.fernet import Fernet
import sys


def encrypt_data(data, key):
    """
    :param key: The key used to encrypt the data
    :param data: Data that should be encrypted
    :type data: str
    :return:
    """
    f = Fernet(key)
    return f.encrypt(data.encode("utf8")).decode("utf8")


def write_to_file(data):
    """ Write data to file

    :param data:
    :type str
    :return:
    """

    current_date_str = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    file_path = path.join(backup_dir, f'backup_rebels_{current_date_str}.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
        f.close()


def load_api_key():
    load_dotenv()
    key = os.getenv("ACTION_NETWORK_API_KEY")

    if not key:
        raise OSError('ACTION_NETWORK_API_KEY not found in .env')

    return key

def load_data(api_key):
    data = {'members': get_all_members(api_key)}
    return json.dumps(data)


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3 :
        print("Please specify the input parameters")
        exit(1)
    if sys.argv[1].lower() == "true":
        use_encryption = True
        if len(sys.argv) == 3:
            encryption_key = sys.argv[2].encode("utf8")
        else:
            print("Please specify the encryption key")
            exit(1)
    else:
        use_encryption = False

    api_key = load_api_key()
    data = load_data(api_key)

    if use_encryption:
        data = encrypt_data(data, encryption_key)
    write_to_file(data)
