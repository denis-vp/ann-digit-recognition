from abc import ABC, abstractmethod

import numpy as np


class LossFunction(ABC):
    @abstractmethod
    def __call__(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        :param y_true: True values, 1D numpy array
        :param y_pred: Predicted values, 1D numpy array
        :return: float
        """
        pass

    @abstractmethod
    def derivative(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        :param y_true: True values, 1D numpy array
        :param y_pred: Predicted values, 1D numpy array
        :return: 1D numpy array
        """
        pass


class MSELoss(LossFunction):
    def __call__(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return np.mean((y_true - y_pred) ** 2)

    def derivative(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        return -2 * (y_true - y_pred)


class BCELoss(LossFunction):
    def __call__(self, y_true: float, y_pred: float) -> float:
        # Avoid log(0) by adding a small value
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
        return -1 * y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)

    def derivative(self, y_true: float, y_pred: float) -> np.ndarray:
        # Avoid division by zero
        y_pred = np.clip(y_pred, 1e-15, 1 - 1e-15)
        return (y_pred - y_true) / (y_pred * (1 - y_pred))


class CrossEntropyLoss(LossFunction):
    def __call__(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        return -np.sum(y_true * np.log(y_pred))

    def derivative(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        return -y_true / y_pred
