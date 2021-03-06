import colorsys
import io
from time import process_time

from rich.color import Color
from rich.columns import Columns
from rich.console import Console, ConsoleOptions, RenderGroup, RenderResult
from rich.markdown import Markdown
from rich.measure import Measurement
from rich.padding import Padding
from rich.panel import Panel
from rich.pretty import Pretty
from rich.segment import Segment
from rich.style import Style
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text
from rich import box


class ColorBox:
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        for y in range(0, 5):
            for x in range(options.max_width):
                h = x / options.max_width
                l = 0.1 + ((y / 5) * 0.7)
                r, g, b = colorsys.hls_to_rgb(h, l, 1.0)
                yield Segment(
                    "█", Style(color=Color.from_rgb(r * 255, g * 255, b * 255))
                )
            yield Segment.line()

    def __rich_measure__(self, console: "Console", max_width: int) -> Measurement:
        return Measurement(1, max_width)


def make_test_card() -> Table:
    """Get a renderable that demonstrates a number of features."""
    table = Table.grid(padding=1, pad_edge=True)
    table.title = "Rich features"
    table.add_column("Feature", no_wrap=True, justify="right", style="bold red")
    table.add_column("Demonstration")

    color_table = Table(
        box=None,
        expand=False,
        show_header=False,
        show_edge=False,
        pad_edge=False,
    )
    color_table.add_row(
        # "[bold yellow]256[/] colors or [bold green]16.7 million[/] colors [blue](if supported by your terminal)[/].",
        (
            "✓ [bold green]4-bit color[/]\n"
            "✓ [bold blue]8-bit color[/]\n"
            "✓ [bold magenta]Truecolor (16.7 million)[/]\n"
            "✓ [bold yellow]Dumb terminals[/]\n"
            "✓ [bold cyan]Automatic color conversion"
        ),
        ColorBox(),
    )

    table.add_row("Colors", color_table)

    table.add_row(
        "Styles",
        "All ansi styles: [bold]bold[/], [dim]dim[/], [italic]italic[/italic], [underline]underline[/], [strike]strikethrough[/], [reverse]reverse[/], and even [blink]blink[/].",
    )

    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque in metus sed sapien ultricies pretium a at justo. Maecenas luctus velit et auctor maximus."
    lorem_table = Table.grid(padding=1, collapse_padding=True)
    lorem_table.pad_edge = False
    lorem_table.add_row(
        Text(lorem, justify="left", style="green"),
        Text(lorem, justify="center", style="yellow"),
        Text(lorem, justify="right", style="blue"),
        Text(lorem, justify="full", style="red"),
    )
    table.add_row(
        "Text",
        RenderGroup(
            Text.from_markup(
                """Word wrap text. Justify [green]left[/], [yellow]center[/], [blue]right[/] or [red]full[/].\n"""
            ),
            lorem_table,
        ),
    )

    def comparison(renderable1, renderable2) -> Table:
        table = Table(show_header=False, pad_edge=False, box=None, expand=True)
        table.add_column("1", ratio=1)
        table.add_column("2", ratio=1)
        table.add_row(renderable1, renderable2)
        return table

    cjk_table = Table.grid()
    cjk_table.add_column(ratio=1)
    cjk_table.add_column(ratio=2)
    cjk_table.add_column(ratio=3)
    cjk_table.add_row(
        Panel(
            Text("该库支持中文，日文和韩文文本！", overflow="fold"),
            expand=False,
            border_style="red",
            box=box.DOUBLE_EDGE,
        ),
        Panel(
            Text("ライブラリは中国語、日本語、韓国語のテキストをサポートしています", overflow="fold"),
            expand=False,
            border_style="Red",
            box=box.DOUBLE_EDGE,
        ),
        Panel(
            Text("도서관은 중국어, 일본어 및 한국어 텍스트를 지원합니다", overflow="fold"),
            expand=False,
            border_style="Red",
            box=box.DOUBLE_EDGE,
        ),
    )
    table.add_row(
        "Asian languages",
        ":flag_for_china:  该库支持中文，日文和韩文文本！\n:flag_for_japan:  ライブラリは中国語、日本語、韓国語のテキストをサポートしています\n:flag_for_south_korea:  도서관은 중국어, 일본어 및 한국어 텍스트를 지원합니다",
    )

    markup_example = (
        "[bold magenta]Rich[/] supports a simple [i]bbcode[/i] like [b]markup[/b] for [yellow]color[/] and [underline]style[/]. "
        "Also renders emoji code: :+1: :apple: :ant: :bear: :baguette_bread: :bus: "
    )
    table.add_row("Console markup", markup_example)

    example_table = Table(
        show_edge=False,
        show_header=True,
        expand=False,
        row_styles=["none", "dim"],
        box=box.SIMPLE,
    )
    example_table.add_column("[green]Date", style="green", no_wrap=True)
    example_table.add_column("[blue]Title", style="blue")
    example_table.add_column(
        "[cyan]Production Budget",
        style="cyan",
        justify="right",
        no_wrap=True,
    )
    example_table.add_column(
        "[magenta]Box Office",
        style="magenta",
        justify="right",
        no_wrap=True,
    )
    example_table.add_row(
        "Dec 20, 2019",
        "Star Wars: The Rise of Skywalker",
        "$275,000,000",
        "$375,126,118",
    )
    example_table.add_row(
        "May 25, 2018",
        "[b]Solo[/]: A Star Wars Story",
        "$275,000,000",
        "$393,151,347",
    )
    example_table.add_row(
        "Dec 15, 2017",
        "Star Wars Ep. VIII: The Last Jedi",
        "$262,000,000",
        "[bold]$1,332,539,889[/bold]",
    )
    example_table.add_row(
        "May 19, 1999",
        "Star Wars Ep. [b]I[/b]: [i]The phantom Menace",
        "$115,000,000",
        "$1,027,044,677",
    )

    table.add_row("Tables", example_table)

    code = '''\
def iter_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value'''

    pretty_data = {
        "foo": [
            3.1427,
            (
                "Paul Atriedies",
                "Vladimir Harkonnen",
                "Thufir Haway",
            ),
        ],
        "atomic": (False, True, None),
    }
    table.add_row(
        "Syntax highlighting\n&\nPretty printing",
        comparison(
            Syntax(code, "python3", line_numbers=True, indent_guides=True),
            Pretty(pretty_data, indent_guides=True),
        ),
    )

    markdown_example = """\
# Markdown

Supports much of the *markdown*, __syntax__!

- Headers
- Basic formatting: **bold**, *italic*, `code`
- Block quotes
- Lists, and more...
    """
    table.add_row(
        "Markdown", comparison("[cyan]" + markdown_example, Markdown(markdown_example))
    )

    table.add_row(
        "And more",
        """Progress bars, columns, styled logging handler, tracebacks, etc...""",
    )
    return table


if __name__ == "__main__":  # pragma: no cover
    console = Console(file=io.StringIO(), force_terminal=True)
    test_card = make_test_card()

    # Print once to warm cache
    console.print(test_card)
    console.file = io.StringIO()

    start = process_time()
    console.print(test_card)
    taken = round((process_time() - start) * 1000.0, 1)

    text = console.file.getvalue()
    # https://bugs.python.org/issue37871
    for line in text.splitlines():
        print(line)

    print(f"rendered in {taken}ms")
