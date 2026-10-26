"""
Smart Outcome Predictor - Streamlit app

Predicts, for an online-course learner:
  * Completion  -> will the student complete the course? (classification)
  * Final score -> expected final score (regression)

Expected folder layout (next to this file):
    app.py
    requirements.txt
    Data/      Smart_Outcome_Predictor_Dataset_5200.xlsx
    Model/     best_clf_pipeline.pkl, best_reg_pipeline.pkl
    Notebook/  Smart Outcome Predictor.ipynb

Run:  streamlit run app.py
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import streamlit as st

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
APP_TITLE = "Smart Outcome Predictor"
APP_ICON = "🎯"

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "Data" / "Smart_Outcome_Predictor_Dataset_5200.xlsx"
CLF_PATH = BASE_DIR / "Model" / "best_clf_pipeline.pkl"
REG_PATH = BASE_DIR / "Model" / "best_reg_pipeline.pkl"

TRAINED_SKLEARN = "1.6.1"  # version the .pkl pipelines were saved with

TARGET_CLF = "completion_status"
TARGET_REG = "final_score"

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem;}
    .result-card {
        padding: 1.4rem; border-radius: 14px; text-align: center; color: white;
        margin-bottom: 0.5rem;
    }
    .result-card h1 {color: white; margin: 0; font-size: 2rem;}
    .result-card p {margin: 0.2rem 0 0 0; opacity: 0.92;}
    .good {background: linear-gradient(135deg, #059669, #10b981);}
    .bad  {background: linear-gradient(135deg, #dc2626, #f97316);}
    .info {background: linear-gradient(135deg, #4f46e5, #7c3aed);}
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# LOADERS
# ----------------------------------------------------------------------------
def _patch_sklearn_compat():
    """Pickles made with some scikit-learn versions reference a private class
    that newer versions removed. Re-create it so the pickle can load."""
    import sklearn.compose._column_transformer as ct

    if not hasattr(ct, "_RemainderColsList"):
        class _RemainderColsList(list):
            pass

        ct._RemainderColsList = _RemainderColsList


@st.cache_resource(show_spinner="Loading models...")
def load_model(path_str: str):
    path = Path(path_str)
    if not path.exists():
        return None
    try:
        return joblib.load(path)
    except AttributeError:
        _patch_sklearn_compat()
        return joblib.load(path)


@st.cache_data(show_spinner="Loading data...")
def load_data():
    if not DATA_PATH.exists():
        return None
    return pd.read_excel(DATA_PATH)


df = load_data()
clf = load_model(str(CLF_PATH))
reg = load_model(str(REG_PATH))


# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
def rng(col, cast=float):
    """(min, max, median) of a dataset column."""
    s = df[col]
    return cast(s.min()), cast(s.max()), cast(s.median())


def options(col):
    return sorted(df[col].dropna().astype(str).unique().tolist())


def build_row(v: dict) -> pd.DataFrame:
    """Build the exact 17-column frame the pipelines were trained on."""
    start = pd.Timestamp(v["course_start_date"])
    row = {
        "student_id": int(df["student_id"].median()),  # identifier only
        "age": v["age"],
        "country_region": v["country_region"],
        "device_type": v["device_type"],
        "education_background": v["education_background"],
        "course_level": v["course_level"],
        "course_category": v["course_category"],
        "course_start_date": start,
        "week_of_year": int(start.isocalendar()[1]),
        "sessions": v["sessions"],
        "time_spent_hours": v["time_spent_hours"],
        "videos_watched": v["videos_watched"],
        "quiz_attempts": v["quiz_attempts"],
        "assignments_submitted": v["assignments_submitted"],
        "forum_posts": v["forum_posts"],
        "avg_quiz_score": v["avg_quiz_score"],
        "attendance_rate": v["attendance_rate"],
    }
    cols = list(clf.feature_names_in_) if hasattr(clf, "feature_names_in_") else list(row)
    return pd.DataFrame([row])[cols]


def feature_importance(pipe, top=12):
    pre, model = pipe.named_steps["preprocessor"], pipe.named_steps["model"]
    names = [n.split("__", 1)[-1] for n in pre.get_feature_names_out()]
    imp = pd.Series(model.feature_importances_, index=names)
    # merge one-hot columns back into their original feature
    cats = ["country_region", "device_type", "education_background",
            "course_level", "course_category"]
    merged = {}
    for n, val in imp.items():
        key = next((c for c in cats if n.startswith(c)), n)
        merged[key] = merged.get(key, 0) + val
    return pd.Series(merged).sort_values(ascending=False).head(top)[::-1]


# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.title(f"{APP_ICON} {APP_TITLE}")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "🔮 Predict", "📊 Data Explorer", "🧠 Model Insights", "ℹ️ About"],
    )
    st.divider()
    st.caption(f"Data: {'✅ loaded' if df is not None else '❌ missing'}")
    st.caption(f"Completion model: {'✅ loaded' if clf is not None else '❌ missing'}")
    st.caption(f"Score model: {'✅ loaded' if reg is not None else '❌ missing'}")
    if sklearn.__version__ != TRAINED_SKLEARN:
        st.warning(
            f"Models were trained with scikit-learn {TRAINED_SKLEARN}, "
            f"but {sklearn.__version__} is installed. Predictions may fail - "
            f"run: pip install scikit-learn=={TRAINED_SKLEARN}"
        )

missing = []
if df is None:
    missing.append(f"`{DATA_PATH.relative_to(BASE_DIR)}`")
if clf is None:
    missing.append(f"`{CLF_PATH.relative_to(BASE_DIR)}`")
if reg is None:
    missing.append(f"`{REG_PATH.relative_to(BASE_DIR)}`")


# ----------------------------------------------------------------------------
# PAGES
# ----------------------------------------------------------------------------
if page == "🏠 Home":
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.subheader("Predict course completion and final score from learner behaviour.")

    if missing:
        st.error("Missing files: " + ", ".join(missing))
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Students", f"{len(df):,}")
        c2.metric("Completion rate", f"{df[TARGET_CLF].mean() * 100:.1f}%")
        c3.metric("Avg final score", f"{df[TARGET_REG].mean():.1f}")
        c4.metric("Features used", 16)

    st.markdown(
        """
        **How it works**
        1. Open **Predict** in the sidebar.
        2. Enter the student's profile, course details and engagement.
        3. Get the chance of completing the course and the expected final score.
        """
    )

elif page == "🔮 Predict":
    st.title("🔮 Make a Prediction")

    if missing:
        st.error("Missing files: " + ", ".join(missing))
        st.stop()

    with st.form("predict_form"):
        st.markdown("#### 👤 Student profile")
        a, b, c, d = st.columns(4)
        amin, amax, amed = rng("age", int)
        age = a.number_input("Age", amin, 100, amed)
        country_region = b.selectbox("Region", options("country_region"))
        device_type = c.selectbox("Device", options("device_type"))
        education_background = d.selectbox("Education", options("education_background"))

        st.markdown("#### 📚 Course")
        a, b, c = st.columns(3)
        course_level = a.selectbox("Level", options("course_level"))
        course_category = b.selectbox("Category", options("course_category"))
        course_start_date = c.date_input(
            "Start date",
            value=pd.Timestamp(df["course_start_date"].median()).date(),
        )

        st.markdown("#### 🖱️ Engagement")
        a, b, c = st.columns(3)
        sessions = a.slider("Sessions", *rng("sessions", int))
        time_spent_hours = b.slider("Time spent (hours)", *rng("time_spent_hours"))
        videos_watched = c.slider("Videos watched", *rng("videos_watched", int))
        a, b, c = st.columns(3)
        quiz_attempts = a.slider("Quiz attempts", *rng("quiz_attempts", int))
        assignments_submitted = b.slider("Assignments submitted", *rng("assignments_submitted", int))
        forum_posts = c.slider("Forum posts", *rng("forum_posts", int))

        st.markdown("#### 🎓 Performance")
        a, b = st.columns(2)
        avg_quiz_score = a.slider("Average quiz score", 0.0, 100.0, float(df["avg_quiz_score"].median()))
        attendance_rate = b.slider("Attendance rate", 0.0, 1.0, float(df["attendance_rate"].median()))

        submitted = st.form_submit_button("Predict", type="primary", use_container_width=True)

    if submitted:
        X = build_row(
            dict(
                age=age, country_region=country_region, device_type=device_type,
                education_background=education_background, course_level=course_level,
                course_category=course_category, course_start_date=course_start_date,
                sessions=sessions, time_spent_hours=time_spent_hours,
                videos_watched=videos_watched, quiz_attempts=quiz_attempts,
                assignments_submitted=assignments_submitted, forum_posts=forum_posts,
                avg_quiz_score=avg_quiz_score, attendance_rate=attendance_rate,
            )
        )
        try:
            pred_c = int(clf.predict(X)[0])
            prob = float(clf.predict_proba(X)[0][list(clf.classes_).index(1)])
            score = float(np.clip(reg.predict(X)[0], 0, 100))
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            if sklearn.__version__ != TRAINED_SKLEARN:
                st.info(f"Install the version used for training: scikit-learn=={TRAINED_SKLEARN}")
            st.stop()

        left, right = st.columns(2)
        with left:
            css, text = ("good", "Likely to COMPLETE") if pred_c == 1 else ("bad", "Likely to DROP OUT")
            st.markdown(
                f'<div class="result-card {css}"><p>Course completion</p>'
                f"<h1>{text}</h1><p>Completion probability: {prob * 100:.1f}%</p></div>",
                unsafe_allow_html=True,
            )
            st.progress(min(max(prob, 0.0), 1.0))
        with right:
            st.markdown(
                f'<div class="result-card info"><p>Expected final score</p>'
                f"<h1>{score:.1f} / 100</h1>"
                f"<p>Dataset average: {df[TARGET_REG].mean():.1f}</p></div>",
                unsafe_allow_html=True,
            )
            st.progress(min(max(score / 100, 0.0), 1.0))

        with st.expander("Input summary"):
            st.dataframe(X.drop(columns=["student_id"]).T.rename(columns={0: "value"}),
                         use_container_width=True)

elif page == "📊 Data Explorer":
    st.title("📊 Data Explorer")
    if df is None:
        st.error("Missing files: " + ", ".join(missing))
        st.stop()

    tab1, tab2, tab3 = st.tabs(["Preview", "Statistics", "Charts"])
    with tab1:
        st.dataframe(df.head(200), use_container_width=True)
        st.download_button("Download CSV", df.to_csv(index=False), "smart_outcome_data.csv", "text/csv")
    with tab2:
        st.dataframe(df.describe().T, use_container_width=True)
    with tab3:
        cat_cols = ["country_region", "device_type", "education_background",
                    "course_level", "course_category"]
        c1, c2 = st.columns(2)
        with c1:
            col = st.selectbox("Completion rate by", cat_cols)
            st.bar_chart(df.groupby(col)[TARGET_CLF].mean())
        with c2:
            col2 = st.selectbox("Average final score by", cat_cols, key="c2")
            st.bar_chart(df.groupby(col2)[TARGET_REG].mean())
        num = st.selectbox(
            "Distribution of",
            [c for c in df.select_dtypes("number").columns if c != "student_id"],
        )
        counts, edges = np.histogram(df[num].dropna(), bins=20)
        st.bar_chart(pd.Series(counts, index=np.round(edges[:-1], 2)))

elif page == "🧠 Model Insights":
    st.title("🧠 Model Insights")
    if clf is None or reg is None:
        st.error("Missing files: " + ", ".join(missing))
        st.stop()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**What drives completion** (Random Forest)")
        st.bar_chart(feature_importance(clf), horizontal=True)
    with c2:
        st.markdown("**What drives final score** (Random Forest)")
        st.bar_chart(feature_importance(reg), horizontal=True)
    st.caption("Importance = share of the model's decisions explained by each feature.")

else:
    st.title("ℹ️ About")
    st.markdown(
        f"""
        **{APP_TITLE}** uses machine learning trained on 5,200 online-learner records
        to estimate whether a student will complete a course and what final score to expect.

        **Models:** Random Forest classifier (completion) and Random Forest regressor (final score),
        each inside a scikit-learn pipeline (imputation, scaling, one-hot encoding).

        **Project structure:** `Data/` dataset, `Notebook/` training work, `Model/` saved pipelines.

        **Tech:** Python, Pandas, Scikit-learn, Streamlit
        """
    )