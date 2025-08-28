import random

class Dados:
  
  def __init__(self, semilla=None):
   self.__semilla__ = semilla
   self.__rng__ = random.Random(semilla)
   self.__ultimo_tiro__ = None 


  def tirar(self):
    d1 = self.__rng__.randint(1, 6)
    d2 = self.__rng__.randint(1, 6)
    if d1 == d2:
        movimientos = [d1, d1, d1, d1]
    else:
        movimientos = [d1, d2]
    self.__ultimo_tiro__ = (d1, d2, movimientos)
    return d1, d2, movimientos


  def ultimo_tiro(self):
    return self.__ultimo_tiro__