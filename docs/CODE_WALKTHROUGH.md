# Code Walkthrough

## `llm_generation.py`

역할:
- KoAlpaca 모델 로딩
- text-generation pipeline 생성
- `ask()` 함수로 질의응답 수행

핵심 포인트:
- CUDA 가능 여부에 따라 dtype과 device 분기
- `return_full_text=False`로 응답 텍스트만 추출

## `poi_recommendation.py`

역할:
- Kakao API geocoding
- 지도/클러스터/경로 시각화
- KoBERT 로딩
- 장소 임베딩 생성
- 유사 장소 검색

주요 함수:
- `kakao_map(address, api_key=None)`
- `get_long_lat(addresses, api_key=None)`
- `get_dataframe(path, api_key=None)`
- `plot_map()`
- `plot_cluster()`
- `plot_route()`
- `load_kobert()`
- `word_embed()`
- `get_similar_spot()`

## `settings.py`

역할:
- 데이터/이미지 디렉터리 설정
- 카테고리 목록 동적 생성
- Folium 색상 매핑 정의
- Kakao REST API Key 환경변수 관리

## `setup.py`

역할:
- `kobert_tokenizer` 로컬 패키지 등록
- KoBERT tokenizer 재사용을 위한 패키징 정의
