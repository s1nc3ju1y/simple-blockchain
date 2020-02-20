# coding:utf-8
import hashlib
from binascii import unhexlify

import rsa

from wallet import Wallet

OP_DUP = 0x76  # 118, 复制栈顶元素
OP_HASH160 = 0xa9  # 169,sha256(ripemd160(栈顶元素))
OP_CHECKSIG = 0xac  # 172, Input：sig+pubkey  Output：True/False  校验签名
OP_EQUALVERIFY = 0x88  # 136 校验是否相等


class Script:
    """
    脚本流程
    栈顶元素复制->加密->校验签名
    """

    @staticmethod
    def sign(privkey, data):
        """
        使用钱包私钥进行签名
        """
        return rsa.sign(data.encode(), privkey, 'SHA-256')

    @staticmethod
    def verify(data, signature, pubkey):
        """
        验证签名
        :param data:
        :param signature:
        :param pubkey:
        :return:
        """
        if data is None or signature is None or pubkey is None:
            return False
        try:
            rsa.verify(data.encode(), signature, pubkey)
        except rsa.pkcs1.VerificationError:
            return False
        return True

    # @staticmethod
    # def encode_scriptPubKey(script_pubkey):
    #     """
    #     将scriptPubKey指令数组转换成指令字符串
    #     :param script_pubkey:
    #     :return:
    #     """
    #     scriptPubKey_str = ""
    #     for i in range(len(script_pubkey)):
    #         element = script_pubkey[i]
    #         if element == OP_DUP \
    #                 or element == OP_EQUALVERIFY \
    #                 or element == OP_CHECKSIG:
    #             scriptPubKey_str += hex(element)[2:]
    #         elif element == OP_HASH160:
    #             scriptPubKey_str = scriptPubKey_str + hex(element)[2:] + hex(len(script_pubkey[i + 1]))[2:]
    #         else:
    #             scriptPubKey_str += element
    #
    #     return scriptPubKey_str
    #
    # @staticmethod
    # def decode_scriptPubKey(scriptPubKey_str):
    #     idx = 0
    #     script_pubkey = list()
    #     while idx < len(scriptPubKey_str):
    #         opcode = scriptPubKey_str[idx:idx + 2]
    #         opcode = int('0x' + opcode, 16)
    #         script_pubkey.append(opcode)
    #         if opcode == OP_DUP or opcode == OP_EQUALVERIFY or opcode == OP_CHECKSIG:
    #             idx += 2
    #         elif opcode == OP_HASH160:
    #             idx += 2
    #             count = int('0x' + scriptPubKey_str[idx:idx + 2], 16)
    #             idx += 2
    #             sha160_str = scriptPubKey_str[idx:idx + count]
    #             script_pubkey.append(sha160_str)
    #             idx += count
    #     return script_pubkey

    @staticmethod
    def sha160(data):
        """
        先sha256，再ripemd160
        :param data:
        :return:
        """
        sha = hashlib.sha256(data.encode('utf-8'))
        hash_256_value = sha.hexdigest()
        obj = hashlib.new('ripemd160', hash_256_value.encode('utf-8'))
        ripemd_160_value = obj.hexdigest()
        return ripemd_160_value

    @staticmethod
    def check_tx_script(data, script_sig, script_pubkey):
        """
        检查交易脚本是否有效
        :param data: 原数据
        :param script_sig: <list> 队列，解锁脚本：<signature> <pubkey>
        :param script_pubkey: <list>队列，锁定脚本
        :return:
        """
        stack = Stack()
        for element in script_sig:
            stack.push(element)
        # stack.output()

        for element in script_pubkey:
            if element == OP_DUP:
                top = stack.peek()
                stack.push(top)
            elif element == OP_HASH160:
                top = str(stack.pop())
                stack.push(Script.sha160(top))
            elif element == OP_EQUALVERIFY:
                top_1 = stack.pop()
                top_2 = stack.pop()
                if top_1 != top_2:
                    return False
            elif element == OP_CHECKSIG:
                pubkey = stack.pop()
                signature = stack.pop()
                result = Script.verify(data, signature, pubkey)
                stack.push(result)
            else:
                stack.push(element)
                # stack.output()

        if stack.size() == 1 and stack.peek() is True:
            return True
        else:
            return False


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def get_address_from_ripemd160(ripemd_hash):
    Wallet.b58encode(unhexlify(ripemd_hash.decode('utf-8')))
    return Wallet.b58encode(unhexlify(ripemd_hash.decode('utf-8')))
