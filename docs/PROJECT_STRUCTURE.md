# Project Structure

## Recommended files for GitHub upload

- `README.md`: 프로젝트 설명, 아키텍처, 실행 방법
- `requirements.txt`: Python 의존성 목록
- `.gitignore`: 업로드 제외 파일 규칙
- `repo_description.txt`: GitHub 저장소 설명 한 줄
- `portfolio_summary_ko.txt`: 이력서/포트폴리오용 한글 요약

## Suggested source file organization

```bash
poi-recommendation-llm-kobert/
├── README.md
├── requirements.txt
├── .gitignore
├── llm_generation.py
├── poi_recommendation.py
├── settings.py
├── setup.py
├── kobert_tokenizer/
│   ├── __init__.py
│   └── tokenizer_kobert.py
├── data/
│   └── *.csv
├── image/
│   └── *.html
└── docs/
    └── PROJECT_STRUCTURE.md
```

## Notes

- Kakao API Key는 코드에 하드코딩하지 말고 환경변수로 분리하는 것이 안전합니다.
- `get_similar_spot()`는 현재 `word_embed()` 호출 인자가 맞지 않아 수정 후 업로드하는 것이 좋습니다.
- LLM 추론 코드는 CPU/GPU device 설정을 일관되게 맞춰야 합니다.
