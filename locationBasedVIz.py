# import the required modules
"""
This interactive data visualization tool depending on regional location was built by Geletaw Sahle.
This code will be updated on a regular basis.
"""
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Dataset we need to import
DATA_URL = (
    '/Users/geletawsahle/Desktop/CP_2020_WEPAPP/EmONCMasterDataSet_Final.csv')


@st.cache(allow_output_mutation=True)
# Function to call historical records
def load_data(nrows):
    # Function to call historical records

    # raw CP data
    data = pd.read_csv(DATA_URL, low_memory=False, encoding='utf-8', nrows=nrows)
    return data


def locationBasedExploration(midpoint):
    st.write(pdk.Deck(
        map_style="mapbox://styles / mapbox / light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=selectedCols[['Q005_NAME', 'latitude', 'longitude']],
                get_position=["longitude", "latitude"],
                auto_highlight=True,
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            ),
        ],
    ))


if __name__ == "__main__":

    st.title("EmONC Location Based Visualization")
    st.sidebar.title("Data Visualization")

    st.markdown("""
        Loading records based on slider choice
    """)
    numRecords = st.slider("", min_value=10, value=10, max_value=4000)
    data = load_data(numRecords)
    selectedCols = data[["Q005_NAME", "Q007", "altitude", "latitude", "longitude"]]
    st.write("Data", selectedCols)

    crossTabulationValue = ["Altitude", "Others"]
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    choice = st.radio("Filitering or Visualization Options:", crossTabulationValue)
    if choice == "Altitude":
        altitudeValue = st.slider("Altitude", min_value=100, value=0, max_value=2000)
        st.map(selectedCols.query("altitude >= @altitudeValue")
               [["Q005_NAME", "latitude", "longitude"]].dropna(how="any"))
    else:
        region = st.selectbox("Region", selectedCols.Q005_NAME.unique())
        healthcenter = st.selectbox("Select healthcenter or hospital", selectedCols.Q007.unique())
        # more information on df.query is found@https://www.codegrepper.com/code-examples/python/df.query+multiple+conditions
        st.map(selectedCols.query("Q005_NAME == @region & Q007 == @healthcenter")
               [["Q005_NAME", "latitude", "longitude"]].dropna(how="any"))

    # Adding code so we can have map default to the center of the data
    midpoint = (np.average(selectedCols['latitude']),
                np.average(selectedCols['longitude']))
    locationBasedExploration(midpoint)
