# LLM 기반 프롬프트 기반 POI 추천 알고리즘 개발

한국어 LLM과 KoBERT 임베딩을 결합하여, 사용자 프롬프트 기반으로 POI(Point of Interest) 추천 및 위치 시각화를 수행하는 프로젝트입니다.

이 프로젝트는 다음 3개 축으로 구성됩니다.

1. **LLM 기반 질의 응답 생성**
   - `beomi/KoAlpaca-Polyglot-5.8B`
   - 사용자 질문과 맥락을 입력받아 한국어 자연어 응답 생성
2. **KoBERT 기반 POI 의미 유사도 검색**
   - `skt/kobert-base-v1`
   - 관광지명/장소명을 dense embedding으로 변환한 뒤 cosine similarity로 유사 POI 탐색
3. **위치 기반 시각화**
   - Kakao Local API로 주소를 위경도로 변환
   - Folium으로 지도, 클러스터, 경로 시각화

## Project Summary

- **프로젝트명**: LLM 모델을 활용한 프롬프트 기반 POI 추천 알고리즘 개발
- **핵심 아이디어**: 텍스트 생성형 한국어 LLM과 의미 기반 POI 검색을 결합해, 설명 생성과 위치 추천을 동시에 수행하는 하이브리드 파이프라인 구현
- **주요 기능**
  - 한국어 프롬프트 기반 장소 설명 생성
  - KoBERT 임베딩 기반 유사 관광지 검색
  - Kakao API 기반 geocoding
  - Folium 기반 지도/클러스터/경로 시각화
- **기술 스택**
  - LLM: KoAlpaca
  - Embedding: KoBERT
  - Geocoding: Kakao Local API
  - Visualization: Folium
  - Data / ML: pandas, numpy, scikit-learn, torch, transformers

## Why This Project Matters

일반적인 챗봇형 응답은 장소를 “설명”하는 데 그치는 경우가 많습니다.
이 프로젝트는 설명 생성에 그치지 않고,

- 의미 기반 유사 POI 검색
- 주소 → 좌표 변환
- 지도 시각화
- 추천 후보의 경로/클러스터 표현

까지 연결하여 **텍스트 이해 + 의미 기반 추천 + 위치 기반 표현**을 하나의 흐름으로 묶었습니다.

## End-to-End Workflow

### 1. Prompt input
예시:

```text
### 질문: 동성로에 대해서 설명해줘
```

### 2. LLM response generation
`llm_generation.py`가 `KoAlpaca-Polyglot-5.8B` 기반으로 장소 설명을 생성합니다.

### 3. Semantic POI retrieval
`poi_recommendation.py`가 KoBERT 임베딩을 이용하여 입력 장소와 의미적으로 유사한 POI 후보를 탐색합니다.

### 4. Geocoding
주소를 Kakao Local API로 변환하여 위경도를 확보합니다.

### 5. Visualization
확보한 좌표를 기반으로 Folium 지도에서 마커, 클러스터, 경로를 시각화합니다.

## Main Architecture

### A. LLM-based Korean QA generation

- 구현 파일: `llm_generation.py`
- 모델: `beomi/KoAlpaca-Polyglot-5.8B`
- 사용 라이브러리: `AutoModelForCausalLM`, `AutoTokenizer`, `pipeline('text-generation')`
- 프롬프트 형식:

```text
### 질문: {question}

### 맥락: {context}

### 답변:
```

- 생성 파라미터
  - `max_new_tokens=128`
  - `temperature=0.7`
  - `top_p=0.9`
  - `do_sample=True`

### B. KoBERT-based POI embedding & similarity search

- 구현 파일: `poi_recommendation.py`
- 모델: `skt/kobert-base-v1`
- 토크나이저: `KoBERTTokenizer`
- 핵심 함수
  - `load_kobert()`
  - `word_embed(src, model, tokenizer, max_length=20)`
  - `get_similar_spot(src, model, tokenizer, k=10)`

동작 방식:
1. 장소명을 토크나이즈
2. KoBERT `pooler_output` 추출
3. cosine similarity 계산
4. 유사도가 높은 POI 후보 정렬

### C. Geocoding & map visualization

- Kakao Local API로 주소 → 위경도 변환
- Folium으로 지도 렌더링

핵심 함수:
- `kakao_map(address)`
- `get_long_lat(addresses)`
- `plot_map(dataframe)`
- `plot_cluster(dataframe, n_cluster=3)`
- `plot_route(src, dst)`

## Project Structure

```bash
poi-recommendation-llm-kobert/
├── README.md
├── requirements.txt
├── .gitignore
├── repo_description.txt
├── portfolio_summary_ko.txt
├── llm_generation.py
├── poi_recommendation.py
├── settings.py
├── setup.py
├── kobert_tokenizer/
│   └── README.md
├── data/
│   └── README.md
├── image/
│   └── README.md
├── docs/
│   ├── PROJECT_STRUCTURE.md
│   ├── PROJECT_OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── CODE_WALKTHROUGH.md
│   ├── RUN_GUIDE.md
│   ├── LIMITATIONS_AND_FUTURE_WORK.md
│   └── PORTFOLIO_POINTS.md
└── references/
    └── source-materials.md
```

## Requirements

```txt
boto3<=1.15.18
gluonnlp>=0.6.0,<=0.10.0
tqdm
torch
transformers
pandas
numpy
folium
scikit-learn
accelerate
sentencepiece
mxnet
requests
```

## Example

```text
### 질문: 동성로에 대해서 설명해줘
```

기대 동작:
- LLM이 장소 소개를 생성
- KoBERT가 의미 유사 POI 후보를 반환
- 주소/좌표 기반 시각화 가능

## Strengths

- 한국어 LLM 기반 질의응답 생성
- KoBERT 임베딩 기반 의미 검색
- Kakao API 기반 실제 위치 좌표화
- Folium 기반 지도/클러스터/경로 시각화
- NLP + Recommendation + Geospatial Visualization 결합 구조

## Limitations

현재 구현 기준으로 아래 보완이 필요합니다.

1. 사용자 선호, 거리, 카테고리, 평점이 통합된 ranking function은 아직 없음
2. API key 관리와 실행 환경 설정을 더 배포 친화적으로 다듬을 필요가 있음
3. sample data / demo UI / API server가 붙으면 프로젝트 전달력이 더 좋아짐
4. `kobert_tokenizer` 패키지와 데이터 파일까지 포함한 재현성 문서를 더 보강할 필요가 있음

## Future Work

- LLM + Retrieval-Augmented POI recommendation
- 사용자 선호 기반 personalized ranking
- 거리/카테고리/평점 통합 scoring
- FastAPI 기반 API 서버화
- Streamlit 또는 Gradio 데모 UI
- GPU inference 최적화

## Portfolio Description

### Korean
한국어 LLM(KoAlpaca)과 KoBERT 임베딩을 결합하여 프롬프트 기반 POI 추천 알고리즘을 구현했습니다. 
장소명 의미 유사도 검색, Kakao API 기반 좌표 변환, Folium 시각화를 통합하여 텍스트 이해부터 위치 기반 추천 결과 표현까지 연결되는 하이브리드 추천 파이프라인을 설계했습니다.

### English
Developed a prompt-based POI recommendation pipeline by combining a Korean LLM (KoAlpaca) with KoBERT embeddings. 
Built an end-to-end workflow that integrates semantic POI retrieval, Kakao API-based geocoding, and Folium visualization for location-aware recommendation.

## License

이 프로젝트는 외부 오픈소스 리소스 기반 아이디어와 구성 요소를 포함합니다.
재배포 전에는 upstream repository의 라이선스를 반드시 확인해야 합니다.
