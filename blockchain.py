import hashlib
import json
import time
import os

# Define the file where blockchain data will be stored
BLOCKCHAIN_FILE = 'blockchain_data.json'

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.load_chain() # Attempt to load existing chain on startup

        if not self.chain: # If no chain loaded (first run or empty/corrupted file)
            # Create the genesis block
            self.new_block(proof=100, previous_hash='1', voter_id="system", candidate="genesis")
            self.save_chain() # Save genesis block immediately

    def new_block(self, proof, previous_hash=None, voter_id=None, candidate=None):
        """
        Creates a new Block and adds it to the chain.
        If voter_id and candidate are provided, they are added as a transaction.
        :param proof: The proof given by the Proof of Work algorithm (simplified here).
        :param previous_hash: Hash of previous Block.
        :param voter_id: ID of the voter (for the transaction).
        :param candidate: Candidate voted for (for the transaction).
        :return: New Block
        """
        # Add the current transaction if provided for this block
        if voter_id and candidate:
            self.new_transaction(voter_id, candidate)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else '1',
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, voter_id, candidate):
        """
        Adds a new transaction to the list of transactions to be included in the next block.
        :param voter_id: ID of the voter.
        :param candidate: Candidate voted for.
        :return: The index of the Block that will hold this transaction.
        """
        # Hash voter ID for privacy/anonymity
        voter_hash = hashlib.sha256(voter_id.encode()).hexdigest()
        self.current_transactions.append({
            'voter_hash': voter_hash,
            'candidate': candidate,
            'timestamp': time.time()
        })
        # If there's no last block yet (e.g., before genesis), return 1.
        # Otherwise, return the index of the next block.
        return self.last_block['index'] + 1 if self.chain else 1


    @property
    def last_block(self):
        """Returns the last block in the chain."""
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block.
        We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes.
        :param block: Block
        :return: str
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def is_valid_chain(self):
        """
        Determine if the current blockchain is valid.
        Checks hash linking and (optionally) proof of work.
        :return: True if valid, False if not.
        """
        current_block_index = 0
        while current_block_index < len(self.chain):
            block = self.chain[current_block_index]
            if current_block_index > 0: # Skip genesis block for previous_hash check
                previous_block = self.chain[current_block_index - 1]
                if block['previous_hash'] != self.hash(previous_block):
                    print(f"Chain invalid: Block {block['index']} previous_hash mismatch.")
                    return False

            # You can add proof of work validation here if you implement it:
            # For example: if not self.valid_proof(block['previous_proof'], block['proof']): return False

            current_block_index += 1
        return True

    def get_votes(self):
        """
        Iterates through the blockchain to count votes for each candidate,
        excluding the 'genesis' candidate.
        :return: A dictionary with candidate names as keys and vote counts as values.
        """
        vote_counts = {}
        # Define a list of candidates to exclude from the vote count
        EXCLUDED_CANDIDATES = ["genesis"] # Add any other system-generated candidates here

        for block in self.chain:
            for transaction in block['transactions']:
                candidate = transaction['candidate']
                # Only count votes for candidates that are not in the excluded list
                if candidate not in EXCLUDED_CANDIDATES:
                    vote_counts[candidate] = vote_counts.get(candidate, 0) + 1
        return vote_counts

    def save_chain(self):
        """
        Saves the current blockchain to a JSON file.
        """
        with open(BLOCKCHAIN_FILE, 'w') as f:
            json.dump(self.chain, f, indent=4)
        print(f"Blockchain saved to {BLOCKCHAIN_FILE}.")

    def load_chain(self):
        """
        Loads the blockchain from a JSON file.
        """
        if os.path.exists(BLOCKCHAIN_FILE) and os.path.getsize(BLOCKCHAIN_FILE) > 0:
            try:
                with open(BLOCKCHAIN_FILE, 'r') as f:
                    self.chain = json.load(f)
                print(f"Blockchain loaded from {BLOCKCHAIN_FILE}.")
            except json.JSONDecodeError:
                print(f"Warning: {BLOCKCHAIN_FILE} is empty or malformed. Starting with a new blockchain.")
                self.chain = [] # Reset if file is corrupted
        else:
            print(f"No existing {BLOCKCHAIN_FILE} found. Starting with a new blockchain.")
            self.chain = [] # Initialize empty if file doesn't exist