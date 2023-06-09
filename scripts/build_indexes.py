import argparse
import pickle
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import torch
from pandas import DataFrame
from pytorch_metric_learning.distances import LpDistance


def parse_args() -> Tuple[Path, float, float]:
    """Parse input CLI arguments.

    Raises:
        ValueError: If the given '--dataset_root' directory does not exist.

    Returns:
        Path: Dataset root path.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_root",
        required=True,
        type=Path,
        help="The path to the preprocessed dataset root directory.",
    )
    parser.add_argument(
        "--pos_threshold",
        required=False,
        type=float,
        default=7.5,
        help="Positive distance threshold in meters. Defaults to 7.5.",
    )
    parser.add_argument(
        "--neg_threshold",
        required=False,
        type=float,
        default=25.0,
        help="Negative distance threshold in meters. Defaults to 25.0.",
    )
    args = parser.parse_args()

    dataset_root: Path = args.dataset_root
    if not dataset_root.exists():
        raise ValueError("Given dataset_root directory does not exist.")

    pos_threshold = args.pos_threshold
    neg_threshold = args.neg_threshold

    return dataset_root, pos_threshold, neg_threshold


def build_positives_index(df: DataFrame, distance_threshold: float) -> Dict[int, List[int]]:
    """Build index of positive elements for given DataFrame.

    Args:
        df (DataFrame): The dataset DataFrame
        distance_threshold (float): UTM distance threshold in meters for positive elements.

    Returns:
        Dict[int, List[int]]: Element with key `i` contains list of positive elements indexes.
    """
    utm_distance_fn = LpDistance(normalize_embeddings=False)
    positives_mask = (
        utm_distance_fn(torch.tensor(df[["northing", "easting"]].to_numpy(dtype=np.float64))).numpy()
        < distance_threshold
    )
    result: Dict[int, List[int]] = {}
    for i, row in enumerate(positives_mask):
        tmp = np.argwhere(row)
        result[i] = np.delete(tmp, np.argwhere(tmp == i)).tolist()
    return result


def build_nonnegatives_index(df: DataFrame, distance_threshold: float) -> Dict[int, List[int]]:
    """Build index of non-negative elements for given DataFrame.

    Args:
        df (DataFrame): The dataset DataFrame
        distance_threshold (float): UTM distance threshold in meters for negative elements.

    Returns:
        Dict[int, List[int]]: Element with key `i` contains list of non-negative elements indexes.
    """
    utm_distance_fn = LpDistance(normalize_embeddings=False)
    nonnegatives_mask = (
        utm_distance_fn(torch.tensor(df[["northing", "easting"]].to_numpy(dtype=np.float64))).numpy()
        < distance_threshold
    )
    result: Dict[int, List[int]] = {}
    for i, row in enumerate(nonnegatives_mask):
        result[i] = np.argwhere(row).squeeze().tolist()
    return result


def build_indexes(dataset_root: Path, pos_threshold: float, neg_threshold: float) -> None:
    for subset in ("train", "val", "test"):
        if (dataset_root / f"{subset}.csv").exists():
            subset_df = pd.read_csv(dataset_root / f"{subset}.csv", index_col=0)
            subset_positives_index = build_positives_index(subset_df, distance_threshold=pos_threshold)
            with open(dataset_root / f"{subset}_positives_index.pkl", "wb") as f:
                pickle.dump(subset_positives_index, f)
                print(f"Saved {subset}_positives_index.pkl")
            subset_negatives_index = build_nonnegatives_index(subset_df, distance_threshold=neg_threshold)
            with open(dataset_root / f"{subset}_nonnegatives_index.pkl", "wb") as f:
                pickle.dump(subset_negatives_index, f)
                print(f"Saved {subset}_nonnegatives_index.pkl")


if __name__ == "__main__":
    dataset_root, pos_threshold, neg_threshold = parse_args()

    build_indexes(dataset_root, pos_threshold, neg_threshold)
