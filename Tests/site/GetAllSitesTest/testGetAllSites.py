from unittest import TestCase
from http import HTTPStatus

from requests.api import get

from ....TestsHelpers.Service import defaultDataCreator

from ....TestsHelpers.Service.helper import Helper 
from ....TestsHelpers.Service.comparator import SiteResponse as Comaprator
from ....TestsHelpers.Service.validator import SiteResponse as Validator
from ....TestsHelpers.Service import constants

from ....TestsHelpers.TestsUtils.compareStatusCodes import compareStatusCodes
from ....TestsHelpers.TestsUtils.randomStuff import randomNumber, randomUUID4, randomWord


class TestGetAllSites(TestCase):
    
    def setUp(self):
        self.createCompanyData = defaultDataCreator.Company()
        self.createCompanyData[constants.name] = randomWord(17)
        self.companyID = Helper().createCompany(self.createCompanyData).json()[constants.companyID]

        self.createSiteData = defaultDataCreator.Site()
        self.createSiteData[constants.companyID] = self.companyID
        self.createSiteResponse = Helper().createSite(self.createSiteData).json()
        self.siteID = self.createSiteResponse[constants.siteID]

    def testGetAllSites(self):
        """Get All Sites"""
        getAllSitesResponse = Helper().getSites()
        compareStatusCodes(self, getAllSitesResponse.status_code, HTTPStatus.OK)

        testing = getAllSitesResponse.json()

        self.assertIn(constants.limit, testing, "No limit field in response body")
        self.assertIn(constants.count, testing, "No count field in response body")
        self.assertIn(constants.sites, testing, "No sites field in response body")

        sitesLength = len(testing[constants.sites])
        self.assertTrue(10 >= sitesLength > 0, "Incorrect number of sites in response body")
        self.assertTrue(testing[constants.count] >= sitesLength, "Incorrect count compared to number of sites in response body")
        self.assertEqual(10, testing[constants.limit], "Incorrect limit in response body")

    def testGetAllSitesLimitAndOffset(self):
        """Get All Sites. Limit And Offset given"""
        getAllSitesResponse = Helper().getSites(limit = 20, offset = 10)
        compareStatusCodes(self, getAllSitesResponse.status_code, HTTPStatus.OK)

        testing = getAllSitesResponse.json()

        self.assertIn(constants.limit, testing, "No limit field in response body")
        self.assertIn(constants.count, testing, "No count field in response body")
        self.assertIn(constants.sites, testing, "No sites field in response body")
        self.assertIn(constants.offset, testing, "No offset field in response body")

        sitesLength = len(testing[constants.sites])
        self.assertTrue(20 >= sitesLength > 0, "Incorrect number of sites in response body")
        self.assertTrue(testing[constants.count] >= sitesLength, "Incorrect count compared to number of sites in response body")
        self.assertEqual(20, testing[constants.limit], "Incorrect limit in response body")
        self.assertEqual(10, testing[constants.offset], "Incorrect offset in response body")

    def tearDown(self):
        Helper().deleteCompany(self.companyID)
        Helper().deleteSite(self.siteID)