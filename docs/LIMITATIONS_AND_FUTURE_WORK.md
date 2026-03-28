# Limitations and Future Work

## Current Limitations

1. 추천 로직이 주로 텍스트 유사도 중심이다.
2. 사용자 선호, 거리, 카테고리, 평점 기반 ranking function은 미구현 상태다.
3. 재현성 측면에서 `kobert_tokenizer` 및 sample data 포함이 더 필요하다.
4. 배포 관점에서는 API 서버, UI, configuration 관리가 추가되어야 한다.

## Future Work

- LLM + Retrieval-Augmented POI recommendation
- 사용자 선호 기반 personalized ranking
- 거리/카테고리/평점 통합 scoring
- FastAPI 기반 API 서버화
- Streamlit 또는 Gradio 기반 데모 UI
- GPU inference 최적화
- sample dataset 및 sample output HTML 공개
