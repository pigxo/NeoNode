import binascii
import time

import requests
from decimal import Decimal
from neocore.Fixed8 import Fixed8
from neocore.UInt256 import UInt256

from app.TX.MyTransaction import InvocationTransaction, ContractTransaction, TransactionInput, TransactionOutput
from app.TX.TransactionAttribute import TransactionAttribute, TransactionAttributeUsage
from app.model import Balance, Vout
from app.utils import ToScriptHash
from config import setting
from app.TX.utils import hex_reverse, ToAddresstHash, createTxid, createMultiSigContract, create_opdata, \
    createRSMCContract, str_reverse
from app.TX.adapter import neo_factory,gas_factory,tnc_factory

#RSMC


def createFundingTx(walletSelf, walletOther, asset_id):

    '''

    :param walletSelf: dict {
            "pubkey":"",
            "deposit":0
    }
    :param walletOhter: dict {
            "pubkey":"",
            "deposit":0
    :return:
    '''

    if asset_id not in [setting.NEO_ASSETID, setting.GAS_ASSETID]:
        return tnc_factory.createFundingTx(walletSelf, walletOther, asset_id)

    elif asset_id == setting.NEO_ASSETID:
        return neo_factory.createFundingTx(walletSelf, walletOther, asset_id)

    elif asset_id == setting.GAS_ASSETID:
        return gas_factory.createFundingTx(walletSelf, walletOther, asset_id)


def createCTX(
        addressFunding,
        balanceSelf,
        balanceOther,
        pubkeySelf,
        pubkeyOther,
        fundingScript,
        asset_id,
        fundingTxId):
    if asset_id == setting.NEO_ASSETID:
        return neo_factory.createCTX(
            balanceSelf,
            balanceOther,
            pubkeySelf,
            pubkeyOther,
            fundingScript,
            asset_id,
            fundingTxId)

    elif asset_id == setting.GAS_ASSETID:
        return gas_factory.createCTX(
            balanceSelf,
            balanceOther,
            pubkeySelf,
            pubkeyOther,
            fundingScript,
            asset_id,
            fundingTxId)
    else:
        # default operations tokens like TNC
        return tnc_factory.createCTX(
            addressFunding,
            balanceSelf,
            balanceOther,
            pubkeySelf,
            pubkeyOther,
            fundingScript,
            asset_id)


def createRDTX(
        addressRSMC,
        addressSelf,
        balanceSelf,
        CTxId,
        RSMCScript,
        asset_id):

    if asset_id == setting.NEO_ASSETID:
        return neo_factory.createRDTX(
            addressSelf, balanceSelf, CTxId, RSMCScript, asset_id)

    elif asset_id == setting.GAS_ASSETID:
        return gas_factory.createRDTX(
            addressSelf, balanceSelf, CTxId, RSMCScript, asset_id)
    else:
        return tnc_factory.createRDTX(
            addressRSMC,
            addressSelf,
            balanceSelf,
            CTxId,
            RSMCScript,
            asset_id)


def createBRTX(addressRSMC, addressOther, balanceSelf, RSMCScript, CTxId, asset_id):

    if asset_id == setting.NEO_ASSETID:
        return neo_factory.createBRTX(
            addressOther, balanceSelf, RSMCScript, CTxId, asset_id)

    elif asset_id == setting.GAS_ASSETID:
        return gas_factory.createBRTX(
            addressOther, balanceSelf, RSMCScript, CTxId, asset_id)
    else:
        return tnc_factory.createBRTX(
            addressRSMC,
            addressOther,
            balanceSelf,
            RSMCScript,
            asset_id)


def createRefundTX(
        addressFunding,
        balanceSelf,
        balanceOther,
        pubkeySelf,
        pubkeyOther,
        fundingScript,
        asset_id):

    if asset_id == setting.NEO_ASSETID:
        return neo_factory.createRefundTX(
            addressFunding,
            balanceSelf,
            balanceOther,
            pubkeySelf,
            pubkeyOther,
            fundingScript,
            asset_id)

    elif asset_id == setting.GAS_ASSETID:
        return gas_factory.createRefundTX(
            addressFunding,
            balanceSelf,
            balanceOther,
            pubkeySelf,
            pubkeyOther,
            fundingScript,
            asset_id)
    else:
        return tnc_factory.createRefundTX(
            addressFunding,
            balanceSelf,
            balanceOther,
            pubkeySelf,
            pubkeyOther,
            fundingScript,
            asset_id)


#COMMON
def createTx(addressFrom,addressTo,value,assetId):
    if assetId == setting.CONTRACTHASH:

        time_stamp = TransactionAttribute(usage=TransactionAttributeUsage.Remark,
                                          data=bytearray.fromhex(hex(int(time.time()))[2:]))
        address_hash = TransactionAttribute(usage=TransactionAttributeUsage.Script,
                                             data=ToAddresstHash(addressFrom).Data)

        txAttributes = [address_hash,time_stamp]

        op_data = create_opdata(address_from=addressFrom, address_to=addressTo, value=value,
                                 contract_hash=assetId)
        tx = InvocationTransaction()
        tx.Version = 1
        tx.Attributes = txAttributes
        tx.Script = binascii.unhexlify(op_data)

        return {
            "txData": tx.get_tx_data(),
            "txid": createTxid(tx.get_tx_data()),
            "witness":"014140{signature}2321{pubkey}ac"
        }

    elif assetId == setting.NEO_ASSETID or assetId == setting.GAS_ASSETID:
        if not _check_balance(address=addressFrom,assetId=assetId,value=value):
            return {}



        time_stamp = TransactionAttribute(usage=TransactionAttributeUsage.Remark,
                                          data=bytearray.fromhex(hex(int(time.time()))[2:]))
        address_hash = TransactionAttribute(usage=TransactionAttributeUsage.Script,
                                             data=ToAddresstHash(addressFrom).Data)
        txAttributes = [address_hash,time_stamp]

        inputs,inputs_total=_get_inputs(address=addressFrom,assetId=assetId,value=value)

        outputs = _get_outputs(addressFrom=addressFrom,addressTo=addressTo,value=value,
                               assetId=assetId,inputs_total=inputs_total)

        tx = ContractTransaction()
        tx.inputs = inputs
        tx.outputs = outputs
        tx.Attributes = txAttributes

        return {
            "txData":tx.get_tx_data(),
            "txId": createTxid(tx.get_tx_data()),
            "witness": "014140{signature}2321{pubkey}ac"
        }

    else:

        return {}


def createMultiTx(addressFrom,addressTo,value,assetId):
    if assetId == setting.CONTRACTHASH:

        time_stamp = TransactionAttribute(usage=TransactionAttributeUsage.Remark,
                                          data=bytearray.fromhex(hex(int(time.time()))[2:]))
        address_hash = TransactionAttribute(usage=TransactionAttributeUsage.Script,
                                             data=ToAddresstHash(addressFrom).Data)

        txAttributes = [address_hash,time_stamp]

        op_data = create_opdata(address_from=addressFrom, address_to=addressTo, value=value,
                                 contract_hash=assetId)
        tx = InvocationTransaction()
        tx.Version = 1
        tx.Attributes = txAttributes

        tx.Script = binascii.unhexlify(op_data*3)

        return {
            "txData": tx.get_tx_data(),
            "txId": createTxid(tx.get_tx_data())
        }

    else:
        return {"message":"asset not exist"}


def _check_balance(address,assetId,value):
    balance = Balance.query.filter_by(address=address).first()
    if balance:
        if assetId == setting.GAS_ASSETID or assetId == setting.NEO_ASSETID:
            gas=balance.gas_balance
            if gas < Decimal(str(value)):
                return False
            return True


        elif assetId == setting.NEO_ASSETID:
            neo=balance.neo_balance
            if neo < Decimal(str(value)):
                return False
            return True
        elif assetId == setting.CONTRACTHASH:
            tnc=_get_tnc_balance(address)
            if tnc < value:
                return False
            return True
    return False

def _get_tnc_balance(address):
    data = {
        "jsonrpc": "2.0",
        "method": "invokefunction",
        "params": [
            setting.CONTRACTHASH,
            "balanceOf",
            [
                {
                    "type":"Hash160",
                    "value":ToScriptHash(address).ToString()
                }
            ]
        ],
        "id": 1
    }
    res = requests.post(setting.NEOCLIURL, json=data).json()
    try:
        value=res["result"]["stack"][0]["value"]
    except:
        value=0
    if value:
        value=int(str_reverse(value),16)/100000000
    else:value=0
    return value



def _get_inputs(address,assetId,value):
    inputs_total=0
    inputs=[]
    if assetId == setting.GAS_ASSETID or assetId == setting.NEO_ASSETID:
        vouts = Vout.query.filter_by(address=address,asset_id=assetId).order_by(Vout.value.desc()).all()

        for item in vouts:
            if float(item.value) >= value:
                input =_createInput(preHash=item.tx_id,preIndex=item.vout_number)
                inputs.append(input)
                inputs_total+=float(item.value)
                return inputs,inputs_total
            else:
                input =_createInput(preHash=item.tx_id,preIndex=item.vout_number)
                inputs.append(input)
                inputs_total+=float(item.value)
                if inputs_total>=value:
                    return inputs,inputs_total

    return inputs,inputs_total

def _get_outputs(addressFrom,addressTo,inputs_total,value,assetId):
    outputs=[]
    if inputs_total == value:
        output=_createOutput(assetId=assetId,amount=value,address=addressTo)
        outputs.append(output)
        return outputs
    output0 = _createOutput(assetId=assetId, amount=value, address=addressTo)
    output1 = _createOutput(assetId=assetId, amount=inputs_total-value, address=addressFrom)
    outputs.append(output0)
    outputs.append(output1)
    return outputs

def _createInput(preHash,preIndex):
    pre_hash = UInt256(data=binascii.unhexlify(hex_reverse(preHash)))
    return TransactionInput(prevHash=pre_hash, prevIndex=preIndex)

def _createOutput(assetId,amount,address):
    assetId = UInt256(data=binascii.unhexlify(hex_reverse(assetId)))
    f8amount = Fixed8.TryParse(amount, require_positive=True)
    address_hash=ToAddresstHash(address)
    return TransactionOutput(AssetId=assetId, Value=f8amount, script_hash=address_hash)

