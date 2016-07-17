import unittest
from src.jstp import jstp


class TestCase(unittest.TestCase):
    def test1(self):
        example = ['Marcus Aurelius', 'AE127095', ['1990-02-15', 'Rome'],\
                   ['Ukraine', 'Kiev', '03056', 'Pobedy', '37', '158', '']]
        test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy','37','158','']]"
        data = jstp.deserialize(test)
        assert data == example

    def test2(self):
        example = ['Marcus Aurelius', 'AE127095', ['1990-02-15', 'Rome'], ['Ukraine', 'Kiev', '03056', 'Pobedy', 37, 158]]
        test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',37,158]]"
        data = jstp.deserialize(test)
        assert data == example

    def test3(self):
        example = ['Marcus Aurelius', 'AE127095', ['1990-02-15', 'Rome'],\
                   ['Ukraine', 'Kiev', '03056', 'Pobedy', -37, None], False, True]
        test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',-37,undefined]" \
                ",false,true]"
        data = jstp.deserialize(test)
        assert data == example

    def test4(self):
        example = {0: 'Marcus Aurelius', 1: 'Marcus Aurelius', 2: 'AE127095', 3: ['1990-02-15', 'Rome'],\
         4: ['Ukraine', 'Kiev', '03056', 'Pobedy', -37, 158]}
        test = "{'Marcus Aurelius', 'AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',-37,158]}"
        data = jstp.parse(test)
        assert data == example

if __name__ == '__main__':
    unittest.main()
