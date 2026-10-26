<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4f46e5,100:7c3aed&height=220&section=header&text=Smart%20Outcome%20Predictor&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=AI-powered%20course%20completion%20%26%20final%20score%20prediction&descAlignY=58&descSize=18" width="100%" alt="Smart Outcome Predictor banner"/>

<a href="https://smart-outcome-predictor-by-master.streamlit.app/">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=7C3AED&center=true&vCenter=true&width=700&lines=Predict+who+will+complete+a+course;Estimate+the+final+score+instantly;Built+with+Machine+Learning+%2B+Streamlit;Data-driven+decisions+for+smarter+learning" alt="Typing animation"/>
</a>

<br/>

<a href="https://smart-outcome-predictor-by-master.streamlit.app/">
  <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit"/>
</a>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

### 🚀 [Live Demo → smart-outcome-predictor-by-master.streamlit.app](https://smart-outcome-predictor-by-master.streamlit.app/)

</div>

---

## 📌 Overview

**Smart Outcome Predictor** is a machine-learning web app that analyses how an online learner behaves and predicts two things:

| Prediction | Type | Question answered |
|---|---|---|
| ✅ **Course Completion** | Classification | Will the student complete the course? (with probability) |
| 🎓 **Final Score** | Regression | What final score is the student likely to achieve? |

Educators and platforms can use it to spot at-risk students early and step in before they drop out.

---

## ✨ Features

- 🔮 **Instant predictions** - completion probability and expected final score in one click
- 🧾 **Simple input form** - student profile, course details, engagement and performance
- 📊 **Data Explorer** - preview data, statistics and interactive charts
- 🧠 **Model Insights** - see which features drive each prediction
- ⚡ **Fast and light** - Streamlit UI with cached models and data

---

## 🔄 How It Works

```mermaid
flowchart LR
    A[📥 Student Inputs] --> B[🧹 Preprocessing<br/>Impute + Scale + One-Hot]
    B --> C[🌲 Random Forest Classifier]
    B --> D[🌲 Random Forest Regressor]
    C --> E[✅ Completion + Probability]
    D --> F[🎓 Expected Final Score]
    E --> G[🖥️ Streamlit Dashboard]
    F --> G
```

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Language | Python |
| Data | Pandas, NumPy, OpenPyXL |
| Machine Learning | scikit-learn (Pipelines, Random Forest), Joblib |
| Web App | Streamlit |
| Deployment | Streamlit Community Cloud |

---

## 📂 Project Structure

```
Smart outcome Predictor/
│
├── app.py                 # Streamlit web application
├── requirements.txt       # Python dependencies
│
├── Data/
│   └── Smart_Outcome_Predictor_Dataset_5200.xlsx
│
├── Model/
│   ├── best_clf_pipeline.pkl   # Completion model
│   └── best_reg_pipeline.pkl   # Final-score model
│
└── Notebook/
    └── Smart Outcome Predictor.ipynb   # EDA + model training
```

---

## 🗃️ Dataset

5,200 learner records with 19 columns, including:

- **Profile:** age, region, device type, education background
- **Course:** level, category, start date, week of year
- **Engagement:** sessions, time spent, videos watched, quiz attempts, assignments submitted, forum posts
- **Performance:** average quiz score, attendance rate
- **Targets:** `completion_status` (classification) and `final_score` (regression)

---

## ⚙️ Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
streamlit run app.py
```

> ⚠️ The saved models were trained with **scikit-learn 1.6.1**. Use the same version
> (`pip install scikit-learn==1.6.1`) to avoid loading or prediction errors.

---

## 🔭 Future Improvements

- Add SHAP-based explanations for individual predictions
- Batch prediction by uploading a CSV or Excel file
- Compare more models and tune hyperparameters
- Add authentication and a dashboard for instructors

---

## 👨‍💻 Owner

<div align="center">

### **Man Trivedi**

*Machine Learning • Data Science • Streamlit Apps*

[![Live App](https://img.shields.io/badge/Live%20App-Open-7C3AED?style=for-the-badge&logo=streamlit&logoColor=white)](https://smart-outcome-predictor-by-master.streamlit.app/)

⭐ If you like this project, give it a star!

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3aed,100:4f46e5&height=120&section=footer" width="100%" alt="footer"/>

</div>
