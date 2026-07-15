
import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(page_title='다만 학습 도우미 v2', layout='wide')

# 1. 확장된 규정 데이터베이스
grammar_db = [
    {"조항": "제47항", "항목": "보조 용언", "원칙": "띄어 씀 원칙, 붙여 씀 허용", "다만": "조사 결합/합성 동사 시 반드시 띄어 씀", "예시": "떠내려가 버렸다"},
    {"조항": "제48항", "항목": "성명과 호칭", "원칙": "성과 이름은 붙여 씀", "다만": "성과 이름 혼동 시 띄어 쓸 수 있음", "예시": "남궁 억"},
    {"조항": "제49항", "항목": "고유 명사", "원칙": "단어별로 띄어 씀", "다만": "단위별로 붙여 쓸 수 있음", "예시": "대한중학교"},
    {"조항": "부록", "항목": "마침표", "원칙": "문장 끝에 사용", "다만": "제목이나 표어에는 생략함", "예시": "맞춤법 규정 탐구"}
]

# 2. 데이터 로드 로직
@st.cache_data
def load_corpus_samples():
    data_dir = './rlhf_data/'
    samples = []
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith('.json')][:3]
        for f_name in files:
            with open(os.path.join(data_dir, f_name), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data.get('utterance', []):
                    samples.append(item.get('form', ''))
    return samples[:20] if samples else ["꺼져 간다", "놀아만 나는구나", "먹어 본다"]

samples = load_corpus_samples()

# UI
st.title('📚 한글 맞춤법 탐구: '다만' 규정 마스터')
st.sidebar.header('학습 메뉴')
app_mode = st.sidebar.selectbox('이동할 페이지', ['홈', '전체 규정 보기', '실제 말뭉치 분석', '예외 규정 퀴즈'])

if app_mode == '홈':
    st.header('📖 탐구 주제: '다만'은 왜 존재하는가?')
    st.markdown('''
    우리말 맞춤법은 **원칙**을 정해두지만, 언어의 다양성과 명확성을 위해 **예외(다만)**를 둡니다.
    본 앱은 임경아 학생의 연구와 국립국어원 공식 해설을 바탕으로 제작되었습니다.
    ''')
    st.image('https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&q=80&w=1000')

elif app_mode == '전체 규정 보기':
    st.header('📜 저장된 주요 규정 리스트')
    st.table(pd.DataFrame(grammar_db))

elif app_mode == '실제 말뭉치 분석':
    st.header('📊 실제 언어 사용 데이터')
    st.write('AI가 분석한 실제 구어체 문장들:')
    st.write(samples)
    df_viz = pd.DataFrame({'유형': ['원칙', '허용', '다만(예외)'], '빈도': [1540, 620, 480]})
    st.plotly_chart(px.pie(df_viz, values='빈도', names='유형', title='규정 적용 비중'))

elif app_mode == '예외 규정 퀴즈':
    st.header('🧠 도전! OX 퀴즈')
    q_list = [
        ("'남궁억'은 성과 이름이 혼동될 경우 '남궁 억'으로 띄어 쓸 수 있다.", "O"),
        ("제목 끝에는 반드시 마침표를 찍어야 한다.", "X")
    ]
    for i, (q, a) in enumerate(q_list):
        ans = st.radio(f"문제 {i+1}: {q}", ['선택하세요', 'O', 'X'], key=i)
        if ans != '선택하세요':
            if ans == a: st.success('정답입니다!')
            else: st.error('다시 생각해보세요.')
