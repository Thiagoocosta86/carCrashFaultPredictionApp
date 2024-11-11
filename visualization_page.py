import streamlit as st
from streamlit_extras import add_vertical_space as avs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer

#@st.cache
def load_data():
    crashes_data = pd.read_csv("Crash_Reporting_-_Drivers_Data.csv", low_memory=False)

    # num_col = crashes_data.select_dtypes(include=['int64', 'float64']).columns
    # corr_matrix = crashes_data[num_col].corr()

    # plt.figure(figsize=(10,8))
    # sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    # plt.title("Correlation Matrix")
    # plt.show()

    crashes_data = crashes_data.drop(['Report Number','Crash Date/Time','Local Case Number', 
                                    'Agency Name','Route Type', 'Road Name', 'Cross-Street Type',
                                    'Cross-Street Name', 'Off-Road Description','Municipality',
                                    'Person ID', 'Drivers License State','Vehicle ID',
                                    'Vehicle Continuing Dir', 'Vehicle Going Dir','Latitude',
                                    'Longitude', 'Location','Circumstance',
                                    'Vehicle First Impact Location','Vehicle Second Impact Location',
                                    'Vehicle Year','Vehicle Make','Vehicle Model'
                                    ], axis=1).copy()

    crashes_data = crashes_data.loc[~crashes_data.duplicated(subset=[
            'ACRS Report Type', 'Related Non-Motorist',
        'Collision Type', 'Weather', 'Surface Condition', 'Light',
        'Traffic Control', 'Driver Substance Abuse',
        'Non-Motorist Substance Abuse', 'Driver At Fault', 'Injury Severity',
        'Driver Distracted By', 'Vehicle Damage Extent',
        'Vehicle Body Type', 'Vehicle Movement', 'Speed Limit',
        'Driverless Vehicle', 'Parked Vehicle','Equipment Problems'])].reset_index(drop=True).copy()

    features = ['Collision Type', 'Weather', 'Light', 'Traffic Control', 'Driver Substance Abuse',
                'Vehicle Damage Extent', 'Vehicle Body Type', 'Vehicle Movement', 'Equipment Problems' ]

    imputer = SimpleImputer(strategy='most_frequent')

    crashes_data[features] = imputer.fit_transform(crashes_data[features])

    crashes_data_mapping = crashes_data.groupby('Weather')['Surface Condition'].agg(lambda x: x.mode().iloc[0]).to_dict()

    def handle_missing(row):
        if pd.isnull(row['Surface Condition']) and row['Weather'] in crashes_data_mapping:
            return crashes_data_mapping[row['Weather']]
        else:
            return row['Surface Condition']
        
    crashes_data['Surface Condition'] = crashes_data.apply(handle_missing,axis=1)

    nan_feat = ['Related Non-Motorist','Non-Motorist Substance Abuse']
    imp_const_nan = SimpleImputer(strategy='constant', fill_value = 'NON')
    crashes_data[nan_feat] = imp_const_nan.fit_transform(crashes_data[nan_feat])

    caps_to_convert = ['ACRS Report Type', 'Driver At Fault', 'Driverless Vehicle', 'Parked Vehicle']
    crashes_data[caps_to_convert] = crashes_data[caps_to_convert].applymap(str.upper)
    
    columns = ['ACRS Report Type', 'Related Non-Motorist', 'Collision Type', 'Weather',
        'Surface Condition', 'Light', 'Traffic Control',
        'Driver Substance Abuse', 'Non-Motorist Substance Abuse',
        'Driver At Fault', 'Injury Severity', 'Driver Distracted By',
        'Vehicle Damage Extent', 'Vehicle Body Type', 'Vehicle Movement',
        'Speed Limit', 'Driverless Vehicle', 'Parked Vehicle',
        'Equipment Problems']

    new_row = {
        'ACRS Report Type': 'UNKNOWN',
        'Related Non-Motorist': 'UNKNOWN',
        'Collision Type': 'UNKNOWN',
        'Weather': 'UNKNOWN',
        'Surface Condition': 'UNKNOWN',
        'Light': 'UNKNOWN',
        'Traffic Control': 'UNKNOWN',
        'Driver Substance Abuse': 'UNKNOWN',
        'Non-Motorist Substance Abuse': 'UNKNOWN',
        'Driver At Fault': 'NO',
        'Injury Severity': 'UNKNOWN',
        'Driver Distracted By': 'UNKNOWN',
        'Vehicle Damage Extent': 'UNKNOWN',
        'Vehicle Body Type': 'UNKNOWN',
        'Vehicle Movement': 'UNKNOWN',
        'Driverless Vehicle': 'UNKNOWN',
        'Parked Vehicle': 'UNKNOWN',
        'Equipment Problems': 'UNKNOWN',
        'Speed Limit': 0 
    }
    df_new_row =pd.DataFrame([new_row], columns=columns)
    crashes_data = pd.concat([crashes_data, df_new_row], ignore_index=True)
    
    crashes_data.drop(crashes_data[crashes_data['Driver At Fault'] == 'UNKNOWN'].index, inplace=True)
    crashes_data.reset_index(drop=True, inplace=True)
    
    non_motorist_mapping = {
        'BICYCLIST, OTHER': 'BICYCLIST',
        'BICYCLIST, PEDESTRIAN': 'BICYCLIST',
        'OTHER CONVEYANCE': 'OTHER',
        'OTHER, PEDESTRIAN': 'OTHER',
        'OTHER, OTHER CONVEYANCE': 'OTHER',
        'OTHER PEDALCYCLIST': 'OTHER',
        'OTHER CONVEYANCE, PEDESTRIAN':'OTHER'
    }
    drivsbab_mapping = {
        'ALCOHOL CONTRIBUTED': 'ALCOHOL PRESENT',
        'COMBINATION CONTRIBUTED': 'COMBINED SUBSTANCE PRESENT',
        'MEDICATION CONTRIBUTED': 'MEDICATION PRESENT',
        'ILLEGAL DRUG CONTRIBUTED': 'ILLEGAL DRUG PRESENT'    
    }
    non_drivsbab_mapping = {
        'ALCOHOL CONTRIBUTED': 'ALCOHOL PRESENT',
        'ALCOHOL CONTRIBUTED, ALCOHOL PRESENT': 'ALCOHOL PRESENT',
        'COMBINATION CONTRIBUTED': 'COMBINED SUBSTANCE PRESENT',
        'MEDICATION CONTRIBUTED': 'MEDICATION PRESENT',
        'ILLEGAL DRUG CONTRIBUTED': 'ILLEGAL DRUG PRESENT',
        'N/A, NONE DETECTED': 'NONE DETECTED',
        'ALCOHOL PRESENT, NONE DETECTED': 'NONE DETECTED',
        'NONE DETECTED, UNKNOWN': 'UNKNOWN',
        'N/A, UNKNOWN':'UNKNOWN'
    }
    driver_distracted_mapping = {
        'OTHER ELECTRONIC DEVICE (NAVIGATIONAL PALM PILOT)': 'OTHER DISTRACTION',
        'USING OTHER DEVICE CONTROLS INTEGRAL TO VEHICLE': 'OTHER DISTRACTION',
        'BY OTHER OCCUPANTS': 'OTHER DISTRACTION',
        'USING DEVICE OBJECT BROUGHT INTO VEHICLE': 'BY MOVING OBJECT IN VEHICLE',
        'TEXTING FROM A CELLULAR PHONE': 'MOBILEPHONE',
        'OTHER CELLULAR PHONE RELATED': 'MOBILEPHONE',
        'TALKING OR LISTENING TO CELLULAR PHONE': 'MOBILEPHONE',
        'DIALING CELLULAR PHONE': 'MOBILEPHONE'
    }
    vehc_bodytype_mapping = {
        'MEDIUM/HEAVY TRUCKS 3 AXLES (OVER 10,000LBS (4,536KG))': 'TRUCK',
        'OTHER LIGHT TRUCKS (10,000LBS (4,536KG) OR LESS)': 'TRUCK',
        'CARGO VAN/LIGHT TRUCK 2 AXLES (OVER 10,000LBS (4,536 KG))': 'TRUCK',
        'PASSENGER CAR': 'CAR',
        '(SPORT) UTILITY VEHICLE': 'CAR',
        'LIMOUSINE': 'CAR',
        'STATION WAGON': 'CAR',
        'MOPED': 'MOTORCYCLE',
        'TRANSIT BUS': 'BUS',
        'OTHER BUS': 'BUS',
        'SCHOOL BUS': 'BUS',
        'CROSS COUNTRY BUS': 'BUS',
        'RECREATIONAL VEHICLE': 'OTHER',
        'AUTOCYCLE': 'OTHER',
        'SNOWMOBILE': 'OTHER',
        'ALL TERRAIN VEHICLE (ATV)': 'OTHER',
        'LOW SPEED VEHICLE': 'OTHER',
    }
    crashes_data['Related Non-Motorist'] = crashes_data['Related Non-Motorist'].replace(non_motorist_mapping)
    crashes_data['Driver Substance Abuse'] = crashes_data['Driver Substance Abuse'].replace(drivsbab_mapping)
    crashes_data['Non-Motorist Substance Abuse'] = crashes_data['Non-Motorist Substance Abuse'].replace(non_drivsbab_mapping)
    crashes_data['Driver Distracted By'] = crashes_data['Driver Distracted By'].replace(driver_distracted_mapping)
    crashes_data['Vehicle Body Type'] = crashes_data['Vehicle Body Type'].replace(vehc_bodytype_mapping)
    
    return crashes_data

crashes_data = load_data()


def visualization_page():
    st.title("Vehicles Crash Data Visualization")
    
    avs.add_vertical_space(3)
    
    def plot_categorical_feature_pie(column):
        fig, ax = plt.subplots(figsize=(10, 8))
        crashes_data[column].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=60, ax=ax)
        ax.set_title(f"Distribution of {column}", fontsize=30)
        ax.axis('equal')  
        ax.tick_params(axis='both', which='major', labelsize=25)
        st.pyplot(fig)

    selected_feature = 'Driver At Fault'
    plot_categorical_feature_pie(selected_feature)
    
    avs.add_vertical_space(3)
    
    
    def plot_categorical_feature_line(column):
        fig, ax = plt.subplots(figsize=(12, 8))
        speed_limit_counts = crashes_data[column].value_counts().sort_index()
        speed_limit_counts.plot(kind='line', marker='o', ax=ax)
        ax.set_title(f"Distribution of {column}", fontsize=30)
        ax.set_ylabel('Count', fontsize=25)
        ax.set_xlabel('Speed Limit', fontsize=25)
        ax.tick_params(axis='both', which='major', labelsize=25)
        st.pyplot(fig)

    selected_feature = 'Speed Limit'  
    plot_categorical_feature_line(selected_feature)
    
    avs.add_vertical_space(3)
    
    cat_col = crashes_data.select_dtypes(include=['object']).columns
    for column in cat_col:
        fig, ax = plt.subplots(figsize=(30, 15))
        sns.countplot(x=column, data=crashes_data, ax=ax)
        ax.set_title(f"Distribution of {column}", fontsize=30)  
        ax.set_ylabel('Count', fontsize=25)                     
        ax.tick_params(axis='x', rotation=45, labelsize=25)     
        ax.tick_params(axis='y', labelsize=25)                  
        st.pyplot(fig)
        
    
        
    