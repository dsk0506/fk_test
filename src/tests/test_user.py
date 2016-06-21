# coding:utf-8

def test_user(cur):
    print cur.execute('select * from student')
    assert 1 == 1


def test_user1(smtp):
    print 'user1'
    assert 1 == 1
