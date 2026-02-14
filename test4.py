import streamlit as st
import time
import os
import threading
import subprocess
from datetime import datetime, timedelta
import tempfile

st.set_page_config(page_title="타이머", page_icon="⏱️", layout="wide")

# 언어 데이터
LANGS = {
    "한국어": {
        "title": "⏱️ 타이머 앱",
        "lang": "🌐 언어",
        "timer": "📋 타이머",
        "time_limit": "⏱️ 시간 제한",
        "app_usage": "💻 앱 사용시간",
        "sleep_time": "😴 자는시간",
        "rest_time": "☕ 쉬는시간",
        "hours": "시간",
        "minutes": "분",
        "seconds": "초",
        "start": "▶️ 시작",
        "stop": "⏸️ 중지",
        "reset": "🔄 리셋",
        "test": "🔊 테스트",
        "remaining": "남은 시간",
        "set_time": "설정된 시간",
        "countdown": "⏰ 10초 이내!",
        "finished": "⚠️ 시간 종료!",
        "siren": "엄청난 사이렌이 울리는 중!",
        "complete": "완료!",
        "timer_type": "타이머 종류",
        "status": "상태",
        "running": "🟢 실행중",
        "stopped": "⚪ 중지",
        "warning": "⚠️ 스피커 음량을 최대로 설정하세요!",
        "current_app": "현재 앱",
        "usage_time": "사용시간",
        "current_time": "현재 시각",
        "rest_until": "쉬는 시간",
        "sleep_until": "자는 시간",
        "wake_up": "일어나는 시간",
        "resting": "🌟 쉬는 중입니다!",
        "sleeping": "😴 자는 중입니다!",
        "alarm_sound": "🔊 알람 음악",
        "select_alarm": "알람 음악 선택",
        "upload_song": "🎵 커스텀 노래 업로드",
        "preset": "기본 알람음",
        "custom": "커스텀 노래",
        "sleep_time_label": "자는 시간 (목표 시간)",
        "wake_time_label": "일어나는 시간"
    },
    "English": {
        "title": "⏱️ Timer App",
        "lang": "🌐 Language",
        "timer": "📋 Timer",
        "time_limit": "⏱️ Time Limit",
        "app_usage": "💻 App Usage",
        "sleep_time": "😴 Sleep Time",
        "rest_time": "☕ Rest Time",
        "hours": "Hours",
        "minutes": "Minutes",
        "seconds": "Seconds",
        "start": "▶️ Start",
        "stop": "⏸️ Stop",
        "reset": "🔄 Reset",
        "test": "🔊 Test",
        "remaining": "Remaining Time",
        "set_time": "Set Time",
        "countdown": "⏰ Within 10 seconds!",
        "finished": "⚠️ Time Finished!",
        "siren": "Loud siren playing!",
        "complete": "Complete!",
        "timer_type": "Timer Type",
        "status": "Status",
        "running": "🟢 Running",
        "stopped": "⚪ Stopped",
        "warning": "⚠️ Set speaker volume to maximum!",
        "current_app": "Current App",
        "usage_time": "Usage Time",
        "current_time": "Current Time",
        "rest_until": "Resting Until",
        "sleep_until": "Sleeping Until",
        "wake_up": "Wake Up Time",
        "resting": "🌟 You are resting!",
        "sleeping": "😴 You are sleeping!",
        "alarm_sound": "🔊 Alarm Sound",
        "select_alarm": "Select Alarm Sound",
        "upload_song": "🎵 Upload Custom Song",
        "preset": "Preset Alarms",
        "custom": "Custom Song",
        "sleep_time_label": "Sleep Time (Goal)",
        "wake_time_label": "Wake Up Time"
    },
    "日本語": {
        "title": "⏱️ タイマーアプリ",
        "lang": "🌐 言語",
        "timer": "📋 タイマー",
        "time_limit": "⏱️ 時間制限",
        "app_usage": "💻 アプリ使用時間",
        "sleep_time": "😴 睡眠時間",
        "rest_time": "☕ 休息時間",
        "hours": "時間",
        "minutes": "分",
        "seconds": "秒",
        "start": "▶️ 開始",
        "stop": "⏸️ 停止",
        "reset": "🔄 リセット",
        "test": "🔊 テスト",
        "remaining": "残り時間",
        "set_time": "設定時間",
        "countdown": "⏰ 10秒以内!",
        "finished": "⚠️ 時間終了!",
        "siren": "大きなサイレンが鳴っています!",
        "complete": "完了!",
        "timer_type": "タイマータイプ",
        "status": "状態",
        "running": "🟢 実行中",
        "stopped": "⚪ 停止",
        "warning": "⚠️ スピーカーの音量を最大にしてください!",
        "current_app": "現在のアプリ",
        "usage_time": "使用時間",
        "current_time": "現在時刻",
        "rest_until": "休息時間",
        "sleep_until": "睡眠時間",
        "wake_up": "起床時間",
        "resting": "🌟 休息中です!",
        "sleeping": "😴 睡眠中です!",
        "alarm_sound": "🔊 アラーム音",
        "select_alarm": "アラーム音を選択",
        "upload_song": "🎵 カスタム曲をアップロード",
        "preset": "プリセットアラーム",
        "custom": "カスタム曲",
        "sleep_time_label": "睡眠時間 (目標)",
        "wake_time_label": "起床時間"
    }
}

TIMERS = {
    "time_limit": {"min": 5, "color": "#3498db"},
    "app_usage": {"min": 30, "color": "#9b59b6"},
    "sleep_time": {"min": 480, "color": "#2c3e50"},
    "rest_time": {"min": 15, "color": "#f39c12"}
}

ALARM_SOUNDS = {
    "🔔 Alarm": "/System/Library/Sounds/Alarm.aiff",
    "🎵 Glass": "/System/Library/Sounds/Glass.aiff",
    "🔊 Basso": "/System/Library/Sounds/Basso.aiff",
    "🎶 Blow": "/System/Library/Sounds/Blow.aiff",
    "🎺 Submarine": "/System/Library/Sounds/Submarine.aiff",
    "🎪 Ping": "/System/Library/Sounds/Ping.aiff",
    "⚡ Pop": "/System/Library/Sounds/Pop.aiff",
    "🎵 Sosumi": "/System/Library/Sounds/Sosumi.aiff"
}

def get_current_app():
    try:
        script = 'tell application "System Events" to name of (processes where frontmost is true)'
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=1)
        return result.stdout.strip() if result.stdout.strip() else "Unknown"
    except:
        return "Unable to detect"

def play_gentle_alarm(sound_file):
    try:
        os.system('osascript -e "set volume output volume 40"')
        for i in range(60):
            os.system(f'afplay -v 3 "{sound_file}" > /dev/null 2>&1 &')
            time.sleep(0.5)
    except:
        pass

# 세션 초기화
if "lang" not in st.session_state:
    st.session_state.lang = "한국어"
if "timer_type" not in st.session_state:
    st.session_state.timer_type = "time_limit"
if "running" not in st.session_state:
    st.session_state.running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "target_time" not in st.session_state:
    st.session_state.target_time = None
if "finished" not in st.session_state:
    st.session_state.finished = False
if "app_start_time" not in st.session_state:
    st.session_state.app_start_time = None
if "rest_target_time" not in st.session_state:
    st.session_state.rest_target_time = None
if "rest_started" not in st.session_state:
    st.session_state.rest_started = False
if "sleep_target_time" not in st.session_state:
    st.session_state.sleep_target_time = None
if "sleep_started" not in st.session_state:
    st.session_state.sleep_started = False
if "wake_target_time" not in st.session_state:
    st.session_state.wake_target_time = None
if "wake_started" not in st.session_state:
    st.session_state.wake_started = False
if "selected_alarm" not in st.session_state:
    st.session_state.selected_alarm = list(ALARM_SOUNDS.values())[0]
if "custom_audio_path" not in st.session_state:
    st.session_state.custom_audio_path = None

# 사이드바
st.sidebar.title("⚙️ 설정")

lang_list = list(LANGS.keys())
lang_idx = lang_list.index(st.session_state.lang)
new_lang = st.sidebar.selectbox("🌐 언어", lang_list, index=lang_idx)
st.session_state.lang = new_lang

st.sidebar.divider()

L = LANGS[st.session_state.lang]

timer_options = {
    L["time_limit"]: "time_limit",
    L["app_usage"]: "app_usage",
    L["sleep_time"]: "sleep_time",
    L["rest_time"]: "rest_time"
}

timer_list = list(timer_options.keys())
timer_idx = list(timer_options.values()).index(st.session_state.timer_type)
selected_timer_name = st.sidebar.radio(L["timer"], timer_list, index=timer_idx)
st.session_state.timer_type = timer_options[selected_timer_name]

st.sidebar.divider()

# 알람음 선택 (자는시간, 쉬는시간에만)
if st.session_state.timer_type in ["sleep_time", "rest_time"]:
    st.sidebar.subheader(L["alarm_sound"])
    
    alarm_tab1, alarm_tab2 = st.sidebar.tabs([L["preset"], L["custom"]])
    
    with alarm_tab1:
        alarm_names = list(ALARM_SOUNDS.keys())
        selected_alarm_name = st.selectbox(L["select_alarm"], alarm_names, key="alarm_select")
        st.session_state.selected_alarm = ALARM_SOUNDS[selected_alarm_name]
    
    with alarm_tab2:
        st.markdown(L["upload_song"])
        uploaded_file = st.file_uploader("선택 (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"], key="audio_upload")
        
        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                st.session_state.custom_audio_path = tmp_file.name
                st.success(f"✅ 업로드됨: {uploaded_file.name}")
                st.session_state.selected_alarm = tmp_file.name

timer_info = TIMERS[st.session_state.timer_type]

# 메인
st.markdown(f"# {L['title']}")
st.markdown(f"## {selected_timer_name}")
st.divider()

st.subheader("⚙️ 시간 설정")

# 자는시간: 자는 시간과 일어나는 시간 모두 입력
if st.session_state.timer_type == "sleep_time":
    st.markdown("**자는 시간과 일어나는 시간을 선택하세요**")
    
    col_sleep, col_wake = st.columns(2)
    
    with col_sleep:
        st.markdown(f"### 😴 {L['sleep_time_label']}")
        sleep_hour = st.number_input("자는 시간 (0-23)", 0, 23, 22, key="sleep_hour")
        sleep_minute = st.number_input("자는 분 (0-59)", 0, 59, 30, key="sleep_minute")
    
    with col_wake:
        st.markdown(f"### 🌅 {L['wake_time_label']}")
        wake_hour = st.number_input("일어나는 시간 (0-23)", 0, 23, 7, key="wake_hour")
        wake_minute = st.number_input("일어나는 분 (0-59)", 0, 59, 0, key="wake_minute")
    
    # 시간 계산
    now = datetime.now()
    sleep_time = datetime.now().replace(hour=sleep_hour, minute=sleep_minute, second=0)
    wake_time = datetime.now().replace(hour=wake_hour, minute=wake_minute, second=0)
    
    # 이미 지난 시간이면 내일로 설정
    if sleep_time < now:
        sleep_time = sleep_time + timedelta(days=1)
    if wake_time < sleep_time:
        wake_time = wake_time + timedelta(days=1)
    
    # 자는 시간부터 일어나는 시간까지의 시간차
    time_diff = wake_time - sleep_time
    h = int(time_diff.total_seconds()) // 3600
    m = (int(time_diff.total_seconds()) % 3600) // 60
    s = int(time_diff.total_seconds()) % 60
    total_sec = int(time_diff.total_seconds())
    
    st.info(f"💤 수면 시간: {h}시간 {m}분")

# 쉬는시간: 시간 직접 입력
elif st.session_state.timer_type == "rest_time":
    st.markdown("**목표 시간을 선택하세요**")
    target_col1, target_col2 = st.columns(2)
    with target_col1:
        target_hour = st.number_input("시간 (0-23)", 0, 23, 22)
    with target_col2:
        target_minute = st.number_input("분 (0-59)", 0, 59, 30)
    
    now = datetime.now()
    target_time = datetime.now().replace(hour=target_hour, minute=target_minute, second=0)
    
    if target_time < now:
        target_time = target_time + timedelta(days=1)
    
    time_diff = target_time - now
    h = int(time_diff.total_seconds()) // 3600
    m = (int(time_diff.total_seconds()) % 3600) // 60
    s = int(time_diff.total_seconds()) % 60
    total_sec = int(time_diff.total_seconds())

else:
    # 시간제한, 앱사용시간: 기존 방식
    col1, col2, col3 = st.columns(3)
    with col1:
        h = st.number_input(L["hours"], 0, 23, 0)
    with col2:
        m = st.number_input(L["minutes"], 0, 59, timer_info["min"])
    with col3:
        s = st.number_input(L["seconds"], 0, 59, 0)
    
    total_sec = h * 3600 + m * 60 + s

st.divider()

bcol1, bcol2, bcol3, bcol4 = st.columns(4)

with bcol1:
    if st.button(L["start"], type="primary", use_container_width=True):
        st.session_state.running = True
        st.session_state.start_time = time.time()
        st.session_state.target_time = st.session_state.start_time + total_sec
        st.session_state.finished = False
        st.session_state.app_start_time = time.time()
        
        if st.session_state.timer_type == "rest_time":
            st.session_state.rest_target_time = datetime.now() + timedelta(seconds=total_sec)
            st.session_state.rest_started = False
        
        if st.session_state.timer_type == "sleep_time":
            st.session_state.sleep_target_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, sleep_hour, sleep_minute)
            st.session_state.wake_target_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, wake_hour, wake_minute)
            
            if st.session_state.sleep_target_time < datetime.now():
                st.session_state.sleep_target_time = st.session_state.sleep_target_time + timedelta(days=1)
            if st.session_state.wake_target_time < st.session_state.sleep_target_time:
                st.session_state.wake_target_time = st.session_state.wake_target_time + timedelta(days=1)
            
            st.session_state.sleep_started = False
            st.session_state.wake_started = False

with bcol2:
    if st.button(L["stop"], use_container_width=True):
        st.session_state.running = False

with bcol3:
    if st.button(L["reset"], use_container_width=True):
        st.session_state.running = False
        st.session_state.finished = False
        st.session_state.rest_started = False
        st.session_state.sleep_started = False
        st.session_state.wake_started = False

with bcol4:
    if st.button(L["test"], use_container_width=True):
        threading.Thread(target=play_gentle_alarm, args=(st.session_state.selected_alarm,), daemon=True).start()

st.divider()

st.markdown("""<style>
@keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0.3; } }
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.2); } 100% { transform: scale(1); } }
</style>""", unsafe_allow_html=True)

display = st.empty()
app_display = st.empty()

if st.session_state.running:
    now = time.time()
    current_datetime = datetime.now()
    
    # 자는시간
    if st.session_state.timer_type == "sleep_time":
        if st.session_state.wake_target_time is not None and current_datetime >= st.session_state.wake_target_time and not st.session_state.wake_started:
            st.session_state.wake_started = True
            threading.Thread(target=play_gentle_alarm, args=(st.session_state.selected_alarm,), daemon=True).start()
        
        if st.session_state.wake_started:
            with app_display.container(border=True):
                st.markdown(f"""
                <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; color: white;">
                    <h2 style="font-size: 48px; margin: 0; font-weight: bold;">🌅 일어날 시간입니다!</h2>
                    <p style="font-size: 24px; margin: 15px 0;">현재 시간: {current_datetime.strftime('%p %I:%M')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with display.container():
                st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 20px; color: white;">
                    <h1 style="font-size: 80px; margin: 0;">🌅 아침이에요!</h1>
                </div>""", unsafe_allow_html=True)
        else:
            if st.session_state.sleep_target_time is not None and st.session_state.wake_target_time is not None:
                period = "오후" if current_datetime.hour >= 12 else "오전"
                display_hour = current_datetime.hour if current_datetime.hour <= 12 else current_datetime.hour - 12
                
                period_sleep = "오후" if st.session_state.sleep_target_time.hour >= 12 else "오전"
                display_hour_sleep = st.session_state.sleep_target_time.hour if st.session_state.sleep_target_time.hour <= 12 else st.session_state.sleep_target_time.hour - 12
                
                period_wake = "오후" if st.session_state.wake_target_time.hour >= 12 else "오전"
                display_hour_wake = st.session_state.wake_target_time.hour if st.session_state.wake_target_time.hour <= 12 else st.session_state.wake_target_time.hour - 12
                
                with app_display.container(border=True):
                    acol1, acol2, acol3 = st.columns(3)
                    with acol1:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
                            <p style="font-size: 16px; margin: 0; font-weight: bold;">{L['current_time']}</p>
                            <h2 style="font-size: 32px; margin: 10px 0;">🕐 {period} {display_hour}:{current_datetime.minute:02d}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with acol2:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; color: white;">
                            <p style="font-size: 16px; margin: 0; font-weight: bold;">😴 {L['sleep_until']}</p>
                            <h2 style="font-size: 32px; margin: 10px 0;">🎯 {period_sleep} {display_hour_sleep}:{st.session_state.sleep_target_time.minute:02d}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with acol3:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 15px; color: white;">
                            <p style="font-size: 16px; margin: 0; font-weight: bold;">🌅 {L['wake_up']}</p>
                            <h2 style="font-size: 32px; margin: 10px 0;">🎯 {period_wake} {display_hour_wake}:{st.session_state.wake_target_time.minute:02d}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                
                remain = st.session_state.target_time - now
                if remain < 0:
                    remain = 0
                
                hour = int(remain) // 3600
                minute = (int(remain) % 3600) // 60
                second = int(remain) % 60
                
                with display.container():
                    st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); border-radius: 20px; color: white;">
                        <h1 style="font-size: 100px; margin: 0;">{hour:02d}:{minute:02d}:{second:02d}</h1>
                        <p style="font-size: 20px;">💤 {L['remaining']}</p>
                    </div>""", unsafe_allow_html=True)
        
        time.sleep(1)
        st.rerun()
    
    # 쉬는시간
    elif st.session_state.timer_type == "rest_time":
        if st.session_state.rest_target_time is not None and current_datetime >= st.session_state.rest_target_time and not st.session_state.rest_started:
            st.session_state.rest_started = True
            threading.Thread(target=play_gentle_alarm, args=(st.session_state.selected_alarm,), daemon=True).start()
        
        if st.session_state.rest_started:
            with app_display.container(border=True):
                st.markdown(f"""
                <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
                    <h2 style="font-size: 48px; margin: 0; font-weight: bold;">{L['resting']}</h2>
                    <p style="font-size: 24px; margin: 15px 0;">{current_datetime.strftime('%p %I:%M')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with display.container():
                st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white;">
                    <h1 style="font-size: 80px; margin: 0;">😴 쉬는 중</h1>
                </div>""", unsafe_allow_html=True)
        else:
            if st.session_state.rest_target_time is not None:
                period = "오후" if current_datetime.hour >= 12 else "오전"
                display_hour = current_datetime.hour if current_datetime.hour <= 12 else current_datetime.hour - 12
                
                with app_display.container(border=True):
                    acol1, acol2 = st.columns(2)
                    with acol1:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%); border-radius: 15px; color: white;">
                            <p style="font-size: 18px; margin: 0; font-weight: bold;">{L['current_time']}</p>
                            <h2 style="font-size: 36px; margin: 10px 0;">🕐 {period} {display_hour}시 {current_datetime.minute}분</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with acol2:
                        period_end = "오후" if st.session_state.rest_target_time.hour >= 12 else "오전"
                        display_hour_end = st.session_state.rest_target_time.hour if st.session_state.rest_target_time.hour <= 12 else st.session_state.rest_target_time.hour - 12
                        st.markdown(f"""
                        <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); border-radius: 15px; color: white;">
                            <p style="font-size: 18px; margin: 0; font-weight: bold;">{L['rest_until']}</p>
                            <h2 style="font-size: 36px; margin: 10px 0;">🎯 {period_end} {display_hour_end}시 {st.session_state.rest_target_time.minute}분</h2>
                        </div>
                        """, unsafe_allow_html=True)
                
                remain = st.session_state.target_time - now
                if remain < 0:
                    remain = 0
                
                hour = int(remain) // 3600
                minute = (int(remain) % 3600) // 60
                second = int(remain) % 60
                
                with display.container():
                    st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, {timer_info['color']} 0%, #34495e 100%); border-radius: 20px; color: white;">
                        <h1 style="font-size: 100px; margin: 0;">{hour:02d}:{minute:02d}:{second:02d}</h1>
                        <p style="font-size: 20px;">{L['remaining']}</p>
                    </div>""", unsafe_allow_html=True)
        
        time.sleep(1)
        st.rerun()
    
    # 앱 사용시간
    elif st.session_state.timer_type == "app_usage":
        current_app = get_current_app()
        app_elapsed = now - st.session_state.app_start_time
        app_h = int(app_elapsed) // 3600
        app_m = (int(app_elapsed) % 3600) // 60
        app_s = int(app_elapsed) % 60
        
        with app_display.container(border=True):
            acol1, acol2 = st.columns(2)
            with acol1:
                st.markdown(f"""
                <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%); border-radius: 15px; color: white;">
                    <p style="font-size: 18px; margin: 0; font-weight: bold;">{L['current_app']}</p>
                    <h2 style="font-size: 36px; margin: 10px 0;">📱 {current_app}</h2>
                </div>
                """, unsafe_allow_html=True)
            with acol2:
                st.markdown(f"""
                <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #00ff88 0%, #00cc66 100%); border-radius: 15px; color: white;">
                    <p style="font-size: 18px; margin: 0; font-weight: bold;">{L['usage_time']}</p>
                    <h2 style="font-size: 36px; margin: 10px 0;">⏱️ {app_h:02d}:{app_m:02d}:{app_s:02d}</h2>
                </div>
                """, unsafe_allow_html=True)
        
        remain = st.session_state.target_time - now
        if remain < 0:
            remain = 0
        
        hour = int(remain) // 3600
        minute = (int(remain) % 3600) // 60
        second = int(remain) % 60
        
        if remain > 10:
            with display.container():
                st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, {timer_info['color']} 0%, #34495e 100%); border-radius: 20px; color: white;">
                    <h1 style="font-size: 100px; margin: 0;">{hour:02d}:{minute:02d}:{second:02d}</h1>
                    <p style="font-size: 20px;">{L['remaining']}</p>
                </div>""", unsafe_allow_html=True)
        
        elif remain > 0:
            with display.container():
                st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, #ffeb3b 0%, #f39c12 100%); border-radius: 20px;">
                    <h1 style="font-size: 100px; margin: 0; color: #ff6b00;">{hour:02d}:{minute:02d}:{second:02d}</h1>
                    <p style="font-size: 20px; color: #ff6b00;">{L['countdown']}</p>
                </div>""", unsafe_allow_html=True)
        
        elif not st.session_state.finished:
            st.session_state.finished = True
            
            with display.container():
                st.markdown(f"""<div style="text-align: center; padding: 80px; background-color: #ff0000; border-radius: 20px; color: white;">
                    <h1 style="font-size: 100px; margin: 0;" class="blink">🔔🔔🔔</h1>
                    <p style="font-size: 40px; margin-top: 20px;" class="pulse">{L['finished']}</p>
                    <p style="font-size: 24px;">{L['siren']}</p>
                </div>""", unsafe_allow_html=True)
            
            threading.Thread(target=play_gentle_alarm, args=(st.session_state.selected_alarm,), daemon=True).start()
            
            for i in range(5, 0, -1):
                with display.container():
                    st.markdown(f"""<div style="text-align: center; padding: 80px; background-color: #ff0000; border-radius: 20px; color: white;">
                        <h1 style="font-size: 150px; margin: 0;" class="pulse">{i}</h1>
                    </div>""", unsafe_allow_html=True)
                time.sleep(1)
            
            st.session_state.running = False
        
        time.sleep(1)
        st.rerun()
    
    else:
        # 시간제한
        remain = st.session_state.target_time - now
        if remain < 0:
            remain = 0
        
        hour = int(remain) // 3600
        minute = (int(remain) % 3600) // 60
        second = int(remain) % 60
        
        if remain > 10:
            with display.container():
                st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, {timer_info['color']} 0%, #34495e 100%); border-radius: 20px; color: white;">
                    <h1 style="font-size: 100px; margin: 0;">{hour:02d}:{minute:02d}:{second:02d}</h1>
                    <p style="font-size: 20px;">{L['remaining']}</p>
                </div>""", unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
        
        elif remain > 0:
            with display.container():
                st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, #ffeb3b 0%, #f39c12 100%); border-radius: 20px;">
                    <h1 style="font-size: 100px; margin: 0; color: #ff6b00;">{hour:02d}:{minute:02d}:{second:02d}</h1>
                    <p style="font-size: 20px; color: #ff6b00;">{L['countdown']}</p>
                </div>""", unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
        
        elif not st.session_state.finished:
            st.session_state.finished = True
            
            with display.container():
                st.markdown(f"""<div style="text-align: center; padding: 80px; background-color: #ff0000; border-radius: 20px; color: white;">
                    <h1 style="font-size: 100px; margin: 0;" class="blink">🔔🔔🔔</h1>
                    <p style="font-size: 40px; margin-top: 20px;" class="pulse">{L['finished']}</p>
                    <p style="font-size: 24px;">{L['siren']}</p>
                </div>""", unsafe_allow_html=True)
            
            threading.Thread(target=play_gentle_alarm, args=(st.session_state.selected_alarm,), daemon=True).start()
            
            for i in range(5, 0, -1):
                with display.container():
                    st.markdown(f"""<div style="text-align: center; padding: 80px; background-color: #ff0000; border-radius: 20px; color: white;">
                        <h1 style="font-size: 150px; margin: 0;" class="pulse">{i}</h1>
                    </div>""", unsafe_allow_html=True)
                time.sleep(1)
            
            st.session_state.running = False

else:
    hour = total_sec // 3600
    minute = (total_sec % 3600) // 60
    second = total_sec % 60
    
    with display.container():
        st.markdown(f"""<div style="text-align: center; padding: 80px; background: linear-gradient(135deg, {timer_info['color']} 0%, #34495e 100%); border-radius: 20px; color: white;">
            <h1 style="font-size: 100px; margin: 0;">{hour:02d}:{minute:02d}:{second:02d}</h1>
            <p style="font-size: 20px;">{L['set_time']}</p>
        </div>""", unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(L["timer_type"], selected_timer_name)
with col2:
    status = L["running"] if st.session_state.running else L["stopped"]
    st.metric(L["status"], status)
with col3:
    st.metric("설정 시간", f"{h:02d}:{m:02d}:{s:02d}")

st.divider()
st.warning(L["warning"])