from test_framework.test_result import TestResult


class TestRunner:
    """
    Classe responsável por orquestrar a execução dos testes e fornecer relatórios.
    """

    def __init__(self):
        self.result = TestResult()

    def run(self, test):
        """
        Args:
            test: Instância de TestCase ou TestSuite para executar
            
        Returns:
            TestResult: Objeto contendo os resultados da execução
        """
        test.run(self.result)
        print(self.result.summary())
        return self.result
