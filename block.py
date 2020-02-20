# coding:utf-8

import json

"""
区块逻辑结构
{
# Head
    "index": "区块编号",
    "previous_hash": "上一区块的哈希值",
    "time_stamp": "区块生成的时间戳",
    "nonce": "计算哈希摘要的随机数，实现工作量证明机制",
    "current_hash": "当前区块的哈希值",
    "difficulty": "控制目标哈希值前导零的个数，个数越多，生成出符合要求的哈希值难度越大",
    "Merkle_root": "当前区块所包括的交易产生的默克尔树的根",
# body
    "transactions": "当前区块所打包的交易"
}
"""


class Block:
    def __init__(
            self,
            index,
            previous_hash,
            timestamp,
            nonce,
            current_hash,
            difficulty):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.nonce = nonce
        self.current_hash = current_hash
        self.difficulty = difficulty
        self.merkleroot = None

        # body
        self.transactions = None  # <Transaction>对象数组

    def get_transactions(self):
        return self.transactions

    def json_output(self):
        """
        TODO 区块打包成json对象
        """
        output = {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'current_hash': self.current_hash,
            'difficulty': self.difficulty,
            'merkleroot': self.merkleroot,
            'transactions': [tx.json_output() for tx in self.transactions]
        }
        return output

    def __str__(self):
        return json.dumps(
            self.json_output(),
            default=lambda obj: obj.__dict__,
            sort_keys=True,
            indent=4)
