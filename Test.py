import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("🧪 Temperature vs. Reaction Rate Simulator")

# 반응 예시: 반응명 → (A, Ea, 반응식)
reactions = {
    "Sodium thiosulfate + Hydrochloric acid": {
        "A": 1.0e6,
        "Ea": 60000,
        "equation": "Na₂S₂O₃ + 2HCl → 2NaCl + SO₂ + S↓ + H₂O"
    },
    "Hydrogen peroxide decomposition": {
        "A": 1.2e7,
        "Ea": 75000,
        "equation": "2H₂O₂ → 2H₂O + O₂"
    },
    "Hydrogen iodide decomposition": {
        "A": 5.0e10,
        "Ea": 100000,
        "equation": "2HI → H₂ + I₂"
    }
}

# 사용자 선택
reaction_name = st.selectbox("Select a reaction", list(reactions.keys()))

# 반응 정보 불러오기
reaction_data = reactions[reaction_name]
A_factor = reaction_data["A"]
Ea = reaction_data["Ea"]
reaction_equation = reaction_data["equation"]

# 사용자 입력 슬라이더
temperature = st.slider("Temperature (°C)", 0, 100, 25)
concentration = st.slider("Reactant Concentration (mol/L)", 0.01, 2.5, 0.10, step=0.01)

# 상수 및 계산 함수
R = 8.314  # J/mol·K
reaction_order = 1

def rate_constant(T):
    T_K = T + 273.15
    return A_factor * math.exp(-Ea / (R * T_K))

def reaction_rate(k, conc):
    return k * (conc ** reaction_order)

# 계산 결과
k_now = rate_constant(temperature)
rate_now = reaction_rate(k_now, concentration)
reaction_time = 1 / rate_now if rate_now != 0 else float('inf')

# 결과 출력
st.markdown("### ✅ Current Conditions")
st.write(f"**Selected Reaction:** {reaction_name}")
st.latex(f"{reaction_equation}")
st.write(f"🌡️ Temperature: **{temperature} °C**")
st.write(f"🧪 Concentration: **{concentration:.2f} mol/L**")
st.write(f"⚙️ Rate constant (k): `{k_now:.5e} s⁻¹`")
st.write(f"⚡ Reaction rate: `{rate_now:.3f} mol/(L·s)`")
st.write(f"⏱️ Estimated time (1/rate): `{reaction_time:.2f} s`")

# 그래프
temps = np.arange(0, 101, 1)
k_values = [rate_constant(t) for t in temps]
rates = [reaction_rate(k, concentration) for k in k_values]

fig, ax = plt.subplots()
ax.plot(temps, rates, label=f"{reaction_name} at {concentration:.2f} mol/L", color='darkorange')
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Reaction Rate (mol/(L·s))")
ax.set_title(f"Effect of Temperature on Reaction Rate")
ax.legend()
ax.grid(True)

fig.tight_layout()
st.pyplot(fig)
