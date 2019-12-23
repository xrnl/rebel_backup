#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import json
from datetime import date
from rebel_management_utilities import get_all_members
from os import path


def make_backup(api_key):
    data = {'members': get_all_members(api_key)}
    current_date_str = date.now().strftime("%d-%m-%Y_%H:%M:%S")

    file_path = path.join('backups', f'backup_rebels_{current_date_str}.json')

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_api_key():
    load_dotenv()
    key = os.getenv("ACTION_NETWORK_API_KEY")

    if not key:
        raise OSError('ACTION_NETWORK_API_KEY not found in .env')

    return key

if __name__ == '__main__':
    api_key = load_api_key()
    make_backup(api_key)
