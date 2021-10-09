# encoding='utf-8'
import logging
log = logging.getLogger(__name__)

import pytest


class Test_case_01():

    # @pytest.mark.skip(reseason="skip")
    def test_01(self):
        log.info('test_01：用例内容')
        print("test_01：用例内容")
        print("test_01：用例内容")
        print("test_01：用例内容")
        print("test_01：用例内容")
        print("test_01：用例内容")
        print("test_01：用例内容")
        print("test_01：用例内容")
        print("test_01：用例内容")
        print("test_01：用例内容")
        print("test_01：用例内容")

    # @pytest.mark.skip(reseason="skip")
    def test_02(self):
        while True:
            log.info('--------------------- Test_02：用例内容')
            print("--------------------- Test_02：用例内容")

    # def test_03(self):
    #     print("Test_case_03：用例内容")
    #     assert 4 + 4 == 0
