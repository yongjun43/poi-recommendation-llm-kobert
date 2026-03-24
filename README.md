# Prompt-based POI Recommendation with KoAlpaca and KoBERT

한국어 LLM과 BERT 임베딩을 결합하여, 사용자 프롬프트 기반으로 POI(Point of Interest) 추천 및 위치 시각화를 수행하는 프로젝트입니다.

이 프로젝트는 다음 두 축으로 구성됩니다.

- **LLM 기반 질의 응답 생성**
  - `beomi/KoAlpaca-Polyglot-5.8B`
  - 사용자 질문과 맥락(context)을 입력받아 한국어 자연어 응답 생성
- **KoBERT 기반 POI 유사도 검색**
  - `skt/kobert-base-v1`
  - 관광지명/장소명을 임베딩으로 변환한 뒤 cosine similarity로 유사 POI 탐색
- **위치 기반 시각화**
  - Kakao Local API로 주소 → 위경도 변환
  - Folium으로 마커, 클러스터, 경로 시각화

## Overview

프로젝트 목표는 사용자의 자연어 프롬프트를 기반으로 장소 정보를 탐색하고, POI 간 유사도 및 위치 정보를 결합해 추천 후보를 제시하는 것입니다.

예를 들어:
- "동성로에 대해서 설명해줘" → LLM이 장소 설명 생성
- 특정 관광지명 입력 → KoBERT 임베딩 기반 유사 장소 검색
- 주소 데이터셋 기반 → 지도 시각화 및 경로 표시

즉, 단순 텍스트 생성이 아니라 다음을 아우르는 하이브리드 POI 추천 파이프라인입니다.

1. 한국어 프롬프트 이해
2. 장소명 임베딩 기반 유사도 계산
3. 주소 좌표화
4. 지도/클러스터/경로 시각화

## Main Architecture

### 1. LLM-based prompt generation
Hugging Face Transformers의 `AutoModelForCausalLM`과 `pipeline('text-generation')`을 사용해 `beomi/KoAlpaca-Polyglot-5.8B` 모델로 한국어 질의 응답을 생성합니다.

입력 포맷:
```text
### 질문: {question}

### 맥락: {context}

### 답변:
```

생성 파라미터:
- `max_new_tokens=128`
- `temperature=0.7`
- `top_p=0.9`
- `do_sample=True`

### 2. KoBERT-based POI embedding
`KoBERTTokenizer`와 `BertModel`을 사용하여 관광지명/장소명을 dense embedding으로 변환합니다.

핵심 함수:
- `word_embed(src, model, tokenizer, max_length=20)`
- `get_similar_spot(src, k=10)`

동작 방식:
1. 장소명을 토크나이즈
2. KoBERT `pooler_output` 추출
3. cosine similarity 계산
4. 유사도가 높은 POI 후보 정렬

### 3. Geocoding with Kakao API
주소 문자열을 Kakao Local API로 변환하여 longitude / latitude를 얻습니다.

핵심 함수:
- `kakao_map(address)`
- `getLongLat(addr)`

### 4. Visualization
Folium을 사용하여 다음 기능을 제공합니다.

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
└── docs/
    └── PROJECT_STRUCTURE.md
```

## Environment

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

## Docker

### 1. Clone
```bash
git clone https://github.com/ceo21ckim/Seoul-ICT.git
cd Seoul-ICT
```

### 2. Build
```bash
docker build --tag seoul_ict:1.0 .
```

### 3. Run
Docker 2.0+:
```bash
docker run -itd --runtime=nvidia --name ict -p 8888:8888 -v C:\Users\Name\:/workspace seoul_ict:1.0 /bin/bash
```

Docker CE 19.03+:
```bash
docker run -itd --gpus all --name ict -p 8888:8888 -v C:\Users\Name\:/workspace seoul_ict:1.0 /bin/bash
```

### 4. Jupyter Notebook
```bash
docker exec -it ict bash
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root
```

## Example

### Prompt
```text
### 질문: 동성로에 대해서 설명해줘
```

## Strengths

- 한국어 LLM 기반 질의응답 생성 가능
- KoBERT 임베딩을 활용한 의미 기반 POI 검색
- Kakao API를 통한 실제 위치 좌표화
- 지도, 클러스터, 경로까지 이어지는 시각화 제공
- NLP + Location Intelligence + Visualization 결합 구조

## Limitations

현재 원본 코드 기준으로는 아래 보완이 필요합니다.

1. **LLM 디바이스 설정 충돌 가능성**
   - 모델은 CPU로 올리지만 pipeline은 `device=0`으로 지정되어 있음

2. **API Key 하드코딩**
   - Kakao REST API Key가 코드에 직접 포함되어 있음
   - 공개 저장소 업로드 전 `.env` 또는 환경변수로 분리 필요

3. **`word_embed()` 호출부 수정 필요**
   - `get_similar_spot()`에서 `model`, `tokenizer` 인자를 넘기지 않아 현재 상태 그대로는 실행 오류 가능

4. **추천 로직 고도화 필요**
   - 현재는 텍스트 유사도 중심
   - 사용자 선호, 거리, 카테고리, 랭킹 등을 함께 반영하는 ranking function으로 확장 가능

## Future Work

- LLM + Retrieval-Augmented POI recommendation
- 사용자 선호 기반 personalized ranking
- 거리/카테고리/평점 통합 scoring
- FastAPI 기반 API 서버화
- Streamlit or Gradio 기반 데모 UI
- GPU inference 최적화

## Resume / Portfolio Description

### Korean
한국어 LLM(KoAlpaca)과 KoBERT 임베딩을 결합하여 프롬프트 기반 POI 추천 알고리즘을 구현했습니다.  
장소명 의미 유사도 검색, Kakao API 기반 좌표 변환, Folium 시각화를 통합하여 텍스트 이해부터 위치 기반 추천 결과 표현까지 연결되는 하이브리드 추천 파이프라인을 설계했습니다.

### English
Developed a prompt-based POI recommendation pipeline by combining a Korean LLM (KoAlpaca) with KoBERT embeddings.  
Built an end-to-end workflow that integrates semantic POI retrieval, Kakao API-based geocoding, and Folium visualization for location-aware recommendation.

## License
This project includes components and ideas based on external open-source resources.  
Please check each upstream repository license before redistribution.
