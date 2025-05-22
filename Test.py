import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("🔥 온도 & 농도에 따른 반응 속도 시뮬레이터")

# 반응물 선택 (예시)
reactant = st.selectbox("반응물 선택", ["A", "B", "C"])

# 반응물별 상수 설정 (예: Ea, A)
# (필요하면 다양하게 확장 가능)
params = {
    "A": {"A": 1000, "Ea": 50000},
    "B": {"A": 2000, "Ea": 60000},
    "C": {"A": 1500, "Ea": 55000},
}

temperature = st.slider("온도 설정 (℃)", 0, 100, 25)
concentration = st.slider("반응물 농도 [A] (mol/L)", 0.1, 2.0, 1.0, step=0.1)

R = 8.314  # 기체 상수 (J/mol·K)
reaction_order = 1  # 1차 반응 가정

A_factor = params[reactant]["A"]
Ea = params[reactant]["Ea"]

def rate_constant(T):
    T_K = T + 273.15
    return A_factor * math.exp(-Ea / (R * T_K))

def reaction_rate(k, conc):
    return k * (conc ** reaction_order)

k_now = rate_constant(temperature)
rate_now = reaction_rate(k_now, concentration)
reaction_time = 1 / rate_now if rate_now != 0 else float('inf')

st.markdown(f"### ✅ 현재 조건 (반응물: **{reactant}**)")
st.write(f"🌡️ 온도: **{temperature} ℃**")
st.write(f"🧪 농도: **{concentration:.2f} mol/L**")
st.write(f"⚙️ 반응 속도 상수 k: `{k_now:.3e}`")
st.write(f"⚡ 반응 속도 (Rate): `{rate_now:.3e} mol/L·s`")
st.write(f"⏱️ 예측 반응 시간: `{reaction_time:.3e} 초`")

temps = np.arange(0, 101, 1)
k_values = [rate_constant(t) for t in temps]
rates = [reaction_rate(k, concentration) for k in k_values]

fig, ax = plt.subplots()
ax.plot(temps, rates, label=f"Reaction rate at concentration {concentration:.2f} mol/L", color='green')
ax.set_xlabel("Temperature (℃)")
ax.set_ylabel("Reaction Rate (mol/L·s)")
ax.set_title(f"Effect of Temperature on Reaction Rate ({reactant})")
ax.legend()
ax.grid(True)

fig.tight_layout()
st.pyplot(fig)
