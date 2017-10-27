import hashlib
import json
from time import time
import requests

from urllib.parse import urlparse

from proof_of_work import proof_of_work, valid_proof


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.nodes = set()
        self.current_transactions = []
        self.proof_of_work = proof_of_work

        # Creates the genesis block
        self.new_block(proof=100, previous_hash=1)

    def valid_chain(self, chain):
        """
        Determine if a given chain is valid

        :param chain: <list> A list of blocks (blockchain)
        :return: <bool> True if valid, False if not
        """
        if not chain:
            return False

        # Need to check each block and its previous block
        check_list = zip(chain[0:-1], chain[1:])
        # Check each block in the chain
        for previous_block, current_block in check_list:
            # If the current block's previous hash does not equal the actual hash of the last block, fail
            if current_block['previous_hash'] != self.hash(previous_block):
                return False

            if not valid_proof(previous_block['proof'], self.hash(previous_block), current_block['proof']):
                return False

        return True

    def resolve_conflicts(self):
        """
        The Consensus Algorithm, it resolves conflicts by replacing our chain
        with the longest one in the network

        :return: <bool> True is our chain was replaced, False if not
        """

        neighbors = self.nodes
        new_chain = None

        # Looks only for chains longer than ours
        max_length = len(self.chain)
        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: <str> Address of a node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block

        :param block: <dict> block
        :return: <str>
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
