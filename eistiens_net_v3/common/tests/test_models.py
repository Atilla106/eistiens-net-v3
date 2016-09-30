from common.tests.base import CustomUnitTestCase
from common.models import SchoolYear


class SchoolYearModelTest(CustomUnitTestCase):

    def test_dundlestr_method(self):
        currYear = SchoolYear(year=2017)
        self.assertEquals(str(currYear), '2017-2018')
