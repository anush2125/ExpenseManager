from abc import ABC

import streamlit as st
from datetime import datetime
import requests
import pandas as pd

from AnalyticsUi import AnalyticsUi
import altair as alt

API_URL = 'http://localhost:8000'

class AnalyticsUiMonthWise(AnalyticsUi, ABC):

    def format_response_to_df(self,response):
        output_dict = {'MonthWise': [], 'Total' : [], 'Percentage' : []}
        print(response)
        for k, v in response.items():
            if k not in output_dict:
                output_dict["MonthWise"].append(k)
                output_dict['Total'].append(v['total_month_wise'])
                output_dict['Percentage'].append(v['percentage_month'])
                #print(v)
        return output_dict

    def analytics_tab(self):
        if st.button('Get Analytics Month wise'):
            response = requests.get(f'{API_URL}/analytics/month')
            # st.write(response.json())
            df = pd.DataFrame(self.format_response_to_df(response.json()))
            df_sorted = df.sort_values(by='Percentage', ascending=False)
            #st.bar_chart(data=df_sorted.set_index('MonthWise')['Percentage'])
            # Generate the chart
            chart = self.create_conditional_bar_chart(df_sorted, category_col="MonthWise", value_col="Percentage")

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
