# Run Guide

## 1. Install requirements

```bash
pip install -r requirements.txt
```

## 2. Set environment variable

```bash
export KAKAO_REST_API_KEY=your_kakao_rest_api_key
```

또는 `.env` 파일을 사용할 수 있습니다.

## 3. Run LLM example

```bash
python llm_generation.py
```

## 4. Run KoBERT POI retrieval example

```bash
python poi_recommendation.py
```

## 5. Docker / Jupyter workflow

원본 실행 예시는 `Seoul-ICT` 기반 Docker + Jupyter 환경을 가정합니다.

```bash
docker build --tag seoul_ict:1.0 .
docker run -itd --gpus all --name ict -p 8888:8888 -v C:\Users\Name\:/workspace seoul_ict:1.0 /bin/bash
docker exec -it ict bash
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root
```

## 6. Data expectation

- `data/*.csv` 파일이 필요합니다.
- CSV는 CP949 인코딩 가정입니다.
- 주요 컬럼 예시: `분류`, `관광지명`, `주소`, `순위`
