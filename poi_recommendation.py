import glob
import os
from typing import List, Optional, Sequence, Tuple

import folium
import numpy as np
import pandas as pd
import requests
import torch
from branca.element import Figure
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from tqdm.auto import tqdm
from transformers import BertModel

from kobert_tokenizer import KoBERTTokenizer
from settings import DATA_DIR, IMG_DIR, TYPE, color_dict, color_list

KAKAO_API_KEY = os.getenv("KAKAO_REST_API_KEY", "")


def kakao_map(address: str, api_key: Optional[str] = None) -> Optional[Tuple[float, float]]:
    """Convert an address into longitude/latitude using Kakao Local API."""
    rest_api_key = api_key or KAKAO_API_KEY
    if not rest_api_key:
        raise ValueError("KAKAO_REST_API_KEY environment variable is not set.")

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {rest_api_key}"}
    response = requests.get(url, headers=headers, params={"query": address}, timeout=10)
    response.raise_for_status()
    documents = response.json().get("documents", [])

    if not documents:
        return None

    address_info = documents[0].get("address")
    if not address_info:
        return None
    return float(address_info["x"]), float(address_info["y"])


def get_long_lat(addresses: Sequence[str], api_key: Optional[str] = None) -> Tuple[List[float], List[float]]:
    longitude, latitude = [], []
    for address in tqdm(addresses, total=len(addresses)):
        location = kakao_map(address, api_key=api_key)
        if location is None:
            longitude.append(np.nan)
            latitude.append(np.nan)
        else:
            lon, lat = location
            longitude.append(lon)
            latitude.append(lat)
    return longitude, latitude


def label_encoder(value: str, types: Sequence[str] = TYPE) -> int:
    label2num = {t: i for i, t in enumerate(types)}
    return label2num[value]


def label_decoder(value: int, types: Sequence[str] = TYPE) -> str:
    num2label = {i: t for i, t in enumerate(types)}
    return num2label[value]


def plot_map(dataframe: pd.DataFrame, save: bool = False, fname: str = "poi_map.html"):
    center_lon = dataframe.loc[:, "long"].mean()
    center_lat = dataframe.loc[:, "lat"].mean()
    poi_map = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    for lon, lat, name, category in dataframe.loc[:, ["long", "lat", "name", "category"]].values:
        if pd.notna(lon) and pd.notna(lat):
            folium.Marker(
                location=[lat, lon],
                popup=f"<b>{name}</b>",
                icon=folium.Icon(color=color_dict.get(int(category), "blue"), icon="bookmark"),
            ).add_to(poi_map)

    if save:
        poi_map.save(os.path.join(IMG_DIR, fname))
    return poi_map


def plot_cluster(
    dataframe: pd.DataFrame,
    n_cluster: int = 3,
    save: bool = False,
    fname: str = "poi_cluster.html",
):
    center_lon = dataframe.loc[:, "long"].mean()
    center_lat = dataframe.loc[:, "lat"].mean()
    poi_map = folium.Map(location=[center_lat, center_lon], zoom_start=15)

    kmeans = KMeans(init="k-means++", n_clusters=n_cluster, n_init=5, random_state=42)
    kmeans.fit(dataframe.loc[:, ["lat", "long"]].values)
    cluster_centers = kmeans.cluster_centers_

    dataframe = dataframe.copy()
    dataframe.loc[:, "label"] = kmeans.labels_

    for i, (lat, lon) in enumerate(cluster_centers):
        folium.Circle(
            location=[lat, lon],
            popup=f"<b>Center {i}</b>",
            radius=8000,
            color=color_list[i],
            fill=True,
            alpha=0.5,
        ).add_to(poi_map)

    for lat, lon, label, name in dataframe.loc[:, ["lat", "long", "label", "name"]].values:
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{name}</b>",
            icon=folium.Icon(color=color_list[int(label)], icon="bookmark"),
        ).add_to(poi_map)

    if save:
        poi_map.save(os.path.join(IMG_DIR, fname))
    return poi_map


def plot_map_all(save: bool = False, extension: str = "html") -> None:
    for file_path in glob.glob(os.path.join(DATA_DIR, "*")):
        file_name = os.path.basename(file_path).split(".")[0]
        dataframe = get_dataframe(file_path)
        plot_map(dataframe, save=save, fname=f"{file_name}.{extension}")
        plot_cluster(dataframe, save=save, fname=f"{file_name}_cluster.{extension}")


def get_dataframe(path: str, api_key: Optional[str] = None) -> pd.DataFrame:
    tour = pd.read_csv(path, encoding="cp949")
    tour.rename({"분류": "category", "관광지명": "name", "주소": "address", "순위": "rank"}, axis=1, inplace=True)
    tour.loc[:, "category"] = tour.loc[:, "category"].apply(label_encoder)
    tour.loc[:, "long"], tour.loc[:, "lat"] = get_long_lat(tour.loc[:, "address"].values, api_key=api_key)
    tour.dropna(inplace=True)
    return tour.loc[:, ["name", "category", "long", "lat"]].copy()


def distance(src: Sequence[float], dst: Sequence[float], types: str = "l2") -> float:
    if types == "l2":
        return float(np.sqrt(np.power(src[0] - dst[0], 2) + np.power(src[1] - dst[1], 2)))
    if types == "l1":
        return float(np.abs(src[0] - dst[0]) + np.abs(src[1] - dst[1]))
    raise ValueError("types must be either 'l1' or 'l2'.")


def get_route(src: Sequence[float], dst: List[Sequence[float]]) -> List[Sequence[float]]:
    answer = []
    remaining = list(dst)
    current = list(src)
    while remaining:
        min_distance = float("inf")
        min_idx = 0
        for i, point in enumerate(remaining):
            dist = distance(current, point)
            if dist < min_distance:
                min_distance = dist
                min_idx = i
        current = remaining.pop(min_idx)
        answer.append(current)
    return answer


def plot_route(
    src: pd.DataFrame,
    dst: pd.DataFrame,
    save: bool = False,
    marker: bool = True,
    fname: str = "route",
    extension: str = "html",
):
    fig = Figure(width=550, height=350)
    src_for_color = src.copy()
    dst_for_color = dst.copy()
    if src_for_color["category"].dtype == object:
        src_for_color.loc[:, "category"] = src_for_color["category"].apply(label_encoder)
    if dst_for_color["category"].dtype == object:
        dst_for_color.loc[:, "category"] = dst_for_color["category"].apply(label_encoder)
    color_map = pd.concat([src_for_color, dst_for_color], axis=0).category.values

    src_location = src.loc[:, ["lat", "long"]].values.tolist()[0]
    dst_location = dst.loc[:, ["lat", "long"]].values.tolist()
    names = np.concatenate([src.name.values, dst.name.values])
    route = get_route(src_location, dst_location)
    center = np.mean(route, axis=0).tolist()
    poi_map = folium.Map(location=center, zoom_start=10)
    fig.add_child(poi_map)
    folium.PolyLine(locations=route).add_to(poi_map)

    if marker:
        for i, ((lat, lon), color) in enumerate(zip(route, color_map)):
            popup = folium.Popup(f"<b>{names[i]}</b>", min_width=60, max_width=60)
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                icon=folium.Icon(color=color_dict.get(int(color), "blue"), icon="bookmark"),
            ).add_to(poi_map)

    if save:
        poi_map.save(os.path.join(IMG_DIR, f"{fname}.{extension}"))
    return poi_map


def load_kobert():
    model = BertModel.from_pretrained("skt/kobert-base-v1")
    tokenizer = KoBERTTokenizer.from_pretrained(
        "skt/kobert-base-v1",
        sp_model_kwargs={"nbest_size": -1, "alpha": 0.6, "enable_sampling": True},
    )
    model.eval()
    return model, tokenizer


def word_embed(src: str, model: BertModel, tokenizer: KoBERTTokenizer, max_length: int = 20) -> np.ndarray:
    encoded = tokenizer.batch_encode_plus([src], max_length=max_length, padding="max_length", truncation=True)
    with torch.no_grad():
        output = model(
            input_ids=torch.tensor(encoded["input_ids"]),
            attention_mask=torch.tensor(encoded["attention_mask"]),
        ).pooler_output
    return output.detach().cpu().numpy()


def get_similar_spot(src: str, model: BertModel, tokenizer: KoBERTTokenizer, k: int = 10):
    outputs = []
    src_vector = word_embed(src, model, tokenizer)
    for file_path in glob.glob(os.path.join(DATA_DIR, "*")):
        if os.path.isdir(file_path):
            continue
        try:
            spots = pd.read_csv(file_path, encoding="cp949").loc[:, "관광지명"].dropna().values
        except Exception:
            continue
        for spot in spots:
            vector = word_embed(str(spot), model, tokenizer)
            score = cosine_similarity(src_vector, vector).item()
            outputs.append([spot, score])
    outputs = sorted(outputs, key=lambda x: x[1], reverse=True)
    return outputs[:k]


if __name__ == "__main__":
    model, tokenizer = load_kobert()
    for name, score in get_similar_spot("동성로", model, tokenizer, k=5):
        print(f"{name}: {score:.4f}")
