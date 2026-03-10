from __future__ import annotations

import io
import os
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

import numpy as np
import pandas as pd
import requests
import xml.etree.ElementTree as ET

S3_BUCKET_URL = "https://tripdata.s3.amazonaws.com"
KEY_PATTERN = re.compile(r"^(\d{6})-citibike-tripdata(?:\.csv)?\.zip$")

DEFAULT_SAMPLE_SIZE = 200_000
DEFAULT_RANDOM_SEED = 42
DEFAULT_MAX_DURATION_MIN = 6 * 60


@dataclass
class WorkshopPaths:
    base_dir: Path
    data_dir: Path
    raw_dir: Path
    processed_dir: Path
    processed_parquet: Path
    processed_csv: Path


def get_base_dir() -> Path:
    cwd = Path.cwd()
    if (cwd / "viz-workshop").exists():
        return cwd / "viz-workshop"
    if (cwd / "notebooks").exists() and (cwd.parent / "data").exists():
        return cwd.parent
    if (cwd / "data").exists():
        return cwd
    return cwd


def get_paths(base_dir: Path | None = None) -> WorkshopPaths:
    base = base_dir or get_base_dir()
    data_dir = base / "data"
    raw_dir = data_dir / "raw"
    processed_dir = data_dir / "processed"
    return WorkshopPaths(
        base_dir=base,
        data_dir=data_dir,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        processed_parquet=processed_dir / "citibike_month_sample.parquet",
        processed_csv=processed_dir / "citibike_month_sample.csv",
    )


def ensure_dirs(paths: WorkshopPaths) -> None:
    paths.raw_dir.mkdir(parents=True, exist_ok=True)
    paths.processed_dir.mkdir(parents=True, exist_ok=True)


def _list_tripdata_keys() -> Iterable[str]:
    url = f"{S3_BUCKET_URL}/?list-type=2"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    root = ET.fromstring(response.text)
    ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
    keys = [elem.text for elem in root.findall("s3:Contents/s3:Key", ns)]
    return [key for key in keys if key]


def _latest_tripdata_key() -> str:
    keys = _list_tripdata_keys()
    candidates: list[tuple[str, str]] = []
    for key in keys:
        match = KEY_PATTERN.match(key)
        if match:
            candidates.append((match.group(1), key))
    if not candidates:
        raise RuntimeError("No Citi Bike tripdata zip files found in bucket listing.")
    candidates.sort(key=lambda item: item[0])
    return candidates[-1][1]


def _download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with open(dest, "wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)


def download_latest_month(paths: WorkshopPaths) -> Path:
    key = _latest_tripdata_key()
    dest = paths.raw_dir / key
    if dest.exists():
        return dest
    url = f"{S3_BUCKET_URL}/{key}"
    _download_file(url, dest)
    return dest


def _read_tripdata_zip(zip_path: Path) -> pd.DataFrame:
    frames = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_names = [name for name in zf.namelist() if name.lower().endswith(".csv")]
        if not csv_names:
            raise RuntimeError("Zip file did not contain any CSV files.")
        for name in csv_names:
            with zf.open(name) as handle:
                frames.append(pd.read_csv(handle))
    return pd.concat(frames, ignore_index=True)


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "started_at": "started_at",
        "ended_at": "ended_at",
        "start_station_name": "start_station_name",
        "end_station_name": "end_station_name",
        "start_lat": "start_lat",
        "start_lng": "start_lng",
        "end_lat": "end_lat",
        "end_lng": "end_lng",
        "rideable_type": "rideable_type",
        "member_casual": "member_casual",
    }
    missing = [col for col in rename_map if col not in df.columns]
    if missing:
        raise RuntimeError(f"Expected columns missing from dataset: {missing}")
    return df[rename_map.keys()].copy()


def clean_sample_tripdata(
    df: pd.DataFrame,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
    random_seed: int = DEFAULT_RANDOM_SEED,
    max_duration_min: int | None = DEFAULT_MAX_DURATION_MIN,
) -> pd.DataFrame:
    df = _standardize_columns(df)

    df["started_at"] = pd.to_datetime(df["started_at"], errors="coerce")
    df["ended_at"] = pd.to_datetime(df["ended_at"], errors="coerce")
    df = df.dropna(subset=["started_at", "ended_at"])

    df["duration_min"] = (df["ended_at"] - df["started_at"]).dt.total_seconds() / 60
    df = df[df["duration_min"] > 0]
    if max_duration_min is not None:
        df = df[df["duration_min"] <= max_duration_min]

    df["date"] = df["started_at"].dt.date
    df["hour"] = df["started_at"].dt.hour
    df["day_of_week"] = df["started_at"].dt.dayofweek
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    df["day_name"] = pd.Categorical(df["started_at"].dt.day_name(), categories=day_order, ordered=True)

    df["member_casual"] = df["member_casual"].astype("category")
    df["rideable_type"] = df["rideable_type"].astype("category")

    if sample_size and len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=random_seed).reset_index(drop=True)
    return df


def save_processed(df: pd.DataFrame, paths: WorkshopPaths) -> Path:
    ensure_dirs(paths)
    try:
        df.to_parquet(paths.processed_parquet, index=False)
        return paths.processed_parquet
    except Exception:
        df.to_csv(paths.processed_csv, index=False)
        return paths.processed_csv


def load_processed(paths: WorkshopPaths) -> pd.DataFrame:
    if paths.processed_parquet.exists():
        return pd.read_parquet(paths.processed_parquet)
    if paths.processed_csv.exists():
        df = pd.read_csv(paths.processed_csv, parse_dates=["started_at", "ended_at", "date"])
        df["date"] = df["date"].dt.date
        return df
    raise FileNotFoundError("Processed dataset not found.")


def load_or_create_dataset(
    sample_size: int = DEFAULT_SAMPLE_SIZE,
    random_seed: int = DEFAULT_RANDOM_SEED,
    max_duration_min: int | None = DEFAULT_MAX_DURATION_MIN,
    base_dir: Path | None = None,
) -> pd.DataFrame:
    paths = get_paths(base_dir)
    ensure_dirs(paths)

    if paths.processed_parquet.exists() or paths.processed_csv.exists():
        return load_processed(paths)

    zip_path = download_latest_month(paths)
    raw_df = _read_tripdata_zip(zip_path)
    cleaned = clean_sample_tripdata(
        raw_df,
        sample_size=sample_size,
        random_seed=random_seed,
        max_duration_min=max_duration_min,
    )
    save_processed(cleaned, paths)
    return cleaned


def print_environment_hint() -> None:
    in_colab = "google.colab" in sys.modules
    if in_colab:
        print("Detected Colab runtime. Paths will be created under /content.")
    else:
        print("Running locally. Paths are relative to the project folder.")
