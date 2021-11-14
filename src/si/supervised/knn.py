from src.si.supervised.model import Modelo
import numpy as np
from src.si.util.util import euclidean
from src.si.util.metrics import accuracy_score

class KNN(Modelo):
    def __init__(self, n_neighbors=5, classification=True):
        super(KNN).__init__()
        self.k_neighbors = n_neighbors
        self.classification = classification

    def fit(self, dataset):
        self.dataset = dataset
        self.is_fitted = True

    def get_neighbors(self, x):
        dist = euclidean(x, self.dataset.X)
        idx_sort = np.argsort(dist)
        return idx_sort[:self.k_neighbors]

    def predict(self, x):
        # todo ver outra forma de fazer isto
        assert self.is_fitted, 'Model must be fitted before prediction'
        neighbors = self.get_neighbors(x)
        values = self.dataset.Y[neighbors].tolist()
        if self.classification:
            prediction = max(set(values), key=values.count)
        else:
            prediction = sum(values)/len(values)
        return prediction

    def cost(self):
        y_pred = np.ma.apply_along_axis(self.predict, axis=0, arr=self.dataset.X.T)
        return accuracy_score(self.dataset.Y, y_pred)
