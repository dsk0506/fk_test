# coding:utf-8
import pytest
import MySQLdb


@pytest.fixture(scope="session")
def cur(request):
    def fin():
        db_cur.close()
        conn.close()

    request.addfinalizer(fin)
    conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='test', port=3306)
    db_cur = conn.cursor()
    return db_cur


def test_user(cur):
    print cur.execute('select * from student')
    assert 1 == 1


def test_user1():
    assert 1 == 1