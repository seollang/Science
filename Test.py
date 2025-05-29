import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("🔥 온도에 따른 반응 속도 시뮬레이터")

# 반응 예시: 반응명 → (A, Ea, 반응식)
reactions = {
    "싸이오황산 나트륨 + 염산": {
        "A": 1.0e6,
        "Ea": 60000,
        "equation": "Na₂S₂O₃ + 2HCl → 2NaCl + SO₂ + S↓ + H₂O"
    },
    "과산화수소 분해": {
        "A": 1.2e7,
        "Ea": 75000,
        "equation": "2H₂O₂ → 2H₂O + O₂"
    },
    "요오드화 수소 열분해": {
        "A": 5.0e10,
        "Ea": 100000,
        "equation": "2HI → H₂ + I₂"
    }
}

reaction_name = st.selectbox("반응을 선택하세요", list(reactions.keys()))

reaction_data = reactions[reaction_name]
A_factor = reaction_data["A"]
Ea = reaction_data["Ea"]
reaction_equation = reaction_data["equation"]

temperature = st.slider("온도 설정 (°C)", 0, 100, 25)
concentration = st.slider("반응물 농도 (mol/L)", 0.01, 2.5, 0.10, step=0.01)

R = 8.314  # J/mol·K
reaction_order = 1

def rate_constant(T):
    T_K = T + 273.15
    return A_factor * math.exp(-Ea / (R * T_K))

def reaction_rate(k, conc):
    return k * (conc ** reaction_order)

k_now = rate_constant(temperature)
rate_now = reaction_rate(k_now, concentration)
reaction_time = 1 / rate_now if rate_now != 0 else float('inf')

st.markdown("### ✅ 현재 조건")
st.write(f"**선택한 반응:** {reaction_name}")
st.latex(f"{reaction_equation}")
st.write(f"🌡️ 온도: **{temperature} °C**")
st.write(f"🧪 농도: **{concentration:.2f} mol/L**")
st.write(f"⚙️ 반응 속도 상수 k: `{k_now:.5e} s⁻¹`")
st.write(f"⚡ 반응 속도: `{rate_now:.3f} mol/(L·s)`")
st.write(f"⏱️ 예측 반응 시간: `{reaction_time:.2f} 초`")

temps = np.arange(0, 101, 1)
k_values = [rate_constant(t) for t in temps]
rates = [reaction_rate(k, concentration) for k in k_values]

fig, ax = plt.subplots()
ax.plot(temps, rates, label=f"{reaction_name} at {concentration:.2f} mol/L", color='darkblue')
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Reaction Rate (mol/(L·s))")
ax.set_title("Temperature Effect on Reaction Rate")
ax.legend()
ax.grid(True)

fig.tight_layout()
st.pyplot(fig)
