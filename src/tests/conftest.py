import pytest
import MySQLdb
from config import config


@pytest.fixture(scope="function")
def cur(request):
    def fin():
        if db_cur:
            db_cur.close()
            conn.close()

    request.addfinalizer(fin)
    host = config.get_config('database', 'db_host')
    user = config.get_config('database', 'db_user')
    passwd = config.get_config('database', 'db_password')
    name = config.get_config('database', 'db_name')
    port = config.get_config('database', 'db_port')
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=name, port=int(port))
    db_cur = conn.cursor()
    return db_cur
