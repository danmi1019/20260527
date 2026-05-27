import streamlit as st
import time
import textwrap

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="소울 캐릭터 & MBTI 궁합 🔮",
    page_icon="💖",
    layout="centered"
)

# 2. 고대비 텍스트 & 네온 스타일 CSS 적용
st.markdown(textwrap.dedent("""
<style>
/* 전체 배경 화면 및 기본 텍스트 색상 (선명한 화이트 강제 적용) */
.stApp {
    background: linear-gradient(135deg, #090d16 0%, #111827 50%, #030712 100%) !important;
    color: #ffffff !important;
}

/* Streamlit 기본 레이블, 문단, 마크다운 텍스트 시인성 강제 보장 */
.stMarkdown, p, li, label, span, .stSelectbox {
    color: #f8fafc !important;
    font-weight: 500 !important;
}

/* 입력 위젯 타이틀(글씨) 크기 및 색상 강조 */
div[data-testid="stWidgetLabel"] p {
    color: #67e8f9 !important;
    font-size: 16px !important;
    font-weight: bold !important;
}

/* 탭 메뉴 글씨 가독성 강화 */
div[data-baseweb="tab-list"] button p {
    color: #94a3b8 !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}
div[data-baseweb="tab-list"] button[aria-selected="true"] p {
    color: #38bdf8 !important;
    font-weight: bold !important;
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
    text-shadow: 0px 0px 20px rgba(236, 72, 153, 0.4);
}

/* 서브 타이틀 */
.sub-title {
    font-size: 16px;
    text-align: center;
    color: #e2e8f0;
    margin-bottom: 25px;
}

/* 고대비 결과 출력 카드 */
.result-card {
    background: #1e293b !important; /* 어두운 회색 솔리드 배경으로 텍스트 가독성 최우선 */
    padding: 25px;
    border-radius: 20px;
    border: 2px solid #38bdf8;
    box-shadow: 0px 10px 30px rgba(56, 189, 248, 0.3);
    margin-top: 15px;
    text-align: center;
}

/* 캐릭터 이름 */
.char-name {
    font-size: 30px;
    font-weight: bold;
    color: #f43f5e !important;
    margin-bottom: 8px;
    text-shadow: 0px 0px 10px rgba(244, 63, 94, 0.3);
}

/* 캐릭터 타이틀 */
.char-title {
    font-size: 18px;
    font-weight: bold;
    color: #38bdf8 !important;
    margin-bottom: 15px;
}

/* 설명 텍스트 */
.char-desc {
    font-size: 16px;
    color: #ffffff !important; /* 완전 하얀색으로 시인성 확보 */
    line-height: 1.7;
    margin-bottom: 15px;
}

/* 명언/대사 */
.char-quote {
    font-style: italic;
    font-size: 16px;
    color: #fcd34d !important; /* 선명한 노란색 */
    background: #0f172a !important;
    padding: 12px 18px;
    border-radius: 10px;
    border-left: 5px solid #fcd34d;
    display: inline-block;
    margin-top: 10px;
}

/* 궁합 지수 원형 스코어 */
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
    color: #34d399 !important; /* 선명한 민트색 */
    margin-bottom: 12px;
}
</style>
"""), unsafe_allow_html=True)


# 3. MBTI별 소울 캐릭터 데이터 정의 (실물 사진 URL 포함)
mbti_data = {
    "ISTJ": {
        "character": "헤르미온느 그레인저 📚",
        "title": "해리포터",
        "desc": "규칙과 체계를 중요하게 생각하며, 엄청난 집중력과 꼼꼼함으로 동료들을 구하는 최고의 브레인입니다!",
        "quote": "“설마 죽거나, 아니면 더 나쁜 일인 퇴학을 당할 뻔했잖아!”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Hermione_Granger_Warner_Bros_Tour_London.jpg"
    },
    "ISFJ": {
        "character": "우디 🤠",
        "title": "토이 스토리",
        "desc": "내 사람들을 향한 헌신과 책임감이 넘치는 따뜻하고 믿음직한 의리파 리더입니다.",
        "quote": "“넌 나의 영원한 파트너야.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/ee/Woody_at_Toy_Story_Land%2C_Hong_Kong.jpg"
    },
    "INFJ": {
        "character": "요다 🪐",
        "title": "스타워즈",
        "desc": "깊은 통찰력과 지혜로 세상을 부드럽게 이끄는 모두의 정신적 지주이자 멘토입니다.",
        "quote": "“하느냐 마느냐의 문제일 뿐, 시도해 보는 것 따위는 없다.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Yoda_at_Madame_Tussauds_London.jpg"
    },
    "INTJ": {
        "character": "배트맨 🦇",
        "title": "DC 코믹스",
        "desc": "한 치의 오차도 없는 완벽한 계획과 뛰어난 지성으로 문제를 해결하는 철저한 전략가입니다.",
        "quote": "“내가 누구인지는 중요하지 않아. 나를 정의하는 것은 나의 행동이다.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/d/df/Cosplay_of_Batman_%2849925232997%29.jpg"
    },
    "ISTP": {
        "character": "리바이 아커만 ⚔️",
        "title": "진격의 거인",
        "desc": "상황 판단 능력이 빠르고 위기에 강하며, 쓸데없는 감정에 휘둘리지 않는 츤데레 실력자입니다.",
        "quote": "“행동해라. 후회는 나중에 해도 늦지 않다.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/01/Attack_on_Titan_Cosplay_at_Epic_Con_2018_-_Part_1_%28108%29_%2839446860094%29.jpg"
    },
    "ISFP": {
        "character": "해리 포터 ⚡",
        "title": "해리포터",
        "desc": "따뜻하고 감수성이 풍부하며 자유를 사랑하고, 신념을 위해 용감히 맞서 싸우는 예술가입니다.",
        "quote": "“만약 우리가 함께 힘을 합친다면, 싸워 이길 수 있어요.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Harry_Potter_costume%2C_Warner_Bros_Studio_Tour_London.jpg"
    },
    "INFP": {
        "character": "피터팬 🧚‍♂️",
        "title": "피터팬",
        "desc": "순수한 마음과 풍부한 상상력으로 세상을 자유롭게 비행하는 영원한 낭만주의자입니다.",
        "quote": "“가장 행복했던 기억들을 떠올려 봐. 그게 너를 날아오르게 할 거야.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/36/The_Boy_Who_Would_Not_Grow_Up_-_Rackham_01.jpg"
    },
    "INTP": {
        "character": "셜록 홈즈 🕵️‍♂️",
        "title": "셜록",
        "desc": "세상의 모든 복잡한 미스터리를 독창적이고 논리적인 사고방식으로 풀어내는 호기심 천재입니다.",
        "quote": "“불가능을 제외하고 남은 것은, 아무리 믿기 힘들어도 진실이다.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/c/cd/Sherlock_Holmes_Sidney_Paget.jpg"
    },
    "ESTP": {
        "character": "토르 ⚡",
        "title": "마블 (MCU)",
        "desc": "걱정은 뒤로 미루고 일단 몸부터 던져 위기를 축제로 바꾸는 에너지 넘치는 행동파입니다.",
        "quote": "“가자, 아스가르드를 위해!”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/39/Thor_Cosplay_%2849508587121%29.jpg"
    },
    "ESFP": {
        "character": "심바 🦁",
        "title": "라이온 킹",
        "desc": "낙천적이고 쾌활하여 모든 순간을 즐기며 주변 사람들을 늘 행복하게 만드는 분위기 메이커입니다.",
        "quote": "“하쿠나 마타타! 걱정 다 버려, 다 잘될 거야.”",
        "image": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?q=80&w=400"
    },
    "ENFP": {
        "character": "에리얼 🧜‍♀️",
        "title": "인어공주",
        "desc": "바깥세상에 대한 호기심이 넘쳐나며 통통 튀는 매력으로 새로운 도전을 멈추지 않는 모험가입니다.",
        "quote": "“저 넓고 푸른 바다 너머에는 분명 다른 세상이 있을 거야!”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/30/Ariel_The_Little_Mermaid_Disney_On_Ice_2012.jpg"
    },
    "ENTP": {
        "character": "잭 스패로우 🏴‍☠️",
        "title": "캐리비안의 해적",
        "desc": "어떤 규칙에도 얽매이지 않고 기발한 잔머리와 유쾌한 말솜씨로 위기를 극복하는 천재 모험가입니다.",
        "quote": "“이날을 기억해라, 캡틴 잭 스패로우를 잡을 뻔한 날로!”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/23/Jack_Sparrow_cosplay.jpg"
    },
    "ESTJ": {
        "character": "닉 퓨리 👁️",
        "title": "마블 (MCU)",
        "desc": "강력한 현실 감각과 추진력으로 흩어져 있던 영웅들을 하나로 모으는 든든한 사령관입니다.",
        "quote": "“우리에겐 영웅들을 한데 모으자는 아이디어가 있었다.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Nick_Fury_Cosplay_2014.jpg"
    },
    "ESFJ": {
        "character": "캡틴 아메리카 🛡️",
        "title": "마블 (MCU)",
        "desc": "동료들을 먼저 배려하고 정의감이 넘치는 따뜻한 사회적 리더이자 등대 같은 존재입니다.",
        "quote": "“하루 종일도 할 수 있어 (I can do this all day).”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/c/c2/Captain_America_Madame_Tussauds_London.jpg"
    },
    "ENFJ": {
        "character": "주디 홉스 🐰",
        "title": "주토피아",
        "desc": "더 좋은 세상을 만들겠다는 긍정 에너지가 가득하며, 불가능을 가능으로 이끄는 열정 리더입니다.",
        "quote": "“누구나 무엇이든 될 수 있으니까요!”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/32/Judy_Hopps_cosplayer_at_Manga_Barcelona_2016.jpg"
    },
    "ENTJ": {
        "character": "아이언맨 🤖",
        "title": "마블 (MCU)",
        "desc": "미래를 내다보는 비전과 거침없는 카리스마로 세상을 혁신하는 뜨거운 심장을 가진 리더입니다.",
        "quote": "“3,000만큼 사랑해. 그리고... 내가 바로 아이언맨이다.”",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/29/Iron_Man_Cosplay_Epic_Con_2018.jpg"
    }
}


# 4. 궁합 계산 함수
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


# 5. 헤더 출력
st.markdown("<div class='main-title'>🔮 소울 캐릭터 & MBTI 궁합 🔮</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>당곡고 친구들을 위한 운명적인 캐릭터 소환과 케미스트리 분석기!</div>", unsafe_allow_html=True)

# 6. 탭 UI
tab1, tab2 = st.tabs(["👤 나의 소울 캐릭터", "💞 우리 궁합 테스트"])

# --- Tab 1: 캐릭터 추천 (이미지 추가) ---
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
        
        st.balloons()
        char_info = mbti_data[my_mbti]
        
        # UI 레이아웃 구성 (좌측 사진, 우측 설명)
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.image(char_info['image'], caption=f"✨ {char_info['character']} ✨", use_container_width=True)
            
        with col2:
            # textwrap.dedent를 이용해 들여쓰기가 코드 블록으로 파싱되는 문제 해결
            card_html = f"""
            <div class="result-card">
                <div style="font-size: 15px; color: #67e8f9; font-weight: bold; margin-bottom: 5px;">🔥 {my_mbti}의 운명적 소울 캐릭터 🔥</div>
                <div class="char-name">{char_info['character']}</div>
                <div class="char-title">출연작: 《 {char_info['title']} 》</div>
                <hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.15); margin: 15px 0;">
                <div class="char-desc">{char_info['desc']}</div>
                <div class="char-quote">{char_info['quote']}</div>
            </div>
            """
            st.markdown(textwrap.dedent(card_html), unsafe_allow_html=True)


# --- Tab 2: 궁합 분석 (코드 노출 해결) ---
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
            time.sleep(1.5)
            
        st.snow()
        
        score, status, comment = get_compatibility(mbti_a, mbti_b)
        char_a = mbti_data[mbti_a]['character']
        char_b = mbti_data[mbti_b]['character']
        
        # textwrap.dedent를 사용하여 궁합 결과 카드가 정상적인 HTML 디자인으로 렌더링되게 만듬! (코드 블록 노출 제거)
        compat_html = f"""
        <div class="result-card">
            <div style="font-size: 16px; color: #67e8f9; font-weight: bold; margin-bottom: 5px;">🧬 {mbti_a}와 {mbti_b}의 Chemistry 🧬</div>
            <div class="compat-score">{score}%</div>
            <div class="compat-status">{status}</div>
            <p class="char-desc" style="padding: 0 10px;">{comment}</p>
            
            <hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.15); margin: 20px 0;">
            
            <div style="display: flex; justify-content: space-around; align-items: center; text-align: center;">
                <div>
                    <div style="font-size: 13px; color: #94a3b8;">나의 캐릭터 ({mbti_a})</div>
                    <div style="font-size: 18px; font-weight: bold; color: #fb7185; margin-top: 5px;">{char_a}</div>
                </div>
                <div style="font-size: 24px; color: #ffffff;">⚡</div>
                <div>
                    <div style="font-size: 13px; color: #94a3b8;">상대 캐릭터 ({mbti_b})</div>
                    <div style="font-size: 18px; font-weight: bold; color: #fb7185; margin-top: 5px;">{char_b}</div>
                </div>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(compat_html), unsafe_allow_html=True)
        
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
st.markdown(textwrap.dedent("""
<hr style="border: 0; height: 1px; background: rgba(255, 255, 255, 0.1); margin-top: 40px;">
<div style="text-align: center; color: #64748b; font-size: 12px;">
    🎯 Dangok High School Python Masterclass 🐍<br>
    Create, Code, and Connect with Streamlit Cloud!
</div>
"""), unsafe_allow_html=True)
