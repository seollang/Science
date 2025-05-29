import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("🧪 온도에 따른 반응 속도 시뮬레이터")

# 반응 예시: 반응명 → (A, Ea)
reactions = {
    "싸이오황산 나트륨 + 염산": {"A": 1.0e6, "Ea": 60000},
    "과산화수소 분해 반응": {"A": 1.2e7, "Ea": 75000},
    "요오드화 수소 열분해": {"A": 5.0e10, "Ea": 100000},
    "아세트산 + 수산화나트륨 중화 반응": {"A": 2.0e5, "Ea": 30000}
}

reaction_name = st.selectbox("반응 선택", list(reactions.keys()))

# 사용자 입력 슬라이더
temperature = st.slider("온도 설정 (℃)", 0, 100, 25)
concentration = st.slider("반응물 농도 (mol/L)", 0.01, 2.5, 0.10, step=0.01)

# 상수 정의
R = 8.314  # 기체 상수 (J/mol·K)
reaction_order = 1  # 1차 반응 가정

# 선택된 반응 정보
A_factor = reactions[reaction_name]["A"]
Ea = reactions[reaction_name]["Ea"]

# 계산 함수
def rate_constant(T):
    T_K = T + 273.15
    return A_factor * math.exp(-Ea / (R * T_K))

def reaction_rate(k, conc):
    return k * (conc ** reaction_order)

# 현재 조건 계산
k_now = rate_constant(temperature)
rate_now = reaction_rate(k_now, concentration)
reaction_time = 1 / rate_now if rate_now != 0 else float('inf')

# 결과 출력
st.markdown("### ✅ 현재 조건")
st.write(f"🔬 반응: **{reaction_name}**")
st.write(f"🌡️ 온도: **{temperature} ℃**")
st.write(f"🧪 농도: **{concentration:.2f} mol/L**")
st.write(f"⚙️ 반응 속도 상수 k: `{k_now:.5e} s⁻¹`")
st.write(f"⚡ 반응 속도: `{rate_now:.3f} mol/(L·s)`")
st.write(f"⏱️ 예측 반응 시간 (역수 기준): `{reaction_time:.2f} 초`")

# 그래프 출력
temps = np.arange(0, 101, 1)
k_values = [rate_constant(t) for t in temps]
rates = [reaction_rate(k, concentration) for k in k_values]

fig, ax = plt.subplots()
ax.plot(temps, rates, label=f"{reaction_name}, 농도 {concentration:.2f} mol/L", color='darkorange')
ax.set_xlabel("온도 (℃)")
ax.set_ylabel("반응 속도 (mol/(L·s))")
ax.set_title(f"온도에 따른 반응 속도 변화: {reaction_name}")
ax.legend()
ax.grid(True)

fig.tight_layout()
st.pyplot(fig)
