import unittest


class TestDecorators(unittest.TestCase):

    def test_decorator_with_kwargs__funcs(self):
        from src.decorators import decorator_with_kwargs

        @decorator_with_kwargs
        def add_5_to_result(original_func: callable = None, adder=None):
            def decorated_func(*args, **kwargs):
                result: int = original_func(*args, **kwargs)

                if adder is None:
                    return result + 5
                else:
                    return result + adder

            return decorated_func

        @add_5_to_result
        def sum_1_and_1():
            return 1 + 1

        @add_5_to_result(adder=4)
        def sum_2_and_2():
            return 2 + 2

        @add_5_to_result
        def sum_3_and_n(n: int):
            return 3 + n

        @add_5_to_result(adder=4)
        def sum_4_and_n(n: int):
            return 4 + n

        @add_5_to_result
        def sum_5_n_m(n: int, m: int):
            return 5 + n + m

        @add_5_to_result(adder=4)
        def sum_6_n_m(n: int, m: int):
            return 6 + n + m

        # raises =================================================
        with self.assertRaises(TypeError) as context:
            @add_5_to_result(imposible_kwarg="Something insane!!!")
            def sum_nothing():
                pass

        self.assertEqual(sum_1_and_1(), 1 + 1 + 5)

        self.assertEqual(sum_2_and_2(), 2 + 2 + 4)

        self.assertEqual(sum_3_and_n(1), 3 + 1 + 5)
        self.assertEqual(sum_3_and_n(n=1), 3 + 1 + 5)

        self.assertEqual(sum_4_and_n(1), 4 + 1 + 4)
        self.assertEqual(sum_4_and_n(n=1), 4 + 1 + 4)

        self.assertEqual(sum_5_n_m(1, 2), 5 + 1 + 2 + 5)
        self.assertEqual(sum_5_n_m(1, m=2), 5 + 1 + 2 + 5)
        self.assertEqual(sum_5_n_m(n=1, m=2), 5 + 1 + 2 + 5)

        self.assertEqual(sum_6_n_m(1, 2), 6 + 1 + 2 + 4)
        self.assertEqual(sum_6_n_m(1, m=2), 6 + 1 + 2 + 4)
        self.assertEqual(sum_6_n_m(n=1, m=2), 6 + 1 + 2 + 4)

        with self.assertRaises(TypeError) as context:
            sum_6_n_m(imposible_kwarg="Something insane!!!")

    def test_decorator_with_kwargs__methods(self):
        from src.decorators import decorator_with_kwargs

        @decorator_with_kwargs
        def louder_n_times(original_func: callable = None, n=None):
            def decorated_func(*args, **kwargs):
                result: str = original_func(*args, **kwargs)

                if n is None:
                    return result
                else:
                    return result.replace('!', '!' * n)

            return decorated_func

        class Dog:
            def __init__(self, size: int):
                self.size = size

            def bark(self):
                return f"Bark{'!' * (self.size // 2)}"

            @louder_n_times
            def regular_bark(self):
                return self.bark()

            @louder_n_times(n=3)
            def best_bark(self):
                return self.bark()

            # raises =================================================
            with self.assertRaises(TypeError) as context:
                @louder_n_times(imposible_kwarg="Something insane!!!")
                def broken_bark(self):
                    pass

        a_dog = Dog(size=2)

        self.assertEqual(a_dog.bark(), "Bark!")
        self.assertEqual(a_dog.regular_bark(), a_dog.bark())
        self.assertEqual(a_dog.best_bark(), "Bark!!!")

    def test_method_not_allowed(self):
        from src.decorators import method_not_allowed

        class Dog:

            @method_not_allowed
            def meow(self):
                pass

            @method_not_allowed
            def meow_1(self, arg):
                pass

            @method_not_allowed
            def meow_2(self, arg, kwarg):
                pass

            @method_not_allowed(exception=ConnectionResetError(1))
            def meow_3(self, arg, kwarg):
                pass

            @method_not_allowed(exception=ConnectionResetError(1))
            def meow_4(self, arg, kwarg):
                pass

            @method_not_allowed(exception=ConnectionResetError(1))
            def meow_5(self, arg, kwarg):
                pass

        a_dog = Dog()

        self.assertRaises(Exception, a_dog.meow)
        self.assertRaises(Exception, a_dog.meow_1)
        self.assertRaises(Exception, a_dog.meow_2)
        self.assertRaises(ConnectionResetError, a_dog.meow_3)
        self.assertRaises(ConnectionResetError, a_dog.meow_4)
        self.assertRaises(ConnectionResetError, a_dog.meow_5)


if __name__ == '__main__':
    unittest.main()
