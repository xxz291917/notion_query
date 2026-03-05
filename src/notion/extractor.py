"""Extract structured data from Notion page properties."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def extract_title(properties: dict) -> str:
    """Find and extract the title property value."""
    for prop in properties.values():
        if prop["type"] == "title":
            return _rich_text_to_plain(prop.get("title", []))
    return ""


def extract_properties(properties: dict) -> dict[str, Any]:
    """Extract all page properties into a flat dict suitable for metadata."""
    result: dict[str, Any] = {}
    for name, prop in properties.items():
        ptype = prop["type"]
        try:
            result[name] = _extract_single(ptype, prop)
        except Exception:
            logger.debug(f"Skipping property {name} ({ptype})")
    return result


def _extract_single(ptype: str, prop: dict) -> Any:
    extractors = {
        "title": lambda p: _rich_text_to_plain(p.get("title", [])),
        "rich_text": lambda p: _rich_text_to_plain(p.get("rich_text", [])),
        "number": lambda p: p.get("number"),
        "select": lambda p: p.get("select", {}).get("name") if p.get("select") else None,
        "multi_select": lambda p: [o["name"] for o in p.get("multi_select", [])],
        "status": lambda p: p.get("status", {}).get("name") if p.get("status") else None,
        "date": lambda p: _extract_date(p.get("date")),
        "people": lambda p: [_extract_person(person) for person in p.get("people", [])],
        "relation": lambda p: [r["id"] for r in p.get("relation", [])],
        "formula": lambda p: _extract_formula(p.get("formula", {})),
        "rollup": lambda p: _extract_rollup(p.get("rollup", {})),
        "checkbox": lambda p: p.get("checkbox"),
        "url": lambda p: p.get("url"),
        "email": lambda p: p.get("email"),
        "phone_number": lambda p: p.get("phone_number"),
        "unique_id": lambda p: _extract_unique_id(p.get("unique_id", {})),
        "created_time": lambda p: p.get("created_time"),
        "last_edited_time": lambda p: p.get("last_edited_time"),
        "created_by": lambda p: _extract_person(p.get("created_by", {})),
        "last_edited_by": lambda p: _extract_person(p.get("last_edited_by", {})),
        "files": lambda p: [_extract_file(f) for f in p.get("files", [])],
    }
    extractor = extractors.get(ptype)
    if extractor:
        return extractor(prop)
    return None


def _rich_text_to_plain(rich_text: list[dict]) -> str:
    return "".join(segment.get("plain_text", "") for segment in rich_text)


def _extract_date(date_obj: dict | None) -> str | None:
    if not date_obj:
        return None
    start = date_obj.get("start", "")
    end = date_obj.get("end")
    return f"{start} → {end}" if end else start


def _extract_person(person: dict) -> str:
    return person.get("name", person.get("id", ""))


def _extract_formula(formula: dict) -> Any:
    ftype = formula.get("type")
    if ftype:
        return formula.get(ftype)
    return None


def _extract_rollup(rollup: dict) -> Any:
    rtype = rollup.get("type")
    if rtype == "array":
        return [_extract_single(item["type"], item) for item in rollup.get("array", [])]
    if rtype:
        return rollup.get(rtype)
    return None


def _extract_unique_id(uid: dict) -> str | None:
    prefix = uid.get("prefix", "")
    number = uid.get("number")
    if number is not None:
        return f"{prefix}-{number}" if prefix else str(number)
    return None


def _extract_file(file_obj: dict) -> str:
    ftype = file_obj.get("type", "")
    if ftype == "file":
        return file_obj.get("file", {}).get("url", "")
    elif ftype == "external":
        return file_obj.get("external", {}).get("url", "")
    return file_obj.get("name", "")


def page_to_document(page: dict, blocks_md: str, db_name: str = "") -> dict:
    """Convert a Notion page + its block content into a document dict for indexing.

    Returns:
        {
            "notion_id": str,
            "title": str,
            "url": str,
            "db_type": str,
            "properties": dict,  # structured metadata
            "content": str,      # full text for embedding
            "last_edited": str,
        }
    """
    props = extract_properties(page.get("properties", {}))
    title = extract_title(page.get("properties", {}))
    url = page.get("url", "")
    notion_id = page["id"]
    last_edited = page.get("last_edited_time", "")

    # Build content: properties summary + block content
    prop_lines = []
    for k, v in props.items():
        if v is not None and v != "" and v != []:
            prop_lines.append(f"{k}: {v}")
    props_text = "\n".join(prop_lines)

    content = f"# {title}\n\n"
    if props_text:
        content += f"{props_text}\n\n"
    if blocks_md:
        content += blocks_md

    return {
        "notion_id": notion_id,
        "title": title,
        "url": url,
        "db_type": db_name,
        "properties": props,
        "content": content.strip(),
        "last_edited": last_edited,
    }
