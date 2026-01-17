import re

def analyze_exam_style(text):
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 5]

    question_starters = []
    avg_length = 0

    for l in lines:
        if re.match(r"^(Explain|Compare|Define|Discuss|Why|How|Prove|Derive)", l, re.I):
            question_starters.append(l[:80])

    if lines:
        avg_length = sum(len(l) for l in lines) // len(lines)

    return {
        "sample_question_openings": question_starters[:5],
        "average_question_length": avg_length,
        "question_count_estimate": len(lines)
    }
