
import streamlit as st
import pickle
import numpy as np



def load_model():
    with open('logreg_model.pkl', 'rb') as file:
        load_model = pickle.load(file)
    return load_model

load_model = load_model()
# --------------------------------------------------------------------------------

driver_at_fault_mapping = {
    0.0: 'NO',
    1.0: 'Yes'
}

report_type_mapping = {
    'PROPERTY DAMAGE CRASH': 1,
    'INJURY CRASH': 2, 
    'FATAL CRASH': 3,  
    'UNKNOWN': 0
}

injury_severity_mapping ={
    'NO APPARENT INJURY': 1,
    'SUSPECTED MINOR INJURY': 2,
    'SUSPECTED SERIOUS INJURY': 4,
    'POSSIBLE INJURY': 3,
    'FATAL INJURY': 5,
    'UNKNOWN': 0
}

related_non_motorist_options = [
    'BICYCLIST', 'IN ANIMAL-DRAWN VEH', 'MACHINE OPERATOR/RIDER', 
    'NON', 'OTHER', 'PEDESTRIAN', 'UNKNOWN'
]

collision_type_options = [
    'ANGLE MEETS LEFT HEAD ON', 'ANGLE MEETS LEFT TURN', 'ANGLE MEETS RIGHT TURN',
    'HEAD ON', 'HEAD ON LEFT TURN', 'OPPOSITE DIR BOTH LEFT TURN', 'OPPOSITE DIRECTION SIDESWIPE',
    'OTHER', 'SAME DIR BOTH LEFT TURN', 'SAME DIR REAR END', 'SAME DIR REND LEFT TURN',
    'SAME DIR REND RIGHT TURN', 'SAME DIRECTION LEFT TURN', 'SAME DIRECTION RIGHT TURN',
    'SAME DIRECTION SIDESWIPE', 'SINGLE VEHICLE', 'STRAIGHT MOVEMENT ANGLE', 'UNKNOWN'
]

weather_options = [
    'BLOWING SAND, SOIL, DIRT', 'BLOWING SNOW', 'CLEAR', 'CLOUDY', 'FOGGY',
    'OTHER', 'RAINING', 'SEVERE WINDS', 'SLEET', 'SNOW', 'UNKNOWN', 'WINTRY MIX'
]

surface_condition_options = [
    'DRY', 'ICE', 'MUD, DIRT, GRAVEL', 'OIL', 'OTHER', 'SAND',
    'SLUSH', 'SNOW', 'UNKNOWN', 'WATER(STANDING/MOVING)', 'WET'
]

light_options = [
    'DARK -- UNKNOWN LIGHTING','DARK LIGHTS ON', 'DARK NO LIGHTS',
    'DAWN', 'DAYLIGHT', 'DUSK', 'OTHER',  'UNKNOWN'
]

traffic_control_options = [
    'FLASHING TRAFFIC SIGNAL', 'NO CONTROLS', 'OTHER', 'PERSON',
    'RAILWAY CROSSING DEVICE', 'SCHOOL ZONE SIGN DEVICE', 'STOP SIGN',
    'TRAFFIC SIGNAL', 'UNKNOWN', 'WARNING SIGN', 'YIELD SIGN'
]

driver_sub_abuse_options = [
    'ALCOHOL PRESENT', 'COMBINED SUBSTANCE PRESENT', 'ILLEGAL DRUG PRESENT',
    'MEDICATION PRESENT', 'NONE DETECTED', 'OTHER', 'UNKNOWN'
]

non_motorist_sub_abu_options = [
    'ALCOHOL PRESENT', 'COMBINED SUBSTANCE PRESENT', 'ILLEGAL DRUG PRESENT',
    'MEDICATION PRESENT', 'NON', 'NONE DETECTED', 'OTHER','UNKNOWN'
]

driver_distractedby_options = [
    'ADJUSTING AUDIO AND OR CLIMATE CONTROLS', 'BY MOVING OBJECT IN VEHICLE', 'DISTRACTED BY OUTSIDE PERSON OBJECT OR EVENT',
    'EATING OR DRINKING', 'INATTENTIVE OR LOST IN THOUGHT', 'LOOKED BUT DID NOT SEE', 'MOBILEPHONE', 'NO DRIVER PRESENT',
    'NOT DISTRACTED', 'OTHER DISTRACTION', 'SMOKING RELATED', 'UNKNOWN'
]

vehc_damage_ext_options = [
    'DESTROYED', 'DISABLING', 'FUNCTIONAL', 'NO DAMAGE', 'OTHER', 'SUPERFICIAL', 'UNKNOWN'
]

vehc_body_type_options = [
    'AMBULANCE/EMERGENCY', 'AMBULANCE/NON EMERGENCY', 'BUS', 'CAR', 'FARM VEHICLE', 'FIRE VEHICLE/EMERGENCY',
    'FIRE VEHICLE/NON EMERGENCY', 'MOTORCYCLE', 'OTHER', 'PICKUP TRUCK', 'POLICE VEHICLE/EMERGENCY',
    'POLICE VEHICLE/NON EMERGENCY', 'TRUCK', 'TRUCK TRACTOR', 'UNKNOWN', 'VAN'
]

vehc_movement_options = [
    'ACCELERATING', 'BACKING', 'CHANGING LANES', 'DRIVERLESS MOVING VEH.', 'ENTERING TRAFFIC LANE',
    'LEAVING TRAFFIC LANE', 'MAKING LEFT TURN', 'MAKING RIGHT TURN', 'MAKING U TURN', 'MOVING CONSTANT SPEED',
    'NEGOTIATING A CURVE', 'OTHER', 'PARKED', 'PARKING', 'PASSING', 'RIGHT TURN ON RED', 'SKIDDING', 'SLOWING OR STOPPING',
    'STARTING FROM LANE', 'STARTING FROM PARKED', 'STOPPED IN TRAFFIC LANE', 'UNKNOWN'
]

driveless_vehc_options = [
    'NO', 'UNKNOWN'
]

parked_vehc_options = [
    'NO', 'UNKNOWN', 'YES'
]

equip_probl_options = [
    'AIR BAG FAILED', 'BELT(S) MISUSED', 'BELTS/ANCHORS BROKE', 'FACING WRONG WAY', 'NO MISUSE',
    'NOT STREPPED RIGHT', 'OTHER', 'SIZE/TYPE IMPROPER', 'STRAP/TETHER LOOSE', 'UNKNOWN'
]
def map_driver_at_fault(prediction):
    return driver_at_fault_mapping.get(prediction)
def map_report_type(report_type):
    return report_type_mapping.get(report_type)
def map_injury_severity(injury_severity):
    return injury_severity_mapping.get(injury_severity)

def  prediction_page():
    st.title("Car Crash Fault Prediction")
    
    st.write("""### Please, provide the info about the crash to be predicted!""")
    

    placeholder = "-----Select-----"
    report_type_options = list(report_type_mapping.keys())
    report_type = st.selectbox("ACRS Report Type",[placeholder] + report_type_options)
        
    injury_severity_options = list(injury_severity_mapping.keys())
    injury_severitys = st.selectbox("Injury Severity",[placeholder] + injury_severity_options)
    
    speed_limit_options = ('0', '5', '10', '15', '20', '25', '35', '30', '40', '45', '50', '55', '60', '65', '70', '75')
    speed_limit_options = [placeholder] + list(speed_limit_options)
    speed_limit_str = st.selectbox("Speed Limit", speed_limit_options)
    speed_limit = int(speed_limit_str.split()[0]) if speed_limit_str != placeholder else 0
        
    related_non_motorist = st.selectbox("Related Non-Motorist", [placeholder] + related_non_motorist_options)
    collision_type = st.selectbox("Collision Type", [placeholder] + collision_type_options)
    weather = st.selectbox("Weather", [placeholder] + weather_options)
    surface_condition = st.selectbox("Surface Condition", [placeholder] + surface_condition_options)
    light = st.selectbox("Light", [placeholder] + light_options)
    traffic_control = st.selectbox("Traffic Control", [placeholder] + traffic_control_options)
    driver_sub_abuse = st.selectbox("Driver Substance Abuse", [placeholder] + driver_sub_abuse_options)
    non_motorist_sub_abu = st.selectbox("Non-Motorist Substance Abuse", [placeholder] + non_motorist_sub_abu_options)
    driver_distractedby = st.selectbox("Driver Distracted By", [placeholder] + driver_distractedby_options)
    vehc_damage_ext = st.selectbox("Vehicle Damage Extent", [placeholder] + vehc_damage_ext_options)
    vehc_body_type = st.selectbox("Vehicle Body Type", [placeholder] + vehc_body_type_options)
    vehc_movement = st.selectbox("Vehicle Movement", [placeholder] + vehc_movement_options)
    driveless_vehc = st.selectbox("Driveless Vehicle", [placeholder] + driveless_vehc_options)
    parked_vehc = st.selectbox("Parked Vehicle", [placeholder] + parked_vehc_options)
    equip_probl = st.selectbox("Equipment Problems", [placeholder] + equip_probl_options)
    
    encoded_report_type = map_report_type(report_type)
    encoded_injury_severitys = map_injury_severity(injury_severitys)
    encoded_related_non_motorist = [1.0 if value == related_non_motorist else 0.0 for value in related_non_motorist_options]
    encoded_collision_type = [1.0 if value == collision_type else 0.0 for value in collision_type_options]
    encoded_weather = [1.0 if value == weather else 0.0 for value in weather_options]
    encoded_surface_condition = [1.0 if value == surface_condition else 0.0 for value in surface_condition_options]
    encoded_light = [1.0 if value == light else 0.0 for value in light_options]
    encoded_traffic_control = [1.0 if value == traffic_control else 0.0 for value in traffic_control_options]
    encoded_driver_sub_abuse = [1.0 if value == driver_sub_abuse else 0.0 for value in driver_sub_abuse_options]
    encoded_non_motorist_sub_abu = [1.0 if value == non_motorist_sub_abu else 0.0 for value in non_motorist_sub_abu_options]
    encoded_driver_distractedby = [1.0 if value == driver_distractedby else 0.0 for value in driver_distractedby_options]
    encoded_vehc_damage_ext = [1.0 if value == vehc_damage_ext else 0.0 for value in vehc_damage_ext_options]
    encoded_vehc_body_type = [1.0 if value == vehc_body_type else 0.0 for value in vehc_body_type_options]
    encoded_vehc_movement = [1.0 if value == vehc_movement else 0.0 for value in vehc_movement_options]
    encoded_driveless_vehc = [1.0 if value == driveless_vehc else 0.0 for value in driveless_vehc_options]
    encoded_parked_vehc = [1.0 if value == parked_vehc else 0.0 for value in parked_vehc_options]
    encoded_equip_probl = [1.0 if value == equip_probl else 0.0 for value in equip_probl_options]
        
    if st.button("Predict"):
        if report_type != placeholder and injury_severitys != placeholder and speed_limit_str != placeholder \
            and related_non_motorist != placeholder and collision_type != placeholder and weather != placeholder \
            and surface_condition != placeholder and light != placeholder and traffic_control != placeholder \
            and driver_sub_abuse != placeholder and non_motorist_sub_abu != placeholder and driver_distractedby != placeholder \
            and vehc_damage_ext != placeholder and vehc_body_type != placeholder and vehc_movement != placeholder \
            and driveless_vehc != placeholder and parked_vehc != placeholder and equip_probl != placeholder:
                
                selected_values = np.hstack([
                    encoded_related_non_motorist,
                    encoded_collision_type,
                    encoded_weather,
                    encoded_surface_condition,
                    encoded_light,
                    encoded_traffic_control,
                    encoded_driver_sub_abuse,
                    encoded_non_motorist_sub_abu,
                    encoded_driver_distractedby,
                    encoded_vehc_damage_ext,
                    encoded_vehc_body_type,
                    encoded_vehc_movement,
                    encoded_driveless_vehc,
                    encoded_parked_vehc,
                    encoded_equip_probl,
                    encoded_report_type,
                    encoded_injury_severitys,
                    speed_limit
                ])
                selected_values = selected_values.reshape(1, -1)
                prediction = load_model.predict(selected_values)
                predicted_driver_at_fault = map_driver_at_fault(prediction[0])
                predicted_probabilities = load_model.predict_proba(selected_values)[0]
                proba_predicted_class = predicted_probabilities[int(prediction)] * 100
                probability_str = "{:.2f}%".format(proba_predicted_class)
                st.write(f"Prediction (Driver At Fault): {predicted_driver_at_fault}")
                st.write(f"Probability of the prediction: {probability_str}")
                st.write('Logistic Regression Model with accuracy at 85%')
        else:
            st.write("All boxes must be selected for prediction.")
