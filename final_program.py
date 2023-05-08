'''
Name: Alan Van Sant
CS230: Section 1
Data: US Mass Shootings
Date: May 8th, 2023

Description:
For this program I will be presenting data for Shootings that have occurred in the US.
This is the main page of the website. You can go to any page on this website by using the sidebar
on the left. There is a page which gives a summary on any mass shooting that is chosen.
Next is a page which allows you to look at demographic data of shooters. You can customize a graph
based around mass shooting weapon and victim information. There is a pie chart that shows how
many shootings involved legal weapons.  Lastly you can go to a map to see where in the country
mass shootings took place. I worked on and completed this project by myself.
'''

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import pydeck as pdk
import string


PUNCTUATION = string.punctuation


df = pd.read_csv('USMassShootings.csv', encoding='cp1252')

# Adding in an age demographic column
# This is what I am proud of
df['sum_age'] = df.SUMMARY
for obj in range(len(df.sum_age)):
    df['sum_age'][obj] = df.sum_age[obj].split(',')
    for i in range(len(df.sum_age[obj])):
        df['sum_age'][obj][i] = df.sum_age[obj][i].lstrip(' ')

df['age'] = df.sum_age
for j in range(len(df.sum_age)):
    if j == 45:
        df['age'][j] = df.sum_age[j][2]
    else:
        df['age'][j] = df.sum_age[j][1]


# Capitalizing column names (first letter only)
for col in df.columns:
    df = df.rename(columns={col:col.capitalize()})

# Making table for demographics
tbl1 = df.loc[:, ['Gender', 'Race', 'Age', 'Priorsignsofmentalillness']]
tbl1 = tbl1.rename(columns={'Priorsignsofmentalillness':'Prior signs of mental illness'})

# Making table for weapons by amount of victims graph
tbl2 = df.loc[:, ['Fatalities', 'Wounded', 'Totalvictims', 'Numweapons', 'Assault']]
tbl2 = tbl2.rename(columns={'Totalvictims':'Total victims', 'Numweapons':'Number of weapons'})
tbl2 = tbl2.rename(columns={'Assault':'Assault rifle involved'})


# Data for the pie chart
pieData = df.loc[:, ['Weaponsobtainedlegally']]
pieData = pieData.rename(columns={'Weaponsobtainedlegally':'Weapons obtained legally'})


# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Overview", "Mass Shooting Summary", "Demographics", "Weapon Information by Victim Information", "Mass Shooting Weapon Legality", "Map of Cases"])

#Introduction
if page == "Overview":
    title = '<div style="text-align:center;"><p style="font-family:Times New Roman; color:Maroon; font-size: 40px;">Python Final Project</p></div>'
    st.markdown(title, unsafe_allow_html=True)
    header = '<div style="text-align:center;"><p style="font-family:Times New Roman; color:Maroon; font-size: 40px;">Mass Shootings in the US</p></div>'
    st.markdown(header, unsafe_allow_html=True)
    header1 = '<div style="text-align:center;"><p style="font-family:Daytona; color:SkyBlue; font-size: 30px;">Overview</p></div>'
    st.markdown(header1, unsafe_allow_html=True)

    # Flag image
    from PIL import Image
    input_image = Image.open("C:\\Users\\duce8\\OneDrive - Bentley University\\Documents\\Junior\\CS230-1\\Final Project\\HalfMastFlag.jpg")
    st.image(input_image, caption="Flag at half mast due to mass shooting", width=550, use_column_width=True)

    st.write("For this project I will be presenting data for Shootings that have occurred in the US. "
             "This is the main page of the website. You can go to any page on this website by using the sidebar "
             "on the left. There is a page which gives a summary on any mass shooting that is chosen. "
             "Next is a page which allows you to look at demographic data of shooters. You can customize a graph "
             "based around mass shooting weapon and victim information. There is a pie chart that shows how "
             "many shootings involved legal weapons.  Lastly you can go to a map to see where in the country "
             "mass shootings took place.")


if page == "Mass Shooting Summary":
    st.subheader("Information about each case of a mass shooting")
    st.write("On this page, you can select any of the cases of a shooting. After doing so "
             "you will be given information about when the case happened, how many people "
             "were injured and killed, and a summary report with further detail about the shooting.")

    # For the selection box
    caselist = df["Case"].tolist()
    caseList = sorted(set(caselist))
    caseCt = {word: caselist.count(word) for word in caselist}

    selectedCase = st.selectbox("Please select a case:", caseList)
    # Getting number of cases
    if selectedCase in caseCt:
        num = caseCt[selectedCase]
    # Retrieving case, summary, year, and victim info
    caseName = df[df["Case"] == selectedCase]
    # Summary
    summaries = caseName["Summary"].tolist()
    newSum = ", ".join(summaries)
    # Year
    years = caseName["Year"].astype(str).tolist()
    newYear = ", ".join(years)
    # Victim info
    injured = caseName["Wounded"].astype(str).tolist()
    newInjur = ", ".join(injured)
    dead = caseName["Fatalities"].astype(str).tolist()
    newDead = ", ".join(dead)
    # Output
    st.write(f"The case of {selectedCase} happened in {newYear}. {newInjur} people were wounded "
             f"and {newDead} people died. In summation, {newSum}")


if page == "Demographics":
    st.subheader("Select a set of demographics of shooters")
    st.write("On this page, you will be able to select a set of demographics of shooters involved in mass shootings. "
             "You will be returned a bar chart that shows how many shooters identified with a category of the "
             "chosen demographic.")

    # Selection box for demographic type
    selectVar = st.selectbox("Choose a demographic", tbl1.columns)
    selectX = tbl1[selectVar].unique()
    selectY = tbl1.groupby(selectVar).size()


    # Graph; age is set up to display vertically, else it's at 45 degrees
    fig, ax = plt.subplots()
    if selectVar == "Age":
        ax.bar(selectX, selectY, width=1, edgecolor="white", linewidth=5)
        ax.set_xticklabels(selectX, rotation=90, ha="center")
    else:
        ax.bar(selectX, selectY, width=1, edgecolor="white", linewidth=5)
        ax.set_xticklabels(selectX, rotation=45, ha="right")
    st.pyplot(fig)


if page == "Weapon Information by Victim Information":
    st.subheader("Customize a graph detailing amount of victims based on weapon information")
    st.write("This page allows you to customize what the graph below shows. You can choose "
             "what weapon information to analyze - number of weapons used vs whether an assault "
             "rifle was involved - as well as information about victims - "
             " how many wounded, dead, or total victims.")

    # Variables for pivot table
    selectWeapon = st.selectbox("Choose weapon information", tbl2[['Number of weapons', 'Assault rifle involved']].columns)
    selectVictim = st.selectbox("Choose victim information", tbl2[['Wounded', 'Fatalities', 'Total victims']].columns)
    selectX = tbl2[selectWeapon].unique()
    selectY = tbl2.groupby(selectVictim).size()

    # Creating pivot table and bar chart
    pivot = pd.pivot_table(tbl2, values=selectVictim, index=selectWeapon, columns=selectY, fill_value=0)
    ax = pivot.plot(kind='bar')

    # The axis labels
    ax.set_xlabel(selectWeapon)
    ax.set_ylabel("Instances of " + selectVictim)

    # Output
    st.pyplot(plt.gcf())

    st.write("The legend is shows categories for the amount of victims in shootings. "
             "The Y-axis shows the amount of shootings in which the different categories "
             'from the legend happened. For example, with the default choices of "Number of weapons" '
             'and "Wounded", the tallest blue column shows the amount of instances in which only '
             'one person got hurt in shootings where the shooter had anywhere from 1-4 weapons. '
             'In shootings with 4 weapons used, there were about 40 instances of 1 person '
             'being wounded (of course more could have been killed too).')

# tbl2, x=selectWeapon, y=selectVictim


# Pie Chart Page
if page == "Mass Shooting Weapon Legality":
    st.subheader("Were the weapons involved in shootings obtained through legal methods?")
    st.write("This page shows a pie chart that tells how many shootings out of the total shootings "
             "used weapons that were obtained through legal means")

    # Counting data
    legalCount = pieData['Weapons obtained legally'].value_counts()
    legality = legalCount[:10]

    # Creating lists for labels and values
    labels = legality.index.tolist()
    vals = legality.values.tolist()

    # Creating pie chart
    fig, ax = plt.subplots()
    ax.axis('equal')
    forExp = [0] * len(legality)
    max = vals.index(max(vals))
    forExp[max] = 0.1

    ax.pie(vals, labels=labels, explode=forExp, autopct='%.1f%%')
    ax.set_title('Proportion of Weapons in Mass Shootings being Legal')
    st.pyplot(fig)


# Map Page
if page == "Map of Cases":
    st.subheader("Map of US Mass Shootings")
    st.write("On this page you can see a map of the US with locations of where different "
             "mass shootings too place. If you hover your mouse over a one of the locations, "
             "a textbox will appear which gives the name of the shooting as well as the total "
             "amount of people who were either injured or killed.")

    # Allows for customizable tilt
    SelectPitch = st.slider('Select the level of pitch (tilt) : ', min_value=0, max_value=60, value=0, step=1)

    # Creating table for map data
    mapTbl = df[["Case", "Totalvictims", "Latitude", "Longitude"]]

    # Initial state of map (and custom pitch)
    view_state = pdk.ViewState(
        latitude=40,
        longitude=-95,
        zoom=3,
        pitch=SelectPitch)

    # Create map layer
    layer1 = pdk.Layer(type='ScatterplotLayer',
                       data=mapTbl,
                       get_position='[Longitude, Latitude]',
                       get_radius=14000,
                       get_color=[0, 0, 255],
                       pickable=True
                       )

    # Map layer #2
    layer2 = pdk.Layer('ScatterplotLayer',
                       data=mapTbl,
                       get_position='[Longitude, Latitude]',
                       get_radius=9000,
                       get_color=[255, 0, 255],
                       pickable=True
                       )

    # Info given on mouse hover
    tool_tip = {"html": "Case: <b>{Case}</b> <br>Total Victims: <b>{Totalvictims}</b>",
                "style": {"backgroundColor": "white",
                          "color": "red"}
                }

    # Create map
    map1 = pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=view_state,
        layers=[layer1, layer2],
        tooltip=tool_tip
    )

    st.pydeck_chart(map1)

