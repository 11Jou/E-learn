def get_quiz_result(related_quiz, QuizResult, current_lesson, current_student):
    all_result = []
    for quiz in related_quiz:
        quiz_result = {}
        result_quiz = QuizResult.objects.filter(lesson = current_lesson, quiz = quiz, student = current_student).exists()
        if result_quiz:
            quiz_result[quiz] = QuizResult.objects.get(lesson = current_lesson, quiz = quiz, student = current_student)
        else:
            quiz_result[quiz] = 'Not Answerd'
        all_result.append(quiz_result)
    return all_result


def check_pass_quiz(correct_answers, questions):
    if correct_answers >= 0.5 * questions.count():
        result = "Passed"
    else:
        result = "Not Passed"
    return result
