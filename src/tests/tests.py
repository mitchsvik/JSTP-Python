import unittest
from src.jstp import jstp


class TestCase(unittest.TestCase):
    def test1(self):
        example = ['Marcus Aurelius', 'AE127095', ['1990-02-15', 'Rome'],\
                   ['Ukraine', 'Kiev', '03056', 'Pobedy', '37', '158', '']]
        test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy','37','158','']]"
        self.assertEqual(example, jstp.deserialize(test))

    def test2(self):
        example = ['Marcus Aurelius', 'AE127095', ['1990-02-15', 'Rome'], ['Ukraine', 'Kiev', '03056', 'Pobedy', 37, 158]]
        test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',37,158]]"
        self.assertEqual(example, jstp.deserialize(test))

    def test3(self):
        example = ['Marcus Aurelius', 'AE127095', ['1990-02-15', 'Rome'],\
                   ['Ukraine', 'Kiev', '03056', 'Pobedy', -37, None], False, True]
        test = "['Marcus Aurelius','AE127095',['1990-02-15','Rome'],['Ukraine','Kiev','03056','Pobedy',-37,undefined]" \
                ",false,true]"
        self.assertEqual(example, jstp.deserialize(test))

    def test4(self):
        example = {'0': 'Marcus Aurelius', '1': 'AE127095', '2': ['1990-02-15', 'Rome'],\
         '3': ['Ukraine', 'Kiev', '03056', 'Pobedy', -37, 158]}
        test = "{0:'Marcus Aurelius',1:'AE127095',2:['1990-02-15','Rome'],3:['Ukraine','Kiev','03056','Pobedy',-37,158]}"
        self.assertEqual(example, jstp.parse(test))

    def test_numbers(self):
        self.assertEqual(0, jstp.parse_number('0'))
        self.assertEqual(42, jstp.parse_number('42'))
        self.assertEqual(-3, jstp.parse_number('-3'))
        self.assertEqual(1e100, jstp.parse_number('1e+100'))
        self.assertEqual(1e-3, jstp.parse_number('0.001'))
        with self.assertRaises(Exception):
            jstp.parse_number('Not a number')

    def test_strings(self):
        self.assertEqual('str', jstp.parse_string('\'str\''))
        self.assertEqual('first\nsecond', jstp.parse_string('\'first\\nsecond\''))
        self.assertEqual('it\'s', jstp.parse_string('\'it\\\'s\''))
        # Don't work with shielded unicode symbols in this release.
        # self.assertEqual('01\u0000\u0001', jstp.parse_string('\'01\\u0000\\u0001\''))

    def test_booleans(self):
        self.assertEqual(True, jstp.parse_boolean('true'))
        self.assertEqual(False, jstp.parse_boolean('false'))
        with self.assertRaises(ValueError):
            jstp.parse_boolean('Not a boolean')

    def test_none(self):
        self.assertEqual(None, jstp.parse_none('undefined'))
        self.assertEqual(None, jstp.parse_none('null'))
        with self.assertRaises(ValueError):
            jstp.parse_none('string')

    def test_date(self):
        pass

if __name__ == '__main__':
    unittest.main()
