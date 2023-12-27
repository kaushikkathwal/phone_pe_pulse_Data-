#Importing required Libraries.


import json
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from PIL import Image
from streamlit_player import st_player

# Create Dataframe From SQl Database
# SQL Connection

mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        password = "12345",
                        database = "phonepe_data",
                        port = "5432"
                        )
cursor = mydb.cursor() 

# Create Dataframe From SQl Database

# Aggregated Transaction
cursor.execute("select* from aggregate_transaction;")
mydb.commit()
table1=cursor.fetchall()
Aggre_trans=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

# Aggregated User

cursor.execute("select * from aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map Transaction

cursor.execute("select * from map_transaction")
mydb.commit()
table3 = cursor.fetchall()
Map_trans = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))


#Map user

cursor.execute("select * from map_user")
mydb.commit()
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top Transaction

cursor.execute("select * from top_transaction")
mydb.commit()
table5 = cursor.fetchall()
Top_trans = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top User

cursor.execute("select * from top_user")
mydb.commit()
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

#Plotting Map of India includes details about the transaction amount in that particular state .

def animate_all_amount():

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 = json.loads(response.content)
    state_names_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    state_names_tra.sort()

    df_state_names_tra = pd.DataFrame({"States":state_names_tra})

    frames = []

    for year in Map_user["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():

            aggregate_transaction = Aggre_trans[(Aggre_trans["Years"]==year)&(Aggre_trans["Quarter"]==quarter)]
            aggregate_frame = aggregate_transaction[["States","Transaction_amount"]]
            aggregate_frame = aggregate_frame.sort_values(by="States")
            aggregate_frame["Years"]=year
            aggregate_frame["Quarter"]=quarter
            frames.append(aggregate_frame)

    merged_df = pd.concat(frames)

    fig_tra = px.choropleth_mapbox(merged_df, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_amount",
                            color_continuous_scale= "Purples", range_color= (0,3000000000), hover_name= "States", title = "TRANSACTION AMOUNT",
                            animation_frame="Years", animation_group="Quarter",mapbox_style="carto-positron",center={"lat": 24, "lon": 79},  color_continuous_midpoint=0,zoom=3.6,width=700,height=900)

    fig_tra.update_geos(fitbounds= "locations", visible =False)
    fig_tra.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_tra)

#Table of States  includes details about the transaction amount in that particular state .

def all_amount_table():



    frames = []

    for year in Map_user["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():

            aggregate_transaction = Aggre_trans[(Aggre_trans["Years"]==year)&(Aggre_trans["Quarter"]==quarter)]
            aggregate_frame = aggregate_transaction[["States","Transaction_amount"]]
            aggregate_frame = aggregate_frame.sort_values(by="States")
            aggregate_frame["Years"]=year
            aggregate_frame["Quarter"]=quarter
            frames.append(aggregate_frame)

    rged_df = pd.concat(frames)
    return st.write(rged_df)


#Visualization of Transaction Amount in The form of Bar chart.

def payment_amount():
    attype= Aggre_trans[["Transaction_type","Transaction_amount"]]
    att1= attype.groupby("Transaction_type")["Transaction_amount"].sum()
    df_att1= pd.DataFrame(att1).reset_index()
    fig_tra_pa= px.bar(df_att1,x="Transaction_type",y= "Transaction_amount",title= "TRANSACTION TYPE and TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Blues)
    
    fig_tra_pa.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_tra_pa.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_tra_pa.update_layout(hovermode="x unified")
    fig_tra_pa.update_xaxes(title_font_family="Courier New")
    fig_tra_pa.update_yaxes(title_font_family="Courier New")

    fig_tra_pa.update_layout(width= 600, height= 500)
    return st.plotly_chart(fig_tra_pa)

#Visualization of Transaction Amount in The form of Table.

def payment_amount_table():
    attype= Aggre_trans[["Transaction_type","Transaction_amount"]]
    att1= attype.groupby("Transaction_type")["Transaction_amount"].sum()
    df_att1= pd.DataFrame(att1).reset_index()
    return st.write(df_att1)
    



#plotting Map of India includes details about the transaction count in that particular state.


def animate_all_count():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tra.sort()

    df_state_names_tra= pd.DataFrame({"States":state_names_tra})

    frames= []

    for year in Aggre_trans["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():

            at1= Aggre_trans[(Aggre_trans["Years"]==year)&(Aggre_trans["Quarter"]==quarter)]
            atf1= at1[["States", "Transaction_count"]]
            atf1=atf1.sort_values(by="States")
            atf1["Years"]=year
            atf1["Quarter"]=quarter
            frames.append(atf1)

    merged_df = pd.concat(frames)



    fig_tra = px.choropleth_mapbox(merged_df, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_count",
                                color_continuous_scale= "Purples", range_color= (0,3000000000), hover_name= "States", title = "TRANSACTION COUNT",
                                animation_frame="Years", animation_group="Quarter",mapbox_style="carto-positron",center={"lat": 24, "lon": 79},  color_continuous_midpoint=0,zoom=3.6,width=700,height=900)

    fig_tra.update_geos(fitbounds= "locations", visible =False)
    fig_tra.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_tra)

#Table of states includes details about the transaction count in that particular state.


def all_count_table():
    

    frames= []

    for year in Aggre_trans["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():

            at1= Aggre_trans[(Aggre_trans["Years"]==year)&(Aggre_trans["Quarter"]==quarter)]
            atf1= at1[["States", "Transaction_count"]]
            atf1=atf1.sort_values(by="States")
            atf1["Years"]=year
            atf1["Quarter"]=quarter
            frames.append(atf1)

    merged_df = pd.concat(frames)
    return st.write(merged_df)



#Visualization of Transaction Count in The form of Bar chart .


def payment_count(): 
    Att1=Aggre_trans[["Transaction_type","Transaction_count"]]
    att1= Att1.groupby("Transaction_type")["Transaction_count"].sum()
    df_att1= pd.DataFrame(att1).reset_index()
    fig_pc= px.bar(df_att1,x="Transaction_type",y= "Transaction_count",title= "TRANSACTION TYPE and TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Blues)
    fig_pc.update_layout(width=600, height= 500)
    fig_pc.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_pc.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_pc.update_layout(hovermode="x unified")
    fig_pc.update_xaxes(title_font_family="Courier New")
    fig_pc.update_yaxes(title_font_family="Courier New")
    return st.plotly_chart(fig_pc)

#Visualization of Transaction Count in The form of Table .


def payment_count_table(): 
    Att1=Aggre_trans[["Transaction_type","Transaction_count"]]
    att1= Att1.groupby("Transaction_type")["Transaction_count"].sum()
    df_att1= pd.DataFrame(att1).reset_index()
    return st.write(df_att1)


#Visualization of Registered Users from particular districts from respective states in the form of bar chart .

def reg_all_states(state):
    mu= Map_user[["States","Districts","RegisteredUser"]]
    mu1= mu.loc[(mu["States"]==state)]
    mu2= mu1[["Districts", "RegisteredUser"]]
    mu3= mu2.groupby("Districts")["RegisteredUser"].sum()
    mu4= pd.DataFrame(mu3).reset_index()

    
    fig_mu= px.bar(mu4,x="Districts",y= "RegisteredUser",title= "DISTRICTS and REGISTERED USER",color_discrete_sequence=px.colors.sequential.Blues)

    fig_mu.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_mu.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_mu.update_layout(hovermode="x unified")
    fig_mu.update_xaxes(title_font_family="Courier New")
    fig_mu.update_yaxes(title_font_family="Courier New")
    fig_mu.update_layout(width= 1200, height= 600)
    return st.plotly_chart(fig_mu)

#Table of Registered Users from particular districts from respective states.

def reg_all_states_table(state):
    mu= Map_user[["States","Districts","RegisteredUser"]]
    mu1= mu.loc[(mu["States"]==state)]
    mu2= mu1[["Districts", "RegisteredUser"]]
    mu3= mu2.groupby("Districts")["RegisteredUser"].sum()
    mu4= pd.DataFrame(mu3).reset_index()
    return st.write(mu4)
    

#Plotting Map of India  including Transaction Amount made in a particular state in a specific year.

def transaction_amount_year(sel_year):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]['ST_NM']for feature in data1["features"]]
    state_names_tra.sort()

    year= int(sel_year)
    atay= Aggre_trans[["States","Years","Transaction_amount"]]
    atay1= atay.loc[(Aggre_trans["Years"]==year)]
    atay2= atay1.groupby("States")["Transaction_amount"].sum()
    atay3= pd.DataFrame(atay2).reset_index()

    fig_atay= px.choropleth_mapbox(atay3, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_amount",
                            color_continuous_scale= "Purples", range_color= (0,800000000000), hover_name= "States", title = "TRANSACTION AMOUNT and STATES",
                        mapbox_style="carto-positron",center={"lat": 24, "lon": 79},  color_continuous_midpoint=0,zoom=3.6,width=700,height=900)

    fig_atay.update_geos(fitbounds= "locations", visible= False)
 
    fig_atay.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_atay)

#Table  including Transaction Amount made in a particular state in a specific year.

def transaction_amount_year_table(sel_year):
    year= int(sel_year)
    atay= Aggre_trans[["States","Years","Transaction_amount"]]
    atay1= atay.loc[(Aggre_trans["Years"]==year)]
    atay2= atay1.groupby("States")["Transaction_amount"].sum()
    atay3= pd.DataFrame(atay2).reset_index()
    return st.write(atay3)

#Plotting Map of India includes details about the transaction amount in that particular state corresponding to a certain year and quarter .

def animate_amount(sel_year,sel_quarter):

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1 = json.loads(response.content)
    state_names_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    state_names_tra.sort()

    df_state_names_tra = pd.DataFrame({"States":state_names_tra})

    frames = []

    for year in Map_user["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():
            year=int(sel_year)
            quarter=int(sel_quarter)

            aggregate_transaction = Aggre_trans[(Aggre_trans["Years"]==year)&(Aggre_trans["Quarter"]==quarter)]
            aggregate_frame = aggregate_transaction[["States","Transaction_amount"]]
            aggregate_frame = aggregate_frame.sort_values(by="States")
            aggregate_frame["Years"]=year
            aggregate_frame["Quarter"]=quarter
            frames.append(aggregate_frame)

    merged_df = pd.concat(frames)

    fig_tra = px.choropleth_mapbox(merged_df, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_amount",
                            color_continuous_scale= "Purples", range_color= (0,3000000000), hover_name= "States", title = "TRANSACTION AMOUNT",
                            animation_frame="Years", animation_group="Quarter",mapbox_style="carto-positron",center={"lat": 24, "lon": 79},  color_continuous_midpoint=0,zoom=3.6,width=700,height=900)

    fig_tra.update_geos(fitbounds= "locations", visible =False)
    fig_tra.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_tra)



#Table includes details about the transaction amount in that particular state corresponding to a certain year and quarter .

def animate_amount_table(sel_year,sel_quarter):
    frames = []
    for year in Map_user["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():
            year=int(sel_year)
            quarter=int(sel_quarter)

            aggregate_transaction = Aggre_trans[(Aggre_trans["Years"]==year)&(Aggre_trans["Quarter"]==quarter)]
            aggregate_frame = aggregate_transaction[["States","Transaction_amount"]]
            aggregate_frame = aggregate_frame.sort_values(by="States")
            aggregate_frame["Years"]=year
            aggregate_frame["Quarter"]=quarter
            frames.append(aggregate_frame)

    merged_df = pd.concat(frames)
    return st.write(merged_df)


#Visualization of transaction Amount in a particular year in The form of Bar chart.


def payment_amount_year(sel_year):
    year= int(sel_year)
    apay = Aggre_trans[["Years", "Transaction_type", "Transaction_amount"]]
    apay1= apay.loc[(Aggre_trans["Years"]==year)]
    apay2= apay1.groupby("Transaction_type")["Transaction_amount"].sum()
    apay3= pd.DataFrame(apay2).reset_index()

    fig_apayc= px.bar(apay3,x= "Transaction_type", y= "Transaction_amount", title= "PAYMENT AMOUNT and PAYMENT TYPE",
            color_discrete_sequence=px.colors.sequential.Blues)
    fig_apayc.update_layout(width=600, height=500)


    fig_apayc.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_apayc.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_apayc.update_layout(hovermode="x unified")
    fig_apayc.update_xaxes(title_font_family="Courier New")
    fig_apayc.update_yaxes(title_font_family="Courier New")

  
    return st.plotly_chart(fig_apayc)

#Table of transaction Amount in a particular year .


def payment_amount_year_table(sel_year):
    year= int(sel_year)
    apay = Aggre_trans[["Years", "Transaction_type", "Transaction_amount"]]
    apay1= apay.loc[(Aggre_trans["Years"]==year)]
    apay2= apay1.groupby("Transaction_type")["Transaction_amount"].sum()
    apay3= pd.DataFrame(apay2).reset_index()
    return st.write(apay3)


#Plotting Map of India  including Transaction count made in a particular state in a specific year.

def transaction_count_year(sel_year):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1=json.loads(response.content)
    state_names_tra= [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tra.sort()

    year= int(sel_year)
    atcy= Aggre_trans[["States", "Years", "Transaction_count"]]
    atcy1= atcy.loc[(Aggre_trans["Years"]==year)]
    atcy2= atcy1.groupby("States")["Transaction_count"].sum()
    atcy3= pd.DataFrame(atcy2).reset_index()

    fig_atcy= px.choropleth_mapbox(atcy3, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_count",
                            color_continuous_scale= "Purples", range_color= (0,8000000000), hover_name= "States", title = "TRANSACTION COUNT and STATES",
                        mapbox_style="carto-positron",center={"lat": 24, "lon": 79},  color_continuous_midpoint=0,zoom=3.6,width=700,height=900)
    
    fig_atcy.update_geos(fitbounds= "locations", visible= False)

    fig_atcy.update_layout(title_font={"size":25})
    return st.plotly_chart(fig_atcy)


#Table of states  including Transaction count made in a specific year.

def transaction_count_year_table(sel_year):
    year= int(sel_year)
    atcy= Aggre_trans[["States", "Years", "Transaction_count"]]
    atcy1= atcy.loc[(Aggre_trans["Years"]==year)]
    atcy2= atcy1.groupby("States")["Transaction_count"].sum()
    atcy3= pd.DataFrame(atcy2).reset_index()
    return st.write(atcy3)

#plotting Map of India includes details about the transaction count in that particular state corresponding to a certain  year and quarter.


def animate_count(sel_year,sel_quarter):
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]["ST_NM"]for feature in data1["features"]]
    state_names_tra.sort()

    df_state_names_tra= pd.DataFrame({"States":state_names_tra})

    frames= []

    for year in Aggre_trans["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():
            year=int(sel_year)
            quarter=int(sel_quarter)
            at1= Aggre_trans[(Aggre_trans["Years"]==year)&(Aggre_trans["Quarter"]==quarter)]
            atf1= at1[["States", "Transaction_count"]]
            atf1=atf1.sort_values(by="States")
            atf1["Years"]=year
            atf1["Quarter"]=quarter
            frames.append(atf1)

    merged_df = pd.concat(frames)



    fig_tra = px.choropleth_mapbox(merged_df, geojson= data1, locations= "States", featureidkey= "properties.ST_NM", color= "Transaction_count",
                                color_continuous_scale= "Purples", range_color= (0,3000000000), hover_name= "States", title = "TRANSACTION COUNT",
                                animation_frame="Years", animation_group="Quarter",mapbox_style="carto-positron",center={"lat": 24, "lon": 79},  color_continuous_midpoint=0,zoom=3.6,width=700,height=900)

    fig_tra.update_geos(fitbounds= "locations", visible =False)
    fig_tra.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_tra)

#Table includes details about the transaction count in that particular state corresponding to a certain year and quarter .

def animate_count_table(sel_year,sel_quarter):

    frames= []

    for year in Aggre_trans["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():
            year=int(sel_year)
            quarter=int(sel_quarter)
            at1= Aggre_trans[(Aggre_trans["Years"]==year)&(Aggre_trans["Quarter"]==quarter)]
            atf1= at1[["States", "Transaction_count"]]
            atf1=atf1.sort_values(by="States")
            atf1["Years"]=year
            atf1["Quarter"]=quarter
            frames.append(atf1)

    merged_df = pd.concat(frames)
    return st.write(merged_df)




#Representation of transaction count in a particular year in The form of Bar chart .

def payment_count_year(sel_year):
    year= int(sel_year)
    apc= Aggre_trans[["Transaction_type", "Years", "Transaction_count"]]
    apc1= apc.loc[(Aggre_trans["Years"]==year)]
    apc2= apc1.groupby("Transaction_type")["Transaction_count"].sum()
    apc3= pd.DataFrame(apc2).reset_index()

    fig_apc= px.bar(apc3,x= "Transaction_type", y= "Transaction_count", title= "PAYMENT COUNT and PAYMENT TYPE",
                color_discrete_sequence=px.colors.sequential.Blues)
    fig_apc.update_layout(width=600, height=500)


    fig_apc.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_apc.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_apc.update_layout(hovermode="x unified")
    fig_apc.update_xaxes(title_font_family="Courier New")
    fig_apc.update_yaxes(title_font_family="Courier New")
    return st.plotly_chart(fig_apc)

#Table of transaction count in a particular year.

def payment_count_year_Table(sel_year):
    year= int(sel_year)
    apc= Aggre_trans[["Transaction_type", "Years", "Transaction_count"]]
    apc1= apc.loc[(Aggre_trans["Years"]==year)]
    apc2= apc1.groupby("Transaction_type")["Transaction_count"].sum()
    apc3= pd.DataFrame(apc2).reset_index()
    return st.write(apc3)


#Visualization of Registered Users in the districts of particular state in a particular year in The form of Bar chart.

def reg_state_all_RU(sel_year,state):
    year= int(sel_year)
    mus= Map_user[["States", "Years", "Districts", "RegisteredUser"]]
    mus1= mus.loc[(Map_user["States"]==state)&(Map_user["Years"]==year)]
    mus2= mus1.groupby("Districts")["RegisteredUser"].sum()
    mus3= pd.DataFrame(mus2).reset_index()

    fig_mus= px.bar(mus3, x= "Districts", y="RegisteredUser", title="DISTRICTS and REGISTERED USER",
                color_discrete_sequence=px.colors.sequential.Blues)
    fig_mus.update_layout(width= 1200, height= 500)
    fig_mus.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_mus.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_mus.update_layout(hovermode="x unified")
    fig_mus.update_xaxes(title_font_family="Courier New")
    fig_mus.update_yaxes(title_font_family="Courier New")

   
    return st.plotly_chart(fig_mus)

#Table of Registered Users in the districts of particular state in a particular year.

def reg_state_all_RU_Table(sel_year,state):
    year= int(sel_year)
    mus= Map_user[["States", "Years", "Districts", "RegisteredUser"]]
    mus1= mus.loc[(Map_user["States"]==state)&(Map_user["Years"]==year)]
    mus2= mus1.groupby("Districts")["RegisteredUser"].sum()
    mus3= pd.DataFrame(mus2).reset_index()
    return st.write(mus3)


#Visualization of Transaction Amount in the districts of particular state in a particular year in The form of Bar chart.

def reg_state_all_TA(sel_year,state):
    year= int(sel_year)
    mts= Map_trans[["States", "Years","Districts", "Transaction_amount"]]
    mts1= mts.loc[(Map_trans["States"]==state)&(Map_trans["Years"]==year)]
    mts2= mts1.groupby("Districts")["Transaction_amount"].sum()
    mts3= pd.DataFrame(mts2).reset_index()

    fig_mts= px.bar(mts3, x= "Districts", y= "Transaction_amount", title= "DISTRICT and TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Blues)
    fig_mts.update_layout(width= 600, height= 500)
    fig_mts.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_mts.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_mts.update_layout(hovermode="x unified")
    fig_mts.update_xaxes(title_font_family="Courier New")
    fig_mts.update_yaxes(title_font_family="Courier New")
    return st.plotly_chart(fig_mts)

#Table of Transaction Amount in the districts of particular state in a particular year.

def reg_state_all_TA_Table(sel_year,state):
    year= int(sel_year)
    mts= Map_trans[["States", "Years","Districts", "Transaction_amount"]]
    mts1= mts.loc[(Map_trans["States"]==state)&(Map_trans["Years"]==year)]
    mts2= mts1.groupby("Districts")["Transaction_amount"].sum()
    mts3= pd.DataFrame(mts2).reset_index()
    return st.write(mts3)
#Visualization of Transaction count in the districts of particular state in a particular year in The form of Bar chart.

def reg_state_all_TC(sel_year,state):

    year= int(sel_year)
    mts= Map_trans[["States", "Years","Districts", "Transaction_count"]]
    mts1= mts.loc[(Map_trans["States"]==state)&(Map_trans["Years"]==year)]
    mts2= mts1.groupby("Districts")["Transaction_count"].sum()
    mts3= pd.DataFrame(mts2).reset_index()

    fig_mts= px.bar(mts3, x= "Districts", y= "Transaction_count", title= "DISTRICT and TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Blues)
    fig_mts.update_layout(width= 600, height= 500)
    fig_mts.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_mts.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_mts.update_layout(hovermode="x unified")
    fig_mts.update_xaxes(title_font_family="Courier New")
    fig_mts.update_yaxes(title_font_family="Courier New")
    return st.plotly_chart(fig_mts)

#Table of Transaction count in the districts of particular state in a particular year.

def reg_state_all_TC_Table(sel_year,state):
    year= int(sel_year)
    mts= Map_trans[["States", "Years","Districts", "Transaction_count"]]
    mts1= mts.loc[(Map_trans["States"]==state)&(Map_trans["Years"]==year)]
    mts2= mts1.groupby("Districts")["Transaction_count"].sum()
    mts3= pd.DataFrame(mts2).reset_index()
    return st.write(mts3)

#Different Questions which show different details with the help of bar charts and pie charts.

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.bar(brand2, x= "Brands", y= "Transaction_count", title= "Top Mobile Brands With Maximum Number of Transaction Count",
                        color_discrete_sequence= px.colors.sequential.Bluered)

    fig_brands.update_layout(width= 1200, height= 500)
    fig_brands.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_brands.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_brands.update_layout(hovermode="x unified")
    fig_brands.update_xaxes(title_font_family="Courier New")
    fig_brands.update_yaxes(title_font_family="Courier New")

    return st.plotly_chart(fig_brands)


def ques1_table():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()
    return st.write(brand2)

def ques2():
    ht= Aggre_trans[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_hts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "TOP 10 STATES WITH HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Bluered)

    fig_hts.update_layout(width= 1200, height= 500)
    fig_hts.update_layout( yaxis = dict( tickfont = dict(size=14)))
    fig_hts.update_layout( xaxis = dict( tickfont = dict(size=13)))
    fig_hts.update_layout(hovermode="x unified")
    fig_hts.update_xaxes(title_font_family="Courier New")
    fig_hts.update_yaxes(title_font_family="Courier New")
    
    return st.plotly_chart(fig_hts)


def ques2_table():
    ht= Aggre_trans[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)
    return st.write(ht2)

def ques3():
    lt= Aggre_trans[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.pie(lt2, names= "States",values= "Transaction_amount",title= "TOP 10 STATES WITH LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)

    fig_lts.update_layout(width= 900, height= 500)
    return st.plotly_chart(fig_lts)

def ques3_table():
    lt= Aggre_trans[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)
    return st.write(lt2)

def ques4():
    htd= Map_trans[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.bar(htd2, y= "Transaction_amount", x= "Districts", title="TOP 10 DISTRICTS IN INDIA WITH HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Bluered)
    fig_htd.update_layout(width= 1200, height= 500)
        
    fig_htd.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_htd.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_htd.update_layout(hovermode="x unified")
    fig_htd.update_xaxes(title_font_family="Courier New")
    fig_htd.update_yaxes(title_font_family="Courier New")
        
    return st.plotly_chart(fig_htd)

def ques4_table():
    htd= Map_trans[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()   
    return st.write(htd2)


def ques5():
    ltd= Map_trans[["Districts", "Transaction_amount"]]
    ltd1= ltd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    ltd2= pd.DataFrame(ltd1).head(10).reset_index()

    fig_ltd= px.pie(ltd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF INDIA WITH LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    fig_ltd.update_layout(width= 900, height= 500)
    return st.plotly_chart(fig_ltd)

def ques5_table():
    ltd= Map_trans[["Districts", "Transaction_amount"]]
    ltd1= ltd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    ltd2= pd.DataFrame(ltd1).head(10).reset_index()
    return st.write(ltd2)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="TOP 10 States IN INDIA With MAXIMUM AppOpens",
                color_discrete_sequence= px.colors.sequential.Bluered)

    fig_sa.update_layout(width= 1200, height= 500)
            
    fig_sa.update_layout( yaxis = dict( tickfont = dict(size=11)))
    fig_sa.update_layout( xaxis = dict( tickfont = dict(size=9)))
    fig_sa.update_layout(hovermode="x unified")
    fig_sa.update_xaxes(title_font_family="Courier New")
    fig_sa.update_yaxes(title_font_family="Courier New")
    return st.plotly_chart(fig_sa)

def ques6_table():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)
    return st.write(sa2)


def ques7():
    la= Map_user[["States", "AppOpens"]]
    la1= la.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    la2= pd.DataFrame(la1).reset_index().head(10)

    fig_la= px.pie(la2, names= "States", values= "AppOpens", title="TOP 10 LOWEST STATES IN INDIA WITH MINIMUM AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    fig_la.update_layout(width= 900, height= 500)
    return st.plotly_chart(fig_la)

def ques7_table():
    la= Map_user[["States", "AppOpens"]]
    la1= la.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    la2= pd.DataFrame(la1).reset_index().head(10)
    return st.write(la2)

def ques8():
    htc= Aggre_trans[["States", "Transaction_count"]]
    htc1= htc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    htc2= pd.DataFrame(htc1).head(10).reset_index()

    fig_htc= px.bar(htc2, x= "States",y= "Transaction_count", title= "TOP 10 STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Bluered)

    fig_htc.update_layout(width= 1200, height= 500)
    return st.plotly_chart(fig_htc)

def ques8_table():
    htc= Aggre_trans[["States", "Transaction_count"]]
    htc1= htc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    htc2= pd.DataFrame(htc1).head(10).reset_index()
    return st.plotly_chart(htc2)


def ques9():
    ltc= Aggre_trans[["States", "Transaction_count"]]
    ltc1= ltc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    ltc2= pd.DataFrame(ltc1).head(10).reset_index()

    fig_ltc=px.pie(ltc2,values="Transaction_count",names="States",title="TOP 10 STATES WITH LOWEST TRANSACTION COUNT",color_discrete_sequence= px.colors.sequential.dense_r)
    fig_ltc.update_layout(width= 900, height= 500)
    return st.plotly_chart(fig_ltc)

def ques9_table():
    ltc= Aggre_trans[["States", "Transaction_count"]]
    ltc1= ltc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    ltc2= pd.DataFrame(ltc1).head(10).reset_index()
    return st.write(ltc2)

def ques10():
    hdtc= Map_trans[["Districts", "Transaction_count"]]
    hdtc1= hdtc.groupby("Districts")["Transaction_count"].sum().sort_values(ascending=False)
    hdtc2= pd.DataFrame(hdtc1).head(10).reset_index()

    fig_hdtc= px.bar(hdtc2, x= "Districts",y= "Transaction_count", title= "TOP 10 DISTRICTS WITH HIGHEST TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Bluered)
    fig_hdtc.update_layout(width= 1200, height= 500)
    return st.plotly_chart(fig_hdtc)

def ques10_table():
    hdtc= Map_trans[["Districts", "Transaction_count"]]
    hdtc1= hdtc.groupby("Districts")["Transaction_count"].sum().sort_values(ascending=False)
    hdtc2= pd.DataFrame(hdtc1).head(10).reset_index()
    return st.write(hdtc2)

def ques11():
    ldtc= Map_trans[["Districts", "Transaction_count"]]
    ldtc1= ldtc.groupby("Districts")["Transaction_count"].sum().sort_values(ascending=True)
    ldtc2= pd.DataFrame(ldtc1).head(10).reset_index()

    fig_ldtc=px.pie(ldtc2,values="Transaction_count",names="Districts",title="TOP 10 DISTRICTS WITH LOWEST TRANSACTION COUNT",color_discrete_sequence= px.colors.sequential.dense_r)
    fig_ldtc.update_layout(width= 900, height= 500)
    return st.plotly_chart(fig_ldtc)

def ques11_table():
    ldtc= Map_trans[["Districts", "Transaction_count"]]
    ldtc1= ldtc.groupby("Districts")["Transaction_count"].sum().sort_values(ascending=True)
    ldtc2= pd.DataFrame(ldtc1).head(10).reset_index()
    return st.write(ldtc2)

#Setup of Streamlit Application

st.set_page_config(page_title="PhonePe Pulse",layout= "wide")

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


col1,col2=st.columns(2)
with col1:
        img=Image.open("phonepe_mainbanner2.jpg")
        st.image(img,width=150)
        
with col2:
    st.markdown("<h1 style='text-align:right; color:white;'>PhonePe Pulse</h1>", unsafe_allow_html=True)

selected=option_menu(
        menu_title="Main Menu",
        options=["HOME","EXPLORE DATA","REPORTS","ADDITIONAL INFORMATION"],
        icons=["house-fill","box-fill","back","book-half"],
        menu_icon="wallet-fill",
        orientation="horizontal")


if selected=="HOME":
    col1,col2=st.columns(2)
    with col1:
        st.header(":white[**Introduction**]")
        st.markdown(":white[**PhonePe Pulse is a geospatial platform that provides insights and reports on digital payments in India. It includes data-driven analysis, trends, and insights about how India transacts**]")
        st.markdown(":white[**The Indian digital payments story has truly captured the world's imagination.From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving back to the digital payments ecosystem.**]")
        
    with col2:
        filepath=load_lottiefile("E:\data science\phonepe project\A.json")
        st.lottie(filepath,speed=1,reverse=False,loop=True,height=550,width=550,quality="highest")
        

    selected=option_menu(
        menu_title="",
        options=["About PhonePe Pulse","Explore Pulse","Conversations","Articles","Download App"],
        icons=["tablet-landscape-fill","grid-fill","distribute-horizontal","newspaper","box-arrow-in-down"],
        orientation="horizontal")
    if selected=="About PhonePe Pulse":
        st.markdown("<h1 style='text-align:center; color:white;'>About PhonePe Pulse</h1>", unsafe_allow_html=True) 
        st.markdown(":white[**The Indian digital payments story has truly captured the world's imagination.From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving back to the digital payments ecosystem.**]")
        st.markdown(":white[**The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones and data.**]")
        st.markdown(":white[**When PhonePe started 5 years back, we were constantly looking for definitive data sources on digital payments in India. Some of the questions we were seeking answers to were - How are consumers truly using digital payments? What are the top cases? Are kiranas across Tier 2 and 3 getting a facelift with the penetration of QR codes?**]")
        st.markdown(":white[**This year as we became India's largest digital payments platform with 46% UPI market share, we decided to demystify the what, why and how of digital payments in India.**]")
        st.markdown(":white[**This year, as we crossed 2000 Cr. transactions and 30 Crore registered users, we thought as India's largest digital payments platform with 46% UPI market share, we have a ring-side view of how India sends, spends, manages and grows its money. So it was time to demystify and share the what, why and how of digital payments in India.**]")
        st.markdown(":white[**PhonePe Pulse is your window to the world of how India transacts with interesting trends, deep insights and in-depth analysis based on our data put together by the PhonePe team.**]")
    if selected=="Explore Pulse":
        st.markdown("<h1 style='text-align:center; color:white;'>What Is Pulse ?</h1>", unsafe_allow_html=True)
        col3,col4= st.columns(2)
        with col3:
            
            st_player("https://youtu.be/c_1H6vivsiA")
        with col4:
            st_player("https://youtu.be/Yy03rjSUIB8")
            

    if selected =="Conversations":
        st.markdown("<h1 style='text-align:center; color:white;'>Visual stories showcasing the beat of progress</h1>", unsafe_allow_html=True)
        filepath=load_lottiefile("E:\data science\phonepe project\A4.json")
        st.lottie(filepath,speed=1,reverse=False,loop=True,height=550,width=1200,quality="highest")
        col1,col2=st.columns(2)
        with col1:
            st.subheader(":White[**1. The Evolution & Future of India's Digital Payments industry**]")
            st_player("https://youtu.be/qL2lT5AWKko")
            
        with col2:
            st.subheader(":White[**2. The Changing Landscapes of Financial Services In India**]")
            st_player("https://youtu.be/CL7A36x0zL4")
    if selected =="Articles":
        if st.button("1.Innovation leading to accelarated Growth: The Merchant Journey"):
            st.markdown(":white[**India's digital transformation is a testament to the power of innovation to propel massive economic growth. From a cash-is-king mindset to walking into a store with a smartphone and the PhonePe app, India has transitioned to making payments digitally, almost overnight. As per the PhonePe Pulse - BCG report, merchant payments are expected to increase from 20% in value today to 65% by 2026, further underscoring the role of the ubiquitous merchant in this transformation.Phasing out cash reliance with a suite of payment solutions At a hole-in-the-wall Chole Bhature shop in Delhi, across a chikankari boutique’s counter in Lucknow, or by the beach shacks in Goa, you can find the ubiquitous UPI QR code everywhere now. The scan-and- pay code, which sees transactions from ₹1 to ₹1,00,000, was the first step in the digital payments’ acceptance journey for merchants. As contactless payments found their way into the Indian psyche, merchants increasingly adopted QR codes pan-India, taking PhonePe’s presence across 99% postal codes. A diverse country comes with diverse challenges, and PhonePe has managed to cater to each and every one of them. Merchants with high Average Transaction Values (ATV) require enablement of credit card transactions (through EDCs or UPI), while for other merchants, transactions such as debit cards or UPI would suffice. To prevent identity theft, custom Photo QRs were introduced, following which SmartSpeakers were launched to validate payments in real-time. On average, PhonePe SmartSpeakers are validating over 100 crore transactions per month. By enabling merchants in more than 17,000 postal codes and successfully deploying over 4.4 million devices across India, this innovative solution is positively impacting the merchant ecosystem. The deployment of devices in remote areas highlights the growing adoption and reach of this technology in rural areas. Added to this is the recent launch of the celebrity voice feature on PhonePe SmartSpeakers that allows merchants to validate customer payments in celebrity voices such as the iconic Mr. Bachchan’s voice for Hindi. This strikes a chord with millions of Indians, enhancing its appeal to merchants and users alike. The recent introduction of PhonePe’s new POS device represents a significant milestone in PhonePe’s suite of payment solutions. This new device, based on the Android platform, brings about a transformation in the way businesses handle checkouts. Whether customers are at a store counter, a table at a restaurant, a delivery location, or anywhere with cellular coverage, this POS device streamlines the entire payment process, ultimately enhancing the overall customer experience. With this new addition, PhonePe has covered the full spectrum of payment solutions, which is a clear indication of their commitment to innovation in the payments space. Driving financial inclusion and creating access to credit Pre-pandemic, digital payments were an afterthought. Today, a bank account and a smartphone are essentials of even the smallest of businesses - bringing a significant portion of merchants into the formal economy. The shift from cash dependence to digital payments has paved the way for enhanced financial inclusivity, establishing trustworthy merchant profiles. Reaffirming the commitment to driving financial inclusion for SMEs and solving merchants’ need for organised credit, PhonePe launched a merchant lending platform on the PhonePe for Business app. This allows banks and NBFCs to provide credit opportunities to merchants in a seamless digital flow in just a matter of minutes. SMEs that previously faced challenges in accessing credit, can now invest in businesses, expand operations and contribute to the overall economic growth - helping create a healthier and empowered SME economy. Building infrastructure for growth As merchants are fully armed with innovative tools to build their businesses, solving for discoverability would have a leapfrog effect on a historically unseen scale. With this in mind, PhonePe built Stores - an engagement channel between merchants and consumers. This equipped consumers to look for mom- and-pop stores in their vicinity that catered to their specific needs. Taking a gargantuan step further, PhonePe also launched Pincode, a hyperlocal shopping app built on the ONDC platform that connects local buyers and sellers. This not only solves discoverability but provides access to inventory and takes the business to the buyer’s doorstep, maximising a merchant’s operational potential. Impact for merchants Let’s hear the story of Anitha, who has been running a bakery in Bengaluru for over three years with her sister. Digital payments have been a boon to her business in transitioning to cashless payments and receiving the right ammunition to expand her business. Anitha is one of the early adopters of all PhonePe solutions for merchants. She has been associated with the brand for over two years and says PhonePe has her complete trust and has been an invaluable part of her journey! Watch the full video here Edging closer to India’s dream of becoming a superpower Only about a decade ago we dreamed of a cashless future and here we are! Cashless transactions built on platforms such as UPI and driven by players like PhonePe encourage consumers and merchants alike to contribute to the overall economic growth. By introducing measures to bring about transparency and accountability along with minimizing costs involved in producing and distributing cash, PhonePe - an incubator of innovative solutions - is nudging India towards the dream of becoming an economic superpower.**]")
        if st.button("2.India is steadily progressing towards the vision of becoming a cashless economy"):
            st.markdown("The shift in consumer behaviour Amplified digital adoption has enhanced customer awareness and education spurring informed choices and a better understanding of financial services. On the investments side, Hemant explained how smart initiatives and simplified processes such as the UPI-based SIP have empowered customers to undertake their investment journeys without unwarranted intervention. Democratizing of information, digital mode of buying, and availability of varied investment avenues is encouraging consumers to diversify their portfolios. On the other hand, the pandemic has prioritized insurance across Life and General categories. Initiatives by Regulatory bodies facilitating financial inclusion Hemant acknowledged the massive efforts made by the governing forces to drive penetration, inclusive growth, and adoption of financial products. He shared that these endeavours have laid the foundation for financial inclusivity and will only get stronger over time. He further shed light on key initiatives undertaken by regulatory bodies - mass programs like the Ayushman Bharat Yojana, policy changes implemented by IRDAI (Insurance Regulatory and Development Authority of India) to ease the insurance acquisition process, liberalizing the insurance space for private participation, SEBI (Securities and Exchange Board of India) relaxing norms for the launch of innovative products by new asset management companies and AMFI (Association of Mutual Funds in India) playing an active role in creating awareness around informed investing. Hemant firmly believes that such measures encourage the spirit of innovation in meeting the needs of a diverse populace and will go a long way in bringing more people into the fold of financial inclusion. Differentiated approach to solving challenge Hemant opined that insurance and investments are under-penetrated categories in India in comparison to global benchmarks owing to problems of distribution, customer education, and awareness. Hemant spoke about the intensive research undertaken by PhonePe to understand customer needs that helped in crafting customized digital solutions. Underscoring a strong customer-first approach, he highlighted that PhonePe is focused on providing consumers with simple-to-understand products at affordable prices backed with features such as ready assistance, instant enrolment, and self-inspection, amongst others. PhonePe has also heavily invested in its tech architecture to ensure efficiencies of time, speed, and comfort of simplified payment flows for the end user. He also explained the importance of forging strong ties with the end-consumer through regular engagement, building long-standing trust by ensuring consistent and relevant communication, and the solutions being easily accessible across geographies. All these efforts have helped PhonePe augment reach, engagement, and adoption by people even in the hinterlands. Sharing an example of PhonePe’s efforts toward customer education and engagement, Hemant spoke about a recent marketing campaign called “No tension insurance”. The campaign is targeted to counter the complexity attached to insurance products and drive awareness that life gets easier for those who anticipate, plan, and buy insurance in time. Solutions oriented journe Hemant shared that PhonePe is committed to providing diversified solutions to encourage the investment climate in the country and drive further adoption of insurance. He also shared key milestones achieved by PhonePe in the mutual funds and insurance categories - over 1.3 million policies sold in the two-wheeler segment, the first to launch a COVID-specific insurance product and selling over 0.5 million policies, over 250% annual growth in PhonePe’s new investors and is the market leader in the digital sale of gold in India.From selling insurance, and facilitating buying gold & silver digitally, to being the first to launch the UPI-backed SIP, PhonePe’s repertoire of financial product offerings is in line with its intent to continue the dream run of adding scale and value to the digital payments ecosystem.")              
    if selected =="Download App":
            col1,col2=st.columns(2)
            with col1:
                filepath=load_lottiefile("E:\data science\phonepe project\dwnld.json")
                st.lottie(filepath,speed=1,reverse=False,loop=True,height=550,width=500,quality="highest")
            with col2:
                if st.button("DOWNLOAD THE APP NOW"):
                    st.write("https://www.phonepe.com/app-download/")
      
if selected=="EXPLORE DATA":

    sel_year = st.selectbox("select the Year",("All", "2018", "2019", "2020", "2021", "2022", "2023"))

    if sel_year == "All" :
        with  st.spinner():
            col1, col2 = st.columns(2)
            with col1:
                animate_all_amount()
                all_amount_table()
                payment_amount()
                payment_amount_table()
           
            with col2:
                animate_all_count()
                all_count_table()
                payment_count()
                payment_count_table()
               
            state=st.selectbox("select the state",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                    'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                    'Uttarakhand', 'West Bengal'))
          
            reg_all_states(state)
            reg_all_states_table(state)

    else:
        sel_quarter=st.selectbox("select the Quarter",("All","1","2","3","4"))
        col1,col2= st.columns(2)
        if sel_quarter=="All":
            with col1:
                transaction_amount_year(sel_year)
                transaction_amount_year_table(sel_year)
                payment_amount_year(sel_year)
                payment_amount_year_table(sel_year)
            with col2:
                transaction_count_year(sel_year)
                transaction_amount_year_table(sel_year)
                payment_count_year(sel_year)
                payment_amount_year_table(sel_year)


        elif sel_quarter=="1":
                with col1:
                    animate_amount(sel_year,sel_quarter)
                    animate_amount_table(sel_year,sel_quarter)
                    payment_amount_year(sel_year)
                    payment_amount_year_table(sel_year)
                with col2:
                    animate_count(sel_year,sel_quarter)
                    animate_count_table(sel_year,sel_quarter)
                    payment_count_year(sel_year)
                    payment_count_year_Table(sel_year)

        elif sel_quarter=="2":
                with col1:
                    animate_amount(sel_year,sel_quarter)
                    animate_amount_table(sel_year,sel_quarter)
                    payment_amount_year(sel_year)
                    payment_amount_year_table(sel_year)
                with col2:
                    animate_count(sel_year,sel_quarter)
                    animate_count_table(sel_year,sel_quarter)
                    payment_count_year(sel_year)
                    payment_count_year_Table(sel_year)


        elif sel_quarter=="3":
                with col1:
                    animate_amount(sel_year,sel_quarter)
                    animate_amount_table(sel_year,sel_quarter)
                    payment_amount_year(sel_year)
                    payment_amount_year_table(sel_year)
                with col2:
                    animate_count(sel_year,sel_quarter)
                    animate_count_table(sel_year,sel_quarter)
                    payment_count_year(sel_year)
                    payment_count_year_Table(sel_year)

        else:
            with col1:
                    animate_amount(sel_year,sel_quarter)
                    animate_amount_table(sel_year,sel_quarter)
                    payment_amount_year(sel_year)
                    payment_amount_year_table(sel_year)
            with col2:
                    animate_count(sel_year,sel_quarter)
                    animate_count_table(sel_year,sel_quarter)
                    payment_count_year(sel_year)
                    payment_count_year_Table(sel_year)


        state= st.selectbox("select the state",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                               'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                               'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                               'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                               'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'))
        
        col5,col6=st.columns(2)
        with col5:
            reg_state_all_TA(sel_year,state)
            reg_state_all_TA_Table(sel_year,state)
            
        with col6:
           reg_state_all_TC(sel_year,state)
           reg_state_all_TC_Table(sel_year,state)
        

        reg_state_all_RU(sel_year,state)
        reg_state_all_RU_Table(sel_year,state)
            
           
if selected=="REPORTS":
    col1,col2=st.columns(2)
    with col1:
        filepath1=load_lottiefile("E:\data science\phonepe project\A7.json")
        st.lottie(filepath1,speed=1,reverse=False,loop=True,height=300,width=320,quality="highest")
    with col2:
        filepath=load_lottiefile("E:\data science\phonepe project\A7.json")
        st.lottie(filepath,speed=1,reverse=False,loop=True,height=300,width=920,quality="highest")
    ques=st.selectbox("Select The Question",(" Which Are The Top Mobile Brands With Maximum Number of Transaction Count ?",
                                             "Which Are The TOP 10 STATES WITH HIGHEST TRANSACTION AMOUNT ?",
                                             "Which Are The TOP 10 STATES WITH LOWEST TRANSACTION AMOUNT ?",
                                             "Which Are The TOP 10 DISTRICTS IN INDIA WITH HIGHEST TRANSACTION AMOUNT ?",
                                             "Which Are The TOP 10 DISTRICTS OF INDIA WITH LOWEST TRANSACTION AMOUNT ?",
                                             "Which Are The TOP 10 States IN INDIA With MAXIMUM AppOpens ?",
                                             "Which Are The TOP 10 LOWEST STATES IN INDIA WITH MINIMUM AppOpens ?",
                                             "Which Are The TOP 10 STATES WITH HIGHEST TRANSACTION COUNT ?",
                                             "Which Are The TOP 10 STATES WITH LOWEST TRANSACTION COUNT ?",
                                             "Which Are The TOP 10 DISTRICTS WITH HIGHEST TRANSACTION COUNT ?",
                                             "Which Are The TOP 10  DISTRICTS WITH LOWEST TRANSACTION COUNT ?"))

    if ques==" Which Are The Top Mobile Brands With Maximum Number of Transaction Count ?":
        ques1()
        ques1_table()
    elif ques=="Which Are The TOP 10 STATES WITH HIGHEST TRANSACTION AMOUNT ?":
        ques2()
        ques2_table()
    elif ques=="Which Are The TOP 10 STATES WITH LOWEST TRANSACTION AMOUNT ?":
        ques3()
        ques3_table()
    elif ques=="Which Are The TOP 10 DISTRICTS IN INDIA WITH HIGHEST TRANSACTION AMOUNT ?":
        ques4()
        ques4_table()
    elif ques=="Which Are The TOP 10 DISTRICTS OF INDIA WITH LOWEST TRANSACTION AMOUNT ?":
        ques5()
        ques5_table()
    elif ques=="Which Are The TOP 10 States IN INDIA With MAXIMUM AppOpens ?":
        ques6()
        ques6_table()
    elif ques=="Which Are The TOP 10 LOWEST STATES IN INDIA WITH MINIMUM AppOpens ?":
        ques7()
        ques7_table()
    elif ques=="Which Are The TOP 10 STATES WITH HIGHEST TRANSACTION COUNT ?":
        ques8()
        ques8_table()
    elif ques=="Which Are The TOP 10 STATES WITH LOWEST TRANSACTION COUNT ?":
        ques9()
        ques9_table()
    elif ques=="Which Are The TOP 10 DISTRICTS WITH HIGHEST TRANSACTION COUNT ?":
        ques10()
        ques10_table()
    elif ques=="Which Are The TOP 10  DISTRICTS WITH LOWEST TRANSACTION COUNT ?":
        ques11()
        ques11_table()

if selected=="ADDITIONAL INFORMATION":
    filepath=load_lottiefile("E:\data science\phonepe project\A6.json")
    st.lottie(filepath,speed=1,reverse=False,loop=True,height=250,width=1110,quality="highest")

    selected=option_menu( menu_title="Phonepe Pulse Data Visualization and Exploration",
        options=["About Project","Technologies Used","Procedure","Results"],
        icons=["distribute-vertical","code","card-text","cloud-arrow-up-fill"],
        menu_icon="play-fill")
    if selected =="About Project":
        st.header(":white[**Objective**]")
        st.markdown(":white[**The Phonepe pulse Github repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.In this project ,the main aim is to extract the data from GitHub repository and then with the help of streamlit and various ploting libraries ,represent the data in the form of geo visualization  and in a user friendly manner**]")
    if selected=="Technologies Used":
        st.header(":white[**1.Python**]")
        st.markdown("Python is an interpreted, high-level, general-purpose programming language. Its design philosophy emphasizes code readability with its notable use of significant whitespace. Its language constructs and object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured particularly, procedural and functional programming, object-oriented, and concurrent programming.Python is widely used for web development, software development, data science, machine learning and artificial intelligence, and more. It is free and open-source software.")
        st.header(":white[**2. Github cloning**]")
        st.markdown(":white[**Cloning a repository on GitHub copies the repository from GitHub.com to your local machine. This includes all versions of every file and folder for the project. The git clone command is a git command that creates a copy of an existing repository into a new directory. It's also used to create remote-tracking branches for each branch in the cloned repository.**]")
        st.header(":white[**3.Pandas**]")
        st.markdown(":white[**Pandas is a Python library used for working with data sets. It has functions for analyzing, cleaning, exploring, and manipulating data. The name Pandas has a reference to both Panel Data, and Python Data Analysis**]")
        st.header(":white[**4.SQL**]")
        st.markdown(":white[**Structured query language (SQL) is a programming language for storing and processing information in a relational database. A relational database stores information in tabular form, with rows and columns representing different data attributes and the various relationships between the data values.**]")  
        st.header(":white[**5.Plotly**]")
        st.markdown(":white[**Plotly is a free and open-source Python library for creating interactive, scientific graphs and charts. It can be used to create a variety of different types of plots, including line charts, bar charts, scatter plots, histograms, and more. Plotly is a popular choice for data visualization because it is easy to use and produces high-quality graphs. It is also very versatile and can be used to create a wide variety of different types of plots.**]")
        st.header(":white[**6.Streamlit**]")
        st.markdown(":white[**Streamlit is an open-source app framework in python language. It helps us create beautiful web apps for data science and machine learning in a little time. It is compatible with major python libraries such as scikit-learn, keras, PyTorch, latex, numpy, pandas, matplotlib, etc.**]")
    if selected=="Procedure":
        st.header(":white[**Procedure**]")
        st.markdown("1. Data extraction: Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as CSV or JSON.")
        st.markdown("2. Data transformation: Use a scripting language such as Python, along with libraries such as Pandas, to manipulate and pre-process the data. This may include cleaning the data, handling missing values, and transforming the data into a format suitable for analysis and visualization.")
        st.markdown("3. Database insertion: Use the mysql-connector-python library in Python to connect to a MySQL database and insert the transformed data using SQL commands.")
        st.markdown("4. Dashboard creation: Use the Streamlit and Plotly libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in geo map functions can be used to display the data on a map and Streamlit can be used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.")
        st.markdown("5. Data retrieval: Use the mysql-connector-python library to connect to the MySQL database and fetch the data into a Pandas dataframe. Use the data in the dataframe to update the dashboard dynamically.")
        st.markdown("6. Deployment: Ensure the solution is secure, efficient, and user-friendly. Test the solution thoroughly and deploy the dashboard publicly, making it accessible to users.")
        st.markdown("")
    if selected=="Results":
        st.header(":white[**Result**]")
        st.markdown("Result is in the form of this Streamlit Application")
        st.markdown("The result of this project will be a live geo visualization dashboard that displays information and insights from the Phonepe pulse Github repository in an interactive and visually appealing manner. The dashboard will have at least 10 different dropdown options for users to select different facts and figures to display. The data will be stored in a MySQL database for efficient retrieval and the dashboard will be dynamically updated to reflect the latest data. Users will be able to access the dashboard from a web browser and easily navigate the different visualizations and facts and figures displayed. The dashboard will provide valuable insights and information about the data in the Phonepe pulse Github repository, making it a valuable tool for data analysis and decision-making.Overall, the result of this project will be a comprehensive and user-friendly solution for extracting, transforming, and visualizing data from the Phonepe pulse Github repository.")

