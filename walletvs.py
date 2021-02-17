import subprocess
import json
import os 
from constants import *
from web3 import Account, middleware, Web3 
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


mnemonic = os.getenv('MNEMONIC', 'oblige monkey actual pudding ramp affair unveil nut belt input dust happy')


def derive_wallets(coin,mnemonic=mnemonic,numderive=3): 
    command = f'./derive -g --mnemonic="{mnemonic}" --coin={coin} --numderive={numderive} --format=jsonpretty'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    print(output)

    return json.loads(output)
def priv_key_to_account(privkey,coin):
    if coin==ETH:
        return Account.privateKeyToAccount(privkey)
    if coin==BTCTEST:
        return PrivateKeyTestnet(privkey)
def create_tx(coin,account,amount,to):
    if coin==ETH:
        value= w3.toWei(amount, "ether"),
        gasEstimate=w3.eth.estimateGas({ "to": to, "from": account.address, "amount": value })
        return {
            "from": account.address,
            "to": to,
            "value": value,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainId":w3.net.chainId
        }
    if coin==BTC:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
def send_tx(coin, account, amount, to):
    if coin==ETH:
        raw_tx=create_tx(coin, account, amount, to)
        signed_tx=account.signTransaction(raw_tx)
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    if coin==BTCTEST:
        raw_tx=create_tx(coin, account, amount, to)
        signed_tx=account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed_tx)
coins = {
    ETH: derive_wallets(coin=ETH),
    BTCTEST: derive_wallets(coin=BTCTEST)
}

print(coins)




