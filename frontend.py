import streamlit as st
import joblib
import pandas as pd
from fpdf import FPDF
from io import BytesIO


model = joblib.load("diabetes_model.pkl")

def predict_diabetes(age, bmi, glucose):
    features = [[age, bmi, glucose]]
    result = model.predict(features)
    return "可能有糖尿病" if result[0] == 1 else "可能没有糖尿病"

st.set_page_config(page_title="Diabetes Assistant", page_icon="🧬", layout="centered")

st.markdown("""
    <style>
    /* 页面背景渐变 + 全局字体 */
    html, body, .stApp {
        background: linear-gradient(to top left, #fdfbfb, #ebedee);
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
        padding: 10px;
    }

    /* 统一按钮样式 */
    .stButton > button {
        background-color: #6c63ff;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #574dcf;
        color: #fff;
    }

    /* 输入框样式优化 */
    .stNumberInput input {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 6px;
        border: 1px solid #cccccc;
    }

    /* 侧边栏样式 */
    section[data-testid="stSidebar"] {
        background-color: #f3f0ff;
        border-right: 1px solid #ccc;
    }

    /* success/warning/info 风格微调 */
    .stSuccess {
        background-color: #e6f7ec;
        border-left: 6px solid #34c38f;
    }
    .stWarning {
        background-color: #fffbe6;
        border-left: 6px solid #f1b44c;
    }
    .stInfo {
        background-color: #e3f2fd;
        border-left: 6px solid #3b8eea;
    }

    /* 移除 Streamlit 默认页脚 */
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 多语言支持字典
LANGUAGES = {
    "English": {
        "title": "Diabetes Assistant",
        "select_service": "Choose Service",
        "select_language": "Select Language",
        "age": "Age",
        "bmi": "BMI",
        "glucose": "Glucose",
        "predict": "Predict",
        "trend_title": "📊 Age vs. Glucose Level Trend",
        "warning": "❗ Please complete all fields before submitting.",
        "error": "Request failed, please check if the Flask server is running!",
        "positive": "Diabetes is likely",
        "negative": "No diabetes risk",
        "calc_bmi": "BMI Calculator",
        "weight": "Weight (kg)",
        "height": "Height (cm)",
        "bmr_calc": "BMR Calculator",
        "bmr_result": "Your Basal Metabolic Rate is",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "ideal_weight": "Ideal Weight (BMI=22)",
        "healthy_range": "Weight range for healthy BMI",
        "already_ideal": "✅ You are already near your ideal weight!",
        "lose": "You may consider losing about",
        "gain": "You may consider gaining about",
        "reach_ideal": "to reach an ideal BMI",
        "computed_bmi": "✅ Your calculated BMI is",
        "report_generate": "Health Report Generator",
        "advice_title": "📋 Personalized Health Advice",
        "advice": {
            "underweight": "🍃 Your BMI is underweight. Consider more nutritious intake and watch your immunity and bone health.",
            "normal_bmi": "✅ Your BMI is in a healthy range. Keep up the good work!",
            "overweight": "⚠️ Slightly overweight. Reduce high-calorie food and increase daily activity.",
            "obese": "❗ Your BMI suggests obesity. Consider diet adjustment and regular exercise.",
            "low_glucose": "🍬 Blood glucose is low. Avoid long fasting, eat regularly.",
            "normal_glucose": "✅ Glucose is normal. Keep balanced diet and physical activity.",
            "high_glucose": "⚠️ Blood glucose is elevated. Reduce sugar intake, monitor regularly.",
            "very_high_glucose": "❗ Blood glucose is very high. Please consult a doctor promptly.",
            "age_glucose_warning": "👁️ Age and high glucose combined — consider checking vision, kidney, and blood pressure.",
            "too_thin": "🔍 Very low BMI may reflect malnutrition. Consider gastrointestinal or thyroid check."
        }
    },
    "中文": {
        "title": "糖尿病助手",
        "select_service": "选择服务",
        "select_language": "语言切换",
        "age": "年龄",
        "bmi": "BMI",
        "glucose": "血糖值",
        "predict": "预测",
        "trend_title": "📊 年龄 vs. 血糖水平趋势",
        "warning": "❗ 请填写所有字段后再提交。",
        "error": "请求失败，请检查 Flask 服务器是否运行！",
        "positive": "可能有糖尿病",
        "negative": "可能没有糖尿病",
        "calc_bmi": "BMI 计算器",
        "weight": "体重（公斤）",
        "height": "身高（厘米）",
        "bmr_calc": "基础代谢率计算器",
        "bmr_result": "您的基础代谢率为",
        "gender": "性别",
        "male": "男",
        "female": "女",
        "ideal_weight": "理想体重（BMI=22）",
        "healthy_range": "BMI 正常范围对应体重",
        "already_ideal": "✅ 您已处于理想体重附近！",
        "lose": "建议减重约",
        "gain": "建议增重约",
        "reach_ideal": "即可达到理想 BMI",
        "computed_bmi": "✅ 您的 BMI 为",
        "report_generate":"健康报告生成器",
        "advice_title": "📋 个性化健康建议",
        "advice": {
            "underweight": "🍃 您的体重偏瘦，建议增加营养摄入，留意免疫力和骨密度。",
            "normal_bmi": "✅ 您的 BMI 处于正常范围，保持健康生活方式。",
            "overweight": "⚠️ 您略微超重，建议减少高热量饮食并增加日常运动。",
            "obese": "❗ 您的 BMI 显示为肥胖，请考虑减脂饮食与规律锻炼。",
            "low_glucose": "🍬 血糖偏低，请注意饮食时间，避免空腹过长。",
            "normal_glucose": "✅ 血糖正常，继续维持均衡饮食与适量活动。",
            "high_glucose": "⚠️ 血糖偏高，建议减少糖分摄入，定期检测。",
            "very_high_glucose": "❗ 血糖显著升高，请尽快咨询医生进一步评估。",
            "age_glucose_warning": "👁️ 年龄较长且血糖偏高，建议检查眼底、肾功能与血压情况。",
            "too_thin": "🔍 体重过轻可能反映营养吸收不良，请关注胃肠健康或甲状腺功能。"
        }
    },
    "Malay": {
            "title": "Pembantu Diabetes",
            "select_service": "Pilih Perkhidmatan",
            "select_language": "Pilih Bahasa",
            "age": "Umur",
            "bmi": "BMI",
            "glucose": "Tahap Glukosa",
            "predict": "Ramalkan",
            "trend_title": "📊 Trend Umur vs. Tahap Glukosa",
            "warning": "❗ Sila lengkapkan semua medan sebelum menghantar.",
            "error": "Permintaan gagal, sila semak sama ada pelayan Flask berjalan.",
            "positive": "Kemungkinan ada diabetes",
            "negative": "Tiada risiko diabetes",
            "calc_bmi": "Kalkulator BMI",
            "weight": "Berat (kg)",
            "height": "Tinggi (cm)",
            "bmr_calc": "Kalkulator BMR",
            "bmr_result": "Kadar Metabolisme Asas anda ialah",
            "gender": "Jantina",
            "male": "Lelaki",
            "female": "Perempuan",
            "ideal_weight": "Berat Ideal (BMI=22)",
            "healthy_range": "Julat berat untuk BMI sihat",
            "already_ideal": "✅ Anda sudah hampir dengan berat ideal!",
            "lose": "Anda mungkin ingin menurunkan sekitar",
            "gain": "Anda mungkin ingin menaikkan sekitar",
            "reach_ideal": "untuk mencapai BMI ideal",
            "computed_bmi": "✅ BMI anda ialah",
            "report_generate": "Penjana Laporan Kesihatan",
            "advice_title": "📋 Nasihat Kesihatan Peribadi",
            "advice": {
                "underweight": "🍃 BMI anda terlalu rendah. Tambahkan nutrisi dan jaga imuniti serta kesihatan tulang anda.",
                "normal_bmi": "✅ BMI anda dalam julat sihat. Teruskan gaya hidup ini!",
                "overweight": "⚠️ Anda sedikit berat badan. Kurangkan makanan berkalori tinggi dan lebihkan aktiviti fizikal.",
                "obese": "❗ BMI menunjukkan obesiti. Sila pertimbangkan untuk mengubah diet dan bersenam secara berkala.",
                "low_glucose": "🍬 Tahap glukosa rendah. Elakkan berpuasa terlalu lama, makan secara berkala.",
                "normal_glucose": "✅ Glukosa normal. Teruskan diet seimbang dan aktiviti fizikal.",
                "high_glucose": "⚠️ Glukosa tinggi. Kurangkan pengambilan gula, pantau secara berkala.",
                "very_high_glucose": "❗ Glukosa sangat tinggi. Sila rujuk doktor dengan segera.",
                "age_glucose_warning": "👁️ Umur dan glukosa tinggi — pertimbangkan pemeriksaan mata, buah pinggang, dan tekanan darah.",
                "too_thin": "🔍 BMI terlalu rendah mungkin menunjukkan kekurangan nutrisi. Pertimbangkan pemeriksaan gastrointestinal atau tiroid."
            },
    }
}

# 🧭 固定语言选择（侧边栏顶部常驻）
st.sidebar.title("🌐 语言设置 / Language")
language = st.sidebar.selectbox("选择语言 / Select Language", list(LANGUAGES.keys()))
texts = LANGUAGES[language]
advice = texts["advice"]

# 服务列表映射到文字
service_options = {
    "predict": texts["predict"],
    "bmi": texts["calc_bmi"],
    "bmr": texts["bmr_calc"],
}

# 🧾 页面主标题
st.title(texts["title"])

tab1, tab2, tab3 = st.tabs([texts["predict"], texts["calc_bmi"], texts["bmr_calc"]])

with tab1:
        st.markdown(f"## 🤖 **{texts['title']}**")
        age = st.number_input(texts["age"], min_value=1, max_value=120, value=30)
        bmi = st.number_input(texts["bmi"], min_value=10.0, max_value=60.0, value=22.0)
        glucose = st.number_input(texts["glucose"], min_value=50.0, max_value=300.0, value=90.0)

        # 📊 示例趋势图
        data = pd.DataFrame({
            "Age": [20, 30, 40, 50, 60, 70],
            "Glucose Level": [85, 90, 120, 140, 160, 180]
        })
        st.subheader(texts["trend_title"])
        st.line_chart(data.set_index("Age"))

        # 🧠 预测请求
        if st.button(texts["predict"]):
            if age == 0 or bmi == 0.0 or glucose == 0.0:
                st.warning(texts["warning"])
            else:
                try:
                    result = predict_diabetes(age, bmi, glucose)

                    if language == "English":
                        if "没有" in result:
                            result = texts["negative"]
                        elif "有" in result:
                            result = texts["positive"]

                    st.success(f"{texts['predict']}：**{result}**")

                except Exception as e:
                    st.error("❌ " + str(e))

        # 🩺 个性化健康建议
        notes = []
        if bmi < 18.5:
            notes.append(advice["underweight"])
        elif 18.5 <= bmi < 25:
            notes.append(advice["normal_bmi"])
        elif 25 <= bmi < 28:
            notes.append(advice["overweight"])
        else:
            notes.append(advice["obese"])

        if glucose < 70:
            notes.append(advice["low_glucose"])
        elif 70 <= glucose <= 140:
            notes.append(advice["normal_glucose"])
        elif 140 < glucose <= 200:
            notes.append(advice["high_glucose"])
        else:
            notes.append(advice["very_high_glucose"])

        if age > 60 and glucose > 140:
            notes.append(advice["age_glucose_warning"])
        if bmi < 18:
            notes.append(advice["too_thin"])

        st.subheader(texts["advice_title"])
        for note in notes:
            st.info(note)

with tab2:
        st.markdown(f"### ⚖️ {texts['calc_bmi']}")

        weight = st.number_input(texts["weight"], min_value=30.0, max_value=200.0, value=60.0,key="bmi_weight")
        height_cm = st.number_input(texts["height"], min_value=100.0, max_value=220.0, value=170.0,key="bmr_height")
        height_m = height_cm / 100
        bmi_value = round(weight / (height_m ** 2), 2)

        st.success(f"{texts['computed_bmi']}：{bmi_value}")

        # 🔍 理想体重计算（BMI = 22）
        ideal_bmi = 22
        ideal_weight = round(ideal_bmi * (height_m ** 2), 1)

        min_bmi = 18.5
        max_bmi = 24.9
        min_weight = round(min_bmi * (height_m ** 2), 1)
        max_weight = round(max_bmi * (height_m ** 2), 1)

        st.markdown(f"🎯 **{texts['ideal_weight']}**：{ideal_weight} kg")
        st.markdown(f"🧭 {texts['healthy_range']}：{min_weight} kg ~ {max_weight} kg")

        delta = weight - ideal_weight
        if abs(delta) < 0.5:
            st.info(texts["already_ideal"])
        elif delta > 0:
            st.warning(f"{texts['lose']} {round(delta, 1)} kg → {texts['reach_ideal']}")
        else:
            st.warning(f"{texts['gain']} {abs(round(delta, 1))} kg → {texts['reach_ideal']}")

with tab3:
        st.markdown(f"### 🔥 {texts['bmr_calc']}")

        gender = st.radio(texts["gender"], [texts["male"], texts["female"]], horizontal=True)
        weight = st.number_input(texts["weight"], min_value=30.0, max_value=200.0, value=60.0,key="bmr_weight")
        height = st.number_input(texts["height"], min_value=100.0, max_value=220.0, value=170.0,key="bmr_height")
        age = st.number_input(texts["age"], min_value=10, max_value=100, value=25,key="bmr_age")

        if gender == texts["male"]:
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        bmr = round(bmr, 2)
        st.success(f"{texts['bmr_result']}：{bmr} kcal/day")
