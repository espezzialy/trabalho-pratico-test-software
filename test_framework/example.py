from test_framework import TestCase, TestResult


class MyTest(TestCase):

    def set_up(self):
        self.value = 10

    def tear_down(self):
        print(f'tear_down para {self.test_method_name}')

    def test_success(self):
        print('test_success - teste que passa')
        assert self.value == 10

    def test_failure(self):
        print('test_failure - teste que falha')
        assert self.value == 5  # Vai falhar pois value = 10

    def test_error(self):
        print('test_error - teste que gera erro')
        result = 10 / 0  # Vai gerar ZeroDivisionError


if __name__ == '__main__':
    print("=== Demonstração TestCase + TestResult ===\n")
    
    result = TestResult()
    
    # Executa teste que passa
    print("1. Executando teste que passa:")
    test = MyTest('test_success')
    test.run(result)
    print()
    
    # Executa teste que falha
    print("2. Executando teste que falha:")
    test = MyTest('test_failure')
    test.run(result)
    print()
    
    # Executa teste que gera erro
    print("3. Executando teste que gera erro:")
    test = MyTest('test_error')
    test.run(result)
    print()
    
    # Exibe resumo final
    print("=== Resumo da Execução ===")
    print(result.summary())
    print(f"Falhas: {result.failures}")
    print(f"Erros: {result.errors}")
