#!/usr/bin/env python3

from rich import print

from media_import.cli import run_cli


def main():
    config = run_cli()

    print()

    print(config)


if __name__ == "__main__":
    main()
