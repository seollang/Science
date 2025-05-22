import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("🔥 Reaction Rate Simulator: Effect of Temperature & Concentration")

# User inputs
temperature = st.slider("Temperature (℃)", 0, 100, 25)
concentration = st.slider("Reactant Concentration [A] (mol/L)", 0.1, 2.0, 1.0, step=0.1)

# Constants
R = 8.314      # Gas constant (J/mol·K)
A = 1000       # Frequency factor
Ea = 50000     # Activation energy (J/mol)
reaction_order = 1  # Reaction order (assumed 1st order)

# Functions to calculate rate constant and reaction rate
def rate_constant(T):
    T_K = T + 273.15
    return A * math.exp(-Ea / (R * T_K))

def reaction_rate(k, conc):
    return k * (conc ** reaction_order)

k_now = rate_constant(temperature)
rate_now = reaction_rate(k_now, concentration)
reaction_time = 1 / rate_now if rate_now != 0 else float('inf')

# Display results
st.markdown("### ✅ Current Conditions")
st.write(f"🌡️ Temperature: **{temperature}℃**")
st.write(f"🧪 Concentration: **{concentration} mol/L**")
st.write(f"⚙️ Rate constant k: `{k_now:.5f}`")
st.write(f"⚡ Reaction rate (Rate): `{rate_now:.5f}` mol/L·s")
st.write(f"⏱️ Estimated reaction time: `{reaction_time:.2f}` seconds")

# Plot reaction rate vs temperature
temps = np.arange(0, 101, 1)
k_values = [rate_constant(t) for t in temps]
rates = [reaction_rate(k, concentration) for k in k_values]

fig, ax = plt.subplots()
ax.plot(temps, rates, label=f"Reaction rate at concentration {concentration} mol/L", color='green')
ax.set_xlabel("Temperature (℃)")
ax.set_ylabel("Reaction Rate (mol/L·s)")
ax.set_title("Effect of Temperature on Reaction Rate")
ax.legend()
ax.grid(True)

fig.tight_layout()
st.pyplot(fig)
