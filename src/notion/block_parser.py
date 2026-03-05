"""Convert Notion blocks to Markdown text."""

import logging

logger = logging.getLogger(__name__)


def blocks_to_markdown(blocks: list[dict], depth: int = 0) -> str:
    """Convert a list of Notion blocks into Markdown string."""
    lines: list[str] = []
    for block in blocks:
        md = _block_to_md(block, depth)
        if md is not None:
            lines.append(md)
        # Recurse into children
        children = block.get("children", [])
        if children:
            lines.append(blocks_to_markdown(children, depth + 1))
    return "\n".join(lines)


def _block_to_md(block: dict, depth: int) -> str | None:
    btype = block.get("type", "")
    data = block.get(btype, {})
    indent = "  " * depth

    handler = _HANDLERS.get(btype)
    if handler:
        return handler(data, indent, depth)

    # Fallback: try to extract rich_text from unknown block types
    if isinstance(data, dict) and "rich_text" in data:
        return f"{indent}{_rt(data)}"
    return None


# ── Rich text helper ──

def _rt(data: dict) -> str:
    """Extract plain text from a block's rich_text array."""
    return "".join(seg.get("plain_text", "") for seg in data.get("rich_text", []))


# ── Block type handlers ──

def _paragraph(data, indent, depth):
    text = _rt(data)
    return f"{indent}{text}" if text else ""


def _heading_1(data, indent, depth):
    return f"# {_rt(data)}"


def _heading_2(data, indent, depth):
    return f"## {_rt(data)}"


def _heading_3(data, indent, depth):
    return f"### {_rt(data)}"


def _bulleted_list_item(data, indent, depth):
    return f"{indent}- {_rt(data)}"


def _numbered_list_item(data, indent, depth):
    return f"{indent}1. {_rt(data)}"


def _to_do(data, indent, depth):
    checked = "x" if data.get("checked") else " "
    return f"{indent}- [{checked}] {_rt(data)}"


def _toggle(data, indent, depth):
    return f"{indent}<details><summary>{_rt(data)}</summary>"


def _code(data, indent, depth):
    lang = data.get("language", "")
    text = _rt(data)
    return f"{indent}```{lang}\n{text}\n{indent}```"


def _quote(data, indent, depth):
    return f"{indent}> {_rt(data)}"


def _callout(data, indent, depth):
    icon = data.get("icon", {})
    emoji = icon.get("emoji", "") if icon else ""
    return f"{indent}> {emoji} {_rt(data)}"


def _divider(data, indent, depth):
    return f"{indent}---"


def _table_row(data, indent, depth):
    cells = data.get("cells", [])
    row_texts = []
    for cell in cells:
        cell_text = "".join(seg.get("plain_text", "") for seg in cell)
        row_texts.append(cell_text)
    return f"{indent}| {' | '.join(row_texts)} |"


def _image(data, indent, depth):
    url = ""
    if data.get("type") == "file":
        url = data.get("file", {}).get("url", "")
    elif data.get("type") == "external":
        url = data.get("external", {}).get("url", "")
    caption = "".join(seg.get("plain_text", "") for seg in data.get("caption", []))
    return f"{indent}![{caption}]({url})"


def _bookmark(data, indent, depth):
    url = data.get("url", "")
    caption = "".join(seg.get("plain_text", "") for seg in data.get("caption", []))
    label = caption or url
    return f"{indent}[{label}]({url})"


def _embed(data, indent, depth):
    return f"{indent}[embed]({data.get('url', '')})"


def _equation(data, indent, depth):
    return f"{indent}$${data.get('expression', '')}$$"


def _child_database(data, indent, depth):
    return f"{indent}> [Child Database: {data.get('title', '')}]"


def _child_page(data, indent, depth):
    return f"{indent}> [Child Page: {data.get('title', '')}]"


def _link_preview(data, indent, depth):
    return f"{indent}[{data.get('url', '')}]({data.get('url', '')})"


_HANDLERS = {
    "paragraph": _paragraph,
    "heading_1": _heading_1,
    "heading_2": _heading_2,
    "heading_3": _heading_3,
    "bulleted_list_item": _bulleted_list_item,
    "numbered_list_item": _numbered_list_item,
    "to_do": _to_do,
    "toggle": _toggle,
    "code": _code,
    "quote": _quote,
    "callout": _callout,
    "divider": _divider,
    "table_row": _table_row,
    "image": _image,
    "bookmark": _bookmark,
    "embed": _embed,
    "equation": _equation,
    "child_database": _child_database,
    "child_page": _child_page,
    "link_preview": _link_preview,
}
