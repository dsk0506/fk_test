import pytest
import MySQLdb
@pytest.fixture(scope="session")
def cur(request):
    def fin():
        db_cur.close()
        conn.close()
        print  'db over'
    request.addfinalizer(fin)
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='test', port=3306)
    db_cur = conn.cursor()
    return db_cur

@pytest.fixture(scope="module")
def smtp():
    print 123