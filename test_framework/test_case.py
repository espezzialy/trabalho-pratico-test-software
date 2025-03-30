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
            test_method()    # chama método de teste
        except AssertionError as e:
            result.add_failure(self.test_method_name)
        except Exception as e:
            result.add_error(self.test_method_name)
        self.tear_down()     # chama método de teardown 

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def assert_equal(self, first, second):
        if first != second:
            msg = f'{first} != {second}'
            raise AssertionError(msg)

    def assert_true(self, expr):
        if not expr:
            msg = f'{expr} is not true'
            raise AssertionError(msg)

    def assert_false(self, expr):
        if expr:
            msg = f'{expr} is not false'
            raise AssertionError(msg)

    def assert_in(self, member, container):
        if member not in container:
            msg = f'{member} not found in {container}'
            raise AssertionError(msg)
