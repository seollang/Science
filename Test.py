import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("🔥 온도 & 농도에 따른 반응 속도 시뮬레이터")

reactants = {
    "과산화수소 (Hydrogen Peroxide, H₂O₂)": {"A": 1.2e7, "Ea": 75000},
    "아세트산 (Acetic Acid, CH₃COOH)": {"A": 3.5e9, "Ea": 92000},
    "요오드화 칼륨 (Potassium Iodide, KI)": {"A": 8.0e6, "Ea": 68000},
}

reactant_name = st.selectbox("반응물 선택", list(reactants.keys()))

temperature = st.slider("온도 설정 (℃)", 0, 150, 25)  # 최대 150도까지 확대
concentration = st.slider("반응물 농도 (mol/L)", 0.1, 5.0, 1.0, step=0.1)  # 최대 농도 5mol/L로 확대

R = 8.314  
reaction_order = 1  

A_factor = reactants[reactant_name]["A"]
Ea = reactants[reactant_name]["Ea"]

def rate_constant(T):
    T_K = T + 273.15
    return A_factor * math.exp(-Ea / (R * T_K))

def reaction_rate(k, conc):
    return k * (conc ** reaction_order)

k_now = rate_constant(temperature)
rate_now = reaction_rate(k_now, concentration)
reaction_time = 1 / rate_now if rate_now != 0 else float('inf')

st.markdown(f"### ✅ 현재 조건 (반응물: **{reactant_name}**)")
st.write(f"🌡️ 온도: **{temperature} ℃**")
st.write(f"🧪 농도: **{concentration:.2f} mol/L**")
st.write(f"⚙️ 반응 속도 상수 k: `{k_now:.5e}`")
st.write(f"⚡ 반응 속도 (Rate): `{rate_now:.3f} mol/(L·s)`")
st.write(f"⏱️ 예측 반응 시간: `{reaction_time:.3f} 초`")

temps = np.arange(0, 151, 1)  # 온도 범위 0~150도
k_values = [rate_constant(t) for t in temps]
rates = [reaction_rate(k, concentration) for k in k_values]

fig, ax = plt.subplots()
ax.plot(temps, rates, label=f"Reaction rate at concentration {concentration:.2f} mol/L", color='green')
ax.set_xlabel("Temperature (℃)")
ax.set_ylabel("Reaction Rate (mol/(L·s))")
ax.set_title(f"Effect of Temperature on Reaction Rate ({reactant_name})")
ax.legend()
ax.grid(True)

fig.tight_layout()
st.pyplot(fig)
