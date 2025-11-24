"""Tests unitarios para Student."""

import pytest
from src.models.student import Student
from src.models.evaluation import Evaluation


class TestStudent:
    """Tests para la clase Student."""

    def test_shouldCreateStudentWhenValidData(self):
        """Debería crear un estudiante con datos válidos."""
        student = Student(student_id="S001")

        assert student.student_id == "S001"
        assert len(student.evaluations) == 0
        assert student.has_reached_minimum_classes is False

    def test_shouldCreateStudentWithEvaluations(self):
        """Debería crear un estudiante con evaluaciones iniciales."""
        evaluations = [
            Evaluation(grade=15.0, weight=50.0),
            Evaluation(grade=16.0, weight=50.0)
        ]
        student = Student(student_id="S001", evaluations=evaluations)

        assert len(student.evaluations) == 2

    def test_shouldAddEvaluationSuccessfully(self):
        """Debería agregar evaluaciones exitosamente."""
        student = Student(student_id="S001")
        evaluation = Evaluation(grade=15.0, weight=30.0)

        student.add_evaluation(evaluation)

        assert len(student.evaluations) == 1

    def test_shouldRaiseErrorWhenExceedingMaxEvaluations(self):
        """Debería lanzar error al exceder el máximo de evaluaciones (RNF01)."""
        student = Student(student_id="S001")

        for i in range(10):
            student.add_evaluation(Evaluation(grade=10.0 + i, weight=10.0))

        with pytest.raises(ValueError, match="No se pueden agregar más de 10"):
            student.add_evaluation(Evaluation(grade=15.0, weight=10.0))

    def test_shouldRaiseErrorWhenCreatingWithTooManyEvaluations(self):
        """Debería lanzar error al crear con más de 10 evaluaciones."""
        evaluations = [Evaluation(grade=15.0, weight=10.0) for _ in range(11)]

        with pytest.raises(ValueError, match="No se pueden tener más de 10"):
            Student(student_id="S001", evaluations=evaluations)

    def test_shouldSetAttendanceStatus(self):
        """Debería establecer el estado de asistencia."""
        student = Student(student_id="S001")

        student.set_attendance_status(True)

        assert student.has_reached_minimum_classes is True

    def test_shouldRaiseErrorWhenStudentIdIsEmpty(self):
        """Debería lanzar error cuando el ID está vacío."""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            Student(student_id="")

    def test_shouldRaiseErrorWhenStudentIdIsWhitespace(self):
        """Debería lanzar error cuando el ID es solo espacios."""
        with pytest.raises(ValueError, match="no puede estar vacío"):
            Student(student_id="   ")

    def test_shouldRaiseErrorWhenStudentIdIsNotString(self):
        """Debería lanzar error cuando el ID no es string."""
        with pytest.raises(ValueError, match="debe ser un string"):
            Student(student_id=123)

    def test_shouldReturnCopyOfEvaluations(self):
        """Debería retornar una copia de las evaluaciones (inmutabilidad)."""
        student = Student(student_id="S001")
        evaluation = Evaluation(grade=15.0, weight=100.0)
        student.add_evaluation(evaluation)

        evaluations_copy = student.evaluations
        evaluations_copy.clear()

        assert len(student.evaluations) == 1
