from test_framework import TestCase, TestResult
from test_framework.test_suite import TestSuite
from test_framework.test_case_test import TestStub


class TestSuiteTest(TestCase):
    def test_suite_size(self):
        suite = TestSuite()

        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.add_test(TestStub('test_error'))

        assert len(suite.tests) == 3

    def test_suite_success_run(self):
        result = TestResult()
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))

        suite.run(result)

        assert result.summary() == '1 run, 0 failed, 0 error'

    def test_suite_multiple_run(self):
        result = TestResult()
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.add_test(TestStub('test_error'))

        suite.run(result)

        assert result.summary() == '3 run, 1 failed, 1 error'


if __name__ == '__main__':
    result = TestResult()
    
    test = TestSuiteTest('test_suite_size')
    test.run(result)
    
    test = TestSuiteTest('test_suite_success_run')
    test.run(result)
    
    test = TestSuiteTest('test_suite_multiple_run')
    test.run(result)
    
    print(f"\n=== Resultado Final ===")
    print(result.summary())
    
    if len(result.failures) > 0:
        print(f"Falhas: {result.failures}")
    if len(result.errors) > 0:
        print(f"Erros: {result.errors}")
