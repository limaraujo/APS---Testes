import pytest 

try:
    from aps.src.main import Status, evaluate_scholarship
except ModuleNotFoundError:
    from src.main import Status, evaluate_scholarship

def test_evaluate_scholarship_approved():
    result = evaluate_scholarship(18, 8.5, 90.0, True, False)
    assert result.status == Status.APPROVED
    assert "Applicant meets all scholarship requirements." in result.reasons


# Test case for manual review due to age and attendance
def test_evaluate_scholarship_manual_review_age():
    result = evaluate_scholarship( 16, 8, 80.0, True, False)
    assert result.status == Status.MANUAL_REVIEW

# Test case for manual review due to attendance and GPA
def test_evaluate_scholarship_manual_review_attendance():
    result = evaluate_scholarship(18,6.5,79.9,True,False)
    assert result.status == Status.MANUAL_REVIEW
    
# Test case for manual review due to age and GPA
def test_evaluate_scholarship_manual_review_age_gpa():
    result = evaluate_scholarship(17,6.5,90.0,True,False)
    assert result.status == Status.MANUAL_REVIEW
  
# Test case for manual review due to age, GPA and attendance
def test_evaluate_scholarship_manual_review_age_gpa_attendance():
    result = evaluate_scholarship(17,6.5,79.9,True,False)
    assert result.status == Status.MANUAL_REVIEW

# Test case for rejection due to age, including manual review reasones
def test_evaluate_scholarship_rejected_age():
    result = evaluate_scholarship(15, 6, 70.0, True, False)
    assert result.status == Status.REJECTED
    assert "Applicant is younger than the minimum age." in result.reasons

# Test case for rejection due having a disciplinary record, including manual review reasones
def test_evaluate_scholarship_rejected_disciplinary_record():
    result = evaluate_scholarship(18, 8.5, 90.0, True, True)
    assert result.status == Status.REJECTED
    assert "Applicant has a disciplinary record." in result.reasons

# Test case for rejection due to not having completed required courses
def test_evaluate_scholarship_rejected_required_courses():
    result = evaluate_scholarship(18, 8.5, 90.0, False, False)
    assert result.status == Status.REJECTED
    assert "Required courses have not been completed." in result.reasons

# Test case for rejection for all factors
def test_evaluate_scholarship_rejected_all_factors():
    result = evaluate_scholarship(15, 5.5, 70.0, False, True)
    assert result.status == Status.REJECTED
    assert "Applicant is younger than the minimum age." in result.reasons
    assert "GPA is below the minimum required." in result.reasons
    assert "Attendance rate is below the minimum required." in result.reasons
    assert "Required courses have not been completed." in result.reasons
    assert "Applicant has a disciplinary record." in result.reasons

# Test case for invalid GPA input
def test_evaluate_scholarship_invalid_gpa():
    with pytest.raises(ValueError) as excinfo:
        evaluate_scholarship(18, -1.0, 90.0, True, False)
    assert "GPA must be between 0 and 10." in str(excinfo.value)

# Test case for invalid attendance rate input
def test_evaluate_scholarship_invalid_attendance_rate():
    with pytest.raises(ValueError) as excinfo:
        evaluate_scholarship(18, 8.5, 150.0, True, False)
    assert "Attendance rate must be between 0 and 100." in str(excinfo.value)
    
# Test case lower boundary for age
def test_evaluate_scholarship_boundary_age():
    result = evaluate_scholarship(16, 8.5, 90.0, True, False)
    assert result.status == Status.MANUAL_REVIEW
    
def test_boundary_age_18():
    result = evaluate_scholarship(18, 8.0, 85.0, True, False)
    assert result.status == Status.APPROVED
    
def test_boundary_gpa_6():
    result = evaluate_scholarship(18, 6.0, 85.0, True, False)
    assert result.status == Status.MANUAL_REVIEW
    
def test_boundary_gpa_7():
    result = evaluate_scholarship(18, 7.0, 85.0, True, False)
    assert result.status == Status.APPROVED
    
def test_boundary_attendance_75():
    result = evaluate_scholarship(18, 8.0, 75.0, True, False)
    assert result.status == Status.MANUAL_REVIEW

def test_boundary_attendance_80():
    result = evaluate_scholarship(18, 8.0, 80.0, True, False)
    assert result.status == Status.APPROVED
    
def test_rejection_overrides_manual_review():
    result = evaluate_scholarship(
        age=17,        # review
        gpa=5.0,       # reject
        attendance_rate=78.0,
        has_required_courses=True,
        disciplinary_record=False
    )
    assert result.status == Status.REJECTED
    
def test_rejected_attendance_only():
    result = evaluate_scholarship(18, 8.0, 70.0, True, False)
    assert result.status == Status.REJECTED
    assert "Attendance rate is below the minimum required." in result.reasons
    
# Cada teste cobre combinações importantes de pares (pairwise)

@pytest.mark.parametrize(
    "age, gpa, attendance, courses, disciplinary, expected_status",
    [
        # Age x GPA
        (15, 5.5, 80.0, True, False, Status.REJECTED),       # REJECTED por idade e GPA
        (16, 7.5, 80.0, True, False, Status.MANUAL_REVIEW), # Age revisão, GPA aprovado
        (18, 6.5, 80.0, True, False, Status.MANUAL_REVIEW), # Age aprovado, GPA revisão

        # Age x Attendance
        (16, 8.0, 76.0, True, False, Status.MANUAL_REVIEW), # Age revisão, Attendance revisão
        (18, 8.0, 78.0, True, False, Status.MANUAL_REVIEW), # Age aprovado, Attendance revisão
        (15, 8.0, 70.0, True, False, Status.REJECTED),      # Age rejeição, Attendance rejeição

        # Age x Courses
        (18, 8.5, 85.0, False, False, Status.REJECTED),     # Age aprovado, courses rejeição
        (16, 7.0, 85.0, False, False, Status.REJECTED),     # Age revisão, courses rejeição

        # Age x Disciplinary
        (18, 8.5, 85.0, True, True, Status.REJECTED),       # Age aprovado, disciplinary rejeição
        (16, 7.0, 85.0, True, True, Status.REJECTED),       # Age revisão, disciplinary rejeição

        # GPA x Attendance
        (18, 6.5, 76.0, True, False, Status.MANUAL_REVIEW), # GPA revisão, Attendance revisão
        (18, 5.5, 78.0, True, False, Status.REJECTED),      # GPA rejeição, Attendance revisão

        # GPA x Courses
        (18, 6.5, 85.0, False, False, Status.REJECTED),     # GPA revisão, Courses rejeição
        (18, 5.5, 85.0, False, False, Status.REJECTED),     # GPA rejeição, Courses rejeição

        # GPA x Disciplinary
        (18, 6.5, 85.0, True, True, Status.REJECTED),       # GPA revisão, disciplinary rejeição
        (18, 5.5, 85.0, True, True, Status.REJECTED),       # GPA rejeição, disciplinary rejeição

        # Attendance x Courses
        (18, 8.0, 76.0, False, False, Status.REJECTED),     # Attendance revisão, Courses rejeição
        (18, 8.0, 78.0, False, False, Status.REJECTED),     # Attendance revisão, Courses rejeição

        # Attendance x Disciplinary
        (18, 8.0, 76.0, True, True, Status.REJECTED),       # Attendance revisão, Disciplinary rejeição
        (18, 8.0, 78.0, True, True, Status.REJECTED),       # Attendance revisão, Disciplinary rejeição

        # Courses x Disciplinary
        (18, 8.5, 85.0, False, True, Status.REJECTED),      # Courses rejeição, Disciplinary rejeição

        # Caso aprovado completo
        (18, 8.5, 85.0, True, False, Status.APPROVED),      # Todos aprovados
    ]
)
def test_evaluate_scholarship_pairwise(age, gpa, attendance, courses, disciplinary, expected_status):
    result = evaluate_scholarship(age, gpa, attendance, courses, disciplinary)
    assert result.status == expected_status