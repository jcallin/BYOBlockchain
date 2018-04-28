import argparse
from flask import Flask, jsonify, request
from uuid import uuid4
from blockchain import Blockchain

parser = argparse.ArgumentParser()
parser.add_argument('port')
args = parser.parse_args()

PORT = args.port

app = Flask(__name__)

# Generate a globally unique address for node
NODE_ID = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    BLOCK_REWARD = 1
    # Run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    last_block_hash = blockchain.hash(last_block)
    new_proof = blockchain.proof_of_work(last_proof, last_block_hash)

    # Receive a reward for finding the proof
    # Sender is '0' to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender=NODE_ID,
        recipient=NODE_ID,
        amount=BLOCK_REWARD
    )

    # Forge the new block by adding it to the chain
    block = blockchain.new_block(new_proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Create a new transaction
    try:
        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    # Check that the required fields are in the POST'd data
    except IndexError:
        return 'Request for transaction is missing values', 400

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }

    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }

    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(PORT))
