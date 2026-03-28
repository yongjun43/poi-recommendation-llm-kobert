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
│   └── ...
├── data/
│   └── *.csv
├── image/
│   └── *.html
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── ARCHITECTURE.md
│   ├── CODE_WALKTHROUGH.md
│   ├── RUN_GUIDE.md
│   ├── LIMITATIONS_AND_FUTURE_WORK.md
│   └── PORTFOLIO_POINTS.md
└── references/
    └── source-materials.md
```

## Notes

- Kakao API Key는 코드에 하드코딩하지 말고 환경변수로 분리하는 것이 안전합니다.
- `kobert_tokenizer` 폴더는 실제 실행을 위해 기존 저장소 구현을 함께 두는 것이 좋습니다.
- LLM 추론 코드는 CPU/GPU device 설정을 일관되게 맞추는 것이 중요합니다.
