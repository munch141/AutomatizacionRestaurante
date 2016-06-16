from datetime import datetime


class Transaccion:
    def __init__(self, monto):
        self.monto = monto
        self.fecha = datetime.now()


class Historial:
    def __init__(self):
        self.trans = []
        self.total = 0
        
    def agregarTransaccion(self, t):
        if not isinstance(t.monto, float) and not isinstance(t.monto, int):
            raise TypeError("Error el monto debe ser un número.")
        else:
            if self.total < 0:
                self.total = 0
    
            if (t.monto == sys.float_info.max and 0 < self.total) or \
               (self.total == sys.float_info.max and 0 < t.monto):
                raise OverflowError('No se realizó la transacción. Límite del'
                                    ' registo excedido.')
            elif t.monto < 0:
                raise ArithmeticError('No se realizó la transacción. Monto'
                                      ' negativo.')
            else:
                self.trans.append(t)
                self.total += t.monto