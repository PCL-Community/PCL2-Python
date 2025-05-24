# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet

CLIENT_ID = "c14b0370-8d75-42f8-b329-5b60d39e319f"

class ModSecret:
    """进行加密相关处理的模块"""
    def __init__(self):
        self.key = Fernet.generate_key()
        self.fernet_key = Fernet(self.key)

        self.encrypt_client_id = self.fernet_key.encrypt(CLIENT_ID.encode())


    @property
    def client_id(self):
        return self.fernet_key.decrypt(self.encrypt_client_id).decode()