from utils.pdf_reader import extract_text_from_pdf
import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
from persona_engine import calculate_persona_scores, get_persona_label

# ENV
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")


st.set_page_config(page_title="Exam Oracle", page_icon="🔮", layout="centered")

st.title("🔮 Exam Oracle Quiz + AI Prediction")
st.write("**Hocanızın sınavda ne soracağını tahmin etmek için quizi doldurun!** 😄")
st.divider()


# Ders & Sınav Bilgileri

st.header("📚 Ders & Sınav Bilgileri")
course_name = st.text_input("Ders Adı", placeholder="Örn: Data Science & AI")
exam_type = st.selectbox("Sınav Türü", ["Test", "Klasik", "Karma"])
question_count = st.selectbox("Tahmini Soru Sayısı", ["<10",10, 20, 30])
if question_count == "<10":
    question_count_llm = 7
else:
    question_count_llm = question_count

st.divider()


# Hoca Profili

st.header("👩‍🏫 Hoca Profili")
degree = st.multiselect(
    "Hocanız lisans/yüksek lisans/doktora derecesini nerede almış?",
    ["ODTÜ/Boğaziçi/İTÜ/YTÜ/Bilkent/Koç", "Amerika", "Avrupa", "Diğer"]
)
age = st.radio("Hocanız hangi yaş aralığında?", ["30-40", "40-50", "50+"])
question_style = st.radio(
    "Hocanızın soru tipi?",
    [
        "Her yerde bulunabilecek tarzda",
        "Üst düzey kitap soruları",
        "Ezber ağırlıklı",
        "İleri düzey yorum",
        "Tuzaklı"
    ]
)
difficulty = st.radio("Zorluk seviyesi?", ["Kolay", "Orta", "Zor", "Karışık"])
assignment_relation = st.radio("Ödev–sınav ilişkisi?", ["Çok", "Orta", "Hiç"])
st.divider()


# Ders Tarzı

st.header("📖 Ders & Sınav Tarzı")
topic_weight = st.radio("Ağırlık?", ["Teori", "Uygulama", "Karışık"])
example_usage = st.radio("Soru anlatımı?", ["Örnekli", "Direkt", "Karışık"])
logic_vs_memorization = st.radio("Mantık / Ezber?", ["Mantık", "Ezber", "Dengeli"])
originality = st.radio("Özgünlük?", ["Standart", "Özgün", "Karışık"])
st.divider()


# Opsiyonel Kullanıcı Girdileri

st.header("💡 Kullanıcı Algısı (Opsiyonel)")
user_prediction = st.text_area(
    "Hocanın favori konu(ları)?",
    max_chars=250
)

uploaded_pdf = st.file_uploader(
    "📎 Geçmiş sınav PDF’i (opsiyonel)",
    type=["pdf"]
)

pdf_text = ""
if uploaded_pdf is not None:
    pdf_text = extract_text_from_pdf(uploaded_pdf)


# Persona

def run_persona_analysis(data):
    scores = calculate_persona_scores(data)
    return get_persona_label(scores)


# 🔮 TAHMİN

if st.button("🔮 Tahmin Et!"):
    quiz_data = {
        "course_name": course_name,
        "exam_type": exam_type,
        "question_count": question_count,
        "degree": degree,
        "age": age,
        "question_style": question_style,
        "difficulty": difficulty,
        "assignment_relation": assignment_relation,
        "topic_weight": topic_weight,
        "example_usage": example_usage,
        "logic_vs_memorization": logic_vs_memorization,
        "originality": originality,
    }

    persona = run_persona_analysis(quiz_data)

    st.subheader("✅ Quiz Sonuçları")
    st.write("📌 Hoca Tipi:", persona["top_persona"])
    st.write("📎 İkincil Persona:", persona["secondary_persona"])
    st.write("🔢 Skorlar:", persona["scores"])

    
    # PROMPT
    
    prompt = f"""
You are an expert university exam analyst.

Instructor Persona:
- Primary: {persona['top_persona']}
- Secondary: {persona['secondary_persona']}
- Scores: {json.dumps(persona['scores'])}

Task:
1. Describe the expected exam style.
2. Generate **at least {question_count_llm} realistic exam questions**.
3. Give concrete study advice.

Bias question themes toward:
{user_prediction if user_prediction else "No specific preference given."}

Course context:
{json.dumps(quiz_data, indent=2)}
"""

    if pdf_text:
        prompt += f"\n\nPast exam questions (for style imitation):\n{pdf_text}"

    if not api_key:
        st.error("OPENROUTER_API_KEY bulunamadı.")
    else:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "google/gemma-3-4b-it:free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.6,
            },
        )

        result = response.json()
        try:
            ai_text = result["choices"][0]["message"]["content"]
            st.markdown("### 💡 AI Tahmini")
            st.markdown(ai_text)
        except:
            st.error("AI yanıtı parse edilemedi")
            st.write(result)

# FOOTER

st.markdown("""
<style>
.footer {
    width: 100vw;
    margin-left: -50vw;
    left: 50%;
    position: relative;
    padding: 12px 0;
    text-align: center;
    font-size: 12px;
    color: #888;
    border-top: 1px solid #e0e0e0;
    background-color: #fafafa;
}
</style>

<div class="footer">
© 2026 All rights reserved.
</div>
""", unsafe_allow_html=True)


