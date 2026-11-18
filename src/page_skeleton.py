"""Turn an HTML page into a structure skeleton without content.

The skeleton keeps what is needed to design selectors: element names,
attribute names, CSS classes and the values of role and type. Texts become
<TEXT:n> or <NUM:n>, other attribute values <VAL:n> and links <URL>, where n
is the length (written with the brackets ⟨ ⟩). Format and reasons:
03_programmierprojekt.md, phase 2.

Usage (from the repository folder):
    python -m src.page_skeleton <folder with saved .html pages> <target folder>
This regenerates the skeleton of every saved page without visiting any site,
e.g. after the rules here were sharpened.
"""

import argparse
import re
import sys
import textwrap
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

# Elements without end tag; they never contain other elements.
VOID_ELEMENTS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
})
# Removed together with their content. head contains e.g. the page title,
# which often names the farm; selectors only need the body.
DROPPED_ELEMENTS = frozenset({"head", "script", "style", "meta", "link", "noscript", "template"})
# Kept as an element (with its classes), but without content: icons.
EMPTIED_ELEMENTS = frozenset({"svg"})

# Attributes whose values are kept, if they look like plain keywords.
KEPT_VALUE_ATTRIBUTES = frozenset({"role", "type"})
KEPT_VALUE_PATTERN = re.compile(r"[A-Za-z0-9_ -]{1,40}")
# Attributes that hold links, and value beginnings that look like links.
URL_ATTRIBUTES = frozenset({"href", "src", "srcset", "action", "formaction", "poster", "xlink:href"})
URL_PREFIXES = ("http:", "https:", "/", "#", "mailto:", "tel:", "./", "../")

TAG_PATTERN = re.compile(r"[a-z][a-z0-9._:-]*")
ATTRIBUTE_NAME_PATTERN = re.compile(r"[a-z_:@][a-z0-9_:.@-]*")
CLASS_TOKEN_PATTERN = re.compile(r"[!-~]+")  # printable ASCII without spaces
LONG_DIGITS = re.compile(r"[0-9]{3,}")  # e.g. a profile id in "host-12345"
# Only digits and characters of numbers, dates and counts, with at least one digit.
NUMBER_PATTERN = re.compile(r"[0-9 .,:;/()+%-]*[0-9][0-9 .,:;/()+%-]*")
# For comparing structures: lengths and counts do not matter.
LENGTHS = re.compile(r"⟨(TEXT|NUM|VAL):\d+⟩")
FOLD_COUNTS = re.compile(r"× \d+ more")

INDENT = "  "
MIN_RUN_TO_FOLD = 3  # at least this many alike siblings in a row are folded
SHOWN_OF_RUN = 2  # ... and this many of them stay visible
MAX_LINES = 4000
# Deeper levels are cut; real pages stay far below. Without a limit, very deep
# nesting would exceed Python's recursion limit.
MAX_DEPTH = 100


class SkeletonError(Exception):
    """Skeletons could not be written; the message says why."""


# ---------------------------------------------------------------- building a tree


@dataclass
class Text:
    content: str


@dataclass
class Element:
    tag: str
    attrs: list[tuple[str, str | None]]
    children: list["Element | Text"] = field(default_factory=list)


class TreeBuilder(HTMLParser):
    """Builds a tree of Element and Text from HTML.

    html.parser only reports events (start tag, text, end tag); this class
    turns them into a tree. Dropped elements are skipped with their content.
    """

    def __init__(self):
        # convert_charrefs: "&amp;" arrives as "&"
        super().__init__(convert_charrefs=True)
        self.root = Element("#root", [])
        self.open_elements = [self.root]
        self.skipped: list[str] = []  # open tags inside a dropped or emptied element

    @property
    def current(self) -> Element:
        return self.open_elements[-1]

    def handle_starttag(self, tag, attrs):
        if self.skipped:
            if tag not in VOID_ELEMENTS:
                self.skipped.append(tag)
            return
        if tag in DROPPED_ELEMENTS:
            if tag not in VOID_ELEMENTS:
                self.skipped.append(tag)
            return
        element = Element(tag, attrs)
        self.current.children.append(element)
        if tag in EMPTIED_ELEMENTS:
            self.skipped.append(tag)
        elif tag not in VOID_ELEMENTS:
            self.open_elements.append(element)

    def handle_startendtag(self, tag, attrs):
        # A self-closing tag such as <br/> or <svg ... />: never has content.
        if self.skipped or tag in DROPPED_ELEMENTS:
            return
        self.current.children.append(Element(tag, attrs))

    def handle_endtag(self, tag):
        if self.skipped:
            if tag in self.skipped:
                # close the tag and anything left open inside it
                while self.skipped.pop() != tag:
                    pass
            return
        # Close the matching open element; an end tag without one is ignored.
        for position in range(len(self.open_elements) - 1, 0, -1):
            if self.open_elements[position].tag == tag:
                del self.open_elements[position:]
                return

    def handle_data(self, data):
        if self.skipped:
            return
        children = self.current.children
        if children and isinstance(children[-1], Text):
            children[-1].content += data  # text split by a dropped element stays one text
        else:
            children.append(Text(data))


# ---------------------------------------------------------------- placeholders


def text_placeholder(content: str) -> str | None:
    """⟨NUM:n⟩ or ⟨TEXT:n⟩ for a text, None for whitespace only."""
    text = " ".join(content.split())
    if not text:
        return None
    kind = "NUM" if NUMBER_PATTERN.fullmatch(text) else "TEXT"
    return f"⟨{kind}:{len(text)}⟩"


def class_token(token: str) -> str:
    """A CSS class, with long digit runs (ids) and unusual tokens replaced."""
    if not CLASS_TOKEN_PATTERN.fullmatch(token):
        return f"⟨VAL:{len(token)}⟩"
    return LONG_DIGITS.sub(lambda match: f"⟨NUM:{len(match[0])}⟩", token)


def attribute_value(name: str, value: str) -> tuple[str, bool]:
    """Return the shown value and whether it is a kept keyword."""
    if name in KEPT_VALUE_ATTRIBUTES and KEPT_VALUE_PATTERN.fullmatch(value):
        return value, True
    if name in URL_ATTRIBUTES or value.strip().lower().startswith(URL_PREFIXES):
        return "⟨URL⟩", False
    return f"⟨VAL:{len(value)}⟩", False


# ---------------------------------------------------------------- rendering


@dataclass
class Tokens:
    """Every readable word in a skeleton, for the check before sharing."""

    elements: set[str] = field(default_factory=set)
    attributes: set[str] = field(default_factory=set)
    classes: set[str] = field(default_factory=set)
    keywords: set[str] = field(default_factory=set)  # kept role and type values


class Renderer:
    def __init__(self):
        self.tokens = Tokens()
        self.folded_runs = 0

    def signature(self, element: Element) -> str:
        """One line describing an element, e.g. div.card[role=listitem]."""
        tag = element.tag if TAG_PATTERN.fullmatch(element.tag) else f"⟨TAG:{len(element.tag)}⟩"
        self.tokens.elements.add(tag)
        parts = [tag]

        attributes = []
        for name, value in sorted(element.attrs, key=lambda attr: attr[0]):
            if name == "class":
                for token in (value or "").split():
                    shown = class_token(token)
                    self.tokens.classes.add(shown)
                    parts.append("." + shown)
                continue
            shown_name = name if ATTRIBUTE_NAME_PATTERN.fullmatch(name) else f"⟨ATTR:{len(name)}⟩"
            self.tokens.attributes.add(shown_name)
            if value is None:  # attribute without value, e.g. hidden
                attributes.append(f"[{shown_name}]")
                continue
            shown_value, is_keyword = attribute_value(name, value)
            if is_keyword:
                self.tokens.keywords.add(shown_value)
            attributes.append(f"[{shown_name}={shown_value}]")
        return "".join(parts + attributes)

    def render_element(self, element: Element, depth: int) -> list[str]:
        indent = INDENT * depth
        if depth >= MAX_DEPTH:
            return [f"{indent}⋯ deeper levels cut"]
        line = indent + self.signature(element)
        children = [
            child for child in element.children
            if isinstance(child, Element) or text_placeholder(child.content)
        ]
        if len(children) == 1 and isinstance(children[0], Text):
            # A single text stays on the line of its element.
            return [f"{line} {text_placeholder(children[0].content)}"]
        return [line] + self.render_children(children, depth + 1)

    def render_children(self, children: list[Element | Text], depth: int) -> list[str]:
        blocks = []
        for child in children:
            if isinstance(child, Text):
                placeholder = text_placeholder(child.content)
                if placeholder:
                    blocks.append((child, [INDENT * depth + placeholder]))
            else:
                blocks.append((child, self.render_element(child, depth)))

        lines: list[str] = []
        start = 0
        while start < len(blocks):
            key = structure_key(blocks[start][1])
            end = start + 1
            while end < len(blocks) and structure_key(blocks[end][1]) == key:
                end += 1
            run = blocks[start:end]
            if len(run) >= MIN_RUN_TO_FOLD and isinstance(run[0][0], Element):
                for _child, block in run[:SHOWN_OF_RUN]:
                    lines += block
                lines.append(f"{INDENT * depth}⋯ × {len(run) - SHOWN_OF_RUN} more like above")
                self.folded_runs += 1
            else:
                for _child, block in run:
                    lines += block
            start = end
        return lines


def structure_key(block: list[str]) -> tuple[str, ...]:
    """Lines of a block with lengths and fold counts removed.

    Two cards with texts of different length, or with lists of different
    length inside, count as alike.
    """
    return tuple(FOLD_COUNTS.sub("× N more", LENGTHS.sub(r"⟨\1⟩", line)) for line in block)


def token_lines(tokens: Tokens) -> list[str]:
    lines = ["# --- readable tokens: check these before sharing ---"]
    groups = [
        ("elements", tokens.elements),
        ("attributes", tokens.attributes),
        ("classes", tokens.classes),
        ("role and type values", tokens.keywords),
    ]
    for label, values in groups:
        text = ", ".join(sorted(values)) or "(none)"
        wrapped = textwrap.wrap(f"{label}: {text}", width=100, break_on_hyphens=False)
        lines.append("# " + wrapped[0])
        lines += ["#     " + line for line in wrapped[1:]]
    return lines


@dataclass(frozen=True)
class Skeleton:
    text: str  # the whole file: header, structure lines, token list
    lines: int  # number of structure lines, as stated in the header


def skeleton_from_html(html: str) -> str:
    """Return the skeleton of an HTML page as text."""
    return build_skeleton(html).text


def build_skeleton(html: str) -> Skeleton:
    """Build the skeleton of an HTML page."""
    builder = TreeBuilder()
    builder.feed(html)
    builder.close()

    renderer = Renderer()
    lines = renderer.render_children(builder.root.children, 0)
    truncated = len(lines) > MAX_LINES
    if truncated:
        lines = lines[:MAX_LINES] + [f"⋯ skeleton truncated after {MAX_LINES} lines"]

    header = f"# structure skeleton: {len(lines)} lines, {renderer.folded_runs} folded runs"
    if truncated:
        header += ", truncated"
    text = "\n".join([header, "", *lines, "", *token_lines(renderer.tokens)]) + "\n"
    return Skeleton(text=text, lines=len(lines))


# ---------------------------------------------------------------- main


def regenerate(samples_dir: Path, target_dir: Path) -> int:
    """Write the skeleton of every .html file in samples_dir. Returns the number of files."""
    if not samples_dir.is_dir():
        raise SkeletonError(f"{samples_dir}: folder not found")
    paths = sorted(samples_dir.glob("*.html", case_sensitive=False))
    if not paths:
        raise SkeletonError(f"{samples_dir}: no .html files")
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        for path in paths:
            skeleton = build_skeleton(path.read_text(encoding="utf-8", errors="replace"))
            target = target_dir / f"{path.stem}.txt"
            target.write_text(skeleton.text, encoding="utf-8")
            print(f"{path.name} -> {target.name} ({skeleton.lines} lines)")
    except OSError as error:
        raise SkeletonError(f"could not read or write a file ({error.strerror})") from None
    return len(paths)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Regenerate skeletons from saved .html pages.")
    parser.add_argument("samples_dir", type=Path, help="folder with saved .html pages")
    parser.add_argument("target_dir", type=Path, help="folder for the skeletons (.txt)")
    args = parser.parse_args(argv)
    try:
        count = regenerate(args.samples_dir, args.target_dir)
    except SkeletonError as error:
        sys.exit(f"Skeleton error: {error}")
    print(f"{count} skeletons written to {args.target_dir}")


if __name__ == "__main__":
    main()
