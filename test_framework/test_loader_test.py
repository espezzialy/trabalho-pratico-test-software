from test_framework import TestCase, TestSuite
from test_framework.test_loader import TestLoader
from test_framework.test_case_test import TestStub, TestSpy


class TestLoaderTest(TestCase):
    """
    Classe de teste que testa a própria classe TestLoader.
    """

    def test_create_suite(self):
        loader = TestLoader()
        suite = loader.make_suite(TestStub)
        assert len(suite.tests) == 3

    def test_create_suite_of_suites(self):
        loader = TestLoader()
        stub_suite = loader.make_suite(TestStub)
        spy_suite = loader.make_suite(TestSpy)

        suite = TestSuite()
        suite.add_test(stub_suite)
        suite.add_test(spy_suite)

        assert len(suite.tests) == 2

    def test_get_multiple_test_case_names(self):
        loader = TestLoader()
        names = loader.get_test_case_names(TestStub)
        assert names == ['test_error', 'test_failure', 'test_success']

    def test_get_no_test_case_names(self):
        class Test(TestCase):
            def foobar(self):
                pass

        loader = TestLoader()
        names = loader.get_test_case_names(Test)
        assert names == []


if __name__ == '__main__':
    from test_framework.test_result import TestResult
    
    result = TestResult()
    loader = TestLoader()
    suite = loader.make_suite(TestLoaderTest)
    
    suite.run(result)
    
    print(f"\n=== Resultado Final ===")
    print(result.summary())
    
    if len(result.failures) > 0:
        print(f"Falhas: {result.failures}")
    if len(result.errors) > 0:
        print(f"Erros: {result.errors}")
    
    print(f"\nMétodos de teste descobertos automaticamente: {len(suite.tests)}")
