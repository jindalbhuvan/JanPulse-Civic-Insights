import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# JANPULSE: SURVEY & GROUND INSIGHTS PLATFORM
# --------------------------------------------------

st.set_page_config(
    page_title="JanPulse | Ground Insights",
    page_icon="📍",
    layout="wide"
)

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "janpulse_responses.csv")

COLUMNS = [
    "timestamp",
    "area",
    "issue_category",
    "frequency",
    "severity",
    "feedback"
]

AREAS = [
    "Area A",
    "Area B",
    "Area C",
    "Other"
]

ISSUES = [
    "Water Supply",
    "Road Maintenance",
    "Waste Collection",
    "Public Transport",
    "Street Lighting",
    "Other"
]


# --------------------------------------------------
# DATA MANAGEMENT
# --------------------------------------------------

def load_responses():
    """Load JanPulse responses from CSV storage."""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=COLUMNS)

    try:
        df = pd.read_csv(DATA_FILE)

        # Avoid crashing if an older dataset has different columns.
        for column in COLUMNS:
            if column not in df.columns:
                df[column] = None

        return df[COLUMNS]

    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=COLUMNS)


def save_response(response):
    """Validate and append a response to the dataset."""
    os.makedirs(DATA_DIR, exist_ok=True)

    df = load_responses()
    new_response = pd.DataFrame([response], columns=COLUMNS)

    updated = pd.concat(
        [df, new_response],
        ignore_index=True
    )

    updated.to_csv(DATA_FILE, index=False)


def get_issue_summary(df):
    """Summarize issue categories using collected responses."""
    if df.empty:
        return []

    counts = df["issue_category"].value_counts()

    return [
        f"{issue}: {count} response(s)"
        for issue, count in counts.items()
    ]


# --------------------------------------------------
# SIDEBAR AND NAVIGATION
# --------------------------------------------------

st.sidebar.title("📍 JanPulse")
st.sidebar.caption("Survey & Ground Insights Platform")

st.sidebar.write(
    "Collect feedback. Understand reported issues. "
    "Support evidence-based decisions."
)

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Create Survey",
        "Ground Insights",
        "Research Summary",
        "Download Data"
    ]
)

st.sidebar.divider()
st.sidebar.caption(
    "Demo environment | Use synthetic or consented responses."
)


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "Overview":

    st.title("JanPulse")
    st.subheader("Understand issues through structured feedback")

    st.write(
        "JanPulse is a prototype survey and research analytics "
        "platform designed to collect feedback about public services "
        "and organize responses into useful insights."
    )

    df = load_responses()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Responses", len(df))

    with col2:
        categories = (
            df["issue_category"].nunique()
            if not df.empty else 0
        )
        st.metric("Issue Categories", categories)

    with col3:
        areas = df["area"].nunique() if not df.empty else 0
        st.metric("Areas Represented", areas)

    st.divider()

    st.subheader("How JanPulse works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 1. Collect")
        st.write(
            "Use a structured questionnaire to collect "
            "feedback about local public services."
        )

    with col2:
        st.markdown("### 2. Analyse")
        st.write(
            "Organize responses by issue category, area, "
            "frequency, and reported severity."
        )

    with col3:
        st.markdown("### 3. Understand")
        st.write(
            "Review patterns and identify questions "
            "that require further investigation."
        )

    st.info(
        "This prototype uses self-reported feedback. "
        "Its results should not be treated as representative "
        "of the entire population without appropriate sampling."
    )


# --------------------------------------------------
# CREATE SURVEY / COLLECT RESPONSES
# --------------------------------------------------

elif page == "Create Survey":

    st.title("Public Service Feedback Survey")

    st.write(
        "Help document experiences with local public services. "
        "Please avoid entering names, phone numbers, or other "
        "personal identifying information in your feedback."
    )

    with st.form("janpulse_survey"):

        area = st.selectbox(
            "Which area does your feedback relate to?",
            AREAS
        )

        issue = st.selectbox(
            "Which public service is involved?",
            ISSUES
        )

        frequency = st.radio(
            "How often have you experienced this issue?",
            [
                "Rarely",
                "Sometimes",
                "Frequently",
                "Almost always"
            ]
        )

        severity = st.select_slider(
            "How serious is the issue for you?",
            options=[
                "Low",
                "Moderate",
                "High",
                "Very High"
            ],
            value="Moderate"
        )

        feedback = st.text_area(
            "Describe your experience (optional)",
            max_chars=1000,
            placeholder=(
                "Describe the issue, when it occurs, "
                "and how it affects access to the service."
            )
        )

        consent = st.checkbox(
            "I agree to submit this feedback for analysis."
        )

        submitted = st.form_submit_button(
            "Submit Response",
            type="primary"
        )

        if submitted:

            if not consent:
                st.error(
                    "Please confirm your consent before submitting."
                )

            else:
                response = {
                    "timestamp": datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    "area": area,
                    "issue_category": issue,
                    "frequency": frequency,
                    "severity": severity,
                    "feedback": feedback.strip()
                }

                save_response(response)

                st.success(
                    "Your response has been recorded successfully."
                )


# --------------------------------------------------
# GROUND INSIGHTS DASHBOARD
# --------------------------------------------------

elif page == "Ground Insights":

    st.title("Ground Insights Dashboard")

    df = load_responses()

    if df.empty:
        st.warning(
            "No responses are available yet. Submit a response "
            "or load clearly labelled synthetic demo data."
        )

    else:
        filtered = df.copy()

        col1, col2 = st.columns(2)

        with col1:
            selected_areas = st.multiselect(
                "Filter by area",
                sorted(filtered["area"].dropna().unique()),
                default=sorted(
                    filtered["area"].dropna().unique()
                )
            )

        with col2:
            selected_issues = st.multiselect(
                "Filter by issue",
                sorted(
                    filtered["issue_category"]
                    .dropna().unique()
                ),
                default=sorted(
                    filtered["issue_category"]
                    .dropna().unique()
                )
            )

        filtered = filtered[
            filtered["area"].isin(selected_areas)
            & filtered["issue_category"].isin(selected_issues)
        ]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Filtered Responses", len(filtered))

        with col2:
            if not filtered.empty:
                frequent = filtered["frequency"].isin(
                    ["Frequently", "Almost always"]
                ).sum()

                frequent_pct = (
                    frequent / len(filtered) * 100
                )

                st.metric(
                    "Frequent Issue Reports",
                    f"{frequent_pct:.1f}%"
                )
            else:
                st.metric("Frequent Issue Reports", "N/A")

        with col3:
            if not filtered.empty:
                high_severity = filtered["severity"].isin(
                    ["High", "Very High"]
                ).sum()

                severity_pct = (
                    high_severity / len(filtered) * 100
                )

                st.metric(
                    "High-Severity Reports",
                    f"{severity_pct:.1f}%"
                )
            else:
                st.metric("High-Severity Reports", "N/A")

        st.caption(
            "Percentages describe submitted responses only, "
            "not the proportion of the area's population."
        )

        if not filtered.empty:

            col1, col2 = st.columns(2)

            with col1:
                issue_counts = (
                    filtered["issue_category"]
                    .value_counts()
                    .rename_axis("Issue")
                    .reset_index(name="Responses")
                )

                fig = px.bar(
                    issue_counts,
                    x="Issue",
                    y="Responses",
                    title="Reported Issues by Category"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with col2:
                area_counts = (
                    filtered["area"]
                    .value_counts()
                    .rename_axis("Area")
                    .reset_index(name="Responses")
                )

                fig = px.bar(
                    area_counts,
                    x="Area",
                    y="Responses",
                    title="Responses by Area"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            severity_counts = (
                filtered["severity"]
                .value_counts()
                .rename_axis("Severity")
                .reset_index(name="Responses")
            )

            fig = px.bar(
                severity_counts,
                x="Severity",
                y="Responses",
                title="Reported Severity Distribution",
                category_orders={
                    "Severity": [
                        "Low",
                        "Moderate",
                        "High",
                        "Very High"
                    ]
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("Response Records")

            st.dataframe(
                filtered,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No responses match the selected filters.")


# --------------------------------------------------
# RESEARCH SUMMARY
# --------------------------------------------------

elif page == "Research Summary":

    st.title("Research Summary")

    df = load_responses()

    if df.empty:
        st.warning(
            "No responses are available to summarize."
        )

    else:
        st.write(
            "This section generates basic descriptive summaries "
            "from the responses currently stored in JanPulse."
        )

        st.metric("Responses Analysed", len(df))

        st.subheader("Frequently Reported Categories")

        for item in get_issue_summary(df):
            st.write(f"- {item}")

        st.subheader("Commonly Reported Issues")

        frequent = df[
            df["frequency"].isin(
                ["Frequently", "Almost always"]
            )
        ]

        if frequent.empty:
            st.write(
                "No responses currently report frequent "
                "or almost-always occurrences."
            )
        else:
            counts = frequent["issue_category"].value_counts()

            for issue, count in counts.items():
                st.write(f"- {issue}: {count} response(s)")

        st.subheader("Research Limitations")

        st.write(
            "- Results reflect submitted responses only.\n"
            "- The sample may not represent the wider population.\n"
            "- Reported experiences are not independently verified.\n"
            "- More data and further investigation may be needed "
            "before drawing conclusions."
        )


# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

elif page == "Download Data":

    st.title("Export Research Data")

    df = load_responses()

    if df.empty:
        st.warning(
            "No response data is currently available for export."
        )

    else:
        st.write(
            "Review the stored responses before downloading."
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Responses as CSV",
            data=csv_data,
            file_name="janpulse_responses.csv",
            mime="text/csv"
        )

        st.caption(
            "Handle exported feedback responsibly and remove "
            "personal information before sharing datasets."
        )
