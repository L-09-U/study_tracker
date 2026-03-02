import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from database import init_db, add_record, get_all_records

# Init DB
init_db()

st.title("Study Tracker")

# SIDEBAR - ADD RECORD

st.sidebar.header("Add Study Record")

date = st.sidebar.date_input("Date")
subject = st.sidebar.text_input("Subject")
hours = st.sidebar.number_input("Study Hours", min_value=0.0)
focus = st.sidebar.slider("Focus Level (1-10)", 1, 10)
exercises = st.sidebar.number_input("Exercises Completed", min_value=0)
grade = st.sidebar.number_input("Grade (0-10)", min_value=0.0, max_value=10.0)

if st.sidebar.button("Save Record"):
    add_record(str(date), subject, hours, focus, exercises, grade)
    st.sidebar.success("Record saved!")

# DATA SOURCE SELECT

st.header("Choose Data Source")
mode = st.radio(
    "",
    ["Use Database", "Upload CSV File"]
)

df = None

# LOAD DATA

if mode == "Use Database":
    records = get_all_records()

    if records:
        df = pd.DataFrame(records, columns=[
            "id", "date", "subject",
            "hours", "focus", "exercises", "grade"
        ])
        df["date"] = pd.to_datetime(df["date"])

else:
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df["date"] = pd.to_datetime(df["date"])

# ANALYSIS SECTION

if df is not None and len(df) > 0:

    st.subheader("📊 Data Preview")
    st.dataframe(df)

    st.subheader("📈 Study Hours Over Time")
    df = df.sort_values("date")
    st.line_chart(df.set_index("date")["hours"])

    st.subheader("📊 Study Hours by Subject")
    subject_hours = df.groupby("subject")["hours"].sum()
    st.bar_chart(subject_hours)

    st.subheader("📌 Total Study Hours")
    st.write(df["hours"].sum())

    st.subheader("📌 Average Study Hours")
    st.write(df["hours"].mean())

    # MACHINE LEARNING

    if len(df) > 1:

        st.header(" Predict Grade (Machine Learning)")

        X = df[["hours", "focus", "exercises"]]
        y = df["grade"]

        model = LinearRegression()
        model.fit(X, y)

        score = model.score(X, y)
        st.write(f"Model R² Score: {score:.2f}")

        st.write("Model Coefficients:")
        st.write(f"Hours weight: {model.coef_[0]:.2f}")
        st.write(f"Focus weight: {model.coef_[1]:.2f}")
        st.write(f"Exercises weight: {model.coef_[2]:.2f}")

        st.subheader("Try Prediction")

        input_hours = st.number_input("Hours", 0.0, 24.0, 2.0)
        input_focus = st.slider("Focus", 1, 10, 5)
        input_exercises = st.number_input("Exercises", 0, 100, 3)

        if st.button("Predict"):
            prediction = model.predict([[input_hours, input_focus, input_exercises]])
            st.success(f"Predicted Grade: {prediction[0]:.2f}")

    else:
        st.warning("Need at least 2 records to train model.")

else:
    st.info("No data available yet.")