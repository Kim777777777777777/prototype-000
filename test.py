import streamlit as st
import time
import subprocess
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_title="타이머 & 자동 종료",
    page_icon="⏱️",
    layout="centered"
)

st.title("⏱️ 자동 종료 타이머")
st.markdown("일정 시간 후 자동으로 컴퓨터를 종료합니다.")

# 세션 상태 초기화
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
    st.session_state.remaining_time = 0
    st.session_state.countdown_mode = False

# 타이머 설정
col1, col2, col3 = st.columns(3)

with col1:
    hours = st.number_input("시간", min_value=0, max_value=23, value=0)

with col2:
    minutes = st.number_input("분", min_value=0, max_value=59, value=5)

with col3:
    seconds = st.number_input("초", min_value=0, max_value=59, value=0)

# 총 시간 (초 단위)
total_seconds = hours * 3600 + minutes * 60 + seconds

st.divider()

# 시작/중지 버튼
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ 시작", use_container_width=True, type="primary"):
        st.session_state.timer_running = True
        st.session_state.remaining_time = total_seconds
        st.session_state.countdown_mode = False

with col2:
    if st.button("⏸️ 중지", use_container_width=True):
        st.session_state.timer_running = False

with col3:
    if st.button("🔄 리셋", use_container_width=True):
        st.session_state.timer_running = False
        st.session_state.remaining_time = 0
        st.session_state.countdown_mode = False

st.divider()

# 타이머 표시
placeholder = st.empty()
countdown_placeholder = st.empty()

def play_siren():
    """Mac에서 사이렌 소리 재생"""
    try:
        # Mac의 기본 알람 사운드 재생
        os.system('afplay /System/Library/Sounds/Alarm.aiff &')
    except:
        st.warning("사이렌 소리 재생에 실패했습니다.")

def shutdown_computer():
    """Mac 컴퓨터 종료"""
    try:
        os.system('osascript -e "tell application \"System Events\" to shut down"')
    except:
        st.error("컴퓨터 종료에 실패했습니다.")

# 타이머 실행 로직
if st.session_state.timer_running:
    # 타이머가 실행 중일 때
    if st.session_state.remaining_time > 0:
        # 남은 시간 표시
        hours_left = st.session_state.remaining_time // 3600
        minutes_left = (st.session_state.remaining_time % 3600) // 60
        seconds_left = st.session_state.remaining_time % 60
        
        with placeholder.container():
            st.markdown(f"""
            <div style="text-align: center; padding: 40px; background-color: #f0f0f0; border-radius: 10px;">
                <h1 style="font-size: 60px; margin: 0;">
                    {hours_left:02d}:{minutes_left:02d}:{seconds_left:02d}
                </h1>
                <p style="font-size: 20px; color: #666;">남은 시간</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.session_state.remaining_time -= 1
        time.sleep(1)
        st.rerun()
    
    elif not st.session_state.countdown_mode:
        # 타이머 종료, 카운트다운 시작
        st.session_state.countdown_mode = True
        play_siren()
        st.rerun()
    
    else:
        # 10초 카운트다운
        for countdown in range(10, 0, -1):
            with countdown_placeholder.container():
                st.markdown(f"""
                <div style="text-align: center; padding: 40px; background-color: #ff6b6b; border-radius: 10px; color: white;">
                    <h1 style="font-size: 80px; margin: 0;">{countdown}</h1>
                    <p style="font-size: 24px;">컴퓨터가 종료됩니다...</p>
                </div>
                """, unsafe_allow_html=True)
            
            # 계속 사이렌 재생
            play_siren()
            time.sleep(1)
        
        # 컴퓨터 종료
        st.error("⚠️ 컴퓨터를 종료합니다!")
        shutdown_computer()
        st.session_state.timer_running = False

else:
    # 타이머가 실행 중이지 않을 때
    hours_left = total_seconds // 3600
    minutes_left = (total_seconds % 3600) // 60
    seconds_left = total_seconds % 60
    
    with placeholder.container():
        st.markdown(f"""
        <div style="text-align: center; padding: 40px; background-color: #e3f2fd; border-radius: 10px;">
            <h1 style="font-size: 60px; margin: 0;">
                {hours_left:02d}:{minutes_left:02d}:{seconds_left:02d}
            </h1>
            <p style="font-size: 20px; color: #666;">설정된 시간</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# 안내 메시지
st.info("""
⚠️ **주의사항:**
- 시작 버튼을 클릭하면 설정된 시간 후 자동 종료됩니다
- Mac 사용자는 관리자 권한이 필요할 수 있습니다
- 중지 버튼으로 언제든 중단할 수 있습니다
""")