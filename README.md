# Rebel backup

Script to backup data of Extinction Rebellion NL members.

## Pre-requisites

Python 3

## Installation

Clone or download repository onto local computer.

```bash
git clone https://github.com/xrnl/rebel_backup.git
```


Install necessary dependencies.

```bash
cd rebel_backup
pip install -r requirements.txt
```

store API key in `.env` file.

```bash
ACTION_NETWORK_API_KEY=<your api key>
```

## Usage

The script has two parameters `use encryption` and the `encryption key` as  positional arguments.
```bash
# Run the backup script and save the data in clear text
./backup_script.py false 
# Run the backup script and encrypt the data
./backup_script.py true <public_key_file>
```

To generate the encryption keys run the key generation script.
The public key is used to encrypt the data.
The private key is used to decrypt the data.
The public key can be shared but the private key must not be disclosed!
```bash
./generate_key.py
```

To decrypt a file use the decrypt script.
```bash
./decrypt_file.py <private_key_file_path> <backup_archive_path>
```

# Managing the keys
The public key can be stored on the server as a file. It is can only be used to encrypt the file.
The private key should be stored in a **password manager** or a **vault**.

A popular password manager is KeePass, it is available for all operating systems: https://keepass.info/

Alternatively a vault like https://github.com/share-secrets-safely/cli can be used. 
The vault has the added benefit that it allows to share secrets safely.
