import hashlib

DIFFICULTY = 4

def proof_of_work(previous_proof, previous_hash):
    """
    Simple PoW algorithm

    - Find a number p' such that hash(p, p') satisfies a valid condition
    where p is the previous proof and p' is the new proof
    :param previous_proof: <int>
    :param previous_hash: <string> the has of the previous block is included
    so that proofs are tied to transaction history. Transaction history cannot
    be simply re-written, block hashes recomputed, and proofs re-used when
    the transaction history is tied to the proof computation through the hash
    of the previous block
    :return: <int>
    """

    proof = 0
    while valid_proof(previous_proof, previous_hash, proof) is False:
        proof += 1

    return proof


def valid_proof(previous_proof, previous_hash, proof):
    """
    Validates the proof
    Does hash(previous_proof, proof) contain 4 leader zeroes?

    :param previous_proof: <int> previous proof
    :param previous_hash: <str> hash of previous block
    :param proof: <int> current_proof
    :return: <bool> True if correct, False if not
    """

    guess = f'{previous_proof}{previous_hash}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:DIFFICULTY] == '0000'
