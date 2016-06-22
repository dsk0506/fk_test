一个pytest测试的架子
项目目录下 运行
创建环境
virtualenv env
启动环境
source env/bin/activate
设置PYTHONPATH
export PYTHONPATH=`pwd`/src
安装依赖
pip install -r requirement.txt
开始测试
src/test.py