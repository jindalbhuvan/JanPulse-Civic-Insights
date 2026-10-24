import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import os

from utils_ import (
    calculate_csat, 
    get_csat_insights, 
    create_csat_visualizations,
    save_survey_response
)

def main():
    st.set_page_config(
        page_title="Customer Satisfaction Survey", 
        page_icon="🌟", 
        layout="wide"
    )

    # Sidebar Navigation
    st.sidebar.title("Customer Satisfaction Dashboard")
    app_mode = st.sidebar.radio(
        "Navigate", 
        ["Survey", "CSat Analysis", "Insights", "Download Data"]
    )

    # Survey Page
    if app_mode == "Survey":
        st.title("Customer Satisfaction Survey")
        
        with st.form("csat_survey"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            
            # Service Area Selection
            service_areas = [
                "Customer Support", 
                "Product Quality", 
                "Delivery", 
                "Sales Process", 
                "Website/App Experience", 
                "Other"
            ]
            service_area = st.selectbox("Service Area", service_areas)
            
            st.write("How would you rate your overall satisfaction?")
            score = st.slider(
                "Satisfaction Score (1 = Very Unsatisfied, 5 = Very Satisfied)", 
                1, 5, 3
            )
            
            feedback = st.text_area("Additional Feedback (Optional)")
            
            submit_button = st.form_submit_button("Submit Survey")
            
            if submit_button:
                if name and email:
                    # Save survey response
                    df = save_survey_response(name, email, score, feedback, service_area)
                    
                    st.success("Thank you for your feedback!")
                    st.balloons()
                else:
                    st.error("Please provide your name and email.")

    # CSat Analysis Page
    elif app_mode == "CSat Analysis":
        st.title("Customer Satisfaction Analysis")
        
        # Check if data exists
        data_file = 'data/csat_responses.csv'
        if os.path.exists(data_file):
            df = pd.read_csv(data_file)
            
            # Calculate overall CSat
            csat_score = calculate_csat(df)
            st.metric("Customer Satisfaction Score", f"{csat_score}%")
            
            # Service Area Analysis
            st.subheader("Satisfaction by Service Area")
            service_area_sat = df.groupby('service_area')['score'].mean().sort_values(ascending=False)
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                pie_chart, _ = create_csat_visualizations(df)
                st.plotly_chart(pie_chart)
            
            with col2:
                _, hist_chart = create_csat_visualizations(df)
                st.plotly_chart(hist_chart)
            
            # Service Area Bar Chart
            service_area_chart = px.bar(
                x=service_area_sat.index, 
                y=service_area_sat.values, 
                title='Average Satisfaction by Service Area',
                labels={'x': 'Service Area', 'y': 'Average Satisfaction Score'}
            )
            st.plotly_chart(service_area_chart)
        else:
            st.warning("No survey data available. Please submit a survey first.")

    # Insights Page
    elif app_mode == "Insights":
        st.title("Customer Satisfaction Insights")
        
        # Check if data exists
        data_file = 'data/csat_responses.csv'
        if os.path.exists(data_file):
            df = pd.read_csv(data_file)
            csat_score = calculate_csat(df)
            
            insights = get_csat_insights(csat_score)
            
            st.subheader(f"CSat Score: {csat_score}%")
            st.subheader(f"Interpretation: {insights['interpretation']}")
            
            st.write("### Recommendations:")
            for rec in insights['recommendations']:
                st.write(f"- {rec}")
        else:
            st.warning("No survey data available. Please submit a survey first.")

    # Download Data Page
    elif app_mode == "Download Data":
        st.title("Download Customer Satisfaction Data")
        
        # Check if data exists
        data_file = 'data/csat_responses.csv'
        if os.path.exists(data_file):
            df = pd.read_csv(data_file)
            
            st.dataframe(df)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSat Survey Data as CSV",
                data=csv,
                file_name="customer_satisfaction_responses.csv",
                mime="text/csv"
            )
        else:
            st.warning("No survey data available. Please submit a survey first.")

if __name__ == "__main__":
    main()