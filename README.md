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
./backup_script.py true <encryption_key>
```

To generate an encryption key run the key generation script.
```bash
./generate_key.py
```

To decrypt a file use the decrypt script.
```bash
./decrypt_file.py <encryption_key> <path_to_file>
```