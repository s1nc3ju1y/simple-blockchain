import json
from hashlib import sha256
from time import sleep, time
from urllib.parse import urlparse
from uuid import uuid4
from argparse import ArgumentParser

import flask
from flask import jsonify, request
import requests

"""
区块链逻辑结构
{
    "index": 0,
    "timestamp": "",
    "transactions": [
        {
            "sender": "",
            "recipient": "",
            "amount": 5
        }
    ],
    "proof": "",
    "previous_hash": ""
}
"""

"""
TODO 验证区块链逻辑结构设计，模拟多节点交易
"""


class Blockchain:
    def __init__(self):
        # 链
        self.chain = []
        # 当前块保存的交易
        self.current_transactions = []
        # 创世区块
        self.new_block(proof=0, previous_hash=0x7fffffff)
        # 网络节点
        self.nodes = set()

    def register_node(self, address: str):
        # htto://127.0.0.1:5001
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        pass

    def valid_chain(self, chain) -> bool:
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.last_block)
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount) -> int:
        self.current_transactions.append(
            {
                "sender": sender,
                "recipient": recipient,
                "amount": amount
            }
        )
        return self.last_block['index'] + 1

    def resolve_conflicts(self) -> bool:
        neighbours = self.nodes
        max_length = len(self.chain)
        new_chain = []
        for node in neighbours:
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
        else:
            return False

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True)
        return sha256(block_string.encode('utf-8')).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    def valid_proof(self, last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[0:4] == "0000"


# testPow = Blockchain()
# testPow.proof_of_work(100)
app = flask.Flask(__name__)
app.debug = True
blockchain = Blockchain()
node_identifier = str(uuid4()).replace('-', '')


@app.route('/index', methods=['GET'])
def index():
    return 'Hello blockchain!'


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ["sender", "recipient", "amount"]
    if values is None or not all(k in values for k in required):
        return "Misiing values", 400
    index = blockchain.new_transaction(values['sender'],
                                       values['recipient'],
                                       values['amount'])
    response = {"message": f'Transaction will be added to block {index}'}
    return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)
    block = blockchain.new_block(proof, None)
    response = {
        "message": "New block detected",
        "index": block['index'],
        "transactions": block['transactions'],
        "proof": block['proof'],
        "previous_hash": block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    try:
        values = request.get_json()
        values = request.get_json()
        nodes = values.get("nodes")
        if nodes is None:
            return "Error: invalid list of nodes", 400
        for node in nodes:
            blockchain.register_node(node)
        response = {
            "message": "New nodes have been added",
            "total_nodes": list(blockchain.nodes)
        }
        return jsonify(response), 201
    except Exception:
        return "Error: Bad request", 400


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            "message": "the chain was replaced",
            "new_chain": blockchain.chain
        }
    else:
        response = {
            "message": "Our chain is authoritative",
            "chain": blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    # -p --port 5001
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen to')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
