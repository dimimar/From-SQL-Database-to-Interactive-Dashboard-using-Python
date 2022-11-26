#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
import sqlalchemy as sql
import pyodbc
#Use some dummy SQL data for our example
server = 'SERVER NAME'
driver = 'DRIVER NAME'
db = 'DATABSE NAME'
myQuery = '''SELECT * FROM [dbo].[yt_Opportunities_Data ]'''
#Establish connection with SQL
connection = sql.create_engine('mssql+pyodbc://{}/{}?driver={}'.format(server, db, driver))
#Create pandas dataframes from different SQl queries
Opportunities = pd.read_sql_query('''SELECT * FROM [dbo].[yt_Opportunities_Data ]''', connection)
Account = pd.read_sql_query('''SELECT * FROM [dbo].[yt_account_lookup ]''', connection)
Calendar = pd.read_sql_query('''SELECT * FROM [dbo].[yt_Calendar]''', connection)
Revenue=pd.read_sql_query('''SELECT * FROM [dbo].[Revenue Raw Data ]''', connection)


# In[23]:


Opportunities.info()


# In[25]:


Opportunities=Opportunities.dropna()
Opportunities.info()


# In[26]:


Account.info()


# In[27]:


Revenue.info()


# In[28]:


Calendar.info()


# In[29]:


#JOIN Opportunities table with Account table
df_merge1 = pd.merge(Opportunities,Account,on='New_Account_No', how='left')


# In[30]:


#Group by month id to make this column unique
Revenue2=pd.pivot_table(Revenue,index=['Month_ID'],aggfunc=sum).drop(columns=['Account_No'])
Revenue2.duplicated().sum()


# In[31]:


#Keep only Months, Quarters and Years in order to JOIN it with Revenue dataframe that includes only Month_ID
Calendar2=Calendar.drop(columns=['Date','Day_Name','Day_No','Week_ID','Week_No','Week_Date'])
#Keep only unique values of month to use is as a map table
Calendar2=Calendar2.drop_duplicates(subset=['Month_ID'])
Calendar2['Month_ID'].duplicated().sum()
#Bring all Calendar info to Opportunities&Account table (df_merge1)
df_merge2=pd.merge(df_merge1,Calendar2,left_on='Est_Completion_Month_ID',right_on='Month_ID', how='left').drop(columns=['Month_ID'])
df_merge2


# In[32]:


df_merge2['New_Opportunity_Name'].value_counts()


# In[33]:


#Bring all Calendar info to Revenue table in order to analyze Revenue by different time periods
df_merge3=pd.merge(Revenue2,Calendar2,on='Month_ID', how='left')
df_merge3


# In[34]:


#Save dataframes to csv files in order to use it in another notebook ("Streamlit Dashboard based on SQL data") to create dashboard in streamlit
df_merge2.to_csv('Opportunitiestable.tsv', sep='\t')
df_merge3.to_csv('Revenuetable.tsv',sep='\t')

