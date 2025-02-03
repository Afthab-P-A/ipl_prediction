import pandas as pd
import streamlit as st
import pickle

st.title('ipl win predictor')
model=pickle.load(open('ipl_model.sav','rb'))

citys=['Hyderabad', 'Mumbai', 'Indore', 'Kolkata', 'Bangalore','Chandigarh','Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth','Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley','Ahmedabad', 'Dharamsala', 'Ranchi', 'Delhi', 'Abu Dhabi','Sharjah', 'Cuttack', 'Pune', 'Visakhapatnam', 'Bengaluru','Mohali']
city=st.selectbox('select city',sorted(citys))

teams=['Royal Challengers Bangalore', 'Mumbai Indians', 'Kings XI Punjab',
       'Kolkata Knight Riders', 'Sunrisers Hyderabad', 'Rajasthan Royals',
       'Chennai Super Kings', 'Delhi Capitals']

team1,team2=st.columns(2)
with team1:
    batting_team=st.selectbox('first batting team',sorted(teams))
with team2:
    chasing_team=st.selectbox('chasing team',sorted(teams))

target=st.number_input('target')
run,over,wicket=st.columns(3)
with run:
    runs=st.number_input('run')
with over:
    overs=st.number_input('over',min_value=1,max_value=20,step=1)
with wicket:
    wickets=st.number_input('wicket',min_value=0,max_value=10)

if st.button('predict win percentage'):
    runs_left=target-runs
    balls_left=120-(overs*6)
    wickets_left=10-wickets
    crr=runs/overs
    rrr=runs_left/(20-overs)

    df=pd.DataFrame({'city':[city],
                  'batting_team':[batting_team],
                  'bowling_team':[chasing_team],
                  'total_runs_x':[target],
                  'balls left':[balls_left],
                  'wikets_left':[wickets_left],
                  'current run rate':[crr],
                  'recquired run rate':[rrr]})

    result=model.predict_proba(df)
    loss=round((result[0][0])*100,2)
    win=round((result[0][1])*100,2)

    st.text(f"Winning chance of {chasing_team}: {win}%")
    st.text(f"Winning chance of {batting_team}: {loss}%")
