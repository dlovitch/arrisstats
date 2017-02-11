#! /usr/bin/env python
# -*- coding: utf-8 -*-

import click
import json

import scraper

@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-h", "--host", required=True)
@click.option("--events", is_flag=True)
@click.option("--status", is_flag=True)
def main(verbose, host, events, status):
    s = scraper.Scraper(verbose, host)
    if events:
        print(json.dumps(s.get_events(), sort_keys=True, indent=4))
    if status:
        print(json.dumps(s.get_status(), sort_keys=True, indent=4))

if __name__ == "__main__":
    main()
