import argparse
import pickle
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from pandas import DataFrame


VAL_POINTS = [[150, 0], [-100, -250]]
VAL_WIDTH = [70, 80]


def parse_args() -> Path:
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
    args = parser.parse_args()

    dataset_root: Path = args.dataset_root
    if not dataset_root.exists():
        raise ValueError("Given dataset_root directory does not exist.")

    return dataset_root


def check_in_test_set(
    northing: float,
    easting: float,
    test_boundary_points: List[Tuple[float, float]],
    boundary_width: Tuple[float, float],
) -> bool:
    """Checks whether the given point is in the test set.

    Args:
        northing (float): x coordinate of the point.
        easting (float): y coordinate of the point.
        test_boundary_points (List[Tuple[float, float]]): List of boundary points of the test set.
        boundary_width (Tuple[float, float]): Boundary width.

    Returns:
        bool: Whether the given point is in the test set.
    """
    in_test_set = False
    x_width, y_width = boundary_width
    for boundary_point in test_boundary_points:
        if (
            boundary_point[0] - x_width < northing < boundary_point[0] + x_width
            and boundary_point[1] - y_width < easting < boundary_point[1] + y_width
        ):
            in_test_set = True
            break
    return in_test_set


def split_dataframe(
    track_df: DataFrame, track_name: str, split_distance: int = 5
) -> Tuple[DataFrame, DataFrame, DataFrame]:
    """Split the given dataframe into train and test parts.

    Args:
        track_df (DataFrame): Track DataFrame.
        track_name (str): Track name (track's directory name).
        split_distance (int): The distance between frames in the split. Should be divisible by 5.
            Defaults to 10.

    Raises:
        ValueError: If the given split_distance is not divisible by 5.

    Returns:
        Tuple[DataFrame, DataFrame]: Train and test DataFrames.
    """
    if split_distance % 5 != 0:
        raise ValueError(f"Given split_distance={split_distance} is not divisible by 5.")
    train_rows = []
    val_rows = []
    test_rows = []
    step = split_distance // 5
    for i in range(0, len(track_df), step):
        row = track_df.iloc[i]
        if check_in_test_set(
            row[["northing", "easting"]].to_numpy().squeeze()[0],
            row[["northing", "easting"]].to_numpy().squeeze()[1],
            test_boundary_points=VAL_POINTS,
            boundary_width=VAL_WIDTH,
        ):
            val_rows.append(row)
        else:
            train_rows.append(row)
        test_rows.append(row)  # test part contains all elements %)
    train_df = pd.DataFrame(train_rows)
    val_df = pd.DataFrame(val_rows)
    test_df = pd.DataFrame(test_rows)
    train_df["track"] = track_name
    val_df["track"] = track_name
    test_df["track"] = track_name
    return train_df, val_df, test_df


def make_csv(dataset_root: Path) -> None:
    track_files = sorted(list(dataset_root.glob("*/track.csv")))
    print(f"Found {len(track_files)} 'track.csv' files in the subdirectories of the given dataset_root")
    column_names = [
        "timestamp",
        "track",
        "front_cam_ts",
        "back_cam_ts",
        "lidar_ts",
        "northing",
        "easting",
        "tz",
        "qx",
        "qy",
        "qz",
        "qw",
    ]
    train_df = DataFrame(columns=column_names)
    val_df = DataFrame(columns=column_names)
    test_df = DataFrame(columns=column_names)
    for track_file in track_files:
        track_name = track_file.parent.name
        track_df = pd.read_csv(track_file, index_col=0)
        track_df = track_df.rename(columns={"tx": "northing", "ty": "easting"})
        train_track_df, val_track_df, test_track_df = split_dataframe(track_df, track_name)
        track_df["track"] = track_name
        train_df = pd.concat([train_df, train_track_df], ignore_index=True)
        val_df = pd.concat([val_df, val_track_df], ignore_index=True)
        test_df = pd.concat([test_df, test_track_df], ignore_index=True)
    train_df = train_df[column_names]
    val_df = val_df[column_names]
    test_df = test_df[column_names]
    train_df[["timestamp", "front_cam_ts", "back_cam_ts", "lidar_ts"]] = train_df[
        ["timestamp", "front_cam_ts", "back_cam_ts", "lidar_ts"]
    ].astype("int64")
    val_df[["timestamp", "front_cam_ts", "back_cam_ts", "lidar_ts"]] = val_df[
        ["timestamp", "front_cam_ts", "back_cam_ts", "lidar_ts"]
    ].astype("int64")
    test_df[["timestamp", "front_cam_ts", "back_cam_ts", "lidar_ts"]] = test_df[
        ["timestamp", "front_cam_ts", "back_cam_ts", "lidar_ts"]
    ].astype("int64")
    train_df.to_csv(dataset_root / "train.csv")
    val_df.to_csv(dataset_root / "val.csv")  # for compatibility with oxford robotcar train/val/test code
    test_df.to_csv(dataset_root / "test.csv")  # for compatibility with oxford robotcar train/val/test code
    print(f"Saved 'train.csv', 'val.csv' and 'test.csv' in the dataset directory: {dataset_root}")


if __name__ == "__main__":
    dataset_root = parse_args()

    make_csv(dataset_root)
