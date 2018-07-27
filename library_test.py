import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')


    def test_dates(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    def test_no_valid_dates(self):
        self.assert_extract('I was born on 2015-15-35.', library.dates_iso8601)

#Assignment test
    def test_dates_timestamp_with_T(self):
        self.assert_extract("date on which me  was formed 2018-06-22T18:22:19.123.", library.dates_iso8601,'2018-06-22T18:22:19.123')
    def test_dates_timestamp_MDT(self):
        self.assert_extract("date on 2018-06-22 18:22:19.123 MDT", library.dates_iso8601, '2018-06-22 18:22:19.123 MDT')
    def test_dates_timestamp_Z(self):
        self.assert_extract("date on 18:22:19.123 Z", library.dates_iso8601, '2018-06-22 18:22:19.123 Z')
    def test_dates_timestamp_0800_negative_offset(self):
        self.assert_extract("date on  2018-06-22 18:22:19.123 -0800", library.dates_iso8601, '2018-06-22 18:22:19.123 -0800')
    def test_dates_timestamp_0800_positive_offset(self):
        self.assert_extract("date on 2018-06-22 18:22:19.123 +0800", library.dates_iso8601, '2018-06-22 18:22:19.123 +0800')
    def test_dates__wrong_format(self):
        self.assert_extract("invalid date on which avengers was formed 2018:23:2017 18:22:19.123", library.dates_iso8601)
    def test_dates_blank(self):
        self.assert_extract("", library.dates_iso8601)
    def test_no_dates(self):
        self.assert_extract("no hay nada aqui", library.dates_iso8601)
    def test_dates_other_format(self):
        self.assert_extract("date on which i got tired 3 Jan, 2017.", library.dates_other, '25 Jan, 2017')
    def test_integers_other_format(self):
        self.assert_extract("123,456,789", library.integers, '123', '456', '789')



if __name__ == '__main__':
    unittest.main()
