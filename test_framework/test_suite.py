class TestSuite:
    """
    Classe que representa uma coleção de casos de teste.
    """

    def __init__(self):
        self.tests = []

    def add_test(self, test):
        """
        Args:
            test: Instância de TestCase ou TestSuite a ser adicionada
        """
        self.tests.append(test)

    def run(self, result):
        """
        Args:
            result (TestResult): Objeto para coletar resultados da execução
        """
        for test in self.tests:
            test.run(result)
