import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("🔥 온도 & 농도에 따른 반응 속도 시뮬레이터")

temperature = st.slider("온도 설정 (℃)", 0, 100, 25)
concentration = st.slider("반응물 농도 [A] (mol/L)", 0.1, 2.0, 1.0, step=0.1)

R = 8.314      # 기체 상수 (J/mol·K)
A = 1000       # 빈도 인자
Ea = 50000     # 활성화 에너지 (J/mol)
reaction_order = 1  # 반응 차수 (1차 가정)

def rate_constant(T):
    T_K = T + 273.15
    return A * math.exp(-Ea / (R * T_K))

def reaction_rate(k, conc):
    return k * (conc ** reaction_order)

k_now = rate_constant(temperature)
rate_now = reaction_rate(k_now, concentration)
reaction_time = 1 / rate_now if rate_now != 0 else float('inf')

st.markdown("### ✅ 현재 조건")
st.write(f"🌡️ 온도: **{temperature}℃**")
st.write(f"🧪 농도: **{concentration} mol/L**")
st.write(f"⚙️ 반응 속도 상수 k: `{k_now:.5f}`")
st.write(f"⚡ 반응 속도 (Rate): `{rate_now:.5f}` mol/L·s")
st.write(f"⏱️ 예측 반응 시간: `{reaction_time:.2f}` 초")

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
