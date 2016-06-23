import pytest
import os

exit(pytest.main("-q -s " + os.path.split(os.path.realpath(__file__))[0] + "/tests"))
