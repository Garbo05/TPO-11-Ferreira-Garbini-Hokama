"""  
Solo letras
Longitud de 5 caracteres
longitud menor a 5
longitud mayor a 5
no numeros
no caracteres especiales
palabras en la lista
palabras fuera de la lista
"""
import unittest
from Validaciones import cargar_palabras, validate_guess, validate_palabra, remove_accents

class TestStringle(unittest.TestCase):

    def setUp(self):
        self.palabras = cargar_palabras('palabras.txt')

    def test_remove_accents(self):
        self.assertEqual(remove_accents('ÁRBOL'), 'ARBOL')
        self.assertEqual(remove_accents('ÉXITO'), 'EXITO')
        self.assertEqual(remove_accents('GATOS'), 'GATOS')  

    def test_validate_guess(self):
        self.assertTrue(validate_guess('CASAS'))
        self.assertFalse(validate_guess('CASA')) 
        self.assertFalse(validate_guess('CASASS'))
        self.assertFalse(validate_guess('CASA1')) 
        self.assertFalse(validate_guess('CA$AS')) 

    def test_validate_palabra(self):
        self.assertTrue(validate_palabra(self.palabras, 'CASAS'))

if __name__ == '__main__':
    unittest.main()
