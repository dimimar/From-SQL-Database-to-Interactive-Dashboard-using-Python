#!/usr/bin/env python
# coding: utf-8

# In[12]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px  # interactive charts
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# For Notebooks
init_notebook_mode(connected=True)
import cufflinks as cf
# For offline use
cf.go_offline()
#Load the files created from the other notebook of sql data
df_merge3=pd.read_csv('Revenuetable.tsv',sep='\t')
df_merge2=pd.read_csv('Opportunitiestable.tsv', sep='\t')
#Set the main title of the page, the page name and use an icon of your preference
st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📈",
    layout="wide",
)
st.title("Data Analytics Dashboard of Opportunities and Revenue")
# Creat sidebar mutliselection for Industry, Product Category and Stage
st.sidebar.header("Please Filter Here for Opportunity Values:")
stage = st.sidebar.multiselect(
    "Select the Opportunity Stage:",
    options=df_merge2["Opportunity_Stage"].unique(),
    default=df_merge2["Opportunity_Stage"].unique()
)

industry = st.sidebar.multiselect(
    "Select Industry:",
    options=df_merge2["Industry"].unique(),
    default=df_merge2["Industry"].unique(),
)

Product_Category = st.sidebar.multiselect(
    "Select Product Category:",
    options=df_merge2["Product_Category"].unique(),
    default=df_merge2["Product_Category"].unique()
)

df_selection = df_merge2.query(
    "Opportunity_Stage == @stage & Industry ==@industry & Product_Category == @Product_Category"
)

#Use pivot_table method to aggregate our data
grouped1=df_selection.pivot_table(index=["Account_Segment"],columns=None,values='Est_Opportunity_Value', aggfunc='sum').sort_values(by=["Est_Opportunity_Value"],ascending = False)
grouped2=df_selection.pivot_table(index=["Sector"],columns=None,values='Est_Opportunity_Value', aggfunc='sum').sort_values(by=["Est_Opportunity_Value"],ascending = False)
grouped3=df_selection.pivot_table(index=["Segment_Manager"],columns=None,values='Est_Opportunity_Value', aggfunc='sum').sort_values(by=["Est_Opportunity_Value"],ascending = False).head(10)
grouped4=df_selection.pivot_table(index=["Industry_Manager"],columns=None,values='Est_Opportunity_Value', aggfunc='sum').sort_values(by=["Est_Opportunity_Value"],ascending = False).head(10)
fig1 = grouped1.iplot(asFigure=True, kind='bar',color='red',xTitle="Account Segment",
                    yTitle="Opportunity", title="Opportunity by Account Segment")
fig2 = grouped2.iplot(asFigure=True, kind='bar',color='red',xTitle="Sector",
                    yTitle="Opportunity", title="Opportunity by Sector")
fig5 = grouped3.iplot(asFigure=True, kind='bar',color='red',xTitle="Segment Manager",
                    yTitle="Opportunity", title="Opportunity by Seg Manager",orientation='h')
fig6 = grouped4.iplot(asFigure=True, kind='bar',color='red',xTitle="Industry Manager",
                    yTitle="Opportunity", title="Opportunity by Industry Manager",orientation='h')
fig3=df_merge3.sort_values(by=["Fiscal_Quarter"],ascending = True).pivot_table(index=["Fiscal_Quarter"],columns=None,values='Revenue', aggfunc='sum').iplot(asFigure=True,color='red',xTitle="Fiscal Quarter",
                    yTitle="Revenue", title="Revenue by Fiscal Quarter")
fig4=df_merge3.pivot_table(index=["Year_No","Month_Name","Month_No"],columns=None,values='Revenue', aggfunc='sum').sort_values(by=["Year_No","Month_No"],ascending = [True,True]).iplot(asFigure=True,color='red',xTitle="Fiscal_Month",
                    yTitle="Revenue", title="Revenue by Fiscal Month")

#Use a subheader
st.subheader("Opportunity Values Breakdown 📊")
#place our barcharts side by side and create the charts based on grouped dataframes created before
col1, col2 = st.columns(2)
with col1:
    chart1=st.plotly_chart(fig1)
with col2:
    chart2=st.plotly_chart(fig2)
col1, col2 = st.columns(2)
with col1:
    chart1=st.plotly_chart(fig5)
with col2:
    chart2=st.plotly_chart(fig6)
#Use a subheader
st.subheader("Revenue Breakdown 📊")
#place our barcharts side by side and create the charts based on grouped dataframes created before
col1, col2 = st.columns(2)
with col1:
    chart1=st.plotly_chart(fig3)
with col2:
    chart2=st.plotly_chart(fig4)
#Save your code in a file.py form
#Finally use: streamlit run file.py on your terminal to make the dashboard appear.

