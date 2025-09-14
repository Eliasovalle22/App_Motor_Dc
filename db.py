import pymysql

DB_CONFIG = {
    "host": "sistema-control-123-sistemadecontrol123.i.aivencloud.com",
    "user": "avnadmin",
    "password": "AVNS_jsj8Y-PONkd7ByvybgA",
    "database": "defaultdb",
    "port": 14718,
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "ssl": {"ssl": {}},
    "connect_timeout": 10
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)
