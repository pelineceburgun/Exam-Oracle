
def calculate_persona_scores(answers):
    """
    answers = {
        "degree": "ABD top üniversite",
        "age": "40-50",
        "question_type": "üst düzey kitap",
        "difficulty": "zor",
        "homework_relation": "orta",
        "exam_focus": "teori",
        "example_usage": "direkt sorar",
        "logic_memory": "mantık",
        "originality": "özgün"
    }
    """

    analytic = 0
    trap = 0
    classical = 0
    commenter = 0
    balanced = 0

    # Degree 
    degree = answers.get("degree")
    if degree in ["Amerika", "Avrupa"]:
        analytic += 2
        commenter += 1
    elif degree in ["ODTÜ/Boğaziçi/İTÜ/YTÜ/Bilkent/Koç"]:
        analytic += 1
    else:
        classical += 1

    #  Age 
    age = answers.get("age")
    if age == "30-40":
        analytic += 1
    elif age == "40-50":
        balanced += 1
    elif age == "50+":
        classical += 1

    #  Question Type 
    qt = answers.get("question_type")
    if qt == "her yerde bulunabilecek":
        classical += 2
    elif qt == "üst düzey kitap":
        analytic += 2
    elif qt == "basit ezber":
        classical += 2
    elif qt == "ileri düzey yorum":
        commenter += 3
    elif qt == "tuzak":
        trap += 3

    #  Difficulty 
    diff = answers.get("difficulty")
    if diff == "kolay":
        balanced += 1
    elif diff == "orta":
        balanced += 1
    elif diff == "zor":
        analytic += 1
        commenter += 1
    elif diff == "karışık":
        trap+= 1
        commenter += 1

    # Homework relation
    hw = answers.get("homework_relation")
    if hw == "çok":
        analytic += 1
    elif hw == "orta":
        balanced += 1
    elif hw == "hiç":
        trap += 1

    # Exam focus 
    focus = answers.get("exam_focus")
    if focus == "teori":
        classical += 1
    elif focus == "uygulama":
        analytic += 1
    elif focus == "karışık":
        balanced += 1
        commenter += 1

    #  Example usage 
    ex = answers.get("example_usage")
    if ex == "örnekle açıklar":
        analytic += 1
    elif ex == "direkt sorar":
        trap += 1
        classical += 1
    elif ex == "karışık":
        balanced += 1

    #  Logic vs memory
    lm = answers.get("logic_memory")
    if lm == "mantık":
        analytic += 1
    elif lm == "ezber":
        classical += 1
    elif lm == "dengeli":
        balanced += 1

    # Originality 
    og = answers.get("originality")
    if og == "standart":
        classical += 1
    elif og == "özgün":
        analytic += 1
        commenter += 1
    elif og == "karışık":
        balanced += 1

    scores = {
        "Analitik": analytic,
        "Tuzakçı": trap,
        "Klasikçi": classical,
        "Yorumcu": commenter,
        "Dengeli": balanced,
    }

    return scores


def get_persona_label(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    persona1, s1 = sorted_scores[0]
    persona2, s2 = sorted_scores[1]

    return {
        "top_persona": persona1,
        "secondary_persona": persona2,
        "scores": scores
    }
