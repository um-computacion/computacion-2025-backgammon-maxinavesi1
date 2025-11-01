"""Test suite principal que descubre y ejecuta todos los tests del proyecto."""
import unittest


def load_tests(loader, tests, pattern):
    """
    Descubre y carga todos los tests del proyecto.

    Args:
        loader: El test loader que ejecuta el descubrimiento.
        tests: TestSuite con los tests ya cargados (no usado).
        pattern: Patrón para buscar archivos de test (no usado).

    Returns:
        TestSuite: Suite con todos los tests descubiertos.
    """
    # Los parámetros tests y pattern no se usan, pero son requeridos por unittest
    _ = tests
    _ = pattern
    return loader.discover('backgammon/tests', pattern='test_*.py', top_level_dir='.')


if __name__ == "__main__":
    unittest.main()