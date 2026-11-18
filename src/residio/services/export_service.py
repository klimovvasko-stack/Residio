import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
import yaml

from repositories import student_repository

# Папка out в корне проекта
BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "out"


def _flatten_dict(record: dict[str, Any], parent_key: str = "", sep: str = "_") -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for key, value in record.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flat.update(_flatten_dict(value, new_key, sep=sep))
        elif isinstance(value, list):
            flat[new_key] = ";".join(map(str, value))
        else:
            flat[new_key] = value
    return flat


def _dict_to_xml(parent: ET.Element, data: Any, item_tag: str = "item") -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            child = ET.SubElement(parent, str(key))
            _dict_to_xml(child, value, item_tag=item_tag)
    elif isinstance(data, list):
        for element in data:
            child = ET.SubElement(parent, item_tag)
            _dict_to_xml(child, element, item_tag=item_tag)
    elif data is None:
        parent.text = ""
    else:
        parent.text = str(data)


def export_records(
    records: list[dict[str, Any]],
    root_tag: str = "records",
    item_tag: str = "record",
    out_dir: Path = OUT_DIR,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON
    with (out_dir / "data.json").open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    # CSV 
    flat_records = [_flatten_dict(rec) for rec in records]
    nested_parents = {
        key for rec in records for key, val in rec.items() if isinstance(val, dict)
    }
    fieldnames: list[str] = []
    for rec in flat_records:
        for key in rec.keys():
            if key not in nested_parents and key not in fieldnames:
                fieldnames.append(key)

    with (out_dir / "data.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for rec in flat_records:
            clean_row = {k: ("" if v is None else v) for k, v in rec.items()}
            writer.writerow(clean_row)

    #XML
    root = ET.Element(root_tag)
    _dict_to_xml(root, records, item_tag=item_tag)
    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    tree.write(out_dir / "data.xml", encoding="utf-8", xml_declaration=True)

    #YAML
    with (out_dir / "data.yaml").open("w", encoding="utf-8") as f:
        yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False)

    return out_dir


def export_students_data() -> Path:
    data = student_repository.get_all_for_export()
    return export_records(data, root_tag="students", item_tag="student")    