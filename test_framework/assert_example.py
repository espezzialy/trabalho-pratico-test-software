from test_framework import TestCase, TestLoader, TestRunner


class AssertExampleTest(TestCase):


    def test_assert_equal_examples(self):
        self.assert_equal("hello", "hello")
        self.assert_equal(42, 42)
        self.assert_equal([1, 2, 3], [1, 2, 3])
        self.assert_equal({'key': 'value'}, {'key': 'value'})

    def test_assert_true_examples(self):
        self.assert_true(1 == 1)
        self.assert_true(5 > 3)
        self.assert_true("hello".startswith("he"))
        self.assert_true(len([1, 2, 3]) == 3)

    def test_assert_false_examples(self):
        self.assert_false(1 == 2)
        self.assert_false(3 > 5)
        self.assert_false("hello".startswith("bye"))
        self.assert_false(len([1, 2, 3]) == 5)

    def test_assert_in_examples(self):
        # Strings
        self.assert_in('o', 'hello')
        
        # Listas
        self.assert_in(2, [1, 2, 3, 4])
        
        # Dicionários (verifica chaves)
        animals = {'monkey': 'banana', 'cow': 'grass', 'seal': 'fish'}
        self.assert_in('monkey', animals)
        
        # Sets
        colors = {'red', 'green', 'blue'}
        self.assert_in('red', colors)


if __name__ == '__main__':
    loader = TestLoader()
    suite = loader.make_suite(AssertExampleTest)
    
    runner = TestRunner()
    runner.run(suite)
    
