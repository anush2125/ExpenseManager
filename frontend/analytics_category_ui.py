import streamlit as st
from datetime import datetime
import requests
import pandas as pd
from AnalyticsUi import AnalyticsUi
from abc import ABC
import altair as alt

API_URL = 'http://localhost:8000'
class AnalyticsUiCategoryWise(AnalyticsUi, ABC):
    def format_response_to_df(self, response):
        output_dict = {'Category': [], 'Total' : [], 'Percentage' : []}
        for k, v in response.items():
            if k not in output_dict:
                output_dict["Category"].append(k)
                output_dict['Total'].append(v['total'])
                output_dict['Percentage'].append(v['percentage'])
        return output_dict

    def analytics_tab(self):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input('Start Date', datetime(2024,8, 1))
        with col2:
            end_date = st.date_input('End Date', datetime(2024, 8, 7))
        if st.button('Get Analytics'):
            payload = {
                'start_date' : start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
            response = requests.post(f'{API_URL}/analytics', json=payload)
            #st.write(response.json())
            df = pd.DataFrame(self.format_response_to_df(response.json()))
            df_sorted = df.sort_values(by='Percentage', ascending=False)
            #st.bar_chart(data=df_sorted.set_index('Category')['Percentage'])
            chart = self.create_conditional_bar_chart(df_sorted, category_col="Category", value_col="Percentage")

            # Display the chart in Streamlit
            st.altair_chart(chart, use_container_width=True)
            st.table(df_sorted)

    def create_conditional_bar_chart(self,df, category_col, value_col):
        """
        Creates a bar chart with conditional colors based on value ranges.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the data.
            category_col (str): The column name for the x-axis (categories).
            value_col (str): The column name for the y-axis (values).

        Returns:
            alt.Chart: The Altair bar chart object.
        """

        # Add a color column based on the condition
        def assign_color(value):
            if value <= 10:
                return "green"
            elif value <= 30:
                return "yellow"
            else:
                return "red"

        df["Color"] = df[value_col].apply(assign_color)

        # Create the Altair chart
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f"{category_col}:O", title=category_col),
            y=alt.Y(f"{value_col}:Q", title=value_col),
            color=alt.Color("Color:N", scale=None),  # Use the color column for conditional coloring
            tooltip=[category_col, value_col]  # Add tooltips for better interactivity
        ).properties(
            width=600,
            height=400,
            title="Conditional Bar Chart"
        )

        return chart
