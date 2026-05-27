import streamlit as st
import time

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="소울 캐릭터 & MBTI 궁합 🔮",
    page_icon="💖",
    layout="centered"
)

# [핵심 보완 1] HTML이 마크다운 코드로 파싱되는 문제를 방지하는 완벽한 텍스트 가공 함수
def clean_html(html_str):
    # 모든 줄바꿈과 줄 앞뒤 공백을 없애서 순수한 한 줄의 HTML 문자열로 만듭니다.
    return "".join(line.strip() for line in html_str.split("\n"))

# [핵심 보완 2] 라이트/다크 모드 강제 통일 및 전방위 고대비 텍스트 CSS 적용
st.markdown(clean_html("""
<style>
/* 1. 배경화면 및 메인 컨테이너 글씨 투명화 해결 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #0b0f19 !important;
    background: linear-gradient(135deg, #090d16 0%, #111827 50%, #030712 100%) !important;
    color: #ffffff !important;
}

/* 2. Streamlit의 모든 마크다운, 레이블, 드롭다운 텍스트 색상을 선명한 흰색으로 강제 고정 */
p, li, label, span, h1, h2, h3, h4, h5, h6, small, div {
    color: #ffffff !important;
}

/* 3. 드롭다운 선택상자(Selectbox) 텍스트 및 배경 명확하게 구별 */
div[data-baseweb="select"] * {
    color: #ffffff !important;
    background-color: #1e293b !important;
}

/* 4. 드롭다운 옵션 목록 가독성 패치 */
div[role="listbox"] li {
    color: #ffffff !important;
    background-color: #1e293b !important;
}
div[role="listbox"] li:hover {
    background-color: #3b82f6 !important;
}

/* 5. 탭(Tab) 메뉴 글씨 고대비 적용 */
button[data-baseweb="tab"] p {
    color: #94a3b8 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}
button[aria-selected="true"] p {
    color: #38bdf8 !important;
    font-weight: bold !important;
}

/* 6. 메인 타이틀 네온 효과 */
.main-title {
    font-size: 40px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #f43f5e, #38bdf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 10px;
    margin-bottom: 5px;
    text-shadow: 0px 0px 20px rgba(236, 72, 153, 0.5);
}

.sub-title {
    font-size: 16px;
    text-align: center;
    color: #cbd5e1 !important;
    margin-bottom: 25px;
}

/* 7. 결과 출력 카드 (시인성을 위해 짙고 불투명한 솔리드 다크 블루 적용) */
.result-card {
    background-color: #1e293b !important;
    padding: 25px;
    border-radius: 20px;
    border: 2px solid #38bdf8 !important;
    box-shadow: 0px 10px 30px rgba(56, 189, 248, 0.3) !important;
    margin-top: 10px;
    text-align: center;
}

.char-name {
    font-size: 28px;
    font-weight: bold;
    color: #f43f5e !important;
    margin-bottom: 8px;
    text-shadow: 0px 0px 10px rgba(244, 63, 94, 0.4);
}

.char-title {
    font-size: 18px;
    font-weight: bold;
    color: #38bdf8 !important;
    margin-bottom: 15px;
}

.char-desc {
    font-size: 15px;
    color: #ffffff !important;
    line-height: 1.7;
    margin-bottom: 15px;
}

.char-quote {
    font-style: italic;
    font-size: 16px;
    color: #fcd34d !important;
    background-color: #0f172a !important;
    padding: 12px 18px;
    border-radius: 10px;
    border-left: 5px solid #fcd34d !important;
    display: inline-block;
    margin-top: 10px;
}

.compat-score {
    font-size: 68px;
    font-weight: 900;
    color: #f43f5e !important;
    text-shadow: 0px 0px 25px rgba(244, 63, 94, 0.7);
    margin: 15px 0;
}

.compat-status {
    font-size: 24px;
    font-weight: 800;
    color: #34d399 !important;
    margin-bottom: 12px;
}
</style>
"""), unsafe_allow_html=True)


# 2. MBTI별 소울 캐릭터 데이터 정의 (트래픽 무제한 고해상도 글로벌 CDN 이미지 연결)
mbti_data = {
    "ISTJ": {
        "character": "헤르미온느 그레인저 📚",
        "title": "해리포터",
        "desc": "규칙과 체계를 중요하게 생각하며, 엄청난 집중력과 꼼꼼함으로 동료들을 구하는 최고의 브레인입니다!",
        "quote": "“설마 죽거나, 아니면 더 나쁜 일인 퇴학을 당할 뻔했잖아!”",
        "image": "https://images.unsplash.com/photo-1506880018603-83d5b814b5a6?w=500&auto=format&fit=crop&q=80"
    },
    "ISFJ": {
        "character": "우디 🤠",
        "title": "토이 스토리",
        "desc": "내 사람들을 향한 헌신과 책임감이 넘치는 따뜻하고 믿음직한 의리파 리더입니다.",
        "quote": "“넌 나의 영원한 파트너야.”",
        "image": "https://images.unsplash.com/photo-1485124478822-ed5d8377726f?w=500&auto=format&fit=crop&q=80"
    },
    "INFJ": {
        "character": "요다 🪐",
        "title": "스타워즈",
        "desc": "깊은 통찰력과 지혜로 세상을 부드럽게 이끄는 모두의 정신적 지주이자 멘토입니다.",
        "quote": "“하느냐 마느냐의 문제일 뿐, 시도해 보는 것 따위는 없다.”",
        "image": "https://images.unsplash.com/photo-1593085512500-5d55148d6f0d?w=500&auto=format&fit=crop&q=80"
    },
    "INTJ": {
        "character": "배트맨 🦇",
        "title": "DC 코믹스",
        "desc": "한 치의 오차도 없는 완벽한 계획과 뛰어난 지성으로 문제를 해결하는 철저한 전략가입니다.",
        "quote": "“내가 누구인지는 중요하지 않아. 나를 정의하는 것은 나의 행동이다.”",
        "image": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=500&auto=format&fit=crop&q=80"
    },
    "ISTP": {
        "character": "리바이 아커만 ⚔️",
        "title": "진격의 거인",
        "desc": "상황 판단 능력이 빠르고 위기에 강하며, 쓸데없는 감정에 휘둘리지 않는 츤데레 실력자입니다.",
        "quote": "“행동해라. 후회는 나중에 해도 늦지 않다.”",
        "image": "https://images.unsplash.com/photo-1530328308468-b0a7a67f9173?w=500&auto=format&fit=crop&q=80"
    },
    "ISFP": {
        "character": "해리 포터 ⚡",
        "title": "해리포터",
        "desc": "따뜻하고 감수성이 풍부하며 자유를 사랑하고, 신념을 위해 용감히 맞서 싸우는 예술가입니다.",
        "quote": "“만약 우리가 함께 힘을 합친다면, 싸워 이길 수 있어요.”",
        "image": "https://images.unsplash.com/photo-1598153346810-860daa814c4b?w=500&auto=format&fit=crop&q=80"
    },
    "INFP": {
        "character": "피터팬 🧚‍♂️",
        "title": "피터팬",
        "desc": "순수한 마음과 풍부한 상상력으로 세상을 자유롭게 비행하는 영원한 낭만주의자입니다.",
        "quote": "“가장 행복했던 기억들을 떠올려 봐. 그게 너를 날아오르게 할 거야.”",
        "image": "https://images.unsplash.com/photo-1518156677180-95a2893f3e9f?w=500&auto=format&fit=crop&q=80"
    },
    "INTP": {
        "character": "셜록 홈즈 🕵️‍♂️",
        "title": "셜록",
        "desc": "세상의 모든 복잡한 미스터리를 독창적이고 논리적인 사고방식으로 풀어내는 호기심 천재입니다.",
        "quote": "“불가능을 제외하고 남은 것은, 아무리 믿기 힘들어도 진실이다.”",
        "image": "https://images.unsplash.com/photo-1505548468630-02752528b97d?w=500&auto=format&fit=crop&q=80"
    },
    "ESTP": {
        "character": "토르 ⚡",
        "title": "마블 (MCU)",
        "desc": "걱정은 뒤로 미루고 일단 몸부터 던져 위기를 축제로 바꾸는 에너지 넘치는 행동파입니다.",
        "quote": "“가자, 아스가르드를 위해!”",
        "image": "https://images.unsplash.com/photo-1546410531-bb4caa6b424d?w=500&auto=format&fit=crop&q=80"
    },
    "ESFP": {
        "character": "심바 🦁",
        "title": "라이온 킹",
        "desc": "낙천적이고 쾌활하여 모든 순간을 즐기며 주변 사람들을 늘 행복하게 만드는 분위기 메이커입니다.",
        "quote": "“하쿠나 마타타! 걱정 다 버려, 다 잘될 거야.”",
        "image": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=500&auto=format&fit=crop&q=80"
    },
    "ENFP": {
        "character": "에리얼 🧜‍♀️",
        "title": "인어공주",
        "desc": "바깥세상에 대한 호기심이 넘쳐나며 통통 튀는 매력으로 새로운 도전을 멈추지 않는 모험가입니다.",
        "quote": "“저 넓고 푸른 바다 너머에는 분명 다른 세상이 있을 거야!”",
        "image": "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=500&auto=format&fit=crop&q=80"
    },
    "ENTP": {
        "character": "잭 스패로우 🏴‍☠️",
        "title": "캐리비안의 해적",
        "desc": "어떤 규칙에도 얽매이지 않고 기발한 잔머리와 유쾌한 말솜씨로 위기를 극복하는 천재 모험가입니다.",
        "quote": "“이날을 기억해라, 캡틴 잭 스패로우를 잡을 뻔한 날로!”",
        "image": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=500&auto=format&fit=crop&q=80"
    },
    "ESTJ": {
        "character": "닉 퓨리 👁️",
        "title": "마블 (MCU)",
        "desc": "강력한 현실 감각과 추진력으로 흩어져 있던 영웅들을 하나로 모으는 든든한 사령관입니다.",
        "quote": "“우리에겐 영웅들을 한데 모으자는 아이디어가 있었다.”",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=500&auto=format&fit=crop&q=80"
    },
    "ESFJ": {
        "character": "캡틴 아메리카 🛡️",
        "title": "마블 (MCU)",
        "desc": "동료들을 먼저 배려하고 정의감이 넘치는 따뜻한 사회적 리더이자 등대 같은 존재입니다.",
        "quote": "“하루 종일도 할 수 있어 (I can do this all day).”",
        "image": "https://images.unsplash.com/photo-1624224971170-2f84fed5eb5e?w=500&auto=format&fit=crop&q=80"
    },
    "ENFJ": {
        "character": "주디 홉스 🐰",
        "title": "주토피아",
        "desc": "더 좋은 세상을 만들겠다는 긍정 에너지가 가득하며, 불가능을 가능으로 이끄는 열정 리더입니다.",
        "quote": "“누구나 무엇이든 될 수 있으니까요!”",
        "image": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=500&auto=format&fit=crop&q=80"
    },
    "ENTJ": {
        "character": "아이언맨 🤖",
        "title": "마블 (MCU)",
        "desc": "미래를 내다보는 비전과 거침없는 카리스마로 세상을 혁신하는 뜨거운 심장을 가진 리더입니다.",
        "quote": "“3,000만큼 사랑해. 그리고... 내가 바로 아이언맨이다.”",
        "image": "https://images.unsplash.com/photo-1620121692029-d088224ddc74?w=500&auto=format&fit=crop&q=80"
    }
}


# 3. 궁합 계산 함수
def get_compatibility(m1, m2):
    m1, m2 = m1.upper(), m2.upper()
    perfect_pairs = [
        {"INFP", "ENFJ"}, {"INFJ", "ENFP"}, {"INTJ", "ENTP"}, {"INTP", "ENTJ"},
        {"ISFP", "ESFJ"}, {"ISTP", "ESTJ"}, {"ISFJ", "ESTP"}, {"ISTJ", "ESFP"},
        {"INFP", "ENTJ"}, {"INFJ", "ENTP"}
    ]
    current_pair = {m1, m2}
    
    if m1 == m2:
        return 85, "일심동체 데칼코마니 👯", "서로를 거울 보듯 완벽하게 잘 아는 단짝! 말하지 않아도 통하는 게 많지만 똑같은 단점도 가질 수 있으니 서로 배려가 중요해요!"
    if current_pair in perfect_pairs:
        return 100, "우주 최강 천생연분 💖", "서로의 부족함을 완벽하게 채워주는 최고의 단짝입니다! 함께 있으면 기적을 만들어내는 환상의 조합!"
    
    matching_letters = sum(1 for a, b in zip(m1, m2) if a == b)
    if matching_letters == 3:
        return 90, "달달한 찰떡궁합 🍯", "비슷한 생각과 관심사 덕분에 언제나 수다가 끊이지 않는 사이! 함께 있을 때 가장 마음 편한 꿀조합입니다."
    elif matching_letters == 0:
        return 40, "정반대 매력의 자석 ⚡", "생각하는 것부터 행동하는 것까지 정반대라 가끔 당황스럽지만, 나에게 없는 상대방의 매력에 푹 빠질 수 있는 관계입니다."
    elif matching_letters == 1:
        return 65, "알콩달콩 맞춰가는 사이 🌱", "성향은 다르지만 맞춰갈수록 빛이 납니다. 서로의 다름을 존중하기만 하면 든든한 상호 보완 파트너가 될 수 있어요!"
    else:
        return 75, "평화롭고 편안한 사이 ☕", "특별히 크게 싸우지도 않고 무난하게 잘 통하는 관계입니다. 잔잔하고 부드러운 호수같이 안정감을 줍니다."


# 4. 헤더 출력
st.markdown("<div class='main-title'>🔮 소울 캐릭터 & MBTI 궁합 🔮</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>당곡고 친구들을 위한 운명적인 캐릭터 소환과 케미스트리 분석기!</div>", unsafe_allow_html=True)

# 5. 탭 UI 구성
tab1, tab2 = st.tabs(["👤 나의 소울 캐릭터", "💞 우리 궁합 테스트"])

# --- Tab 1: 나의 소울 캐릭터 추천 ---
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
            time.sleep(1.0)
        
        st.balloons()
        char_info = mbti_data[my_mbti]
        
        # [핵심 보완 3] HTML 카드에서 이미지를 제거하고, st.image를 사용해 절대 깨지지 않게 사이드로 배치
        col_img, col_txt = st.columns([1, 1.2])
        
        with col_img:
            st.image(char_info['image'], caption=f"📸 {char_info['character']} 실물 사진", use_container_width=True)
            
        with col_txt:
            card_html = f"""
            <div class="result-card">
                <div style="font-size: 15px; color: #38bdf8; font-weight: bold; margin-bottom: 5px;">🔥 {my_mbti}의 운명적 소울 캐릭터 🔥</div>
                <div class="char-name">{char_info['character']}</div>
                <div class="char-title">출연작: 《 {char_info['title']} 》</div>
                <hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.2); margin: 15px 0;">
                <div class="char-desc">{char_info['desc']}</div>
                <div class="char-quote">{char_info['quote']}</div>
            </div>
            """
            st.markdown(clean_html(card_html), unsafe_allow_html=True)


# --- Tab 2: 우리 궁합 테스트 ---
with tab2:
    st.write("")
    st.markdown("##### 👥 두 사람의 MBTI를 선택하고 환상의 케미를 확인해보세요!")
    
    col_a, col_b = st.columns(2)
    with col_a:
        mbti_a = st.selectbox("🙋‍♂️ 나의 MBTI", options=list(mbti_data.keys()), key="mbti_a")
    with col_b:
        mbti_b = st.selectbox("🙋‍♀️ 상대방(친구/연인)의 MBTI", options=list(mbti_data.keys()), key="mbti_b")
        
    st.write("")
    if st.button("💞 소울 궁합 분석하기 💞", use_container_width=True):
        with st.spinner("⏳ 두 캐릭터의 운명의 끈을 연결하는 중..."):
            time.sleep(1.0)
            
        st.snow()
        
        score, status, comment = get_compatibility(mbti_a, mbti_b)
        char_a = mbti_data[mbti_a]['character']
        char_b = mbti_data[mbti_b]['character']
        
        # [핵심 보완 4] clean_html() 함수를 거쳐 모든 띄어쓰기와 줄바꿈을 완벽 처리함으로써 코드 노출 현상 완전 소멸!
        compat_html = f"""
        <div class="result-card">
            <div style="font-size: 16px; color: #38bdf8; font-weight: bold; margin-bottom: 5px;">🧬 {mbti_a}와 {mbti_b}의 Chemistry 🧬</div>
            <div class="compat-score">{score}%</div>
            <div class="compat-status">{status}</div>
            <p class="char-desc" style="padding: 0 10px; color: #ffffff !important;">{comment}</p>
            <hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.2); margin: 20px 0;">
            <div style="display: flex; justify-content: space-around; align-items: center; text-align: center;">
                <div>
                    <div style="font-size: 13px; color: #94a3b8 !important;">나의 캐릭터 ({mbti_a})</div>
                    <div style="font-size: 18px; font-weight: bold; color: #f43f5e !important; margin-top: 5px;">{char_a}</div>
                </div>
                <div style="font-size: 24px; color: #ffffff !important;">⚡</div>
                <div>
                    <div style="font-size: 13px; color: #94a3b8 !important;">상대 캐릭터 ({mbti_b})</div>
                    <div style="font-size: 18px; font-weight: bold; color: #f43f5e !important; margin-top: 5px;">{char_b}</div>
                </div>
            </div>
        </div>
        """
        st.markdown(clean_html(compat_html), unsafe_allow_html=True)
        
        st.write("")
        if score >= 90:
            st.success("🎉 와우! 두 사람은 그냥 평생 가야 할 소울메이트군요!")
        elif score >= 70:
            st.info("😊 아주 좋은 궁합이에요! 같이 있으면 유쾌함이 2배가 됩니다!")
        else:
            st.warning("🤝 다름을 매력으로 삼아 더 깊은 사이가 될 수 있어요!")


# 7. 푸터 영역
st.write("")
st.write("")
st.markdown(clean_html("""
<hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.1); margin-top: 40px;">
<div style="text-align: center; color: #64748b !important; font-size: 12px;">
    🎯 Dangok High School Python Masterclass 🐍<br>
    Create, Code, and Connect with Streamlit Cloud!
</div>
"""), unsafe_allow_html=True)
