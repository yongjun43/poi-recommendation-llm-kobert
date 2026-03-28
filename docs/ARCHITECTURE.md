# Architecture

## Overview

이 프로젝트는 아래 3개 계층으로 구성된다.

1. LLM response generation
2. Semantic POI retrieval
3. Geospatial visualization

## 1. LLM Response Generation

- 모델: `beomi/KoAlpaca-Polyglot-5.8B`
- 구현 파일: `llm_generation.py`
- 역할: 사용자 질문 또는 질문+맥락을 받아 한국어 응답 생성

프롬프트 형식:

```text
### 질문: {question}

### 맥락: {context}

### 답변:
```

## 2. Semantic POI Retrieval

- 모델: `skt/kobert-base-v1`
- 구현 파일: `poi_recommendation.py`
- 역할: 장소명 임베딩 생성 및 cosine similarity 기반 유사 POI 검색

핵심 흐름:
- 장소명 입력
- tokenizer 인코딩
- BERT `pooler_output` 추출
- 유사도 계산
- top-k 후보 반환

## 3. Geospatial Visualization

- API: Kakao Local API
- 라이브러리: Folium
- 역할: 주소 좌표화 및 마커/클러스터/경로 시각화

핵심 함수:
- `kakao_map()`
- `get_long_lat()`
- `plot_map()`
- `plot_cluster()`
- `plot_route()`

## High-level Pipeline

```text
User Prompt
  ↓
KoAlpaca Prompt Response
  ↓
KoBERT Embedding-based POI Similarity Search
  ↓
Kakao Geocoding
  ↓
Folium Visualization
```
