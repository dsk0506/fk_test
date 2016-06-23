#!env/bin/python
import pytest
import os

exit(pytest.main("-q -s " + os.getcwd() + "/src/tests"))
