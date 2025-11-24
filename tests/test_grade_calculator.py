"""Tests unitarios para GradeCalculator."""

import pytest
from src.models.student import Student
from src.models.evaluation import Evaluation
from src.services.grade_calculator import GradeCalculator
from src.policies.attendance_policy import AttendancePolicy
from src.policies.extra_points_policy import ExtraPointsPolicy


class TestGradeCalculator:
    """Tests para la clase GradeCalculator."""

    def test_shouldCalculateNormalGradeSuccessfully(self):
        """Debería calcular la nota normal exitosamente."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[False, False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001", has_reached_minimum_classes=True)
        calculator.register_evaluation(student, grade=15.0, weight=50.0)
        calculator.register_evaluation(student, grade=17.0, weight=50.0)

        # Act
        grade_detail = calculator.calculate_final_grade(student)

        # Assert
        assert grade_detail.weighted_average == 16.0
        assert grade_detail.attendance_penalty == 0.0
        assert grade_detail.extra_points == 0.0
        assert grade_detail.final_grade == 16.0

    def test_shouldApplyPenaltyWhenNoMinimumAttendance(self):
        """Debería aplicar penalización cuando no hay asistencia mínima."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001", has_reached_minimum_classes=False)
        calculator.register_evaluation(student, grade=18.0, weight=100.0)

        # Act
        grade_detail = calculator.calculate_final_grade(student)

        # Assert
        assert grade_detail.weighted_average == 18.0
        assert grade_detail.attendance_penalty == -18.0
        assert grade_detail.final_grade == 0.0

    def test_shouldApplyExtraPointsWhenAllTeachersAgree(self):
        """Debería aplicar puntos extra cuando todos los docentes acuerdan."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[True, True, True])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001", has_reached_minimum_classes=True)
        calculator.register_evaluation(student, grade=15.0, weight=100.0)

        # Act
        grade_detail = calculator.calculate_final_grade(student)

        # Assert
        assert grade_detail.weighted_average == 15.0
        assert grade_detail.extra_points == 1.0
        assert grade_detail.final_grade == 16.0

    def test_shouldNotApplyExtraPointsWhenNotAllTeachersAgree(self):
        """No debería aplicar puntos extra si no todos los docentes acuerdan."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[True, False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001", has_reached_minimum_classes=True)
        calculator.register_evaluation(student, grade=15.0, weight=100.0)

        # Act
        grade_detail = calculator.calculate_final_grade(student)

        # Assert
        assert grade_detail.extra_points == 0.0
        assert grade_detail.final_grade == 15.0

    def test_shouldClampGradeToMaximum(self):
        """Debería limitar la nota al máximo de 20."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(
            all_years_teachers=[True, True],
            extra_points_amount=5.0
        )
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001", has_reached_minimum_classes=True)
        calculator.register_evaluation(student, grade=19.0, weight=100.0)

        # Act
        grade_detail = calculator.calculate_final_grade(student)

        # Assert
        assert grade_detail.weighted_average == 19.0
        assert grade_detail.extra_points == 5.0
        assert grade_detail.final_grade == 20.0

    def test_shouldRaiseErrorWhenNoEvaluations(self):
        """Debería lanzar error cuando no hay evaluaciones (caso borde)."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[True])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001")

        # Act & Assert
        with pytest.raises(ValueError, match="al menos una evaluación"):
            calculator.calculate_final_grade(student)

    def test_shouldRaiseErrorWhenWeightsDoNotSum100(self):
        """Debería lanzar error cuando los pesos no suman 100% (caso borde)."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[True])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001")
        calculator.register_evaluation(student, grade=15.0, weight=50.0)
        calculator.register_evaluation(student, grade=17.0, weight=30.0)

        # Act & Assert
        with pytest.raises(ValueError, match="deben sumar 100"):
            calculator.calculate_final_grade(student)

    def test_shouldCalculateCorrectlyWithMultipleEvaluations(self):
        """Debería calcular correctamente con múltiples evaluaciones."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001", has_reached_minimum_classes=True)
        calculator.register_evaluation(student, grade=16.0, weight=20.0)
        calculator.register_evaluation(student, grade=14.0, weight=30.0)
        calculator.register_evaluation(student, grade=18.0, weight=50.0)

        # Act
        grade_detail = calculator.calculate_final_grade(student)

        # Assert
        expected_average = (16.0 * 0.2) + (14.0 * 0.3) + (18.0 * 0.5)
        assert abs(grade_detail.weighted_average - expected_average) < 0.01
        assert grade_detail.final_grade == expected_average

    def test_shouldBeDeterministicWithSameInputs(self):
        """Debería ser determinista: mismos inputs = mismo resultado (RNF03)."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[True, True])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student1 = Student(student_id="S001", has_reached_minimum_classes=True)
        calculator.register_evaluation(student1, grade=15.0, weight=60.0)
        calculator.register_evaluation(student1, grade=17.0, weight=40.0)

        student2 = Student(student_id="S002", has_reached_minimum_classes=True)
        calculator.register_evaluation(student2, grade=15.0, weight=60.0)
        calculator.register_evaluation(student2, grade=17.0, weight=40.0)

        # Act
        grade_detail1 = calculator.calculate_final_grade(student1)
        grade_detail2 = calculator.calculate_final_grade(student2)

        # Assert
        assert grade_detail1.weighted_average == grade_detail2.weighted_average
        assert grade_detail1.final_grade == grade_detail2.final_grade

    def test_shouldRegisterAttendanceCorrectly(self):
        """Debería registrar la asistencia correctamente (RF02)."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001")

        # Act
        calculator.register_attendance(student, has_reached_minimum=True)

        # Assert
        assert student.has_reached_minimum_classes is True

    def test_shouldHandleEdgeCaseWithZeroGrade(self):
        """Debería manejar caso borde con nota cero."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001", has_reached_minimum_classes=True)
        calculator.register_evaluation(student, grade=0.0, weight=100.0)

        # Act
        grade_detail = calculator.calculate_final_grade(student)

        # Assert
        assert grade_detail.weighted_average == 0.0
        assert grade_detail.final_grade == 0.0

    def test_shouldHandleEdgeCaseWithPerfectGrade(self):
        """Debería manejar caso borde con nota perfecta."""
        # Arrange
        attendance_policy = AttendancePolicy()
        extra_points_policy = ExtraPointsPolicy(all_years_teachers=[False])
        calculator = GradeCalculator(attendance_policy, extra_points_policy)

        student = Student(student_id="S001", has_reached_minimum_classes=True)
        calculator.register_evaluation(student, grade=20.0, weight=100.0)

        # Act
        grade_detail = calculator.calculate_final_grade(student)

        # Assert
        assert grade_detail.weighted_average == 20.0
        assert grade_detail.final_grade == 20.0
