from gravipy.tensorial import *

class Weyl(Tensor):
    def __init__(self, symbol, metric, RiemannT, RicciT, *args, **kwargs):
        self._connection_required(metric)
        super(Weyl, self).__init__(symbol, 4, metric, metric.conn, *args, **kwargs)
        self.Rm = RiemannT
        self.Ri = RicciT
        
        self._s = None

    def _compute_covariant_component(self, idxs):
        if (idxs[0] == idxs[1] or idxs[2] == idxs[3]) \
           and apply_tensor_symmetry:
            component = sympify(0)
        else:
            component = (self.Rm(idxs[0],idxs[1],idxs[2],idxs[3]) -
                         Rational(1,(self.dim-2))*(
                             self.metric(idxs[0],idxs[2])*self.Ri(idxs[3],idxs[1]) -
                             self.metric(idxs[0],idxs[3])*self.Ri(idxs[2],idxs[1]) -
                             self.metric(idxs[1],idxs[2])*self.Ri(idxs[3],idxs[0]) +
                             self.metric(idxs[1],idxs[3])*self.Ri(idxs[2],idxs[0]) 
                        ) + Rational(1,(self.dim-1)*(self.dim-2))*self.Ri.scalar()*(
                             self.metric(idxs[0],idxs[2])*self.metric(idxs[3],idxs[1]) -
                             self.metric(idxs[0],idxs[3])*self.metric(idxs[2],idxs[1])
                        )
                        ).together().simplify()
            self.components.update({idxs: component})
            if self.apply_tensor_symmetry:
                self.components.update({(idxs[1], idxs[0], idxs[2], idxs[3]): -component})
                self.components.update({(idxs[0], idxs[1], idxs[3], idxs[2]): -component})
                self.components.update({(idxs[1], idxs[0], idxs[3], idxs[2]): component})
                self.components.update({(idxs[2], idxs[3], idxs[0], idxs[1]): component})
                self.components.update({(idxs[3], idxs[2], idxs[0], idxs[1]): -component})
                self.components.update({(idxs[2], idxs[3], idxs[1], idxs[0]): -component})
                self.components.update({(idxs[3], idxs[2], idxs[1], idxs[0]): component})
        return component

    def square(self):
        if self._s is None:
            self._s = sum(
                self(k, l, m, n) * self(-k, -l, -m, -n) for k, l, m, n in
                list(variations(self.index_values[1], 4, True))
            ).together().simplify()
            return self._s
        else:
            return self._s
        
class Bach(Tensor):
    def __init__(self, symbol, metric, RicciT, WeylT, *args, **kwargs):
        self._connection_required(metric)
        super(Bach, self).__init__(symbol, 2, metric, metric.conn, *args, **kwargs)
        self.Ri = RicciT
        self.W = WeylT

    def _compute_covariant_component(self, idxs):
        component = (sum(sum(self.W.covariantD(idxs[0],-c,idxs[1],-d,c,d) +
                     Rational(1,2)*self.Ri(c,d)*self.W(idxs[0],-c,idxs[1],-d)
                     for c in self.index_values[1])
                     for d in self.index_values[1])
                    ).together().simplify()
        self.components.update({idxs: component})
        if self.apply_tensor_symmetry:
                self.components.update({(idxs[1], idxs[0]): component})
        return component