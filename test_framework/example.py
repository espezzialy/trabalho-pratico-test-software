from test_framework import TestCase


class MyTest(TestCase):
    """
    Exemplo de classe de teste que estende TestCase.
    """

    def set_up(self):
        print('set_up')

    def tear_down(self):
        print('tear_down')

    def test_a(self):
        print('test_a')

    def test_b(self):
        print('test_b')

    def test_c(self):
        print('test_c')


if __name__ == '__main__':
    # Demonstração da execução individual de cada teste
    print("=== Executando testes individualmente ===")
    
    test = MyTest('test_a')
    test.run()
    
    test = MyTest('test_b')
    test.run()
    
    test = MyTest('test_c')
    test.run()
