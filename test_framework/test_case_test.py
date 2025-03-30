from test_framework import TestCase, TestResult


class TestStub(TestCase):
    def test_success(self):
        """Teste que passa com sucesso"""
        assert True

    def test_failure(self):
        """Teste que falha (AssertionError)"""
        assert False

    def test_error(self):
        """Teste que lança uma exceção"""
        raise Exception


class TestSpy(TestCase):
    """
    Classe auxiliar que "espiona" a execução do template method.
    """

    def __init__(self, name):
        TestCase.__init__(self, name)
        self.was_run = False
        self.was_set_up = False
        self.was_tear_down = False
        self.log = ""

    def set_up(self):
        self.was_set_up = True
        self.log += "set_up "

    def test_method(self):
        self.was_run = True
        self.log += "test_method "

    def tear_down(self):
        self.was_tear_down = True
        self.log += "tear_down"


class TestCaseTest(TestCase):
    """
    Classe de teste que testa a própria classe TestCase.
    """

    def set_up(self):
        self.result = TestResult()

    def test_result_success_run(self):
        stub = TestStub('test_success')
        stub.run(self.result)
        assert self.result.summary() == '1 run, 0 failed, 0 error'

    def test_result_failure_run(self):
        stub = TestStub('test_failure')
        stub.run(self.result)
        assert self.result.summary() == '1 run, 1 failed, 0 error'

    def test_result_error_run(self):
        stub = TestStub('test_error')
        stub.run(self.result)
        assert self.result.summary() == '1 run, 0 failed, 1 error'

    def test_result_multiple_run(self):
        stub = TestStub('test_success')
        stub.run(self.result)
        stub = TestStub('test_failure')
        stub.run(self.result)
        stub = TestStub('test_error')
        stub.run(self.result)
        assert self.result.summary() == '3 run, 1 failed, 1 error'

    def test_was_set_up(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.was_set_up

    def test_was_run(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.was_run

    def test_was_tear_down(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.was_tear_down

    def test_template_method(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert spy.log == "set_up test_method tear_down"

    def test_assert_true(self):
        self.assert_true(True)

    def test_assert_false(self):
        self.assert_false(False)

    def test_assert_equal(self):
        self.assert_equal("", "")
        self.assert_equal("foo", "foo")
        self.assert_equal([], [])
        self.assert_equal(['foo'], ['foo'])
        self.assert_equal((), ())
        self.assert_equal(('foo',), ('foo',))
        self.assert_equal({}, {})
        self.assert_equal({'foo'}, {'foo'})

    def test_assert_in(self):
        animals = {'monkey': 'banana', 'cow': 'grass', 'seal': 'fish'}

        self.assert_in('a', 'abc')
        self.assert_in('foo', ['foo'])
        self.assert_in(1, [1, 2, 3])
        self.assert_in('monkey', animals)


if __name__ == '__main__':
    print("=== Testando a classe TestCase ===\n")
    
    result = TestResult()
    
    # Executando todos os 12 testes de TestCaseTest
    print("Executando testes...")
    
    test = TestCaseTest('test_result_success_run')
    test.run(result)
    
    test = TestCaseTest('test_result_failure_run')
    test.run(result)
    
    test = TestCaseTest('test_result_error_run')
    test.run(result)
    
    test = TestCaseTest('test_result_multiple_run')
    test.run(result)
    
    test = TestCaseTest('test_was_set_up')
    test.run(result)
    
    test = TestCaseTest('test_was_run')
    test.run(result)
    
    test = TestCaseTest('test_was_tear_down')
    test.run(result)
    
    test = TestCaseTest('test_template_method')
    test.run(result)
    
    test = TestCaseTest('test_assert_true')
    test.run(result)
    
    test = TestCaseTest('test_assert_false')
    test.run(result)
    
    test = TestCaseTest('test_assert_equal')
    test.run(result)
    
    test = TestCaseTest('test_assert_in')
    test.run(result)
    
    print(f"\n=== Resultado Final ===")
    print(result.summary())
    
    if len(result.failures) > 0:
        print(f"Falhas: {result.failures}")
    if len(result.errors) > 0:
        print(f"Erros: {result.errors}")
