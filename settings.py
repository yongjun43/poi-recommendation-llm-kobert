import os
import glob
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR = os.path.join(BASE_DIR, "image")

os.makedirs(IMG_DIR, exist_ok=True)


def get_unique_type():
    types = []
    if not os.path.exists(DATA_DIR):
        return []

    for fname in glob.glob(os.path.join(DATA_DIR, "*")):
        try:
            df = pd.read_csv(fname, encoding="cp949")
            if "분류" in df.columns:
                u_type = df["분류"].dropna().unique().tolist()
                types.extend(u_type)
        except Exception:
            continue

    return list(set(types))


TYPE = get_unique_type()

color_list = [
    "orange",
    "blue",
    "green",
    "beige",
    "darkgreen",
    "darkpurple",
    "lightblue",
    "darkblue",
    "darkred",
    "lightred",
    "lightgray",
    "white",
    "pink",
    "cadetblue",
    "purple",
    "gray",
    "red",
    "black",
    "lightgreen",
] * 2

color_dict = {i: value for i, value in enumerate(color_list)}

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "")
