"""Finds the derivation path that generates the target address from the given seed phrase.

Iterates through the provided derivation paths, accounts, and addresses to generate addresses from the seed phrase. 
Checks each generated address against the target address. Returns the first derivation path that generates the target address.
"""

from bip44 import Wallet
from eth_account import Account
import eth_utils
from bip44.utils import get_eth_addr
from coincurve import PrivateKey

"""Generates Ethereum addresses from a seed phrase using common derivation paths.

Scans through a range of accounts and addresses per path to find the path 
that generates the target address from the given seed phrase.

Returns:
    str: The derivation path that generates the target address from the seed.
"""
def generate_addresses_from_seed(seed, derivation_paths, account_limit=10, address_limit=100):
    addresses = {}
    wallet = Wallet(seed)
    for path in derivation_paths:
        for account_id in range(account_limit):
            for address_index in range(address_limit):
                if "'/0/" in path:
                    # For paths ending with '/0/b'
                    derived_path = path.format(a=account_id, b=address_index)
                elif "'/" in path and "/0" not in path:
                    # For paths ending with '/a/b'
                    derived_path = path.format(a=account_id, b=address_index)
                else:
                    # For paths ending with '/a'
                    derived_path = path.format(a=account_id)
                    address_index = 0  # Reset address index for paths without it
                sk, pk = wallet.derive_account("eth", account_id, 0, address_index)
                print(f"Checking {derived_path}")
                sk = PrivateKey(sk)
                address = get_eth_addr(pk)
                addresses[address] = derived_path
    return addresses

def find_matching_address(seed, target_address, derivation_paths):
    addresses = generate_addresses_from_seed(seed, derivation_paths, num_accounts, num_addresses)
    for address, path in addresses.items():
        if eth_utils.to_checksum_address(address) == eth_utils.to_checksum_address(target_address):
            return path
    return None

# Seed phrase input
seed_phrase = input("Enter your wallet seed phrase. Do this OFFLINE on a safe/secure computer: ")
seed_phrase = seed_phrase.strip()

# Target address input
target_address = input("What address are you trying to find? ")
target_address = target_address.strip()

num_accounts = input("How many accounts do you want to scan per-seed? (Default: 10) ") or "10"
num_accounts = int(num_accounts)

num_addresses = input("How many addresses do you want to scan per-account? (Default: 100) ") or "100"
num_addresses = int(num_addresses)

# Common derivation paths to check
derivation_paths = [
    "m/44'/60'/{a}'/0/{b}",
    "m/44'/60'/{a}'/{b}",
    "m/44'/60'/{a}'"
]

matching_path = find_matching_address(seed_phrase, target_address, derivation_paths)

if matching_path:
    print(f"Match found at derivation path: {matching_path}")
else:
    print("No match found.")
