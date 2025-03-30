from test_framework import TestLoader, TestSuite, TestRunner
from test_framework.test_case_test import TestCaseTest
from test_framework.test_suite_test import TestSuiteTest
from test_framework.test_loader_test import TestLoaderTest


if __name__ == '__main__':
    # Criando TestLoader para descobrir métodos automaticamente
    loader = TestLoader()
    
    test_case_suite = loader.make_suite(TestCaseTest)     
    test_suite_suite = loader.make_suite(TestSuiteTest)   
    test_load_suite = loader.make_suite(TestLoaderTest)   
    
    
    suite = TestSuite()
    suite.add_test(test_case_suite)
    suite.add_test(test_suite_suite)
    suite.add_test(test_load_suite)
    
    print(f"\n=== Resultado Final ===")
    
    # Executando todos os testes através do TestRunner
    runner = TestRunner()
    runner.run(suite)
    
