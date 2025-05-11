
import hashlib
import os
import json

HASH_ALGO = 'sha256'
HASH_DB = 'hashes.json'

def hash_file(filepath, algo=HASH_ALGO):
    hasher = getattr(hashlib, algo)()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_hashes():
    return json.load(open(HASH_DB)) if os.path.exists(HASH_DB) else {}

def save_hashes(hashes):
    with open(HASH_DB, 'w') as f:
        json.dump(hashes, f, indent=4)

def monitor_folder(folder):
    stored_hashes = load_hashes()
    current_hashes = {}
    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            file_hash = hash_file(path)
            current_hashes[path] = file_hash
            old_hash = stored_hashes.get(path)
            if not old_hash:
                print(f"[NEW] {path}")
            elif old_hash != file_hash:
                print(f"[CHANGED] {path}")
    save_hashes(current_hashes)
    print("Hash log updated.")

if __name__ == "__main__":
    folder_to_monitor = input("Enter folder path to monitor: ")
    monitor_folder(folder_to_monitor)
