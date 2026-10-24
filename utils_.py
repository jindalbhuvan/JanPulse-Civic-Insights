import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import os

def calculate_csat(df):
    """
    Calculate Customer Satisfaction Score
    """
    satisfied_responses = len(df[df['score'] >= 4])
    total_responses = len(df)
    
    csat_score = (satisfied_responses / total_responses) * 100
    return round(csat_score, 2)

def categorize_csat_segment(score):
    """
    Categorize CSat score into segments
    """
    if score <= 2:
        return 'Unsatisfied'
    elif score <= 3:
        return 'Neutral'
    else:
        return 'Satisfied'

def get_csat_insights(csat_score):
    """
    Provide business insights based on CSat score
    """
    insights = {
        'critical': {
            'score_range': 'Below 60%',
            'interpretation': 'Severe Customer Satisfaction Issues',
            'recommendations': [
                'Conduct comprehensive customer experience audit',
                'Implement immediate service improvement plan',
                'Create cross-functional task force to address customer pain points',
                'Develop comprehensive customer feedback mechanism'
            ]
        },
        'poor': {
            'score_range': '60-70%',
            'interpretation': 'Significant Improvement Needed',
            'recommendations': [
                'Identify key areas of customer dissatisfaction',
                'Develop targeted service improvement strategies',
                'Enhance staff training and customer service protocols',
                'Implement regular customer feedback surveys'
            ]
        },
        'average': {
            'score_range': '70-80%',
            'interpretation': 'Moderate Customer Satisfaction',
            'recommendations': [
                'Continue current service improvement efforts',
                'Conduct deep-dive analysis of customer feedback',
                'Develop incremental improvement strategies',
                'Create customer experience enhancement program'
            ]
        },
        'good': {
            'score_range': '80-90%',
            'interpretation': 'Strong Customer Satisfaction',
            'recommendations': [
                'Maintain current service quality',
                'Develop loyalty and retention programs',
                'Implement proactive customer engagement strategies',
                'Create customer success stories and testimonials'
            ]
        },
        'excellent': {
            'score_range': '90-100%',
            'interpretation': 'Exceptional Customer Satisfaction',
            'recommendations': [
                'Document and replicate successful practices',
                'Develop advanced customer experience strategies',
                'Create industry-leading customer service benchmarks',
                'Use satisfied customers as brand advocates'
            ]
        }
    }
    
    if csat_score < 60:
        return insights['critical']
    elif csat_score < 70:
        return insights['poor']
    elif csat_score < 80:
        return insights['average']
    elif csat_score < 90:
        return insights['good']
    else:
        return insights['excellent']

def create_csat_visualizations(df):
    """
    Create CSat visualizations
    """
    # Segment Distribution Pie Chart
    segment_counts = df['segment'].value_counts()
    pie_chart = px.pie(
        values=segment_counts.values, 
        names=segment_counts.index, 
        title='Customer Satisfaction Segment Distribution',
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
    
    # Score Distribution Histogram
    hist_chart = px.histogram(
        df, 
        x='score', 
        title='Satisfaction Score Distribution',
        labels={'score': 'CSat Score', 'count': 'Number of Responses'},
        color_discrete_sequence=['#45B7D1']
    )
    
    return pie_chart, hist_chart

def save_survey_response(name, email, score, feedback, service_area):
    """
    Save survey response to CSV
    """
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir, 'csat_responses.csv')
    
    # Check if file exists, if not create with headers
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=['name', 'email', 'score', 'feedback', 'service_area', 'segment', 'timestamp'])
        df.to_csv(file_path, index=False)
    
    # Read existing data
    df = pd.read_csv(file_path)
    
    # Add new response
    new_response = pd.DataFrame([{
        'name': name,
        'email': email,
        'score': score,
        'feedback': feedback,
        'service_area': service_area,
        'segment': categorize_csat_segment(score),
        'timestamp': pd.Timestamp.now()
    }])
    
    # Append and save
    df = pd.concat([df, new_response], ignore_index=True)
    df.to_csv(file_path, index=False)
    
    return df