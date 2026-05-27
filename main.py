import streamlit as st
import time

# 1. 페이지 기본 설정 및 디자인
st.set_page_config(
    page_title="소울 캐릭터 & MBTI 궁합 🔮",
    page_icon="💖",
    layout="centered"
)

# 멋진 그라데이션, 네온 스타일 카드, 하트 애니메이션 느낌의 CSS 적용
st.markdown("""
<style>
/* 전체 배경 화면 */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
    color: #f8fafc;
}

/* 메인 타이틀 */
.main-title {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #f43f5e, #38bdf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 20px;
    margin-bottom: 5px;
    text-shadow: 0px 0px 15px rgba(236, 72, 153, 0.3);
}

/* 서브 타이틀 */
.sub-title {
    font-size: 16px;
    text-align: center;
    color: #94a3b8;
    margin-bottom: 25px;
}

/* 결과 출력 카드 */
.result-card {
    background: rgba(255, 255, 255, 0.06);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(12px);
    margin-top: 20px;
    text-align: center;
}

/* 캐릭터 이름 */
.char-name {
    font-size: 28px;
    font-weight: bold;
    color: #fb7185;
    margin-bottom: 8px;
}

/* 캐릭터 타이틀 */
.char-title {
    font-size: 18px;
    color: #38bdf8;
    margin-bottom: 12px;
}

/* 설명 텍스트 */
.char-desc {
    font-size: 15px;
    color: #e2e8f0;
    line-height: 1.6;
    margin-bottom: 15px;
}

/* 명언/대사 */
.char-quote {
    font-style: italic;
    font-size: 16px;
    color: #fcd34d;
    background: rgba(0, 0, 0, 0.35);
    padding: 10px 15px;
    border-radius: 10px;
    border-left: 4px solid #fcd34d;
    display: inline-block;
}

/* 궁합 지수 원형 스코어 */
.compat-score {
    font-size: 64px;
    font-weight: 900;
    color: #f43f5e;
    text-shadow: 0px 0px 20px rgba(244, 63, 94, 0.6);
    margin: 15px 0;
}

.compat-status {
    font-size: 22px;
    font-weight: 800;
    color: #34d399;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# 2. MBTI별 소울 캐릭터 데이터 정의
mbti_data = {
    "ISTJ": {
        "character": "헤르미온느 그레인저 📚",
        "title": "해리포터",
        "desc": "규칙과 체계를 중요하게 생각하며, 엄청난 집중력과 꼼꼼함으로 동료들을 구하는 최고의 브레인입니다!",
        "quote": "“설마 죽거나, 아니면 더 나쁜 일인 퇴학을 당할 뻔했잖아!”"
    },
    "ISFJ": {
        "character": "우디 🤠",
        "title": "토이 스토리",
        "desc": "내 사람들을 향한 헌신과 책임감이 넘치는 따뜻하고 믿음직한 의리파 리더입니다.",
        "quote": "“넌 나의 영원한 파트너야.”"
    },
    "INFJ": {
        "character": "요다 🪐",
        "title": "스타워즈",
        "desc": "깊은 통찰력과 지혜로 세상을 부드럽게 이끄는 모두의 정신적 지주이자 멘토입니다.",
        "quote": "“하느냐 마느냐의 문제일 뿐, 시도해 보는 것 따위는 없다.”"
    },
    "INTJ": {
        "character": "배트맨 🦇",
        "title": "DC 코믹스",
        "desc": "한 치의 오차도 없는 완벽한 계획과 뛰어난 지성으로 문제를 해결하는 철저한 전략가입니다.",
        "quote": "“내가 누구인지는 중요하지 않아. 나를 정의하는 것은 나의 행동이다.”"
    },
    "ISTP": {
        "character": "리바이 아커만 ⚔️",
        "title": "진격의 거인",
        "desc": "상황 판단 능력이 빠르고 위기에 강하며, 쓸데없는 감정에 휘둘리지 않는 츤데레 실력자입니다.",
        "quote": "“행동해라. 후회는 나중에 해도 늦지 않다.”"
    },
    "ISFP": {
        "character": "해리 포터 ⚡",
        "title": "해리포터",
        "desc": "따뜻하고 감수성이 풍부하며 자유를 사랑하고, 신념을 위해 용감히 맞서 싸우는 예술가입니다.",
        "quote": "“만약 우리가 함께 힘을 합친다면, 싸워 이길 수 있어요.”"
    },
    "INFP": {
        "character": "피터팬 🧚‍♂️",
        "title": "피터팬",
        "desc": "순수한 마음과 풍부한 상상력으로 세상을 자유롭게 비행하는 영원한 낭만주의자입니다.",
        "quote": "“가장 행복했던 기억들을 떠올려 봐. 그게 너를 날아오르게 할 거야.”"
    },
    "INTP": {
        "character": "셜록 홈즈 🕵️‍♂️",
        "title": "셜록",
        "desc": "세상의 모든 복잡한 미스터리를 독창적이고 논리적인 사고방식으로 풀어내는 호기심 천재입니다.",
        "quote": "“불가능을 제외하고 남은 것은, 아무리 믿기 힘들어도 진실이다.”"
    },
    "ESTP": {
        "character": "토르 ⚡",
        "title": "마블 (MCU)",
        "desc": "걱정은 뒤로 미루고 일단 몸부터 던져 위기를 축제로 바꾸는 에너지 넘치는 행동파입니다.",
        "quote": "“가자, 아스가르드를 위해!”"
    },
    "ESFP": {
        "character": "심바 🦁",
        "title": "라이온 킹",
        "desc": "낙천적이고 쾌활하여 모든 순간을 즐기며 주변 사람들을 늘 행복하게 만드는 분위기 메이커입니다.",
        "quote": "“하쿠나 마타타! 걱정 다 버려, 다 잘될 거야.”"
    },
    "ENFP": {
        "character": "에리얼 🧜‍♀️",
        "title": "인어공주",
        "desc": "바깥세상에 대한 호기심이 넘쳐나며 통통 튀는 매력으로 새로운 도전을 멈추지 않는 모험가입니다.",
        "quote": "“저 넓고 푸른 바다 너머에는 분명 다른 세상이 있을 거야!”"
    },
    "ENTP": {
        "character": "잭 스패로우 🏴‍☠️",
        "title": "캐리비안의 해적",
        "desc": "어떤 규칙에도 얽매이지 않고 기발한 잔머리와 유쾌한 말솜씨로 위기를 극복하는 천재 모험가입니다.",
        "quote": "“이날을 기억해라, 캡틴 잭 스패로우를 잡을 뻔한 날로!”"
    },
    "ESTJ": {
        "character": "닉 퓨리 👁️",
        "title": "마블 (MCU)",
        "desc": "강력한 현실 감각과 추진력으로 흩어져 있던 영웅들을 하나로 모으는 든든한 사령관입니다.",
        "quote": "“우리에겐 영웅들을 한데 모으자는 아이디어가 있었다.”"
    },
    "ESFJ": {
        "character": "캡틴 아메리카 🛡️",
        "title": "마블 (MCU)",
        "desc": "동료들을 먼저 배려하고 정의감이 넘치는 따뜻한 사회적 리더이자 등대 같은 존재입니다.",
        "quote": "“하루 종일도 할 수 있어 (I can do this all day).”"
    },
    "ENFJ": {
        "character": "주디 홉스 🐰",
        "title": "주토피아",
        "desc": "더 좋은 세상을 만들겠다는 긍정 에너지가 가득하며, 불가능을 가능으로 이끄는 열정 리더입니다.",
        "quote": "“누구나 무엇이든 될 수 있으니까요!”"
    },
    "ENTJ": {
        "character": "아이언맨 🤖",
        "title": "마블 (MCU)",
        "desc": "미래를 내다보는 비전과 거침없는 카리스마로 세상을 혁신하는 뜨거운 심장을 가진 리더입니다.",
        "quote": "“3,000만큼 사랑해. 그리고... 내가 바로 아이언맨이다.”"
    }
}

# 3. 궁합 지수 계산 함수 정의
def get_compatibility(m1, m2):
    m1, m2 = m1.upper(), m2.upper()
    
    # 천생연분 관계 설정 (전통적인 MBTI 궁합 기반)
    perfect_pairs = [
        {"INFP", "ENFJ"}, {"INFJ", "ENFP"}, {"INTJ", "ENTP"}, {"INTP", "ENTJ"},
        {"ISFP", "ESFJ"}, {"ISTP", "ESTJ"}, {"ISFJ", "ESTP"}, {"ISTJ", "ESFP"},
        {"INFP", "ENTJ"}, {"INFJ", "ENTP"}
    ]
    
    current_pair = {m1, m2}
    
    if m1 == m2:
        return 85, "일심동체 데칼코마니 👯", "서로를 거울 보듯 완벽하게 잘 아는 단짝! 말하지 않아도 통하는 게 많지만 똑같은 단점도 가질 수 있으니 배려가 중요해요!"
    
    if current_pair in perfect_pairs:
        return 100, "우주 최강 천생연분 💖", "서로의 부족함을 완벽하게 채워주는 최고의 단짝입니다! 함께 있으면 기적을 만들어내는 환상의 조합!"
    
    # 공통 알파벳 개수 계산
    matching_letters = sum(1 for a, b in zip(m1, m2) if a == b)
    
    if matching_letters == 3:
        return 90, "달달한 찰떡궁합 🍯", "비슷한 생각과 관심사 덕분에 언제나 수다가 끊이지 않는 사이! 함께 있을 때 가장 마음 편한 꿀조합입니다."
    elif matching_letters == 0:
        return 40, "정반대 매력의 자석 ⚡", "생각하는 것부터 행동하는 것까지 정반대라 가끔 당황스럽지만, 나에게 없는 상대방의 매력에 푹 빠질 수 있는 관계입니다."
    elif matching_letters == 1:
        return 65, "알콩달콩 맞춰가는 사이 🌱", "성향은 다르지만 맞춰갈수록 빛이 납니다. 서로의 다름을 존중하기만 하면 든든한 상호 보완 파트너가 될 수 있어요!"
    else: # matching_letters == 2
        return 75, "평화롭고 편안한 사이 ☕", "특별히 크게 싸우지도 않고 무난하게 잘 통하는 관계입니다. 잔잔하고 부드러운 호수같이 안정감을 줍니다."


# 4. 메인 화면 헤더
st.markdown("<div class='main-title'>🔮 소울 캐릭터 & MBTI 궁합 🔮</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>당곡고 친구들을 위한 운명적인 캐릭터 소환과 케미스트리 분석기!</div>", unsafe_allow_html=True)

# 5. 탭(Tab) UI 구성
tab1, tab2 = st.tabs(["👤 나의 소울 캐릭터", "💞 우리 궁합 테스트"])

# --- Tab 1: 나의 소울 캐릭터 찾기 ---
with tab1:
    st.write("")
    my_mbti = st.selectbox(
        "👉 당신의 MBTI를 선택해 주세요!",
        options=list(mbti_data.keys()),
        key="my_mbti_select"
    )
    
    st.write("")
    if st.button("✨ 캐릭터 소환하기 ✨", use_container_width=True):
        with st.spinner("🔮 우주의 기운을 모아 소울메이트를 찾는 중..."):
            time.sleep(1.2)
        
        st.balloons() # 풍선 팡팡!
        
        char_info = mbti_data[my_mbti]
        
        st.markdown(f"""
        <div class="result-card">
            <div style="font-size: 16px; color: #a78bfa; font-weight: bold; margin-bottom: 5px;">🔥 {my_mbti}의 운명적 소울 캐릭터 🔥</div>
            <div class="char-name">{char_info['character']}</div>
            <div class="char-title">출연작: 《 {char_info['title']} 》</div>
            <hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.15); margin: 15px 0;">
            <div class="char-desc">{char_info['desc']}</div>
            <div class="char-quote">{char_info['quote']}</div>
        </div>
        """, unsafe_allow_html=True)


# --- Tab 2: 우리 궁합 테스트 ---
with tab2:
    st.write("")
    st.markdown("##### 👥 두 사람의 MBTI를 선택하고 환상의 케미를 확인해보세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        mbti_a = st.selectbox("🙋‍♂️ 나의 MBTI", options=list(mbti_data.keys()), key="mbti_a")
    with col2:
        mbti_b = st.selectbox("🙋‍♀️ 상대방(친구/연인)의 MBTI", options=list(mbti_data.keys()), key="mbti_b")
        
    st.write("")
    if st.button("💞 소울 궁합 분석하기 💞", use_container_width=True):
        with st.spinner("⏳ 두 캐릭터의 운명의 끈을 연결하는 중..."):
            time.sleep(1.5)
            
        st.snow() # 눈 내리는 이펙트!
        
        score, status, comment = get_compatibility(mbti_a, mbti_b)
        char_a = mbti_data[mbti_a]['character']
        char_b = mbti_data[mbti_b]['character']
        
        # 궁합 결과 화면 출력
        st.markdown(f"""
        <div class="result-card">
            <div style="font-size: 16px; color: #38bdf8; font-weight: bold; margin-bottom: 5px;">🧬 {mbti_a}와 {mbti_b}의 Chemistry 🧬</div>
            <div class="compat-score">{score}%</div>
            <div class="compat-status">{status}</div>
            <p style="font-size: 16px; color: #e2e8f0; line-height: 1.6; padding: 0 10px;">{comment}</p>
            
            <hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.15); margin: 20px 0;">
            
            <div style="display: flex; justify-content: space-around; align-items: center; text-align: center;">
                <div>
                    <div style="font-size: 13px; color: #94a3b8;">나의 캐릭터 ({mbti_a})</div>
                    <div style="font-size: 18px; font-weight: bold; color: #fb7185; margin-top: 5px;">{char_a}</div>
                </div>
                <div style="font-size: 24px;">⚡</div>
                <div>
                    <div style="font-size: 13px; color: #94a3b8;">상대 캐릭터 ({mbti_b})</div>
                    <div style="font-size: 18px; font-weight: bold; color: #fb7185; margin-top: 5px;">{char_b}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 스코어에 따른 피드백 메시지
        if score >= 90:
            st.success("🎉 와우! 두 사람은 그냥 평생 가야 할 소울메이트군요!")
        elif score >= 70:
            st.info("😊 아주 좋은 궁합이에요! 같이 있으면 유쾌함이 2배가 됩니다!")
        else:
            st.warning("🤝 다름을 매력으로 삼아 더 깊은 사이가 될 수 있어요!")


# 6. 푸터 영역
st.write("")
st.write("")
st.markdown("""
<hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.1); margin-top: 40px;">
<div style="text-align: center; color: #64748b; font-size: 12px;">
    🎯 Dangok High School Python Masterclass 🐍<br>
    Create, Code, and Connect with Streamlit Cloud!
</div>
""", unsafe_allow_html=True)
