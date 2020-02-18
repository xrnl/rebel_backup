#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from datetime import datetime
from os import path
import sys
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from rebel_management_utilities import get_all_members
from cryptography.fernet import Fernet
from zipfile import ZipFile


def encrypt_data(data, asymmetric_public_key):
    """ The data is encrypted using a symmetric key that will be encrypted by the assymetric public key.

    :param data: Data that should be encrypted
    :type data: str
    :return: a dict containing the symmetric key encrypted and the data encrypted
    """

    symmetric_key = Fernet.generate_key()
    f = Fernet(symmetric_key)
    encrypted_data = f.encrypt(data.encode("utf8")).decode("utf8")

    encrypted_symmetric_key = asymmetric_public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return {"key": encrypted_symmetric_key, "data": encrypted_data}


def write_to_file_raw(data):
    """ Write string data to file
    """



    file_path = create_backup_path() + "json"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
        f.close()

def create_backup_path():
    """ Creates the directory for the backups

    :return: the timestampt file
    """
    current_date_str = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    return path.join(backup_dir, 'backup_rebels_' + current_date_str + '.')


def write_to_file_encrypted(data):
    """ Write data to file

    :param data: Contains the symmetric key and the data
    :type data: dict
    :return:
    """

    file_path = create_backup_path()
    data_file_path = file_path + "enc"
    key_file_path = file_path + "key"
    zip_file_path = file_path + "zip"

    # Write the data to a file
    with open(data_file_path, 'w', encoding='utf-8') as f:
        f.write(data["data"])
        f.close()

    # Write the symmetric key to a file
    with open(key_file_path, 'wb') as f:
        f.write(bytearray(data["key"]))
        f.close()

    # Zip everything into zip file
    with ZipFile(zip_file_path, "w") as zipObj:
        zipObj.write(data_file_path)
        zipObj.write(key_file_path)
        zipObj.close()

    # Remove single files
    os.remove(data_file_path)
    os.remove(key_file_path)






def load_api_key():
    load_dotenv()
    key = os.getenv("ACTION_NETWORK_API_KEY")

    if not key:
        raise OSError('ACTION_NETWORK_API_KEY not found in .env')

    return key

def load_data(api_key):
    data = {'members': get_all_members(api_key)}
    return json.dumps(data, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3 :
        print("Please specify the input parameters")
        exit(1)
    if sys.argv[1].lower() == "true":
        use_encryption = True
        if len(sys.argv) == 3:
            with open(sys.argv[2], "rb") as public_key_file:
                encryption_key = serialization.load_pem_public_key(
                    public_key_file.read(),
                    backend=default_backend()
                )
        else:
            print("Please specify the path to the file with the encryption key as second argument")
            exit(1)
    else:
        use_encryption = False

    api_key = load_api_key()
    data = load_data(api_key)

    if use_encryption:
        data = encrypt_data(data, encryption_key)
        write_to_file_encrypted(data)
    else:
        write_to_file_raw(data)
