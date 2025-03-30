from test_framework import TestCase, TestResult, TestSuite
from test_framework.test_case_test import TestCaseTest
from test_framework.test_suite_test import TestSuiteTest


if __name__ == '__main__':
    result = TestResult()
    suite = TestSuite()
    
    # Adicionando todos os 8 testes de TestCaseTest à suíte
    suite.add_test(TestCaseTest('test_result_success_run'))
    suite.add_test(TestCaseTest('test_result_failure_run'))
    suite.add_test(TestCaseTest('test_result_error_run'))
    suite.add_test(TestCaseTest('test_result_multiple_run'))
    suite.add_test(TestCaseTest('test_was_set_up'))
    suite.add_test(TestCaseTest('test_was_run'))
    suite.add_test(TestCaseTest('test_was_tear_down'))
    suite.add_test(TestCaseTest('test_template_method'))
    
    # Adicionando todos os 3 testes de TestSuiteTest à suíte
    suite.add_test(TestSuiteTest('test_suite_size'))
    suite.add_test(TestSuiteTest('test_suite_success_run'))
    suite.add_test(TestSuiteTest('test_suite_multiple_run'))
    
    print(f"Total de testes na suíte: {len(suite.tests)}")
    
    # Executando todos os testes de uma vez usando TestSuite
    suite.run(result)
    
    print(f"\n=== Resultado Final ===")
    print(result.summary())
    
    if len(result.failures) > 0:
        print(f"Falhas: {result.failures}")
    if len(result.errors) > 0:
        print(f"Erros: {result.errors}")
    
