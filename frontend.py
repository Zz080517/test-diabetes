# import streamlit as st
# import requests
# import pandas as pd
#
# # 🌈 添加渐变背景样式
# st.markdown("""
#     <style>
#         html, body, .stApp {
#             height: 100%;
#             background: linear-gradient(to bottom right, #fefcea, #f1daff);
#         }
#     </style>
# """, unsafe_allow_html=True)
#
# # 🌐 多语言设置
# LANGUAGES = {
#     "English": {
#         "title": "Diabetes Risk Assessment",
#         "age": "Age",
#         "bmi": "BMI",
#         "glucose": "Glucose",
#         "predict": "Predict",
#         "trend_title": "📊 Age vs. Glucose Level Trend"
#     },
#     "中文": {
#         "title": "糖尿病风险评估",
#         "age": "年龄",
#         "bmi": "BMI",
#         "glucose": "血糖值",
#         "predict": "预测",
#         "trend_title": "📊 年龄 vs. 血糖水平趋势"
#     }
# }
#
# # 🔘 语言选择放在侧边栏
# st.sidebar.title("🌐 Language Settings")
# language = st.sidebar.selectbox("选择语言 / Select Language", list(LANGUAGES.keys()))
#
# # 🧾 页面主标题
# st.title(LANGUAGES[language]["title"])
#
# # 📥 输入字段
# age = st.number_input(LANGUAGES[language]["age"], min_value=1)
# bmi = st.number_input(LANGUAGES[language]["bmi"], min_value=10.0)
# glucose = st.number_input(LANGUAGES[language]["glucose"], min_value=50.0)
#
# # 📊 展示趋势图
# data = pd.DataFrame({
#     "Age": [20, 30, 40, 50, 60, 70],
#     "Glucose Level": [85, 90, 120, 140, 160, 180]
# })
# st.subheader(LANGUAGES[language]["trend_title"])
# st.line_chart(data.set_index("Age"))
#
# # 🤖 调用 Flask API 获取预测
# if st.button(LANGUAGES[language]["predict"]):
#     url = "http://127.0.0.1:5000/predict"
#     payload = {"Age": age, "BMI": bmi, "Glucose": glucose}
#     try:
#         response = requests.post(url, json=payload)
#         if response.status_code == 200:
#             result = response.json()["prediction"]
#             if language == "English":
#                 if "没有" in result:
#                     result = "No diabetes risk"
#                 elif "有" in result:
#                     result = "Diabetes is likely"
#             st.success(f"{LANGUAGES[language]['predict']} result: **{result}**")
#         else:
#             msg = "请求失败，请检查 Flask 服务器是否运行！" if language == "中文" else "Request failed, please check if the Flask server is running!"
#             st.error(msg)
#     except Exception as e:
#         st.error("❌ " + str(e))

import streamlit as st
import requests
import pandas as pd

# 🌈 渐变背景样式
st.markdown("""
    <style>
        html, body, .stApp {
            height: 100%;
            background: linear-gradient(to bottom right, #fefcea, #f1daff);
        }
    </style>
""", unsafe_allow_html=True)

# 🌐 多语言字典
LANGUAGES = {
    "English": {
        "title": "Diabetes Risk Assessment",
        "age": "Age",
        "bmi": "BMI",
        "glucose": "Glucose",
        "predict": "Predict",
        "trend_title": "📊 Age vs. Glucose Level Trend",
        "warning": "❗ Please complete all fields before submitting.",
        "error": "Request failed, please check if the Flask server is running!",
        "positive": "Diabetes is likely",
        "negative": "No diabetes risk"
    },
    "中文": {
        "title": "糖尿病风险评估",
        "age": "年龄",
        "bmi": "BMI",
        "glucose": "血糖值",
        "predict": "预测",
        "trend_title": "📊 年龄 vs. 血糖水平趋势",
        "warning": "❗ 请填写所有字段后再提交。",
        "error": "请求失败，请检查 Flask 服务器是否运行！",
        "positive": "可能有糖尿病",
        "negative": "可能没有糖尿病"
    }
}

# 🧭 语言选择在侧边栏
st.sidebar.title("🌐 Language Settings")
language = st.sidebar.selectbox("选择语言 / Select Language", list(LANGUAGES.keys()))

# 🧾 页面标题
st.title(LANGUAGES[language]["title"])

# 👤 用户输入（含范围限制 + 默认值）
age = st.number_input(LANGUAGES[language]["age"], min_value=1, max_value=120, value=18)
bmi = st.number_input(LANGUAGES[language]["bmi"], min_value=10.0, max_value=60.0, value=20.0)
glucose = st.number_input(LANGUAGES[language]["glucose"], min_value=50.0, max_value=300.0, value=85.0)

# 📊 示例趋势图
data = pd.DataFrame({
    "Age": [20, 30, 40, 50, 60, 70],
    "Glucose Level": [85, 90, 120, 140, 160, 180]
})
st.subheader(LANGUAGES[language]["trend_title"])
st.line_chart(data.set_index("Age"))

# 🧠 预测逻辑 + 输入验证
if st.button(LANGUAGES[language]["predict"]):
    if age == 0 or bmi == 0.0 or glucose == 0.0:
        st.warning(LANGUAGES[language]["warning"])
    else:
        try:
            url = "http://127.0.0.1:5000/predict"
            payload = {"Age": age, "BMI": bmi, "Glucose": glucose}
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()["prediction"]
                if language == "English":
                    if "没有" in result:
                        result = LANGUAGES[language]["negative"]
                    elif "有" in result:
                        result = LANGUAGES[language]["positive"]
                st.success(f"{LANGUAGES[language]['predict']} result: **{result}**")
            else:
                st.error("⚠️ " + LANGUAGES[language]["error"])
        except Exception as e:
            st.error("❌ " + str(e))