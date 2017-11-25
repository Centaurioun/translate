# -*- coding: utf-8 -*-
#
# Copyright 2008, 2011 Zuza Software Foundation
#
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

# Original Author: Dan Schafer <dschafer@mozilla.com>
# Date: 10 Jun 2008

"""Convert Mozilla .lang files to Gettext PO localization files.
"""

from translate.convert import convert
from translate.storage import mozilla_lang as lang, po


class lang2po(object):
    """Convert one Mozilla .lang file to a single PO file."""

    SourceStoreClass = lang.LangStore
    TargetStoreClass = po.pofile
    TargetUnitClass = po.pounit

    def __init__(self, input_file, duplicate_style="msgctxt", encoding="utf-8"):
        """Initialize the converter."""
        self.duplicate_style = duplicate_style

        self.source_store = self.SourceStoreClass(input_file,
                                                  encoding=encoding)
        self.target_store = self.TargetStoreClass()

    def convert_unit(self, unit):
        """Convert a source format unit to a target format unit."""
        target_unit = self.TargetUnitClass()
        target_unit.source = unit.source
        target_unit.target = unit.target
        target_unit.addlocations(unit.getlocations())
        target_unit.addnote(unit.getnotes(), 'developer')
        return target_unit

    def convert_store(self):
        """Convert a single source format file to a target format file."""
        targetheader = self.target_store.header()
        targetheader.addnote("extracted from %s" %
                             self.source_store.filename, "developer")

        for source_unit in self.source_store.units:
            self.target_store.addunit(self.convert_unit(source_unit))

        self.target_store.removeduplicates(self.duplicate_style)
        return self.target_store


def run_converter(inputfile, outputfile, templates, pot=False,
                  duplicatestyle="msgctxt", encoding="utf-8"):
    """Wrapper around converter."""
    convertor = lang2po(inputfile, duplicate_style=duplicatestyle,
                        encoding=encoding)
    outputstore = convertor.convert_store()
    if outputstore.isempty():
        return 0
    outputstore.serialize(outputfile)
    return 1


formats = {
    "lang": ("po", run_converter)
}


def main(argv=None):
    parser = convert.ConvertOptionParser(formats, usepots=True,
                                         description=__doc__)
    parser.add_option(
        "", "--encoding", dest="encoding", default='utf-8',
        help="The encoding of the input file (default: UTF-8)")
    parser.passthrough.append("encoding")
    parser.add_duplicates_option()
    parser.run(argv)


if __name__ == '__main__':
    main()
