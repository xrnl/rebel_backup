#!/usr/bin/env python3
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import sys
from datetime import datetime
import zipfile
from cryptography.fernet import Fernet

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Please specify the path to the encryption key file and the path to the data zip file")
        exit(1)

    private_key = ""
    with open(sys.argv[1], "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=None,
            backend=default_backend()
        )

    # Open the zip archive
    archive = zipfile.ZipFile(sys.argv[2], 'r')
    try:
        archive_content_name_list = archive.namelist()
        symmetric_key_file = ''
        data_file_encrypted = ''
        for name in archive_content_name_list:
            if name.endswith('key'):
                symmetric_key_file = name
            elif name.endswith('enc'):
                data_file_encrypted = name

        # Read and decrypt the symmetric key
        symmetric_key_encrypted = archive.read(symmetric_key_file)

        symmetric_key = private_key.decrypt(
            symmetric_key_encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        data_encrypted = archive.read(data_file_encrypted)
        fernet = Fernet(symmetric_key)
        data = fernet.decrypt(data_encrypted)
        data = data.decode("utf8")

        current_date_str = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        with open(f'backup_rebels_decrypt_{current_date_str}.json', 'w', encoding='utf-8') as output:
            output.write(data)

    finally:
        archive.close()


