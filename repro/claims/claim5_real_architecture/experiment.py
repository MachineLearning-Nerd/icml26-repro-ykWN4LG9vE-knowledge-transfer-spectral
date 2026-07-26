#!/usr/bin/env python3
"""UTKFace frozen-backbone reproduction of the paper's real W2S experiment."""
from __future__ import annotations

import os

# Set before importing numerical libraries. The HF cpu-upgrade allocation is
# larger, but this experiment is deliberately bounded to 16 compute threads
# plus 8 image-loading workers (24-core estimate).
for _name in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ[_name] = "16"

import csv
import hashlib
import json
import math
import shutil
import time
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image
from sklearn.linear_model import Ridge
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import ResNet18_Weights, resnet18
from torchvision.transforms import InterpolationMode

from clip_vision import load_visual


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / ".openresearch" / "artifacts" / "claim-5"
CACHE = ROOT / ".cache" / "claim-5"
USER_AGENT = "OpenResearch-Reproduction/1.0"
SEED = 260601295
TRAIN_SIZE = 20_000
TEST_SIZE = 2_000
TEACHER_LABELS = 1_000
EPOCHS = 20
BATCH_SIZE = 128
THREADS = 16
WORKERS = 8

DATA_REVISION = "fb7f7d7102fd040c4211002b0c43e3ab727afffc"
DATA_BASE = (
    "https://huggingface.co/datasets/nlphuji/utk_faces/resolve/"
    f"{DATA_REVISION}"
)
METADATA_URL = f"{DATA_BASE}/utk_dataset_metadata.csv"
IMAGES_URL = f"{DATA_BASE}/utk_faces_images.zip"
METADATA_SHA256 = (
    "f46078943dc84ed141b97956f49c861c5cbc5a44ac13f9349fa7b048daf237fc"
)
IMAGES_SHA256 = (
    "938b68cafa61c4f58732f312d04caa808ddd420ff24a4c9cff0c2145e8255783"
)
CLIP_URL = (
    "https://openaipublic.azureedge.net/clip/models/"
    "40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af/"
    "ViT-B-32.pt"
)
CLIP_SHA256 = (
    "40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, target: Path, expected_sha256: str) -> None:
    if target.is_file() and sha256(target) == expected_sha256:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".partial")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        with temporary.open("wb") as handle:
            shutil.copyfileobj(response, handle, length=1024 * 1024)
    observed = sha256(temporary)
    if observed != expected_sha256:
        raise RuntimeError(
            f"Hash mismatch for {target.name}: {observed} != {expected_sha256}"
        )
    temporary.replace(target)


def extract_images(archive: Path, destination: Path) -> None:
    marker = destination / ".complete"
    if marker.is_file() and marker.read_text().strip() == IMAGES_SHA256:
        return
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as zipped:
        members = [
            item
            for item in zipped.infolist()
            if item.filename.startswith("utk_faces_images/")
            and not item.is_dir()
        ]
        for item in members:
            relative = Path(item.filename).relative_to("utk_faces_images")
            if relative.is_absolute() or ".." in relative.parts:
                raise RuntimeError(f"Unsafe archive path: {item.filename}")
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with zipped.open(item) as source, target.open("wb") as sink:
                shutil.copyfileobj(source, sink)
    marker.write_text(IMAGES_SHA256 + "\n")


class ImageDataset(Dataset):
    def __init__(
        self,
        paths: list[Path],
        ages: np.ndarray,
        transform: transforms.Compose,
    ) -> None:
        self.paths = paths
        self.ages = ages
        self.transform = transform

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, float]:
        with Image.open(self.paths[index]) as image:
            tensor = self.transform(image.convert("RGB"))
        return tensor, float(self.ages[index])


def extract_features(
    name: str,
    model: nn.Module,
    transform: transforms.Compose,
    paths: list[Path],
    ages: np.ndarray,
) -> np.ndarray:
    loader = DataLoader(
        ImageDataset(paths, ages, transform),
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=WORKERS,
        persistent_workers=True,
    )
    batches = []
    model.eval()
    with torch.inference_mode():
        for index, (images, _) in enumerate(loader):
            batches.append(model(images).float().cpu())
            if index % 25 == 0:
                print(
                    f"FEATURE_PROGRESS_JSON={json.dumps({'model': name, 'batch': index, 'batches': len(loader)})}",
                    flush=True,
                )
    return torch.cat(batches).numpy()


def train_head(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    test_features: np.ndarray,
    test_truth: np.ndarray,
    test_teacher: np.ndarray,
    *,
    seed: int,
) -> tuple[list[dict], list[np.ndarray], list[np.ndarray]]:
    torch.manual_seed(seed)
    features = torch.from_numpy(train_features)
    targets = torch.from_numpy(train_targets.astype(np.float32))
    test = torch.from_numpy(test_features)
    head = nn.Linear(train_features.shape[1], 1)
    nn.init.zeros_(head.weight)
    nn.init.zeros_(head.bias)
    optimizer = torch.optim.SGD(
        head.parameters(), lr=1e-4, momentum=0.9
    )
    generator = torch.Generator().manual_seed(seed)
    rows: list[dict] = []
    predictions: list[np.ndarray] = []
    weights: list[np.ndarray] = []
    for epoch in range(1, EPOCHS + 1):
        permutation = torch.randperm(len(features), generator=generator)
        head.train()
        for start in range(0, len(features), BATCH_SIZE):
            indices = permutation[start : start + BATCH_SIZE]
            prediction = head(features[indices]).squeeze(1)
            loss = torch.mean((prediction - targets[indices]) ** 2)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
        head.eval()
        with torch.no_grad():
            test_prediction = head(test).squeeze(1).numpy()
        predictions.append(test_prediction)
        weights.append(head.weight.detach().squeeze(0).numpy().copy())
        rows.append(
            {
                "epoch": epoch,
                "true_mse": float(
                    np.mean((test_prediction - test_truth) ** 2)
                ),
                "teacher_fit_mse": float(
                    np.mean((test_prediction - test_teacher) ** 2)
                ),
            }
        )
    return rows, predictions, weights


def paired_ci(
    worse_errors: np.ndarray,
    better_errors: np.ndarray,
    *,
    seed: int,
    resamples: int = 2_000,
) -> dict:
    difference = worse_errors - better_errors
    rng = np.random.default_rng(seed)
    means = np.empty(resamples)
    for index in range(resamples):
        sample = rng.integers(0, len(difference), size=len(difference))
        means[index] = np.mean(difference[sample])
    return {
        "mean_difference": float(np.mean(difference)),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "resamples": resamples,
    }


def main() -> None:
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(THREADS)
    torch.set_num_interop_threads(2)
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    stage_times: dict[str, float] = {}
    stage = time.perf_counter()
    metadata_path = CACHE / "utk_dataset_metadata.csv"
    images_archive = CACHE / "utk_faces_images.zip"
    clip_checkpoint = CACHE / "ViT-B-32.pt"
    download(METADATA_URL, metadata_path, METADATA_SHA256)
    download(IMAGES_URL, images_archive, IMAGES_SHA256)
    download(CLIP_URL, clip_checkpoint, CLIP_SHA256)
    image_root = CACHE / "images"
    extract_images(images_archive, image_root)
    stage_times["download_and_extract_s"] = time.perf_counter() - stage

    metadata = pd.read_csv(metadata_path)
    all_paths = [
        image_root / f"{name}.chip.jpg"
        for name in metadata["image_name"].astype(str)
    ]
    missing = [str(path) for path in all_paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"Missing {len(missing)} metadata images")
    all_ages = metadata["age"].to_numpy(dtype=np.float32)
    split_rng = np.random.default_rng(SEED)
    selected = split_rng.permutation(len(all_paths))[
        : TRAIN_SIZE + TEST_SIZE
    ]
    selected_paths = [all_paths[index] for index in selected]
    selected_ages = all_ages[selected]
    train_ages = selected_ages[:TRAIN_SIZE]
    test_ages = selected_ages[TRAIN_SIZE:]

    stage = time.perf_counter()
    resnet_weights = ResNet18_Weights.IMAGENET1K_V1
    teacher_backbone = resnet18(weights=resnet_weights)
    teacher_backbone.fc = nn.Identity()
    resnet_checkpoint = (
        Path(torch.hub.get_dir())
        / "checkpoints"
        / Path(resnet_weights.url).name
    )
    clip_transform = transforms.Compose(
        [
            transforms.Resize(224, interpolation=InterpolationMode.BICUBIC),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                (0.48145466, 0.4578275, 0.40821073),
                (0.26862954, 0.26130258, 0.27577711),
            ),
        ]
    )
    student_backbone = load_visual(clip_checkpoint)
    stage_times["model_load_s"] = time.perf_counter() - stage

    stage = time.perf_counter()
    teacher_features = extract_features(
        "torchvision-resnet18-imagenet1k-v1",
        teacher_backbone,
        resnet_weights.transforms(),
        selected_paths,
        selected_ages,
    )
    del teacher_backbone
    stage_times["resnet18_feature_s"] = time.perf_counter() - stage

    stage = time.perf_counter()
    student_features = extract_features(
        "openai-clip-vit-b32-preprojection",
        student_backbone,
        clip_transform,
        selected_paths,
        selected_ages,
    )
    del student_backbone
    stage_times["clip_vit_b32_feature_s"] = time.perf_counter() - stage

    teacher_train = teacher_features[:TRAIN_SIZE]
    teacher_test = teacher_features[TRAIN_SIZE:]
    student_train = student_features[:TRAIN_SIZE]
    student_test = student_features[TRAIN_SIZE:]

    stage = time.perf_counter()
    teacher = Ridge(alpha=1e-6, fit_intercept=True, solver="cholesky")
    teacher.fit(
        teacher_train[:TEACHER_LABELS],
        train_ages[:TEACHER_LABELS],
    )
    pseudo_train = teacher.predict(teacher_train).astype(np.float32)
    teacher_test_prediction = teacher.predict(teacher_test).astype(np.float32)
    teacher_mse = float(
        np.mean((teacher_test_prediction - test_ages) ** 2)
    )

    w2s_rows, w2s_predictions, w2s_weights = train_head(
        student_train,
        pseudo_train,
        student_test,
        test_ages,
        teacher_test_prediction,
        seed=SEED + 1,
    )
    direct_rows, direct_predictions, _ = train_head(
        student_train,
        train_ages,
        student_test,
        test_ages,
        teacher_test_prediction,
        seed=SEED + 2,
    )
    shuffled = pseudo_train.copy()
    np.random.default_rng(SEED + 3).shuffle(shuffled)
    control_rows, control_predictions, _ = train_head(
        student_train,
        shuffled,
        student_test,
        test_ages,
        teacher_test_prediction,
        seed=SEED + 4,
    )
    stage_times["linear_heads_s"] = time.perf_counter() - stage

    stage = time.perf_counter()
    covariance_features = torch.from_numpy(student_train[:10_000])
    covariance = covariance_features.T @ covariance_features / len(
        covariance_features
    )
    _, eigenvectors = torch.linalg.eigh(covariance)
    eigenvectors = eigenvectors.flip(1).numpy()
    k80_by_epoch = []
    for weight in w2s_weights:
        energy = (eigenvectors.T @ weight) ** 2
        cumulative = np.cumsum(energy) / np.sum(energy)
        k80_by_epoch.append(int(np.searchsorted(cumulative, 0.8) + 1))
    stage_times["pca_projection_s"] = time.perf_counter() - stage

    best_index = int(np.argmin([row["true_mse"] for row in w2s_rows]))
    direct_best_index = int(
        np.argmin([row["true_mse"] for row in direct_rows])
    )
    control_best_index = int(
        np.argmin([row["true_mse"] for row in control_rows])
    )
    best_prediction = w2s_predictions[best_index]
    final_prediction = w2s_predictions[-1]
    direct_best_prediction = direct_predictions[direct_best_index]
    control_best_prediction = control_predictions[control_best_index]
    teacher_errors = (teacher_test_prediction - test_ages) ** 2
    best_errors = (best_prediction - test_ages) ** 2
    final_errors = (final_prediction - test_ages) ** 2
    control_errors = (control_best_prediction - test_ages) ** 2

    bootstrap = {
        "teacher_minus_best_w2s": paired_ci(
            teacher_errors, best_errors, seed=SEED + 10
        ),
        "final_minus_best_w2s": paired_ci(
            final_errors, best_errors, seed=SEED + 11
        ),
        "control_minus_best_w2s": paired_ci(
            control_errors, best_errors, seed=SEED + 12
        ),
    }
    direct_best_mse = direct_rows[direct_best_index]["true_mse"]
    denominator = teacher_mse - direct_best_mse
    checkpoint_rows = []
    for index in range(EPOCHS):
        pgr = (
            (teacher_mse - w2s_rows[index]["true_mse"]) / denominator
            if denominator > 0
            else math.nan
        )
        checkpoint_rows.append(
            {
                "epoch": index + 1,
                "teacher_mse": teacher_mse,
                "w2s_mse": w2s_rows[index]["true_mse"],
                "direct_mse": direct_rows[index]["true_mse"],
                "shuffled_control_mse": control_rows[index]["true_mse"],
                "student_teacher_fit_mse": w2s_rows[index][
                    "teacher_fit_mse"
                ],
                "PGR_using_best_direct_ceiling": pgr,
                "projection_k80": k80_by_epoch[index],
            }
        )

    real_w2s = (
        bootstrap["teacher_minus_best_w2s"]["ci95_low"] > 0
        and denominator > 0
    )
    early_stopping = (
        best_index + 1 < EPOCHS
        and bootstrap["final_minus_best_w2s"]["ci95_low"] > 0
    )
    control_passed = (
        bootstrap["control_minus_best_w2s"]["ci95_low"] > 0
    )
    status = (
        "VERIFIED"
        if real_w2s and early_stopping and control_passed
        else "BLOCKED"
    )

    with (OUT / "checkpoints.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(checkpoint_rows[0])
        )
        writer.writeheader()
        writer.writerows(checkpoint_rows)
    prediction_rows = []
    for index in range(TEST_SIZE):
        prediction_rows.append(
            {
                "test_index": index,
                "age": float(test_ages[index]),
                "teacher": float(teacher_test_prediction[index]),
                "w2s_best": float(best_prediction[index]),
                "w2s_final": float(final_prediction[index]),
                "direct_best": float(direct_best_prediction[index]),
                "shuffled_control_best": float(
                    control_best_prediction[index]
                ),
            }
        )
    with (OUT / "test_predictions.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(prediction_rows[0])
        )
        writer.writeheader()
        writer.writerows(prediction_rows)
    (OUT / "bootstrap.json").write_text(
        json.dumps(bootstrap, indent=2) + "\n"
    )

    summary = {
        "claim": "Figures 2-3 real architectures and early stopping",
        "verdict": status,
        "source_sha256": (
            "4d29b2ae21c4611695532f6fd304b22f678139a19311e21e9b65d8a6d0b00089"
        ),
        "protocol": {
            "dataset": "nlphuji/utk_faces",
            "dataset_revision": DATA_REVISION,
            "dataset_metadata_sha256": METADATA_SHA256,
            "dataset_images_sha256": IMAGES_SHA256,
            "total_metadata_rows": len(metadata),
            "train_size": TRAIN_SIZE,
            "test_size": TEST_SIZE,
            "teacher_labeled_samples": TEACHER_LABELS,
            "teacher": "torchvision ResNet18 ImageNet-1K V1, frozen",
            "teacher_checkpoint_sha256": sha256(resnet_checkpoint),
            "student": (
                "official OpenAI CLIP ViT-B/32, frozen, "
                "768-dimensional pre-projection features"
            ),
            "student_checkpoint_sha256": sha256(clip_checkpoint),
            "student_epochs": EPOCHS,
            "paper_primary_UTKFace_epochs": 5,
            "extended_early_stopping_audit_epochs": EPOCHS,
            "batch_size": BATCH_SIZE,
            "learning_rate": 1e-4,
            "momentum": 0.9,
            "ridge_alpha": 1e-6,
            "PCA_samples": 10_000,
            "seed": SEED,
        },
        "results": {
            "teacher_mse": teacher_mse,
            "best_w2s_epoch": best_index + 1,
            "best_w2s_mse": w2s_rows[best_index]["true_mse"],
            "final_w2s_mse": w2s_rows[-1]["true_mse"],
            "best_direct_epoch": direct_best_index + 1,
            "best_direct_mse": direct_best_mse,
            "best_control_epoch": control_best_index + 1,
            "best_control_mse": control_rows[control_best_index][
                "true_mse"
            ],
            "best_PGR": max(
                row["PGR_using_best_direct_ceiling"]
                for row in checkpoint_rows
            ),
            "best_projection_k80": k80_by_epoch[best_index],
            "bootstrap": bootstrap,
            "real_architecture_W2S_verified": real_w2s,
            "early_stopping_critical_verified": early_stopping,
            "shuffled_pseudolabel_control_passed": control_passed,
        },
        "resource": {
            "estimated_required_cores": 24,
            "torch_compute_threads": THREADS,
            "image_loader_workers": WORKERS,
            "actual_logical_cpu_allocation": os.cpu_count(),
            "selected_backend": "hf",
            "selected_flavor": "cpu-upgrade",
            "runtime_s": time.perf_counter() - started,
            "stage_runtime_s": stage_times,
        },
        "limitations": [
            "The paper does not publish its exact train/test indices; this run uses a pinned seeded split.",
            "The 20-epoch early-stopping audit extends the paper's five-epoch UTKFace projection-energy protocol.",
            "This run reproduces the real W2S arm, not the expensive ViT-L/16 fine-tuning arm of Figure 2.",
        ],
    }
    (OUT / "experiment_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n"
    )
    print(f"CLAIM5_RESULT_JSON={json.dumps(summary, sort_keys=True)}")


if __name__ == "__main__":
    main()
