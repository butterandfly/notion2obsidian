import argparse
from notion2obsidian import n2o
from notion2obsidian.n2o import notion2obsidian_nosubdir
from rich.console import Console
from rich.theme import Theme

from rich.padding import Padding
from rich.markup import escape

console = None


def log(text: str, style: str):
    if style == 'info':
        console.print(text, style='info')
    if style == 'success':
        console.print(text, style='success')
    if style == 'error':
        console.print(text, style='error')
    if style == 'sub':
        estr = escape(text)
        console.print(Padding(estr, (0, 2)))


def main() -> None:
    """
    Convert Notion md files to Obsidian md files.
    """
    parser = argparse.ArgumentParser(description='Convert Notion exported md to Obsidian md',
                                     add_help=True,
                                     usage='%(prog)s [options] src [dest]',
                                     prog='notion2obsidian')

    parser.add_argument('src', help='note folder exported by Notion', type=str)

    parser.add_argument('-o', '--output', 
                        help='Obsidian md folder', default='', action='store')
    parser.add_argument('-l', '--delete-emptylines',
                        help='delete empty lines.', action='store_true')
    parser.add_argument('-q', '--quiet', help='quiet mode.',
                        action='store_true')

    args = vars(parser.parse_args())

    custom_theme = Theme({
        "info": "bold",
        "success": "bold green",
        "error": "bold red"
    })

    global console
    console = Console(theme=custom_theme, quiet=args['quiet'])
    n2o.log = log
    notion2obsidian_nosubdir(args)


if __name__ == "__main__":
    main()
