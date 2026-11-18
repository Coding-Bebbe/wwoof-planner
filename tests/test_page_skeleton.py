"""Tests for src/page_skeleton.py with invented HTML only."""

import pytest

from src.page_skeleton import (
    INDENT,
    MAX_DEPTH,
    MAX_LINES,
    build_skeleton,
    main,
    skeleton_from_html,
)


def body_lines(html: str) -> list[str]:
    """The skeleton lines between the header and the token list."""
    skeleton = skeleton_from_html(html)
    lines = skeleton.splitlines()
    end = lines.index("# --- readable tokens: check these before sharing ---")
    return [line for line in lines[1:end] if line]


def token_section(html: str) -> str:
    skeleton = skeleton_from_html(html)
    return skeleton[skeleton.index("# --- readable tokens"):]


# ---------------------------------------------------------------- removing


def test_head_scripts_styles_and_comments_are_removed():
    html = """<!DOCTYPE html><html><head><title>Beispielhof Morgentau</title>
    <meta name="description" content="Hof"><link rel="stylesheet" href="/a.css"></head>
    <body><!-- comment --><script>var host = "Erika";</script><style>p {color: red}</style>
    <noscript>Bitte JavaScript</noscript><template><p>Vorlage</p></template><p>Hallo</p></body></html>"""

    assert body_lines(html) == ["html", "  body", "    p ⟨TEXT:5⟩"]


def test_svg_is_kept_without_content():
    html = '<span class="count"><svg class="icon icon-book" viewBox="0 0 10 10"><path d="M0 0"/><title>Gästebuch</title></svg>12</span>'

    assert body_lines(html) == [
        "span.count",
        "  svg.icon.icon-book[viewbox=⟨VAL:9⟩]",
        "  ⟨NUM:2⟩",
    ]


def test_self_closing_svg_is_kept():
    assert body_lines('<div><svg class="icon"/></div>') == ["div", "  svg.icon"]


# ---------------------------------------------------------------- texts


@pytest.mark.parametrize(
    ("text", "placeholder"),
    [
        ("Hallo Welt", "⟨TEXT:10⟩"),
        ("  Hallo \n   Welt  ", "⟨TEXT:10⟩"),
        ("12", "⟨NUM:2⟩"),
        ("(12)", "⟨NUM:4⟩"),
        ("01.06.2027 - 30.06.2027", "⟨NUM:23⟩"),
        ("12 Einträge", "⟨TEXT:11⟩"),
        ("Tom &amp; Jerry", "⟨TEXT:11⟩"),
    ],
)
def test_text_becomes_placeholder_with_length(text, placeholder):
    assert body_lines(f"<p>{text}</p>") == [f"p {placeholder}"]


def test_whitespace_only_text_is_dropped():
    assert body_lines("<div>\n   <p>A</p>\n   </div>") == ["div", "  p ⟨TEXT:1⟩"]


def test_mixed_text_and_elements_are_separate_lines():
    assert body_lines("<p>Ein <b>großer</b> Garten</p>") == [
        "p",
        "  ⟨TEXT:3⟩",
        "  b ⟨TEXT:6⟩",
        "  ⟨TEXT:6⟩",
    ]


# ---------------------------------------------------------------- attributes


def test_attributes_are_replaced_except_class_role_and_type():
    html = (
        '<button class="btn btn-primary" type="submit" role="button" id="ember123" '
        'aria-label="Erika anschreiben" data-host="musterhof" disabled>Senden</button>'
    )

    assert body_lines(html) == [
        "button.btn.btn-primary[aria-label=⟨VAL:17⟩][data-host=⟨VAL:9⟩][disabled]"
        "[id=⟨VAL:8⟩][role=button][type=submit] ⟨TEXT:6⟩"
    ]


@pytest.mark.parametrize(
    "attribute",
    [
        'href="https://example.org/farms/1001"',
        'href="/farms/1001"',
        'href="#calendar"',
        'href="mailto:erika@example.com"',
        'href="tel:+496990009123"',
        'src="https://example.org/img/hof.jpg"',
        'srcset="/img/a.jpg 1x, /img/b.jpg 2x"',
        'data-url="/farms/1001"',
    ],
)
def test_links_become_url(attribute):
    lines = body_lines(f"<a {attribute}>x</a>")

    assert "⟨URL⟩" in lines[0]
    assert "example" not in lines[0]
    assert "1001" not in lines[0]


def test_long_digit_runs_in_classes_are_replaced():
    lines = body_lines('<div class="host-12345 col-6 card">x</div>')

    assert lines == ["div.host-⟨NUM:5⟩.col-6.card ⟨TEXT:1⟩"]


def test_unusual_class_and_keyword_values_are_replaced():
    html = '<div class="höfe card" role="button&quot;onclick" type="Erika Mustermann wohnt hier am Waldrand seit vielen Jahren">x</div>'

    line = body_lines(html)[0]
    assert line.startswith("div.⟨VAL:4⟩.card")
    assert "[role=⟨VAL:" in line
    assert "[type=⟨VAL:" in line
    assert "Erika" not in line


# ---------------------------------------------------------------- tree


def test_void_elements_do_not_swallow_siblings():
    html = '<div><img src="/a.jpg" alt="Hof"><br><input type="text" name="q"><span>x</span></div>'

    assert body_lines(html) == [
        "div",
        "  img[alt=⟨VAL:3⟩][src=⟨URL⟩]",
        "  br",
        "  input[name=⟨VAL:1⟩][type=text]",
        "  span ⟨TEXT:1⟩",
    ]


def test_incomplete_html_does_not_crash():
    html = "<div><ul><li>a<li>b</ul><p>offen</div></span><table><tr><td>1"

    lines = body_lines(html)

    assert lines[0] == "div"
    assert any("⟨TEXT:5⟩" in line for line in lines)


# ---------------------------------------------------------------- folding


def test_alike_siblings_are_folded_after_two():
    items = "".join(f'<li class="item"><a href="/f/{n}">{"x" * n}</a></li>' for n in range(1, 6))

    assert body_lines(f'<ul class="list">{items}</ul>') == [
        "ul.list",
        "  li.item",
        "    a[href=⟨URL⟩] ⟨TEXT:1⟩",
        "  li.item",
        "    a[href=⟨URL⟩] ⟨TEXT:2⟩",
        "  ⋯ × 3 more like above",
    ]


def test_different_structure_is_not_folded():
    cards = (
        '<div class="card"><h2>A</h2></div>'
        '<div class="card"><h2>B</h2></div>'
        '<div class="card"><h2>C</h2><span class="badge">neu</span></div>'
    )

    lines = body_lines(f"<main>{cards}</main>")

    assert "⋯" not in "\n".join(lines)
    assert "    span.badge ⟨TEXT:3⟩" in lines


def test_cards_with_lists_of_different_length_are_alike():
    def card(n):
        return '<div class="card"><ul>' + "<li>x</li>" * n + "</ul></div>"

    lines = body_lines(f"<main>{card(3)}{card(4)}{card(5)}</main>")

    assert lines[-1] == "  ⋯ × 1 more like above"


def test_two_alike_siblings_are_not_folded():
    assert body_lines("<ul><li>a</li><li>b</li></ul>") == ["ul", "  li ⟨TEXT:1⟩", "  li ⟨TEXT:1⟩"]


# ---------------------------------------------------------------- header, size, tokens


def test_header_counts_lines_and_folded_runs():
    skeleton = build_skeleton("<ul>" + "<li>a</li>" * 4 + "</ul>")

    assert skeleton.text.splitlines()[0] == "# structure skeleton: 4 lines, 1 folded runs"
    assert skeleton.lines == 4


def test_size_is_limited():
    # Alternating siblings cannot be folded, so each one is a line.
    html = "<p>a</p><div>b</div>" * (MAX_LINES // 2 + 50)

    skeleton = skeleton_from_html(html)

    assert f"⋯ skeleton truncated after {MAX_LINES} lines" in skeleton
    assert skeleton.splitlines()[0].endswith(", truncated")


def test_depth_is_limited():
    html = "<div>" * (MAX_DEPTH + 500) + "x"

    lines = body_lines(html)

    assert lines[-1] == INDENT * MAX_DEPTH + "⋯ deeper levels cut"
    assert len(lines) == MAX_DEPTH + 1


def test_token_list_names_every_readable_word():
    html = '<div class="card" role="listitem"><a href="/x" data-id="7">x</a><input type="checkbox"></div>'

    tokens = token_section(html)

    assert "# elements: a, div, input" in tokens
    assert "# attributes: data-id, href, role, type" in tokens
    assert "# classes: card" in tokens
    assert "# role and type values: checkbox, listitem" in tokens


# ---------------------------------------------------------------- privacy


INVENTED_PROFILE = """<!DOCTYPE html>
<html lang="de">
<head>
  <title>Beispielhof Morgentau – Erika Mustermann</title>
  <meta property="og:title" content="Beispielhof Morgentau">
  <script>window.host = {"name": "Erika Mustermann", "email": "erika@example.com"};</script>
</head>
<body class="host-profile">
  <header><h1 class="host-name">Beispielhof Morgentau</h1>
    <img class="avatar" src="https://example.org/avatars/1001.jpg" alt="Foto von Erika Mustermann"></header>
  <section class="location" data-place="Musterdorf" data-lat="47.123456">
    <span class="town">Musterdorf</span>
    <address>Musterstraße 12, 12345 Musterdorf</address>
  </section>
  <div class="description" aria-label="Beschreibung von Max Mustermann">
    <p>Wir sind Erika und Max Mustermann. Ruf an: 069 90009 123.</p>
  </div>
  <a class="contact" href="mailto:erika@example.com" title="Erika Mustermann">E-Mail</a>
  <a class="phone" href="tel:+496990009123">069 90009 123</a>
  <span class="guestbook-count">12</span>
  <input type="hidden" name="host" value="beispielhof-morgentau">
</body>
</html>"""

PRIVATE_TEXTS = [
    "Beispielhof", "Morgentau", "Erika", "Mustermann", "Max", "erika@example.com",
    "example", "Musterdorf", "Musterstraße", "12345", "90009", "069", "1001",
    "47.123456", "Foto", "Beschreibung", "beispielhof-morgentau",
]


@pytest.mark.parametrize("private_text", PRIVATE_TEXTS)
def test_skeleton_of_invented_profile_contains_no_private_text(private_text):
    assert private_text not in skeleton_from_html(INVENTED_PROFILE)


def test_skeleton_of_invented_profile_keeps_structure():
    lines = body_lines(INVENTED_PROFILE)

    assert "  body.host-profile" in lines
    assert "      h1.host-name ⟨TEXT:21⟩" in lines
    assert "    span.guestbook-count ⟨NUM:2⟩" in lines
    assert "    a.contact[href=⟨URL⟩][title=⟨VAL:16⟩] ⟨TEXT:6⟩" in lines


# ---------------------------------------------------------------- command line


def test_main_regenerates_skeletons(tmp_path, capsys):
    samples = tmp_path / "samples"
    samples.mkdir()
    (samples / "20261119-153012-1.html").write_text("<p>Erika</p>", encoding="utf-8")
    (samples / "20261119-153012-2.html").write_text("<ul><li>a</li></ul>", encoding="utf-8")
    (samples / "index.csv").write_text("not a page", encoding="utf-8")

    main([str(samples), str(tmp_path / "structure")])

    first = (tmp_path / "structure" / "20261119-153012-1.txt").read_text(encoding="utf-8")
    assert "p ⟨TEXT:5⟩" in first
    assert "Erika" not in first
    assert (tmp_path / "structure" / "20261119-153012-2.txt").exists()
    output = capsys.readouterr().out
    assert "20261119-153012-1.html -> 20261119-153012-1.txt (1 lines)" in output
    assert "2 skeletons written" in output


def test_main_without_pages_exits_with_message(tmp_path):
    with pytest.raises(SystemExit) as error:
        main([str(tmp_path), str(tmp_path / "structure")])

    assert str(error.value.code) == f"Skeleton error: {tmp_path}: no .html files"
