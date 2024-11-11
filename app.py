import streamlit as st
from streamlit_option_menu import option_menu
from prediction_page import prediction_page
from visualization_page import visualization_page


    
#pages = st.sidebar.selectbox("Predict and Graphs", ("Predict", "Graphs"))
pages = option_menu(
        menu_title= None,
        options=["Predict", "Graphs"],
        orientation= "horizontal",
    )

if pages =="Predict":
    prediction_page()
else:    
    visualization_page()
    
    #runs in Anaconda Navegator environment.
    # 