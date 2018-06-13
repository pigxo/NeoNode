#!/usr/bin/env python
# encoding: utf-8
"""
@author: Maiganne

"""


from app import db



#
# class NeoVout(db.Model):
#     __tablename__ = 'neo_vout'
#     id = db.db.Column(db.Integer, primary_key=True)
#     tx_id = db.db.Column(db.String(256))
#     address = db.db.Column(db.String(256))
#     asset_id = db.db.Column(db.String(256))
#     vout_number = db.db.Column(db.Integer)
#     value = db.db.Column(db.Integer,default=0)
#
#
#     def to_json(self):
#         return {
#                 'tx_id': self.tx_id,
#                 'address': self.address,
#                 'asset_id': self.asset_id,
#                 'vout_number': self.vout_number,
#                 'value' : float(self.value)
#                 }
#     @staticmethod
#     def save(tx_id,address,asset_id,vout_number,value):
#         new_instance = NeoVout(tx_id=tx_id, address=address, asset_id=asset_id, vout_number=vout_number,value=value)
#         db.session.add(new_instance)
#         db.session.commit()
#     @staticmethod
#     def delete(instanse):
#         db.session.delete(instanse)
#         db.session.commit()
#
#
# class GasVout(db.Model):
#     __tablename__ = 'gas_vout'
#     id = db.db.Column(db.Integer, primary_key=True)
#     tx_id = db.db.Column(db.String(256))
#     address = db.db.Column(db.String(256))
#     asset_id = db.db.Column(db.String(256))
#     vout_number = db.db.Column(db.Integer)
#     value = db.db.Column(db.Numeric(16,8),default=0)
#
#
#     def to_json(self):
#         return {
#                 'tx_id': self.tx_id,
#                 'address': self.address,
#                 'asset_id': self.asset_id,
#                 'vout_number': self.vout_number,
#                 'value' : float(self.value)
#                 }
#
#     @staticmethod
#     def save(tx_id,address,asset_id,vout_number,value):
#         new_instance = GasVout(tx_id=tx_id, address=address, asset_id=asset_id, vout_number=vout_number,value=value)
#         db.session.add(new_instance)
#         db.session.commit()
#     @staticmethod
#     def delete(instanse):
#         db.session.delete(instanse)
#         db.session.commit()





class Balance(db.Model):
    __tablename__ = 'balance'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(40),index=True)
    neo_balance = db.Column(db.DECIMAL(17,8),default=0)
    gas_balance =db.Column(db.DECIMAL(17,8),default=0)






class Vout(db.Model):
    __tablename__ = 'vout'
    id = db.Column(db.Integer, primary_key=True)
    tx_id = db.Column(db.String(66),index=True)
    address = db.Column(db.String(40))
    asset_id = db.Column(db.String(66))
    vout_number = db.Column(db.SmallInteger)
    value = db.Column(db.DECIMAL(17,8))








class InvokeTx(db.Model):
    __tablename__ = 'invoke_tx'
    id = db.Column(db.Integer, primary_key=True)
    tx_id = db.Column(db.String(66))
    contract = db.Column(db.String(42))
    address_from = db.Column(db.String(40),index=True)
    address_to = db.Column(db.String(40),index=True)
    value = db.Column(db.DECIMAL(17,8))
    vm_state = db.Column(db.String(16))
    has_pushed=db.Column(db.Boolean,default=False)
    block_timestamp=db.Column(db.Integer)
    block_height=db.Column(db.Integer)




    def to_json(self):
        return {
            "txId":self.tx_id,
            "asset":self.contract,
            "addressFrom":self.address_from,
            "addressTo":self.address_to,
            "value":float(self.value),
            "vmState":self.vm_state,
            "blockTime":self.block_timestamp,
            "blockHeight":self.block_height
        }


class ContractTx(db.Model):
    __tablename__ = 'contract_tx'
    id = db.Column(db.Integer, primary_key=True)
    tx_id = db.Column(db.String(66))
    asset = db.Column(db.String(66))
    address_from = db.Column(db.String(40),index=True)
    address_to = db.Column(db.String(40),index=True)
    value = db.Column(db.DECIMAL(17,8))
    block_timestamp=db.Column(db.Integer)
    block_height=db.Column(db.Integer)

    def to_json(self):
        return {
            "txId":self.tx_id,
            "asset":self.asset,
            "addressFrom":self.address_from,
            "addressTo":self.address_to,
            "value":float(self.value),
            "blockTime":self.block_timestamp,
            "blockHeight":self.block_height
        }