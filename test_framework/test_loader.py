from test_framework.test_suite import TestSuite


class TestLoader:
    """
    Classe responsável por descobrir automaticamente métodos de teste
    e criar suítes de teste a partir de classes de teste.
    """

    TEST_METHOD_PREFIX = 'test'

    def get_test_case_names(self, test_case_class):
        """
        Args:
            test_case_class: Classe de teste para inspecionar
            
        Returns:
            list: Lista de nomes dos métodos de teste encontrados
        """
        methods = dir(test_case_class)
        test_method_names = list(filter(lambda method: 
            method.startswith(self.TEST_METHOD_PREFIX), methods))
        return test_method_names

    def make_suite(self, test_case_class):
        """
        Args:
            test_case_class: Classe de teste para criar a suíte
            
        Returns:
            TestSuite: Suíte contendo todos os testes da classe
        """
        suite = TestSuite()
        for test_method_name in self.get_test_case_names(test_case_class):
            test_method = test_case_class(test_method_name)
            suite.add_test(test_method)
        return suite
