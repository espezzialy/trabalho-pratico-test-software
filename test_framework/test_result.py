class TestResult:
    """
    Classe responsável por coletar e sumarizar os resultados da execução dos testes.
    """

    RUN_MSG = 'run'
    FAILURE_MSG = 'failed'
    ERROR_MSG = 'error'

    def __init__(self, suite_name=None):
        """
        Args:
            suite_name (str, optional): Nome da suíte de testes
        """
        self.run_count = 0
        self.failures = []
        self.errors = []

    def test_started(self):
        self.run_count += 1

    def add_failure(self, test):
        """
        Args:
            test: Nome ou referência do teste que falhou
        """
        self.failures.append(test)

    def add_error(self, test):
        """
        Args:
            test: Nome ou referência do teste que gerou erro
        """
        self.errors.append(test)

    def summary(self):
        return f'{self.run_count} {self.RUN_MSG}, ' \
               f'{str(len(self.failures))} {self.FAILURE_MSG}, ' \
               f'{str(len(self.errors))} {self.ERROR_MSG}'
