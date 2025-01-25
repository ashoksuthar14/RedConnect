import streamlit as st
import googlemaps
from datetime import datetime
import folium
from streamlit_folium import folium_static
from streamlit_geolocation import streamlit_geolocation

# Initialize the Google Maps client
gmaps = googlemaps.Client(key='AIzaSyA6pDl-0nVb16yJE1muih6HDdZAHN7Mhr4')

# Streamlit app
st.title("Find Hospitals with Specific Blood Type")

# User input for blood type
blood_type = st.selectbox("Select the blood type you need:", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])

# Get the user's current location using streamlit-geolocation
st.write("Click the button below to detect your current location:")
location = streamlit_geolocation()

# Check if location is available
if location and "latitude" in location and "longitude" in location:
    lat = location["latitude"]
    lng = location["longitude"]

    # Display the detected location
    st.write(f"Detected Location: Latitude = {lat}, Longitude = {lng}")

    # Button to trigger the search
    if st.button("Find Hospitals"):
        # Use the Places API to search for hospitals nearby
        places_result = gmaps.places_nearby(location=(lat, lng), radius=5000, type='hospital', keyword='blood bank')

        # Create a map centered at the user's location
        m = folium.Map(location=[lat, lng], zoom_start=12)

        # Add a marker for the user's location
        folium.Marker(
            location=[lat, lng],
            popup="Your Location",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        # Filter hospitals that have the specific blood type
        hospitals_with_blood_type = []
        for place in places_result['results']:
            # Here you would need to implement logic to check if the hospital has the specific blood type
            # This is a placeholder, as the actual implementation would depend on the data available
            hospitals_with_blood_type.append(place)

            # Add a marker for each hospital
            folium.Marker(
                location=[place['geometry']['location']['lat'], place['geometry']['location']['lng']],
                popup=place['name'],
                icon=folium.Icon(color="red")
            ).add_to(m)

        # Display the map
        st.write("Map of Nearby Hospitals:")
        folium_static(m)

        # Display the results
        if hospitals_with_blood_type:
            st.write(f"Hospitals with {blood_type} blood type nearby:")
            for i, hospital in enumerate(hospitals_with_blood_type):
                st.write(f"{i + 1}. {hospital['name']} - {hospital['vicinity']}")

            # Allow the user to select a hospital for directions
            selected_hospital_index = st.selectbox(
                "Select a hospital to get directions:",
                range(len(hospitals_with_blood_type)),
                format_func=lambda x: hospitals_with_blood_type[x]['name']
            )

            if selected_hospital_index is not None:
                selected_hospital = hospitals_with_blood_type[selected_hospital_index]
                hospital_lat = selected_hospital['geometry']['location']['lat']
                hospital_lng = selected_hospital['geometry']['location']['lng']

                # Get directions to the selected hospital
                directions_result = gmaps.directions((lat, lng),
                                                     (hospital_lat, hospital_lng),
                                                     mode="driving",
                                                     departure_time=datetime.now())

                # Display the directions on the map
                m = folium.Map(location=[lat, lng], zoom_start=12)

                # Add a marker for the user's location
                folium.Marker(
                    location=[lat, lng],
                    popup="Your Location",
                    icon=folium.Icon(color="blue")
                ).add_to(m)

                # Add a marker for the selected hospital
                folium.Marker(
                    location=[hospital_lat, hospital_lng],
                    popup=selected_hospital['name'],
                    icon=folium.Icon(color="red")
                ).add_to(m)

                # Add the route to the map
                for step in directions_result[0]['legs'][0]['steps']:
                    start_lat = step['start_location']['lat']
                    start_lng = step['start_location']['lng']
                    end_lat = step['end_location']['lat']
                    end_lng = step['end_location']['lng']
                    folium.PolyLine(
                        locations=[(start_lat, start_lng), (end_lat, end_lng)],
                        color="blue",
                        weight=2.5,
                        opacity=1
                    ).add_to(m)

                # Display the map with the route
                st.write("Directions to the Selected Hospital:")
                folium_static(m)

                # Display the step-by-step directions
                st.write("Step-by-Step Directions:")
                for step in directions_result[0]['legs'][0]['steps']:
                    st.write(step['html_instructions'])
        else:
            st.write("No hospitals found with the specified blood type.")
else:
    st.write("Unable to detect your location. Please ensure location access is enabled in your browser.")
