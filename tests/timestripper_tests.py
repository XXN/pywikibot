# -*- coding: utf-8  -*-
"""
Tests for archivebot.py/Timestripper.
"""
#
# (C) Pywikipedia bot team, 2014
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'


import pywikibot
from utils import PywikibotTestCase, unittest
import scripts.archivebot as ab
import re
import datetime

site = pywikibot.Site('fr', 'wikipedia')

global Months
Months = ab.Months(site=site)


class TestTimeStripper(unittest.TestCase):
    """Test cases for Link objects"""

    def setUp(self):
        Months.updateMonths(site=site)
        self.ts = ab.TimeStripper()

    def test_findmarker(self):
        """Test that string which is not part of text is found"""

        txt = u'this is a string with a maker is @@@@already present'
        self.assertEqual(self.ts.findmarker(txt, base=u'@@', delta='@@'),
                         '@@@@@@')

    def test_last_match_and_replace(self):
        """Test that pattern matches the righmost item"""

        txtWithMatch = u'this string has one 1998, 1999 and 3000 in it'
        txtWithNoMatch = u'this string has no match'
        pat = self.ts.yearR

        self.assertEqual(self.ts.last_match_and_replace(txtWithMatch, pat),
                         (u'this string has one @@, @@ and 3000 in it',
                          {'year': u'1999'})
                         )
        self.assertEqual(self.ts.last_match_and_replace(txtWithNoMatch, pat),
                         (txtWithNoMatch,
                          None)
                         )

    def test_timestripper(self):
        """Test that correct date is matched"""

        txtMatch = u'3 février 2010 à 19:48 (CET) 7 février 2010 à 19:48 (CET)'
        txtNoMatch = u'3 March 2010 19:48 (CET) 7 March 2010 19:48 (CET)'

        res = datetime.datetime(2010, 2, 7, 19, 48,
                                tzinfo=ab.tzoneFixedOffset(60, 'Europe/Paris'))

        self.assertEqual(self.ts.timestripper(txtMatch), res)
        self.assertEqual(self.ts.timestripper(txtNoMatch), None)


if __name__ == '__main__':
    try:
        try:
            unittest.main()
        except SystemExit:
            pass
    finally:
        pywikibot.stopme()