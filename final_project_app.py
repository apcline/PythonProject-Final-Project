#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 19:07:59 2023

@author: alexis
"""

# libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import requests


# reading the data
@st.cache
def load_data():
    """
    Loading the HR Attrition data from a CSV into a dataframe.
    
    The data is to see the attrition but also contains other employee
    informtation.
    
    Returns
    -------
    hr_data : TYPE
        DESCRIPTION.

    """
    hr_data = pd.read_csv(
        '/Users/alexis/Documents/TBS-M2/U3-Programming/Python/03-advanced'
        '/final_project/HR Employee Attrition.csv')
    return hr_data


# creating a bar chart for attrition analysis
def create_bar_chart(hr_data):
    """
    Creates and displays a bar chart for attrition analysis.
    
    """
    fig = px.bar(
        hr_data,
        x='Attrition',
        title='Attrition Analysis'
    )
    st.plotly_chart(fig)


# function to display employee data
def show_employee_data(hr_data):
    """
    A funtion to display essential employee data and attrition analysis by
    creating a bar chart of attrition analysis.

    """
    st.subheader("Employee Data")
    st.write(hr_data.head())

    # attrition distribution
    attrition_counts = hr_data['Attrition'].value_counts()
    st.write("Attrition Distribution:")
    st.write(attrition_counts)

    # bar chart for attrition analysis
    create_bar_chart(attrition_counts)


# function to interact via API
def interact_with_model(text_input):
    """
    A function to interact with a model API to get text sentiment.

    This function makes an API request with the given text_input and returns
    the text sentiment.
    
    If there's an error contacting the API, an error message is returned.

    :param text_input: The input text for sentiment analysis.
    :return: The text sentiment or an error message.
    """
    print(f"Making API request with text: {text_input}")
    try:
        # adding a timeout parameter to the request
        response = requests.get \
        (f"http://127.0.0.1:8080/predict?text={text_input}", timeout=5)
        if response.status_code == 200:
            text_sentiment = response.json().get('polarity')
            return text_sentiment
    except requests.exceptions.RequestException as error:
        # for exceptions such as connection timeouts or request errors.
        print(f"Error while contacting the model API: {error}")

    # error (contact with the API failed)
    return "Error while contacting the model API..."


def main():
    """
    The main function for HR Employee Attrition Analysis.
    
    This function serves as the entry point for the HR Employee Attrition
    Analysis app. 
    
    This app displays a title, reads HR employee attrition data, and creates a
    menu in the sidebar for users to choose from differnt analysis options.

    """
    # title
    st.title("HR Employee Attrition Analysis")

    # reading the HR employee attrition data
    hr_data_employees = load_data()

    # create sidebar
    with st.sidebar:
        st.header("Menu")
        menu_selected = st.sidebar.selectbox(
            "Choose a menu", [
                "Show Employee Data", "Attrition Analysis",
                "Sentiment Analysis"])

        department_filter = None

    if menu_selected == 'Show Employee Data':
        show_employee_data(hr_data_employees)

    if menu_selected == 'Attrition Analysis':
        st.subheader("Attrition Analysis")

        # create a dropdown menu for department selection
        department_options = ['All'] + \
            hr_data_employees['Department'].unique().tolist()
        department_filter = st.selectbox(
            "Select Department", department_options)

        if department_filter == 'All':
            st.write("Attrition Analysis for All Departments")
            # show the chart for all departments
            create_bar_chart(hr_data_employees)
        else:
            filtered_hr_data = hr_data_employees[hr_data_employees \
                                                 ['Department']
                                                 == department_filter]
            st.write(f"Attrition Analysis for: {department_filter}")

            # show the chart for the selected department
            create_bar_chart(filtered_hr_data)

    elif menu_selected == 'Sentiment Analysis':
        st.subheader("Sentiment Analysis")
        st.write("Employee Feedback Analysis: This sentiment analysis can be \
                 used to analyze employee feedback from surveys, reviews, or \
                 comments to gauge employee sentiment and identify potential \
                 issues or areas for improvement.")
        text_input = st.text_area("Enter your text:")
        if st.button("Analyze Sentiment"):
            sentiment = interact_with_model(text_input)
            if sentiment:
                st.write(f"The sentiment is: {sentiment}")

if __name__ == "__main__":
    main()
