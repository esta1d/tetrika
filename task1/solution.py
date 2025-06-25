import unittest

def strict(func):
    def inner(a, b):
        if isinstance(a, int) and isinstance(b, int):
            result = func(a, b)
        else:
            raise TypeError('Неверный тип данных')
        return result
    return inner

@strict
def sum_two(a: int, b: int) -> int:
    return a + b


try:
    print(sum_two(1, 2))       # Результат: 3
    print(sum_two(1, 2.4))     # Ошибка
except TypeError as e:
    print(f'Ошибка: {e}') 

class TestStrictDecorator(unittest.TestCase):

    # Тестируем успешный сценарий с двумя целыми числами
    def test_valid_input(self):
        self.assertEqual(sum_two(1, 2), 3)
        
    # Проверяем возникновение исключения при передаче некорректных типов
    def test_invalid_type_error(self):
        with self.assertRaises(TypeError):
            sum_two(1, 'a')  # Передаем строку вместо числа
            
        with self.assertRaises(TypeError):
            sum_two(1, 2.4)  # Передаем float вместо целого числа
            
if __name__ == '__main__':
    unittest.main()

# Можно использовать и такой подход
# decorator = strict(sum_two)
# print (decorator(1, 2.4))
# print (decorator(1, 2))