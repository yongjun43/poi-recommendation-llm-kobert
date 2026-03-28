# data

이 폴더에는 POI 원천 CSV 파일을 넣습니다.

예상 컬럼 예시:
- `분류`
- `관광지명`
- `주소`
- `순위`

`poi_recommendation.py`의 `get_dataframe()`은 기본적으로 CP949 인코딩 CSV를 읽도록 구현되어 있습니다.
