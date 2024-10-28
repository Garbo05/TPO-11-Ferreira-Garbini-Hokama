"""
modo oscuro y claro dependiedo de la hora
Solo letras
Longitud de 5 caracteres
longitud menor a 5
longitud mayor a 5
no numeros
no caracteres especiales
palabras en la lista
palabras fuera de la lista
comprobar coincidencia de 1 letra
                            2 letras
                            3 letras
                            4 letras
                            5 letras

"""
import unittest
import HtmlTestRunner
from Validaciones import cargar_palabras, validate_guess, \
    validate_palabra, remove_accents


class TestStringle(unittest.TestCase):

    def setUp(self):
        self.palabras = cargar_palabras('palabras.txt')

    def test_remove_accents(self):
        self.assertEqual(remove_accents('ÁRBOL'), 'ARBOL')
        self.assertEqual(remove_accents('ÉXITO'), 'EXITO')
        self.assertEqual(remove_accents('GATOS'), 'GATOS')

    def test_validate_length_guess_equals_five(self):
        self.assertTrue(validate_guess('CASAS'))
        self.assertTrue(validate_guess('LICUA'))
        self.assertTrue(validate_guess('MAMUT'))

    def test_validate_length_guess_less_than_five(self):
        self.assertFalse(validate_guess('CASA'))
        self.assertFalse(validate_guess('OJO'))
        self.assertFalse(validate_guess('OLA'))

    def test_validate_length_guess_more_than_five(self):
        self.assertFalse(validate_guess('CASASS'))
        self.assertFalse(validate_guess('ABEJAS'))
        self.assertFalse(validate_guess('LICUAR'))

    def test_validate_guess_is_all_letters(self):
        self.assertTrue(validate_guess('CASAS'))

    def test_validate_guess_have_numbers(self):
        self.assertFalse(validate_guess('CASA5'))
        self.assertFalse(validate_guess('AB3JA'))
        self.assertFalse(validate_guess('LICU4'))

    def test_validate_guess_have_special_characters(self):
        self.assertFalse(validate_guess('CA$AS'))
        self.assertFalse(validate_guess('MAPE0'))
        self.assertFalse(validate_guess('N1CHO'))

    def test_validate_guess_match_one_letter(self):
        for i in 'CASAS':
            if i == 'C':
                first_letter = 'C'
        self.assertEqual(first_letter, 'C')

    def test_validate_palabra_in_text_file(self):
        self.assertTrue(validate_palabra(self.palabras, 'CASAS'))

    def test_validate_word_not_in_text_file(self):
        self.assertFalse(validate_palabra(self.palabras, 'AAAAA'))

if __name__ == '__main__':
     unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner())
