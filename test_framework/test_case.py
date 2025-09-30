class TestCase:
    """
    Classe base para criar casos de teste no framework xUnit.
    """

    def __init__(self, test_method_name):
        """
        Args:
            test_method_name (str): Nome do método de teste
        """
        self.test_method_name = test_method_name

    def run(self, result):
        """
        Template method que executa o teste seguindo o padrão:
        1. Registra início do teste no result
        2. Chama set_up() para preparar o ambiente
        3. Executa o método de teste especificado (com tratamento de exceções)
        4. Chama tear_down() para limpar o ambiente
        """
        result.test_started()
        self.set_up()
        try:
            test_method = getattr(self, self.test_method_name)
            test_method()  
        except AssertionError as e:
            result.add_failure(self.test_method_name)
        except Exception as e:
            result.add_error(self.test_method_name)
        self.tear_down()    

    def set_up(self):
        """
        Método de fixture executado antes de cada teste.
        """
        pass

    def tear_down(self):
        """
        Método de fixture executado após cada teste.
        """
        pass
