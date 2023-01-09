#
# Copyright (c) 2022 Jim Bauer <4985656-jim_bauer@users.noreply.gitlab.com>
# This software is licensed according to the included LICENSE file
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys
import re
import argparse
import datetime
from pytz import timezone
from pathlib import Path
import traceback
import requests
import contextlib
import html
import urllib

# https://feedparser.readthedocs.io/en/latest/
import feedparser

# https://feedgen.kiesow.be/
from feedgen.feed import FeedGenerator

# https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup

# Local imports
import feedfilter.logger as logger
from feedfilter import __version__ as __version__


@contextlib.contextmanager
def open_file_or_stdio(fname: str, mode: str = 'r', *args, **kwargs):
    '''
    Open either a file or stdin/stdout
    Must be used in a 'with' statement
    '''
    if fname in ('stdout', '-', None):
        if 'r' in mode:
            stream = sys.stdin
        else:
            stream = sys.stdout

        if 'b' in mode:
            fh = stream.buffer
        else:
            fh = stream

        close_needed = False
    else:
        fh = open(fname, mode, *args, **kwargs)
        close_needed = True

    try:
        yield fh
    finally:
        if close_needed:
            fh.close()


def getrsslink(link):
    # fetch page at link
    # search it for rss2 feed link and return it

    logger.debug('Original link: %s', link)
    # Remove any fragment (i.e. the '#frag' in http://hosts/path/#frag)
    link = urllib.parse.urldefrag(link).url
    logger.debug('Fetching: %s', link)

    resp = requests.get(link)
    logger.info('Fetched %s, status=%s', link, resp.status_code)
    if resp.status_code != 200:
        logger.error('Error: Failed to download %s', link)
        logger.error('Status: %s', resp)
        logger.error('Response Headers: %s', resp.headers)
        raise IOError

    soup = BeautifulSoup(resp.text, 'html.parser')

    regex = re.compile(f'^{re.escape(link)}.*type=rss', re.IGNORECASE)
    logger.debug('Trying to find rss URL using regex=%s', regex)
    rss = soup.find_all(href=regex)
    logger.debug('found: %s', rss)
    href = rss[0].get('href')
    logger.debug('href: %s', href)
    return href


def fix_date(odatestr):
    try:
        dt = datetime.datetime.fromisoformat(odatestr)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        return odatestr

    return dt


def content_auto_links(orig):

    new = re.sub(r'(?<!(href| src)=[\'"])' # if not preceeded by
                 r'(https?://[^<]+?)'      # match URL (group 2)
                 r'(?=<|\s|\Z)'            # followed by
                 r'(?!</a>)',              # not followed by
                 r'<a href="\2">\2</a>',
                 orig)
    if new != orig:
        logger.debug('Content changed (old): %s', orig)
        logger.debug('Content changed (new): %s', new)

    return new


class MangleTitle:
    def __init__(self, title_re=None, title_sub=None, add_date=None):
        logger.debug('title_re=%s', title_re)
        logger.debug('title_sub=%s', title_sub)
        logger.debug('add_date=%s', add_date)

        if title_re is None:
            self.title_re = None
        else:
            self.title_re = re.compile(title_re, re.IGNORECASE)

        # Handle someone using '\0' as a reference to the whole match
        if title_sub == r'\0':
            self.title_sub = r'\g<0>'
        else:
            self.title_sub = title_sub

        if isinstance(add_date, str):
            if add_date.lower() in ('yes', 'true'):
                self.add_date = True
            elif add_date.lower() in ('no', 'false'):
                self.add_date = False
        else:
            self.add_date = add_date

    def mangle(self, title, date):
        if self.title_re and self.title_sub:
            title = self.title_re.sub(self.title_sub, title)

        if self.add_date:
            dt = date.astimezone(timezone('UTC'))
            title += ' ' * 150 + f'({dt})'

        logger.debug('new title = %s', title)
        return title


class FeedParserToFeedGenerator:
    def __init__(self, extensions=None, auto_links=False):
        self.fg = FeedGenerator()

        if extensions is not None:
            for ext in extensions:
                self.fg.load_extension(ext)

        self.auto_links = auto_links

    def create_feed(self, feed):
        self.fg = FeedGenerator()
        # Required fields: id, title, updated

        title = feed.get('title', 'No Title')
        title = html.unescape(title)
        logger.info('Feed title: %s', title)
        self.fg.title(html.unescape(title))

        if 'id' in feed:
            self.fg.id(feed.id)
        else:
            self.fg.id(feed.link)

        updated = fix_date(feed.updated)
        self.fg.updated(updated)
        logger.info('updated=%s; id=%s', updated, self.fg.id)

        if 'links' in feed:
            for link in feed.links:
                self.fg.link(link)

        if 'description' in feed:
            self.fg.description(feed.description) # a.k.a subtitle

        if 'ttl' in feed:
            self.fg.ttl(feed.ttl)

        if 'language' in feed:
            self.fg.language(feed.language)

        if 'author_detail' in feed:
            logger.debug('author: %s', feed.author)
            logger.debug('author_detail: %s', feed.author_detail)
            self.fg.author(feed.author_detail)

        return self.fg

    def add_entry(self, entry):
        fe = self.fg.add_entry()

        # Required fields: title, id, updated and (content or alternate link)

        title = entry.get('title', 'No title')
        logger.debug('Original Entry title: %s', title)
        if not title:
            title = '*title empty*'
        title = html.unescape(title)
        logger.info('Entry title: %s', title)
        fe.title(title)
        fe.guid(entry.id) # sets id as well
        fe.updated(fix_date(entry.updated))

        if 'author_detail' in entry:
            fe.author(entry.author_detail)

        if 'published' in entry:
            fe.published(fix_date(entry.published))

        if 'links' in entry:
            for link in entry.links:
                fe.link(link)

        if 'summary' in entry:
            fe.description(entry.summary)

        if 'content' in entry:
            # XXX should probably include all elements of array
            #     but I have never seen any examples
            content = entry.content[0]
            if self.auto_links:
                value = content_auto_links(content.value)
            else:
                value = content.value

            fe.content(value, type=content.type)

        if 'tags' in entry:
            # tags have the following fields: term, scheme, label
            # term is required for category
            logger.debug('Tags=%s', entry.tags)
            #XXX add other tags?  No examples seen
            tag = entry.tags[0]
            if tag.term is not None:
                logger.debug('Adding category')
                fe.category(term=tag.term, scheme=tag.scheme, label=tag.label)
            else:
                logger.debug('No term in tag, skipping')

        if not (fe.title() and fe.id() and fe.updated()):
            logger.error('Missing required fields')
            logger.error('orig entry: %s', entry)
            logger.error('new entry: title=%s id=%s updated=%s',
                         fe.title(), fe.id(), fe.updated())
            raise KeyError

        return fe

    def _write_summary(self, fd):
        print(f'Title:   {self.fg.title()}', file=fd)
        print(f'Updated: {self.fg.updated()}', file=fd)
        count = 0
        for entry in self.fg.entry():
            count += 1
            print(f'Entry:   {count}', file=fd)
            title = ' '.join(entry.title().split())
            print(f'  Title:   {title}', file=fd)
            print(f'  Author:  {entry.author()[0]["name"]}', file=fd)
            print(f'  Updated: {entry.updated()}', file=fd)

    def write_output(self, ofile, format):
        assert format in ('atom', 'rss', 'summary')

        if format == 'summary':
            with open_file_or_stdio(ofile, 'w') as fd:
                self._write_summary(fd=fd)
            return

        if format == 'atom':
            bytes = self.fg.atom_str(pretty=True)
        else:
            bytes = self.fg.rss_str(pretty=True)

        with open_file_or_stdio(ofile, 'wb') as fd:
            fd.write(bytes)


def get_feed_data(forum_url):
    if forum_url:
        feed = feedparser.parse(forum_url)
    else:
        stdin = sys.stdin.read()
        feed = feedparser.parse(stdin)

    return feed


def add_all_entries(fp2fg, mt, entries, title_override=None):
    for entry in entries:
        fe = fp2fg.add_entry(entry)
        if fe.published():
            title_date = fe.published()
        else:
            title_date = fe.updated()

        if title_override is None:
            title = fe.title()
        else:
            title = title_override

        fe.title(mt.mangle(title, title_date))


def feed_filter():
    prog_name = Path(sys.argv[0]).name

    # Default regex\n
    # - <prefix> is typically a forum name\n
    # - Re: is added to responses automatically
    # - <brackets> is often something like "[solved]" added to be
    #   the title to denote that the issue have been resolved
    # - <main> Main part of the title
    reg = r'(?P<prefix>[^•]+ • )?(Re: )?(?P<brackets>\[[^]]+] ?)?(?P<main>.*)'
    sub = r'\g<prefix>\g<main>'

    p = argparse.ArgumentParser(description='Filter RSS/Atom feeds',
                                add_help=False)
    p.add_argument('-h', '--help', action='store_true',
                   help='show this help message and exit')
    logger.add_argparse_args(p)
    p.add_argument('--forum', help='Forum URL or input filename')
    p.add_argument('--outfile', default=None,
                   help='Output file (default: stdout)')
    p.add_argument('--output-fmt', default='atom',
                   choices=['atom', 'rss', 'summary'],
                   help='format of feed output (default: atom)')
    p.add_argument('--title-re', default=reg,
                   help='python regex used to match titles')
    p.add_argument('--title-sub', default=sub,
                   help='python regex subsitution')
    p.add_argument('--add-date-to-title', default='yes',
                   choices=['yes', 'no'],
                   help='add date/time string to entry title (for sorting)')
    p.add_argument('--add-posts', action='store_true',
                   help='Add posts made to this topic '
                   '(requires network access)')
    p.add_argument('--auto-links', action='store_true',
                   help='Automatically add links for test that looks like URLs')
    p.add_argument('--version', action='store_true',
                   help='display version and exit')

    args = p.parse_args()

    if args.help:
        p.print_help()
        print(f'''
By default, reads feed from stdin, writes to stdout

Additional notes on some options:

  Option --title-re:
    - Default: {reg}
    - Uses python regular expression syntax
    - <prefix> is typically a forum name
    - Re: is added to responses automatically
    - <brackets> is often something like "[solved]" added to be
      the title to denote that the issue have been resolved
    - <main> Main part of the title

  Option --title-sub:
    - Default: {sub}
    - Replaces matched title with prefix followed by main part of title
      i.e. Removes "Re: " and most things between '[' and ']'
    - To reference any of: <prefix> <brackets> or <main> in title subsitution
      specify tham as \\g<name> (i.e. \\g<prefix>)

''')
        sys.exit(0)

    if args.version:
        print(f'{prog_name} {__version__}')
        sys.exit(0)

    logger.init(prog_name, args=args)
    logger.info('%s %s starting', prog_name, __version__)
    logger.info('Options: %s', args)

    mt = MangleTitle(args.title_re, args.title_sub, args.add_date_to_title)
    fp2fg = FeedParserToFeedGenerator(auto_links=args.auto_links)

    parsed = get_feed_data(args.forum)

    fp2fg.create_feed(parsed.feed)

    if args.add_posts:
        for entry in parsed.entries:
            logger.info('Title: %s', entry.title)
            logger.debug(entry.keys())

            try:
                #XXX this is a bit forum specific
                rss = getrsslink(entry.link)
            except (IndexError, IOError) as e:
                logger.error('Failed to get RSS URL for %s, %s',
                             entry.link, e)
                continue

            logger.info('  rss URL is %s', rss)
            post_feed = feedparser.parse(rss)
            logger.info('  Post Entries: %s', len(post_feed.entries))
            add_all_entries(fp2fg, mt, post_feed.entries, entry.title)
    else:
        add_all_entries(fp2fg, mt, parsed.entries)

    fp2fg.write_output(args.outfile, args.output_fmt)

    logger.info('--end--')
    logger.stop()


def main():
    try:
        feed_filter()
    except Exception:
        if logger.critical is not None:
            logger.critical('Got unhandled exception', exc_info=True)
            logger.stop()
        else:
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
