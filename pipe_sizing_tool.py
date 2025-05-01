# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 17:46:15 2025

@author: AsfiyaKhanam
"""

import streamlit as st
import math

st.title("DLE Pipe Sizing Calculator")

# Step 1: Column Geometry
st.header("1. Column Geometry and Bed Volume")

diameter_mm = st.number_input("Column Diameter (mm)", min_value=0.0)
height_mm = st.number_input("Column Height (mm)", min_value=0.0)

diameter_m = diameter_mm / 1000
height_m = height_mm / 1000
bed_volume_m3 = math.pi * (diameter_m / 2) ** 2 * height_m

st.write(f"**Bed Volume:** {bed_volume_m3:.4f} m³")

# Step 2: Flowrate Conversion (No input here)
st.header("2. Base Flowrate Conversion")

one_bv_l_hr = bed_volume_m3 * 1000
st.write(f"**1 BV/hr = {one_bv_l_hr:.2f} L/hr**")

# Step 3: Flowrate Input and Initial Diameter Estimate
st.header("3. Pipe Flowrate and Rule-of-Thumb Diameter")

pipe_bv_per_hr = st.number_input("Pipe Flowrate (BV/hr)", min_value=0.0)

pipe_flow_l_hr = pipe_bv_per_hr * one_bv_l_hr
pipe_flow_m3_hr = pipe_flow_l_hr / 1000
pipe_flow_m3_s = pipe_flow_m3_hr / 3600
pipe_flow_gpm = pipe_flow_l_hr / (3.785 * 60)

# Rule-of-thumb pipe diameter estimate
initial_diameter_in = math.sqrt(pipe_flow_gpm / 20)

st.write(f"**Pipe Flowrate:** {pipe_flow_gpm:.2f} GPM")
st.write(f"**Initial Pipe Diameter (Rule of Thumb):** {initial_diameter_in:.2f} in")

# Step 4: Velocity Calculation for Initial Diameter
st.header("4. Velocity for Estimated Diameter")

diameter_m = initial_diameter_in * 0.0254
pipe_area_m2 = math.pi * (diameter_m ** 2) / 4
velocity_m_s = pipe_flow_m3_s / pipe_area_m2

st.write(f"**Calculated Velocity:** {velocity_m_s:.2f} m/s")

# Step 5: Target Velocity Input
st.header("5. Target Velocity")

target_velocity = st.number_input("Enter Target Velocity (m/s)", min_value=0.01)

# Step 6: Velocity Check and Adjusted Diameter
st.header("6. Velocity Check and Adjusted Diameter")

if abs(velocity_m_s - target_velocity) > 0.01:
    required_diameter_m = math.sqrt((4 * pipe_flow_m3_s) / (math.pi * target_velocity))
    required_diameter_in = required_diameter_m / 0.0254

    # Round up to nearest standard pipe size
    standard_pipe_sizes = [
        0.5, 0.75, 1, 1.25, 1.5, 2, 2.5, 3, 4, 5,
        6, 8, 10, 12, 14, 16, 18, 20, 24
    ]
    suggested_size = next((size for size in standard_pipe_sizes if size >= required_diameter_in), None)

    st.warning("⚠️ Velocity mismatch.")
    st.write(f"Calculated Required Diameter: **{required_diameter_in:.2f} in**")

    if suggested_size:
        suggested_diameter_m = suggested_size * 0.0254
        suggested_area_m2 = math.pi * (suggested_diameter_m ** 2) / 4
        suggested_velocity = pipe_flow_m3_s / suggested_area_m2

        st.success(f"🔧 Suggested Standard Pipe Size: **{suggested_size} in**")
        st.write(f"Estimated Velocity at {suggested_size} in: **{suggested_velocity:.2f} m/s**")
    else:
        st.error("❌ No suitable standard pipe size found (diameter too large).")
else:
    st.success("✅ Calculated velocity matches target velocity.")
