
# from refnx.analysis import Objective
from refnx._lib import flatten
from refnx._lib import unique as f_unique
import numpy as np

# class ObjectiveOverlay(Objective):
#     def __init__(self, model, data, lnsigma=None, use_weights=True,
#                  transform=None, logp_extra=None, name=None):
#         super().__init__(model, data, lnsigma=None, use_weights=True,
#                  transform=None, logp_extra=None, name=None):


#     def ptform():
#         pass


class CFitter:
    def __init__(self, objective):
        self.objective=objective
        self.pValues=None
        self.upperBounds=None
        self.lowerBounds=None
        self.nDimensions=None
        self.bounds()
        self.nDim()
        self._bestPost = -np.inf
        self._best = []
#         print(self.nDimensions)
#         print(self.upperBounds,self.lowerBounds)
#         print(list(f_unique(p for p
#                      in flatten(self.objective.parameters) if p.vary )))
#         print(list(p for p
#                      in f_unique(flatten(self.objective.parameters)) if p.vary ))
        

    def priorTransform(self,u):
        return u*(self.upperBounds-self.lowerBounds) + self.lowerBounds

    def bounds(self):
        bounds = list( (p.bounds.lb, p.bounds.ub) for p
                     in f_unique(flatten(self.objective.parameters)) if p.vary )
        self.lowerBounds = np.array(list(bound[0] for bound in bounds))
        self.upperBounds = np.array(list(bound[1] for bound in bounds))

    def nDim(self):
        if self.nDimensions is None:
            self.nDimensions = len(list(p for p
                     in f_unique(flatten(self.objective.parameters)) if p.vary ))
        return self.nDimensions

#     @property
#     def pValues(self):
#         return self.pValues

#     @pValues.setter
#     def pVals(self, pValues):
#         self.pValues=pValues
#         self.objective.setp(pValues)

    def logl(self, pvalues):
#         self.pVals(pvalues)
        returns = 0
        returns+=self.objective.logl(pvalues)
        if self.objective.logp_extra and self.objective.logp_extra() == -np.inf:
            returns+=-np.inf#self.objective.model, self.objective.data)
        else:
            post = self.objective.logpost()
            if post > self._bestPost:
                self._bestPost = post
                self._best = pvalues
        return returns

    def fit(self):
        pass
