"""Tests unitarios para Evaluation."""

import pytest
from src.models.evaluation import Evaluation


class TestEvaluation:
    """Tests para la clase Evaluation."""

    def test_shouldCreateEvaluationWhenValidData(self):
        """Debería crear una evaluación con datos válidos."""
        evaluation = Evaluation(grade=15.5, weight=30.0)

        assert evaluation.grade == 15.5
        assert evaluation.weight == 30.0

    def test_shouldRaiseErrorWhenGradeBelowMinimum(self):
        """Debería lanzar error cuando la nota es menor que 0."""
        with pytest.raises(ValueError, match="debe estar entre"):
            Evaluation(grade=-1.0, weight=30.0)

    def test_shouldRaiseErrorWhenGradeAboveMaximum(self):
        """Debería lanzar error cuando la nota es mayor que 20."""
        with pytest.raises(ValueError, match="debe estar entre"):
            Evaluation(grade=21.0, weight=30.0)

    def test_shouldRaiseErrorWhenWeightBelowMinimum(self):
        """Debería lanzar error cuando el peso es menor que 0."""
        with pytest.raises(ValueError, match="debe estar entre"):
            Evaluation(grade=15.0, weight=-1.0)

    def test_shouldRaiseErrorWhenWeightAboveMaximum(self):
        """Debería lanzar error cuando el peso es mayor que 100."""
        with pytest.raises(ValueError, match="debe estar entre"):
            Evaluation(grade=15.0, weight=101.0)

    def test_shouldRaiseErrorWhenGradeIsNotNumeric(self):
        """Debería lanzar error cuando la nota no es numérica."""
        with pytest.raises(ValueError, match="debe ser un número"):
            Evaluation(grade="invalid", weight=30.0)

    def test_shouldRaiseErrorWhenWeightIsNotNumeric(self):
        """Debería lanzar error cuando el peso no es numérico."""
        with pytest.raises(ValueError, match="debe ser un número"):
            Evaluation(grade=15.0, weight="invalid")

    def test_shouldAcceptBoundaryValues(self):
        """Debería aceptar valores en los límites."""
        eval_min = Evaluation(grade=0.0, weight=0.0)
        eval_max = Evaluation(grade=20.0, weight=100.0)

        assert eval_min.grade == 0.0
        assert eval_min.weight == 0.0
        assert eval_max.grade == 20.0
        assert eval_max.weight == 100.0

    def test_shouldCompareEvaluationsCorrectly(self):
        """Debería comparar evaluaciones correctamente."""
        eval1 = Evaluation(grade=15.0, weight=30.0)
        eval2 = Evaluation(grade=15.0, weight=30.0)
        eval3 = Evaluation(grade=16.0, weight=30.0)

        assert eval1 == eval2
        assert eval1 != eval3
