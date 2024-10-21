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
        # Lista de palabras de ejemplo
        self.palabras = cargar_palabras('palabras.txt')

    def test_remove_accents(self):
        # Probar la eliminación de acentos
        self.assertEqual(remove_accents('ÁRBOL'), 'ARBOL')
        self.assertEqual(remove_accents('ÉXITO'), 'EXITO')
        self.assertEqual(remove_accents('GATOS'), 'GATOS')  

    def test_validate_guess(self):
        # Probar que solo palabras de 5 letras sean válidas
        self.assertTrue(validate_guess('CASAS'))
        self.assertFalse(validate_guess('CASA'))  # Menos de 5 letras
        self.assertFalse(validate_guess('CASASS'))  # Más de 5 letras
        self.assertFalse(validate_guess('CASA1'))  # Contiene número
        self.assertFalse(validate_guess('CA$AS'))  # Contiene símbolo no alfabético

    def test_validate_palabra(self):
        # Probar que las palabras estén en la lista
        self.assertTrue(validate_palabra(self.palabras, 'CASAS'))
if __name__ == '__main__':
    unittest.main()
