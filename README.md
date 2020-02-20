# 小型区块链(python3)

------
## 一、介绍

该项目主要是通过实践的方法来加深学习和理解区块链的相关原理知识，  
其中交易部分的代码参考了bit-cash开源项目的代码，使用配置文件作为区块持久化保存的方式。
覆盖区块链的大部分核心功能：
> * 网络节点通讯
> * 挖矿
> * 钱包
> * 交易和验证
> * 共识机制
> * 链式结构

涉及到如下知识：
> * Merkle树和SPV机制
> * Kademlia算法、P2P技术
> * 区块链共识机制
> * 比特币交易原理
> * 区块链网络设计

## 二、项目组成
1、区块链  
实现了一个具有白皮书中提到的大部分核心功能的简化版区块链，包括了钱包，区块，交易，
签名，共识机制和工作量证明等  
2、p2p网络  
实现了一个进程构成的p2p网络

## 三、使用方法

### **启动节点**

python run.py -p 端口号 &  
例: python run.py -p 5001 &

------

### **模拟交易**
执行：python simulation_test.py  
模拟节点之间的交易行为。

------

### **json api接口调用**
使用flask服务器实现了部分json api，可以直接通过api调用来获取各个节点之间的信息：
（1）获取区块链高度

请求：

http://127.0.0.1:5001/height
```
返回示例
{
    "code": 0, 
    "value": 2
}
```
-----
（2）获取钱包余额

请求：

http://127.0.0.1:5001/balance?address=3Q7KKThJr5qcT7hM189AkVtqYLS8

```
返回示例
{                                            
    "address": "3Q7KKThJr5qcT7hM189AkVtqYLS8", 
    "balance": 24                              
} 
```
-----
（3）获取区块信息

请求：

http://127.0.0.1:5001/block_info?height=1

-----

（4）创建一笔交易
请求：
http://127.0.0.1:5000/transactions/new
```
返回示例
{
    'amount': 1, 
    'sender': u'23DvZ2MzRoGhQk4vSUDcVsvJDEVb', 
    'receiver': u'2dgzLQJgWKhdt3ETnf3tFA9m4ZpK'
}
```
-----
