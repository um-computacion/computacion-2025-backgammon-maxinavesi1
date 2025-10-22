"""Tests para el módulo checker."""
import unittest
from backgammon.core.checker import Checker


class PruebasChecker(unittest.TestCase):
    """Pruebas para la clase Checker."""

    def test_crear_checker_con_id(self):
        """Verifica que se pueda crear un checker con un ID."""
        ficha = Checker(1)
        self.assertEqual(ficha.owner_id, 1)

    def test_owner_id_property(self):
        """Verifica que la property owner_id funcione correctamente."""
        ficha = Checker(5)
        self.assertEqual(ficha.owner_id, 5)

    def test_eq_con_otro_checker_mismo_owner(self):
        """Verifica igualdad entre checkers con mismo owner_id."""
        ficha1 = Checker(1)
        ficha2 = Checker(1)
        self.assertEqual(ficha1, ficha2)

    def test_eq_con_otro_checker_distinto_owner(self):
        """Verifica desigualdad entre checkers con distinto owner_id."""
        ficha1 = Checker(1)
        ficha2 = Checker(2)
        self.assertNotEqual(ficha1, ficha2)

    def test_eq_con_int_igual(self):
        """Verifica igualdad entre checker y entero igual a su owner_id."""
        ficha = Checker(3)
        self.assertEqual(ficha, 3)

    def test_eq_con_int_distinto(self):
        """Verifica desigualdad entre checker y entero distinto."""
        ficha = Checker(3)
        self.assertNotEqual(ficha, 5)

    def test_eq_con_tipo_incompatible(self):
        """Verifica que comparar con tipo incompatible no cause error."""
        ficha = Checker(1)
        self.assertNotEqual(ficha, "string")

    def test_eq_con_none(self):
        """Verifica que comparar con None retorne False."""
        ficha = Checker(1)
        self.assertNotEqual(ficha, None)

    def test_eq_con_lista(self):
        """Verifica que comparar con lista retorne False."""
        ficha = Checker(1)
        self.assertNotEqual(ficha, [1, 2, 3])

    def test_eq_con_dict(self):
        """Verifica que comparar con diccionario retorne False."""
        ficha = Checker(1)
        self.assertNotEqual(ficha, {"id": 1})

    def test_repr_formato_correcto(self):
        """Verifica que __repr__ retorne el formato correcto."""
        ficha = Checker(7)
        representacion = repr(ficha)
        self.assertEqual(representacion, "Checker(PID=7)")

    def test_repr_con_distintos_ids(self):
        """Verifica que __repr__ funcione con diferentes IDs."""
        ficha1 = Checker(1)
        ficha2 = Checker(99)
        self.assertIn("PID=1", repr(ficha1))
        self.assertIn("PID=99", repr(ficha2))

    def test_str_usa_repr(self):
        """Verifica que str() use __repr__."""
        ficha = Checker(42)
        self.assertEqual(str(ficha), "Checker(PID=42)")

    def test_multiples_checkers_distintos_ids(self):
        """Verifica que se puedan crear múltiples checkers con IDs distintos."""
        fichas = [Checker(i) for i in range(1, 6)]
        for i, ficha in enumerate(fichas, 1):
            self.assertEqual(ficha.owner_id, i)

    def test_checker_en_lista(self):
        """Verifica que checkers se puedan usar en listas."""
        ficha1 = Checker(1)
        ficha2 = Checker(1)
        lista = [ficha1]
        self.assertIn(ficha2, lista)


if __name__ == "__main__":
    unittest.main()