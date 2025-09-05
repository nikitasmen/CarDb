from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Tuple
import uuid


ALLOWED_KEYS = [
    "id",
    "model",
    "manufacturer",
    "year",
    "country_of_origin",
    "category",
    "replica_model",
    "info",
]


@dataclass
class Car:
    id: str
    model: str
    manufacturer: str = ""
    year: str = ""
    country_of_origin: str = ""
    category: str = ""
    replica_model: str = ""
    info: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Car":
        normalized = normalize_car_record(data or {})
        return Car(**normalized)


def _coerce_year(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    # Keep as string for UI compatibility; validate range if numeric
    if text.isdigit():
        year_int = int(text)
        if 1885 <= year_int <= 2100:
            return str(year_int)
        return ""  # out-of-range cleaned to empty
    return text  # leave non-digit as-is; could be 'N/A'


def normalize_car_record(data: Dict[str, Any]) -> Dict[str, Any]:
    # Key normalization already handled in importers, enforce again defensively
    norm: Dict[str, Any] = {}
    for key, value in (data or {}).items():
        key_norm = str(key).lower().replace(" ", "_")
        if key_norm in ALLOWED_KEYS:
            norm[key_norm] = value

    # Ensure all keys exist and trim strings
    def _s(v: Any) -> str:
        return str(v).strip() if v is not None else ""

    # Generate or preserve id
    record_id = str(norm.get("id", "")).strip()
    if not record_id:
        record_id = str(uuid.uuid4())

    normalized = {
        "id": record_id,
        "model": _s(norm.get("model", "")),
        "manufacturer": _s(norm.get("manufacturer", "")),
        "year": _coerce_year(norm.get("year")),
        "country_of_origin": _s(norm.get("country_of_origin", "")),
        "category": _s(norm.get("category", "")),
        "replica_model": _s(norm.get("replica_model", "")),
        "info": _s(norm.get("info", "")),
    }

    return Car(**normalized).to_dict()


def validate_car_record(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    car_id = str(data.get("id", "")).strip()
    if not car_id:
        errors.append("id is required")
    model = str(data.get("model", "")).strip()
    if not model:
        errors.append("model is required")

    year = str(data.get("year", "")).strip()
    if year and year.isdigit():
        year_int = int(year)
        if year_int < 1885 or year_int > 2100:
            errors.append("year out of valid range (1885-2100)")

    info = str(data.get("info", "")).strip()
    if info and not (info.startswith("http://") or info.startswith("https://")):
        # not fatal; warn-only
        pass

    return (len(errors) == 0, errors)


def to_car_list(records: List[Dict[str, Any]]) -> List[Car]:
    cars: List[Car] = []
    for rec in (records or []):
        try:
            cars.append(Car.from_dict(rec))
        except Exception:
            continue
    return cars


def to_dict_list(cars: List[Car]) -> List[Dict[str, Any]]:
    return [c.to_dict() for c in (cars or [])]


