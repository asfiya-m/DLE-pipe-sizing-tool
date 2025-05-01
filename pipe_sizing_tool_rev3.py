# -*- coding: utf-8 -*-
"""
Created on Thu May  1 11:08:24 2025

@author: AsfiyaKhanam
"""

import streamlit as st
import math

st.title("🔁 DLE Pipe Sizing & Flowrate Calculator")
st.markdown("""
### 💡 What This App Does
This tool helps engineers working on Direct Lithium Extraction (DLE) systems calculate:
- Pipe diameter based on bed volume and flowrate
- Velocity checks against target values
- Flowrate based on a selected pipe diameter
- Header sizing for multiple columns

Use the dropdown above to choose your task and get started!
""")


# Select calculation mode
mode = st.selectbox("Choose calculation mode:", [
    "Calculate Pipe Diameter (from flowrate)",
    "Calculate Flowrate (from pipe diameter)",
    "Calculate Header Size (from flowrate and number of columns)"
])

# Column dimensions input
st.header("1. Column Dimensions")
column_diameter_mm = st.number_input("Enter Column Diameter (mm):", min_value=1.0)
column_height_mm = st.number_input("Enter Column Height (mm):", min_value=1.0)

# Calculate bed volume
column_diameter_m = column_diameter_mm / 1000
column_height_m = column_height_mm / 1000
bed_volume_m3 = math.pi * (column_diameter_m ** 2) / 4 * column_height_m
bed_volume_L = bed_volume_m3 * 1000
st.write(f"🧮 **Bed Volume:** {bed_volume_m3:.3f} m³ ({bed_volume_L:.2f} L)")

# Common pipe sizes
standard_pipe_sizes = [
    0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5,
    6, 8, 10, 12, 14, 16, 18, 20, 24
]

if mode == "Calculate Pipe Diameter (from flowrate)":
    st.header("2. Flowrate Input (in BV/hr)")
    pipe_flowrate_bvhr = st.number_input("Enter flowrate through pipe (BV/hr):", min_value=0.01)
    
    # Convert BV/hr → L/hr → GPM
    pipe_flow_Lhr = pipe_flowrate_bvhr * bed_volume_L
    pipe_flow_gpm = pipe_flow_Lhr / (3.785*60)
    st.write(f"💧 Flowrate: {pipe_flow_Lhr:.2f} L/hr | {pipe_flow_gpm:.2f} gpm")
    
    # Step 3: Diameter using rule of thumb
    diameter_in = math.sqrt(pipe_flow_gpm / 20)
    st.write(f"📏 Calculated Pipe Diameter: {diameter_in:.2f} in")
    
    # Step 4: Calculate velocity
    diameter_m = diameter_in * 0.0254
    pipe_area_m2 = math.pi * (diameter_m ** 2) / 4
    pipe_flow_m3_s = pipe_flow_Lhr / (1000 * 3600)
    velocity_m_s = pipe_flow_m3_s / pipe_area_m2
    st.write(f"🏃 Velocity: {velocity_m_s:.2f} m/s")
    
    # Step 5: Target velocity check
    st.header("3. Target Velocity Check")
    target_velocity = st.number_input("Enter Target Velocity (m/s):", min_value=0.01)
    
    st.header("4. Velocity Check and Suggested Pipe Size")
    if abs(velocity_m_s - target_velocity) > 0.01:
        # Calculate required diameter
        required_diameter_m = math.sqrt((4 * pipe_flow_m3_s) / (math.pi * target_velocity))
        required_diameter_in = required_diameter_m / 0.0254

        # Round up to standard size
        suggested_size = next((size for size in standard_pipe_sizes if size >= required_diameter_in), None)

        st.warning("⚠️ Velocity mismatch.")
        st.write(f"Required Diameter: **{required_diameter_in:.2f} in**")

        if suggested_size:
            suggested_diameter_m = suggested_size * 0.0254
            suggested_area_m2 = math.pi * (suggested_diameter_m ** 2) / 4
            suggested_velocity = pipe_flow_m3_s / suggested_area_m2

            st.success(f"🔧 Suggested Standard Pipe Size: **{suggested_size} in**")
            st.write(f"Velocity at {suggested_size} in: **{suggested_velocity:.2f} m/s**")
        else:
            st.error("❌ No standard pipe size found.")
    else:
        st.success("✅ Calculated velocity matches target velocity.")

elif mode == "Calculate Flowrate (from pipe diameter)":
    st.header("2. Pipe Diameter Input")
    input_diameter_in = st.number_input("Enter Pipe Diameter (in):", min_value=0.1)
    input_velocity = st.number_input("Enter Target Velocity (m/s):", min_value=0.01)

    input_diameter_m = input_diameter_in * 0.0254
    input_area_m2 = math.pi * (input_diameter_m ** 2) / 4

    # Calculate flowrate in m³/s → L/hr → BV/hr
    flowrate_m3_s = input_velocity * input_area_m2
    flowrate_L_hr = flowrate_m3_s * 1000 * 3600
    flowrate_bv_hr = flowrate_L_hr / bed_volume_L

    st.write(f"💧 Flowrate: {flowrate_L_hr:.2f} L/hr")
    st.write(f"📦 Flowrate in BV/hr: **{flowrate_bv_hr:.2f} BV/hr**")

elif mode == "Calculate Header Size (from flowrate and number of columns)":
    st.header("2. Header Flowrate Input (in BV/hr)")
    number_of_columns = st.number_input("Enter Number of Columns:", min_value=1, step=1)
    column_flowrate_bvhr = st.number_input("Enter Flowrate through each column (BV/hr):", min_value=0.01)

    # Calculate total flowrate
    total_flow_bvhr = number_of_columns * column_flowrate_bvhr
    st.write(f"📦 Total Flowrate through all columns: **{total_flow_bvhr:.2f} BV/hr**")

    # Convert total flow to L/hr and GPM
    total_flow_Lhr = total_flow_bvhr * bed_volume_L
    total_flow_gpm = total_flow_Lhr / (3.785 * 60)
    st.write(f"💧 Total Flowrate: {total_flow_Lhr:.2f} L/hr | {total_flow_gpm:.2f} gpm")

    # Step 3: Header Diameter using rule of thumb
    header_diameter_in = math.sqrt(total_flow_gpm / 20)
    st.write(f"📏 Calculated Header Diameter: {header_diameter_in:.2f} in")

    # Step 4: Calculate velocity through header
    header_diameter_m = header_diameter_in * 0.0254
    header_area_m2 = math.pi * (header_diameter_m ** 2) / 4
    header_flow_m3_s = total_flow_Lhr / (1000 * 3600)
    header_velocity_m_s = header_flow_m3_s / header_area_m2
    st.write(f"🏃 Velocity through Header: {header_velocity_m_s:.2f} m/s")

    # Step 5: Target velocity check for header
    st.header("3. Target Velocity Check")
    target_velocity_header = st.number_input("Enter Target Velocity (m/s) for Header:", min_value=0.01)

    st.header("4. Velocity Check and Suggested Header Size")
    if abs(header_velocity_m_s - target_velocity_header) > 0.01:
        # Calculate required diameter for header
        required_header_diameter_m = math.sqrt((4 * header_flow_m3_s) / (math.pi * target_velocity_header))
        required_header_diameter_in = required_header_diameter_m / 0.0254

        # Round up to standard size
        suggested_header_size = next((size for size in standard_pipe_sizes if size >= required_header_diameter_in), None)

        st.warning("⚠️ Velocity mismatch.")
        st.write(f"Required Header Diameter: **{required_header_diameter_in:.2f} in**")

        if suggested_header_size:
            suggested_header_diameter_m = suggested_header_size * 0.0254
            suggested_header_area_m2 = math.pi * (suggested_header_diameter_m ** 2) / 4
            suggested_header_velocity = header_flow_m3_s / suggested_header_area_m2

            st.success(f"🔧 Suggested Standard Header Size: **{suggested_header_size} in**")
            st.write(f"Velocity at {suggested_header_size} in: **{suggested_header_velocity:.2f} m/s**")
        else:
            st.error("❌ No standard header size found.")
    else:
        st.success("✅ Calculated velocity through header matches target velocity.")
