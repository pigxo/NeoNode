
import os

ENVIRON=os.environ

NEO_RPC_POOL=[
    "https://seed2.switcheo.network:10331",
    "https://seed4.switcheo.network:10331",
    "https://seed3.switcheo.network:10331",
    "https://seed5.switcheo.network:10331",
    "http://node1.nyc3.bridgeprotocol.io:10332",
    "http://node1.sgp1.bridgeprotocol.io:10332",
    "http://node1.ams2.bridgeprotocol.io:10332",
    "http://seed1.aphelion-neo.com:10332",
    "http://seed4.aphelion-neo.com:10332",
    "http://seed3.aphelion-neo.com:10332",
    "http://seed8.bridgeprotocol.io:10332",
    "http://seed9.bridgeprotocol.io:10332",
    "http://seed7.bridgeprotocol.io:10332",
    "http://seed6.bridgeprotocol.io:10332",
    "http://seed5.bridgeprotocol.io:10332",
    "http://seed4.bridgeprotocol.io:10332",
    "http://seed3.bridgeprotocol.io:10332",
    "http://seed2.bridgeprotocol.io:10332",
    "http://seed1.bridgeprotocol.io:10332",
    "http://seed0.bridgeprotocol.io:10332",
    "http://api.otcgo.cn:10332",
    "http://seed3.neo.org:10332",
    "https://seed1.neo.org:10331",
    "http://seed10.ngd.network:10332",
    "http://seed9.ngd.network:10332",
    "http://seed8.ngd.network:10332",
    "http://seed7.ngd.network:10332",
    "http://seed6.ngd.network:10332",
    "http://seed3.ngd.network:10332",
    "http://seed2.ngd.network:10332",
    "http://seed1.ngd.network:10332",
    "https://seed8.cityofzion.io",
    "https://seed7.cityofzion.io",
    "https://seed6.cityofzion.io",
    "https://seed0.cityofzion.io"
]

NEO_RPC_APPLICATION_LOG_POOL=[
    "http://seed10.ngd.network:10332",
    "http://seed9.ngd.network:10332",
    "http://seed8.ngd.network:10332",
    "http://seed7.ngd.network:10332",
    "http://seed6.ngd.network:10332",
    # "http://127.0.0.1:10332"
]


class SettingHolder(object):

    NEO_ASSETID = "0xc56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b"
    GAS_ASSETID = "0x602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7"

    MYSQLDATABASE = {
        "host": "127.0.0.1",
        "user": ENVIRON.get("DATABASE_USERNAME"),
        "passwd": ENVIRON.get("DATABASE_PASSWORD"),
        "db_block_info": ENVIRON.get("DATABASE_DB_BLOCK_INFO"),
        "db_account_info": ENVIRON.get("DATABASE_DB_ACCOUNT_INFO"),
    }

    def setup_mainnet(self):
        self.CONTRACTHASH="0x08e8c4400f1af2c20c28e0018f29535eb85d15b6"
        self.NEOCLIURL = NEO_RPC_POOL
        self.NEO_RPC_APPLICATION_LOG = NEO_RPC_APPLICATION_LOG_POOL
        self.PRIVTKEY=ENVIRON.get("PRIVTKEY")
        self.PASSWD_HASH="$2b$10$F7GVmj.eahbHMIUjOxooYuLBMqZaIGcJZ7KxufGfbxwGTErKCzNQm"
        self.REMOTE_ADDR=ENVIRON.get("REMOTE_ADDR")
        self.FUNDING_ADDRESS=ENVIRON.get("FUNDING_ADDRESS")
        self.WEBAPI=ENVIRON.get("WEB_API")

        self.REDIS_IP="47.97.96.192"
        self.REDIS_PORT=6379

    def setup_testnet(self):
        self.CONTRACTHASH = "0x849d095d07950b9e56d0c895ec48ec5100cfdff1"
        self.NEOCLIURL = ["http://127.0.0.1:20332"]
        self.NEO_RPC_APPLICATION_LOG = ["http://127.0.0.1:20332"]
        self.PRIVTKEY=ENVIRON.get("PRIVTKEY")
        self.PASSWD_HASH=ENVIRON.get("PASSWORD_HASH")
        self.REMOTE_ADDR=ENVIRON.get("REMOTE_ADDR")
        self.FUNDING_ADDRESS=""
        self.WEBAPI=ENVIRON.get("WEB_API")
        self.REDIS_IP="47.104.81.20"
        self.REDIS_PORT=9001
    def setup_privtnet(self):
        self.CONTRACTHASH = "0x0c34a8fd0109df360c7cf7ca454404901db77f5e"
        self.NEOCLIURL = "http://localhost:10332"
        self.REDIS_IP="localhost"
        self.REDIS_PORT=6379

setting=SettingHolder()

if ENVIRON.get("CURRENT_ENVIRON") == "testnet":
    setting.setup_testnet()
elif ENVIRON.get("CURRENT_ENVIRON") == "mainnet":
    setting.setup_mainnet()
else:
    setting.setup_testnet()
