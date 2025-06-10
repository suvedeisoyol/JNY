import pandas as pd
import numpy as np
import streamlit as st


# function

@st.fragment()   
def display_df():
    df = pd.read_csv("colors_inventory.csv")
    st.dataframe(df)

# importing csv file
df = pd.read_csv("colors_inventory.csv")
brand_names = df["Brand"].unique()

# Creating selectbox for receiving or stocking

option = st.sidebar.radio("Choose", ("Receiving", "Stocking", "Edit"))

if option == "Receiving":
    
    brand_option = st.selectbox(
        "Select Brand of the Color",
        brand_names,
    )
    st.write("You Selected:", brand_option)

    # Adding new color to the DF
    st.write("Adding new Color: ")
    color = st.text_input("Enter the color")
    total = st.text_input(f"Enter total quantity for {color}", value = 0)

    if st.button("insert"):
        df.loc[len(df)] = [brand_option, color, total, 0]
        df.to_csv("colors_inventory.csv", index=False)

    # updating color using empty  

    # Updating received product to the Inventory
    st.write("Input receiving order: ")
    brand_df = df.query("Brand == @brand_option")

    update_df = pd.DataFrame()
    color_name = brand_df["Color"].unique()

    update_df["Color"] = color_name
    update_df["Received"] = 0
    update_df = st.data_editor(update_df)

        # updating df
    for index, row in update_df.iterrows():
        df.loc[(df["Brand"] == brand_option) & (df["Color"] == row["Color"]), "Stock" ] += row["Received"]
    if st.button("Update"):
        st.write(update_df.query("Received > 0"))
        df.to_csv("colors_inventory.csv", index=False)

if option == "Edit":
    brand_option = st.selectbox(
        "Select Brand of the Color to add color",
        brand_names,
    )
    color = st.text_input("Enter the color").upper()
    if st.button("insert"):
        df.loc[len(df)] = [brand_option, color, 0, 0]
        df.to_csv("colors_inventory.csv", index=False)

    edited_df = st.data_editor(df.sort_values(by = ["Brand", "Color"]))
    if st.button("done"):
        edited_df.to_csv("colors_inventory.csv", index=False)

if option == "Stocking":
    brand_option = st.selectbox(
        "Select Brand of the Color",
        brand_names,
    )
    st.write("You Selected:", brand_option)


    brand_df = df.query("Brand == @brand_option")

    st.display(brand_df)
    
    update_df = pd.DataFrame()
    color_name = brand_df["Color"].unique()

    update_df["Color"] = color_name
    update_df["on Stock"] = brand_df["Stock"]
    update_df["Stocking"] = 0
    update_df = st.data_editor(update_df)

        # updating df
    for index, row in update_df.iterrows():
        df.loc[(df["Brand"] == brand_option) & (df["Color"] == row["Color"]), "Stock" ] -= row["Stocking"]
    if st.button("Update"):
        st.write(update_df.query("Stocking > 0"))
        df.to_csv("colors_inventory.csv", index=False)

if st.button("display"):
    display_df()   
