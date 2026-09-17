import streamlit as st
import pandas as pd
import numpy as np

# Page settings
st.set_page_config(
    page_title="Mental Health in Tech Survey",
    page_icon="🧠",
    layout="wide"
)

# Load dataset
df = pd.read_csv("survey.csv")

# Clean Age
df.loc[(df["Age"] < 0) | (df["Age"] > 100), "Age"] = np.nan
df = df.dropna(subset=["Age"])

# Clean Gender
def clean_gender(gender):
    gender = str(gender).strip().lower()

    if gender in [
        'male', 'm', 'man', 'cis male', 'male (cis)', 'cis man',
        'mal', 'maile', 'mail', 'malr', 'msle', 'male-ish',
        'guy (-ish) ^_^', 'something kinda male?',
        'male leaning androgynous',
        'ostensibly male, unsure what that really means'
    ]:
        return "Male"

    elif gender in [
        'female', 'f', 'woman', 'cis female', 'female (cis)',
        'cis-female/femme', 'femake', 'femail', 'female (trans)',
        'trans-female', 'trans woman'
    ]:
        return "Female"

    else:
        return "Other"

df["Gender"] = df["Gender"].apply(clean_gender)

# Fill missing values
df["self_employed"] = df["self_employed"].fillna("Unknown")
df["work_interfere"] = df["work_interfere"].fillna("Unknown")

# Title
st.title("🧠 Mental Health in Tech Survey")

st.write(
    "This interactive dashboard explores mental health treatment patterns "
    "and workplace factors among technology workers."
)

st.divider()

# Main metrics
st.subheader("📊 Overview")

total = len(df)
treatment_yes = (df["treatment"] == "Yes").sum()
treatment_no = (df["treatment"] == "No").sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Respondents", total)
col2.metric("Reported Treatment", treatment_yes)
col3.metric("Did Not Report Treatment", treatment_no)
# Treatment Distribution
st.subheader("🧠 Mental Health Treatment Distribution")

treatment_counts = df["treatment"].value_counts()

st.bar_chart(treatment_counts)
# Family History vs Treatment
st.subheader("👨‍👩‍👧 Family History vs Treatment")

family_treatment = pd.crosstab(
    df["family_history"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(family_treatment)
# Country Analysis
st.subheader("🌍 Treatment by Country")

top_countries = df["Country"].value_counts()
top_countries = top_countries[top_countries >= 20].index

country_treatment = pd.crosstab(
    df[df["Country"].isin(top_countries)]["Country"],
    df[df["Country"].isin(top_countries)]["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(country_treatment)
# Work Interference Analysis
st.subheader("💼 Work Interference vs Treatment")

work_treatment = pd.crosstab(
    df["work_interfere"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(work_treatment)
# Gender Analysis
st.subheader("👥 Treatment by Gender")

gender_treatment = pd.crosstab(
    df["Gender"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(gender_treatment)
# Workplace Benefits Analysis
st.subheader("🏢 Workplace Mental Health Benefits vs Treatment")

benefits_treatment = pd.crosstab(
    df["benefits"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(benefits_treatment)
# Care Options Analysis
st.subheader("🩺 Mental Health Care Options vs Treatment")

care_treatment = pd.crosstab(
    df["care_options"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(care_treatment)
# Wellness Program Analysis
st.subheader("🧘 Wellness Program vs Treatment")

wellness_treatment = pd.crosstab(
    df["wellness_program"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(wellness_treatment)
# Seeking Help Analysis
st.subheader("🤝 Seeking Help vs Treatment")

help_treatment = pd.crosstab(
    df["seek_help"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(help_treatment)
# Anonymity Analysis
st.subheader("🔐 Anonymity vs Treatment")

anonymity_treatment = pd.crosstab(
    df["anonymity"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(anonymity_treatment)
# Mental Health Consequence Analysis
st.subheader("⚠️ Mental Health Consequence vs Treatment")

consequence_treatment = pd.crosstab(
    df["mental_health_consequence"],
    df["treatment"],
    normalize="index"
).mul(100)

st.bar_chart(consequence_treatment)
# Age Distribution
st.subheader("📈 Age Distribution of Respondents")

st.bar_chart(
    df["Age"].value_counts().sort_index()
)
# Treatment Filter
st.subheader("🎯 Explore Treatment Data")

treatment_filter = st.selectbox(
    "Select Treatment Status",
    ["All", "Yes", "No"]
)

if treatment_filter == "All":
    filtered_df = df
else:
    filtered_df = df[df["treatment"] == treatment_filter]

st.write("Number of respondents:", len(filtered_df))
# Country Filter
st.subheader("🌍 Explore by Country")

countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())

country_filter = st.selectbox(
    "Select Country",
    countries
)

if country_filter == "All":
    country_df = df
else:
    country_df = df[df["Country"] == country_filter]

st.write("Number of respondents:", len(country_df))
# Gender Filter
st.subheader("👥 Explore by Gender")

gender_filter = st.selectbox(
    "Select Gender",
    ["All", "Male", "Female", "Other"]
)

if gender_filter == "All":
    gender_df = df
else:
    gender_df = df[df["Gender"] == gender_filter]

st.write("Number of respondents:", len(gender_df))
# Sidebar
st.sidebar.title("🧠 Mental Health Survey")

st.sidebar.write(
    "This dashboard analyzes the 2014 Mental Health in Tech Survey "
    "to explore treatment patterns and workplace mental health factors."
)

st.sidebar.markdown("---")

st.sidebar.write("📌 Dataset: 2014 Mental Health in Tech Survey")
st.sidebar.write("📌 Total respondents: 1254")
st.sidebar.write("📌 Analysis: Exploratory Data Analysis")
st.divider()

st.caption("🧠 Mental Health in Tech Survey | Exploratory Data Analysis | Streamlit")
