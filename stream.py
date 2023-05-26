from gc import callbacks
from http import client
from unicodedata import name
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
import time
import random

def reload_opt(choice):
   
    if choice == 'Project 1':
        return Tasks
    if choice == 'Project 2':
        return Tasks2
    if choice == 'Project 3':
        return Tasks3
def reload_nam(choice):
   
    if choice == 'Project 1':
        return pronames[0]
    if choice == 'Project 2':
        return pronames[1]
    if choice == 'Project 3':
        return pronames[2]
pronames = ['Real Estate Case','Antitrust Case','Venture Capital Case']
if 'count' not in st.session_state:
	st.session_state.count = 0

def increment_counter(increment_value=0):
	st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
	st.session_state.count -= decrement_value



    



st.set_page_config(
    page_title= "Mattos Filho Client Portal",
    page_icon = "⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
    )

st.title('Online User Interface (OUI)')

with st.sidebar:
    date = st.date_input('Chose date')

tab1, tab2, tab3 = st.tabs(["Projects", "Billing","Project history"])

with tab1:
    col1, col2 = st.columns([3, 1])


    with col1:

        with st.container():

            

            ### Gantt Chart
            uploaded_file = "project_template.csv"
            uploaded_file2 = "project_template2.csv"
            uploaded_file3 = "project_template3.csv"

            Tasks=pd.read_csv(uploaded_file)
            Tasks['Start'] = Tasks['Start'].values.astype('datetime64[ns]')
            Tasks['Finish'] = Tasks['Finish'].values.astype('datetime64[ns]')
            Tasks['startdate'] = Tasks['Start'].dt.date
            Tasks['finishdate'] = Tasks['Start'].dt.date

            Tasks2=pd.read_csv(uploaded_file2)
            Tasks2['Start'] = Tasks2['Start'].values.astype('datetime64[ns]')
            Tasks2['Finish'] = Tasks2['Finish'].values.astype('datetime64[ns]')
            Tasks2['startdate'] = Tasks2['Start'].dt.date
            Tasks2['finishdate'] = Tasks2['Start'].dt.date

            Tasks3=pd.read_csv(uploaded_file3)
            Tasks3['Start'] = Tasks3['Start'].values.astype('datetime64[ns]')
            Tasks3['Finish'] = Tasks3['Finish'].values.astype('datetime64[ns]')
            Tasks3['startdate'] = Tasks3['Start'].dt.date
            Tasks3['finishdate'] = Tasks3['Start'].dt.date

            with st.container():
                col111, col112 = st.columns([3, 1])
                col121, col122 = st.columns([3, 1])
                
                choice = col112.selectbox(
                'Select Project',
                options = ['Project 1','Project 2','Project 3']
                )
                contnum = str(930284)
                prolead = "João Silva"
                option = reload_opt(str(choice))
                col111.subheader(reload_nam(choice))
                col121.markdown(f"Status: _:green[In progress]_    |    Contract Number: _{random.randint(100000,999999)}_    |    Project Lead: _{prolead}_")
                st.markdown(f"Project Start: _{str(option['startdate'][:1][0])}_    |    Project End: _{str(option['finishdate'][-1:][len(option)-1])}_")
            st.divider()  # 👈 Draws a horizontal rule
            with st.container():
                col211, col212 = st.columns([3, 1])
                col221, col222, col223, col224 = st.columns([1, 1, 12, 12])
            
                case = st.session_state.count
                if case < 0:
                    st.session_state.count = 0
                if case >= len(option.values)-1:
                    st.session_state.count = 0
                    
                col211.subheader(option['Task'].values[case])
                col211.markdown(option['Task Description'].values[case])
                if option['Completion'].values[case] == 0:
                    maxtask = random.randint(2,7)
                    donetask = 0
                elif 0 < option['Completion'].values[case] < 1:
                    maxtask = random.randint(2,7)
                    donetask = random.randint(1,maxtask-1)
                elif option['Completion'].values[case] == 1:
                    maxtask = random.randint(2,7)
                    donetask = maxtask
                substasks = "("+str(donetask)+"/"+str(maxtask)+")"
                col212.metric('Sub-tasks complete',substasks)
            
                col222.button('\>', on_click=increment_counter,
	            kwargs=dict(increment_value=1))

                col221.button('<', on_click=decrement_counter,
	            kwargs=dict(decrement_value=1))
                nameclient= 'Marco Silva'
                namecomp= 'Vermelho S.A.'
                casenam=reload_nam(choice)
                tasknam=option['Task'].values[case]
                with st.expander('Feedback'):
                    with st.form('feedback'):
                        st.text_area('Type in your feedback', value=f"Client:{nameclient}\nCompany:{namecomp}\nCase:{casenam}\nTask:{tasknam}\nConcern:\n", height=200)
                        submitted = st.form_submit_button("Submit")
                        if submitted:
                            st.success("Feedback Submitted")
    

            st.divider()  # 👈 Draws a horizontal rule

            
            
            st.subheader('Project roadmap')
            fig = px.timeline(
                            option, 
                            x_start="Start", 
                            x_end="Finish", 
                            y="Task",
                            color='Completion',
                            color_continuous_scale='Agsunset',
                        
                            hover_name="Task Description"
                            )

            fig.update_yaxes(autorange="reversed")          #if not specified as 'reversed', the tasks will be listed from bottom up       
                
            fig.update_layout(
                            title="",
                            hoverlabel_bgcolor='#DAEEED',   #Change the hover tooltip background color to a universal light blue color. If not specified, the background color will vary by team or completion pct, depending on what view the user chooses
                            bargap=0.2,
                            ###height=300,              
                            xaxis_title="", 
                            yaxis_title="",                 
                            title_x=0.5, #Make title centered                                       
                            xaxis=dict(
                                    tickfont_size=15,
                                    tickangle = 270,
                                    rangeslider_visible=True,
                                    side ="top",            #Place the tick labels on the top of the chart
                                    showgrid = True,
                                    zeroline = True,
                                    showline = True,
                                    showticklabels = True,
                                    tickformat="%x\n",      #Display the tick labels in certain format. To learn more about different formats, visit: https://github.com/d3/d3-format/blob/main/README.md#locale_format
                                )
                        )
            fig.add_vline(x=date, line_width=3, line_color="red")    
            fig.update_xaxes(tickangle=0)

            st.plotly_chart(fig, use_container_width=True)  #Display the plotly chart in Streamlit

            ### Customisable chart
            """  
            grid_response = AgGrid(
                Tasks,
                editable=True, 
                height=300, 
                width='100%',
                    )
            """

            
            

        

    with col2:
        for index, row in option.iterrows():
            donetick = ""
            numberstr = "("+str(index+1) +"/"+ str(len(option))+") "
            if row['Completion'] == 1:
                donetick = " | ✓"
            if 0 < row['Completion'] < 1:
                with st.expander(numberstr+str(row['Task']+donetick), expanded=True):
                    st.subheader(str(row['Task']))
                    st.write(str(row['Task Description']))
                    st.divider()
                    st.progress(row['Completion'], text=str(row['Completion']*100)+'%')
            elif row['Completion'] == 0 or row['Completion']==1:
                with st.expander(numberstr+str(row['Task']+donetick)):
                    st.subheader(str(row['Task']))
                    st.write(str(row['Task Description']))
                    st.divider()
                    st.progress(row['Completion'], text=str(row['Completion']*100)+'%')
