# Portfolio Points

이 프로젝트를 포트폴리오에서 강조할 때의 핵심 포인트:

## Technical Highlights
- 한국어 LLM 기반 질의응답 생성
- KoBERT 임베딩 기반 의미 유사도 검색
- Kakao API 연동
- 위치 기반 추천 결과 시각화
- Docker / Jupyter 실험 환경

## System Highlights
- 단일 모델이 아니라 여러 컴포넌트를 연결한 end-to-end pipeline
- 텍스트 이해에서 끝나지 않고 지도 기반 추천 표현까지 확장
- 한국어 환경에 맞춘 KoAlpaca + KoBERT 조합

## Resume-friendly Summary
한국어 LLM과 KoBERT 임베딩을 결합하여 프롬프트 기반 POI 추천 알고리즘을 구현했다.
의미 기반 POI 검색, Kakao API 기반 geocoding, Folium 지도 시각화를 통합하여 텍스트 이해부터 위치 기반 추천 결과 표현까지 연결되는 하이브리드 추천 파이프라인을 설계했다.
