"""
Module for processing Sitemaps.

Note: The main purpose of this module is to provide support for the
SitemapSpider, its API is subject to change without notice.
"""

from typing import Any, Dict, Iterable, Iterator, Optional, Union

import lxml.etree  # nosec


class Sitemap:
    """Class to parse Sitemap (type=urlset) and Sitemap Index
    (type=sitemapindex) files"""

    def __init__(self, xmltext: Union[str, bytes]):
        xmlp = lxml.etree.XMLParser(
            recover=True, remove_comments=True, resolve_entities=False
        )
        self._root = lxml.etree.fromstring(xmltext, parser=xmlp)  # nosec
        rt = self._root.tag
        self.type = self._root.tag.split("}", 1)[1] if "}" in rt else rt

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        for elem in self._root.getchildren():
            d: Dict[str, Any] = {}
            for el in elem.getchildren():
                tag = el.tag
                name = tag.split("}", 1)[1] if "}" in tag else tag

                if name == "link":
                    if "href" in el.attrib:
                        d.setdefault("alternate", []).append(el.get("href"))
                else:
                    d[name] = el.text.strip() if el.text else ""

            if "loc" in d:
                yield d



