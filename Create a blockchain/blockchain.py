# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 17:23:55 2022

@author: FIRDOUSE
"""

# Module 1 - Create Blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Building blockchain
# Sha256 always only accept string format
class Blockchain:
    def __init__(self):
        self.chain = []  # Should be null
        self.create_block(proof = 1, previous_hash = '0',data = 'Transactions for block 1 is added') # First block is genesis block
        
    # To create block 
        
    def create_block(self,proof, data, previous_hash):
        block = {'index' : len(self.chain) + 1,
                 # To have the time at which it is created                 
                 'timestamp' : str(datetime.datetime.now()), 
                 'proof' : proof,
                 'data' : data,
                 'previous_hash' : previous_hash                 
                 }
        self.chain.append(block)
        return block
    
    # Collecting values to add in a block
    # To get data
    
    def get_data(self,chain):
        n = len(chain)
        data = 'Transactions for block '+str(n+1)+' is added'
        return data
    
    # To get Previous block    
    
    def get_previous_block(self):
        return self.chain[-1]
    
    # To add proof of work (piece of data the miner have to find to mine a new block)
    # We have create a challenging problem and it should be easy to verify.
    
    # Previous proof is needed to solve the problem
    
    def proof_of_work(self, previous_proof):
        # We are solving this problem using trial and error approach whenever it
        # fails we increment new_proof value by 1 so initially we assign it to 1.
        new_proof = 1  
        # To check new_proof value is correct or not
        check_proof = False
        # 2 condition
        
        while check_proof is False:
            # ***1: To have 64 char hash***
            hash_operation = hashlib.sha256(str(new_proof**3 - previous_proof**2).encode()).hexdigest()
            # Should be non symmetrical (new_proof**2 - previous_proof**2 viseversa is not same)
            # Hexdigest is to have hexadecimal value            
            
            # ***2: 4 leading zeros (More leading zeros make more harder to solve)***
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
                
        return new_proof
    
    # Creating Hash function
    
    def hash(self, block):
        # Change block format(dictionary format to string format using json dumps)
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Check blockchain is valid or not
     
    def is_chain_valid(self, chain): # We are checking chains
    # Previous hash of each block is equal to the hash of its previous block
        previous_block = chain[0] # First block in the chain then we will increment it by 1 till the current block we are working with
        block_index = 1 # Creating looping variable length of previous_block
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block) : # self hash bcoz it is a func of blockchain
                return False      
    # Proof of each block is valid                   
            previous_proof = previous_block['proof'] # Proof of prev block
            proof = block['proof'] # Gives proof of the current block
            hash_operation = hashlib.sha256(str(proof**3 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1    
        return True
            
# Mining our Blockchain

# Creating a web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
            
# Creating a blockchain 
blockchain = Blockchain()           

# Mining new block refer https://flask.palletsprojects.com/en/1.1.x/quickstart/#http-methods

@app.route('/mine_block', methods = ['GET'])            
def mine_block():
    # Parameters needed to create a block
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    chain = blockchain.chain
    proof = blockchain.proof_of_work(previous_proof)
    # To call create block
    previous_hash = blockchain.hash(previous_block)
    data = blockchain.get_data(chain)
    block = blockchain.create_block(proof, data, previous_hash)
    response = {'message': 'Congratulations, You mined a new block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof' : block['proof'],
                'data' : block['data'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200 # 200 refer https://en.wikipedia.org/wiki/List_of_HTTP_status_codes        
            
            
# Getting the full blockchain
            
@app.route('/get_chain', methods = ['GET']) 
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking blockchain is valid or not
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'All good...'}
    else:
        response = {'message' : 'Sorry your block is not valid..'}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)     
            
            