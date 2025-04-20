import streamlit as st
import requests
import datetime

st.title('TaxiFareModel front')

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

st.header('Select your ride details')

date = st.date_input("Date of your ride", datetime.date(2019, 7, 6))
time = st.time_input("Time of your ride", datetime.time(8, 45))

pickup_long = st.number_input("Pickup Longitude", value=-73.985428)
pickup_lat = st.number_input("Pickup Latitude", value=40.748817)
dropoff_long = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_lat = st.number_input("Dropoff Latitude", value=40.748817)

passenger_count = st.number_input("Number of passengers", min_value=1, max_value=8, step=1)

pickup_datetime = datetime.datetime.combine(date, time).strftime('%Y-%m-%d %H:%M:%S')

params = {
    'pickup_datetime': pickup_datetime,
    'pickup_longitude': pickup_long,
    'pickup_latitude': pickup_lat,
    'dropoff_longitude': dropoff_long,
    'dropoff_latitude': dropoff_lat,
    'passenger_count': int(passenger_count)
}

st.header("Prediction")

st.markdown('''
See? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API? Of course... The `requests` package 💡
''')

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':
    st.info('Using Le Wagon’s public prediction API. You could swap this out with your own!')

if st.button('Predict fare'):
    try:
        response = requests.get(url, params=params)

        # Log response status code and full response for debugging
        st.write("Response status code:", response.status_code)
        st.write("Raw API response:", response.text)

        if response.status_code == 200:
            result = response.json()
            fare = result.get('prediction')

            if isinstance(fare, (float, int)):
                st.success(f"Predicted fare: ${fare:.2f}")
            else:
                st.error(f"Something went wrong with the prediction. API returned: {fare}")
        else:
            st.error(f"API request failed with status code {response.status_code}")
    except Exception as e:
        st.error(f"Error calling the API: {e}")
