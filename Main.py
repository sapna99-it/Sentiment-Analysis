import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Sentiment Analysis System",page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQFbvzaEfqPd55moVz6zwLzUViHxuDrZuOynQ&s")
st.title("SENTIMENT ANALYSIS SYSTEM")
choice=st.sidebar.selectbox("MY HOME",("HOME","ANALYSIS","RESULTS"))
if(choice=="HOME"):
    st.image("https://miro.medium.com/v2/1*_JW1JaMpK_fVGld8pd1_JQ.gif")
    st.write("1.It is a Natural Language Processing Application(It is a field of AI that enables computers to understand, interpret, and generate human language) which can analyse the sentiment on text data")
    st.write("2.This Application predict the sentiment into 3 categories Positive, Negative and Neutral.")
    st.write("3.This Application then visualize the result based on different different factor such as age,gender,language,city etc.")
elif(choice=="ANALYSIS"):
    sid=st.text_input("Enter your Google Sheet ID")
    r=st.text_input("Enter Range Between first column and last columns")
    c=st.text_input("Enter column name that is to be analyzed")
    btn=st.button("Analyze")
    if btn:
        if 'cred' not in st.session_state:
            f=InstalledAppFlow.from_client_secrets_file("key.json",["https://www.googleapis.com/auth/spreadsheets"])
            st.session_state['cred']=f.run_local_server(port=0)
        mymodel=SentimentIntensityAnalyzer()
        service=build("Sheets","v4",credentials=st.session_state['cred']).spreadsheets().values()
        k=service.get(spreadsheetId=sid,range=r).execute()
        d=k['values']
        df=pd.DataFrame(data=d[1:],columns=d[0])
        l=[]
        for i in range(0,len(df)):
            t=df._get_value(i,c)
            pred=mymodel.polarity_scores(t)
            if(pred['compound']>0.5):
                l.append("Positive")
            elif(pred['compound']<-0.5):
                l.append("Negative")
            else:
                l.append("Neutral")
        df['Sentiment']=l
        df.to_csv("result.csv",index=False)
        st.success("The Anaysis Result Are Saved By The Name Of A result.csv File Successfully")
elif(choice=="RESULTS"):
    df=pd.read_csv("result.csv")
    choice2=st.selectbox("Choose Visualization",("NONE","PIE CHART","HISTOGRAM","SCATTER PLOT"))
    st.dataframe(df)
    if(choice2=="PIE CHART"):
        posper=(len(df[df['Sentiment']=='Positive'])/len(df))*100
        negper=(len(df[df['Sentiment']=='Negative'])/len(df))*100
        neuper=(len(df[df['Sentiment']=='Neutral'])/len(df))*100
        fig=px.pie(values=[posper,negper,neuper],names=['Positive','Negative','Neutral'])
        st.plotly_chart(fig)
    elif(choice2=="HISTOGRAM"):
        k=st.selectbox("Choose Column",df.columns)
        if k:
            fig=px.histogram(x=df[k],color=df['Sentiment'])
            st.plotly_chart(fig)
    elif(choice2=="SCATTER PLOT"):
        k=st.text_input("Enter the Continous column name")
        if k:
            fig=px.scatter(x=df[k],y=df['Sentiment'])
            st.plotly_chart(fig)

    
