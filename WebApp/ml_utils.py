"""ML inference — Organic (O) / Recyclable (R) → Biodegradable / Non-Biodegradable."""
from __future__ import annotations

import io
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent.parent

IMG_SIZE_LEGACY = (150, 150)
IMG_SIZE_MOBILENET = (224, 224)

DEFAULT_CONFIG = {
    "class_names": ["O", "R"],
    "biodegradable_classes": ["O"],
    "display_names": {"O": "Organic Waste", "R": "Recyclable Waste"},
}

CATEGORY_MAP_LEGACY = {
    "Organic": ("Biodegradable", "#28A745", "Organic Waste"),
    "Recyclable": ("Non-Biodegradable", "#DC3545", "Recyclable Waste"),
}

DISPOSAL_TIPS = {
    "Organic": "Dispose in the green wet / biodegradable waste bin.",
    "Recyclable": "Rinse and place in the dry / recyclable (non-biodegradable) bin.",
    "O": "Dispose in the green organic / biodegradable bin.",
    "R": "Rinse and place in the recyclable (non-biodegradable) bin.",
}

MODEL_CANDIDATES = [
    APP_DIR.parent / "Jupyter File" / "waste_classification_model.keras",
    APP_DIR.parent / "Jupyter File" / "waste_classification_model.h5",
    APP_DIR / "saved_models" / "waste_classification_model.h5",
    APP_DIR / "saved_models" / "waste_classification_model.keras",
    APP_DIR / "waste_classification_model.h5",
    PROJECT_ROOT / "saved_models" / "waste_classification_model.h5",
    Path(os.environ.get("SMARTWASTE_MODEL_PATH", "")),
]


def find_model_path() -> Path | None:
    for p in MODEL_CANDIDATES:
        if p and str(p) and p.is_file():
            return p
    return None


def load_model_config() -> dict:
    for base in (APP_DIR, PROJECT_ROOT):
        path = base / "model_config.json"
        if path.is_file():
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return DEFAULT_CONFIG.copy()


def build_model_architecture():
    from tensorflow.keras import layers, models

    return models.Sequential(
        [
            layers.Conv2D(32, (3, 3), activation="relu", input_shape=(150, 150, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(128, (3, 3), activation="relu"),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(512, activation="relu"),
            layers.Dense(1, activation="sigmoid"),
        ]
    )


def load_keras_model():
    import tensorflow as tf

    last_path = None
    for path in MODEL_CANDIDATES:
        if not path or not str(path) or not path.is_file():
            continue
        last_path = path
        try:
            model = tf.keras.models.load_model(str(path), compile=False)
            return model, str(path)
        except Exception:
            continue
    return None, str(last_path) if last_path else None


def _is_mobilenet(model) -> bool:
    try:
        shape = model.input_shape
        if shape and len(shape) >= 3 and shape[1] == 224:
            return True
        out = model.output_shape
        if out and len(out) >= 2 and out[-1] in (2, 6):
            return True
    except Exception:
        pass
    return False


def preprocess_image(image_bytes: bytes, size: tuple[int, int], mobilenet: bool) -> np.ndarray:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = _fit_image(img, size)
    arr = np.asarray(img, dtype=np.float32)
    if mobilenet:
        try:
            from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

            arr = preprocess_input(arr)
        except Exception:
            arr = arr / 127.5 - 1.0
    else:
        arr = arr / 255.0
    return np.expand_dims(arr, axis=0)


def _fit_image(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(img, size, Image.Resampling.LANCZOS)


def _predict_mobilenet(model, batch, cfg: dict) -> tuple[str, float]:
    preds = model.predict(batch, verbose=0)[0]
    names = cfg.get("class_names", ["O", "R"])
    if len(preds) == len(names):
        idx = int(np.argmax(preds))
        cls = names[idx]
        conf = float(preds[idx])
    elif len(preds) == 2:
        idx = int(np.argmax(preds))
        cls = "O" if idx == 0 else "R"
        conf = float(preds[idx])
    else:
        idx = int(np.argmax(preds))
        cls = str(idx)
        conf = float(preds[idx])

    bio_set = set(cfg.get("biodegradable_classes", ["O"]))
    display = cfg.get("display_names", {})
    category = "Biodegradable" if cls in bio_set else "Non-Biodegradable"
    item = display.get(cls, cls)
    color = "#28A745" if category == "Biodegradable" else "#DC3545"
    tip = DISPOSAL_TIPS.get(cls, DISPOSAL_TIPS.get("Organic" if category == "Biodegradable" else "Recyclable", ""))
    return category, conf, item, cls, color, tip


def _predict_binary(model, batch) -> tuple[str, float]:
    prob = float(model.predict(batch, verbose=0)[0][0])
    class_name = "Recyclable" if prob >= 0.5 else "Organic"
    confidence = prob if class_name == "Recyclable" else 1.0 - prob
    category, color, item = CATEGORY_MAP_LEGACY[class_name]
    return category, confidence, item, class_name, color, DISPOSAL_TIPS[class_name]


def predict_waste(image_bytes: bytes) -> dict:
    import streamlit as st

    model, model_path = st.session_state.get("_sw_model_cache", (None, None))
    if model is None and "_sw_model_loaded" not in st.session_state:
        model, model_path = load_keras_model()
        st.session_state["_sw_model_cache"] = (model, model_path)
        st.session_state["_sw_model_loaded"] = True

    if model is None:
        return {
            "class_name": None,
            "category": None,
            "item": None,
            "confidence": 0.0,
            "tip": "",
            "color": "#94a3b8",
            "model_loaded": False,
            "model_path": model_path,
        }

    mobilenet = _is_mobilenet(model)
    size = IMG_SIZE_MOBILENET if mobilenet else IMG_SIZE_LEGACY
    batch = preprocess_image(image_bytes, size, mobilenet)

    if mobilenet or (hasattr(model, "output_shape") and model.output_shape[-1] not in (1,)):
        cfg = load_model_config()
        category, conf, item, cls, color, tip = _predict_mobilenet(model, batch, cfg)
        class_name = cls
    else:
        category, conf, item, class_name, color, tip = _predict_binary(model, batch)

    return {
        "class_name": class_name,
        "category": category,
        "item": item,
        "confidence": round(conf * 100, 1),
        "tip": tip,
        "color": color,
        "model_loaded": True,
        "model_path": model_path,
    }
