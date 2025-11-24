"""Tests unitarios para AttendancePolicy."""

import pytest
from src.policies.attendance_policy import AttendancePolicy


class TestAttendancePolicy:
    """Tests para la clase AttendancePolicy."""

    def test_shouldNotApplyPenaltyWhenAttendanceIsSufficient(self):
        """No debería aplicar penalización si la asistencia es suficiente."""
        policy = AttendancePolicy()
        calculated_grade = 15.5

        final_grade = policy.apply_penalty(
            has_reached_minimum=True,
            calculated_grade=calculated_grade
        )

        assert final_grade == calculated_grade

    def test_shouldApplyPenaltyWhenAttendanceIsInsufficient(self):
        """Debería aplicar penalización si la asistencia es insuficiente."""
        policy = AttendancePolicy()
        calculated_grade = 15.5

        final_grade = policy.apply_penalty(
            has_reached_minimum=False,
            calculated_grade=calculated_grade
        )

        assert final_grade == 0.0

    def test_shouldCalculatePenaltyAmountCorrectly(self):
        """Debería calcular el monto de la penalización correctamente."""
        policy = AttendancePolicy()
        calculated_grade = 15.5

        penalty_amount = policy.calculate_penalty_amount(
            has_reached_minimum=False,
            calculated_grade=calculated_grade
        )

        assert penalty_amount == -15.5

    def test_shouldReturnZeroPenaltyWhenAttendanceIsSufficient(self):
        """Debería retornar penalización cero si la asistencia es suficiente."""
        policy = AttendancePolicy()

        penalty_amount = policy.calculate_penalty_amount(
            has_reached_minimum=True,
            calculated_grade=15.5
        )

        assert penalty_amount == 0.0

    def test_shouldAllowCustomPenaltyGrade(self):
        """Debería permitir configurar una nota de penalización personalizada."""
        custom_penalty = 5.0
        policy = AttendancePolicy(penalty_grade=custom_penalty)

        final_grade = policy.apply_penalty(
            has_reached_minimum=False,
            calculated_grade=15.0
        )

        assert final_grade == custom_penalty
        assert policy.penalty_grade == custom_penalty
