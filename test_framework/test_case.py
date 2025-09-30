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

    def run(self):
        """
        Template method que executa o teste seguindo o padrão:
        1. Chama set_up() para preparar o ambiente
        2. Executa o método de teste especificado
        3. Chama tear_down() para limpar o ambiente
        """
        self.set_up()    # chama método de setup
        test_method = getattr(self, self.test_method_name)
        test_method()    # chama método de teste 
        self.tear_down() # chama método de teardown 

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
