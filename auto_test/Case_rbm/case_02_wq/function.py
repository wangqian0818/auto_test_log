# encoding='utf-8'

class Test_case_01():

    def test_01(self):
        print("Test_case_01：用例内容")
        assert 4 + 1 == 0

    # @pytest.mark.skip(reseason="skip")
    def test_02(self):
        print("Test_case_02：用例内容")

    def test_03(self):
        print("Test_case_03：用例内容")
        assert 4 + 4 == 0
