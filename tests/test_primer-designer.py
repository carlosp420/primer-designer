import os
import unittest
import responses
import requests

from mock import Mock

from primer_designer import PrimerDesigner


TEST_FOLDER = os.path.join(os.path.dirname(os.getcwd()), 'tests', 'Data')
ALIGNMENT = os.path.join(os.path.dirname(os.getcwd()), 'tests', 'Data', 'Ca2.fst')
RESPONSE = os.path.join(os.path.dirname(os.getcwd()), 'tests', 'Data', 'response_Ca2.fst.html')


class PrimerDesignerTest(unittest.TestCase):
    def setUp(self):
        self.pd = PrimerDesigner(
            folder=TEST_FOLDER,
            tm="55",
            min_amplength="200",
            max_amplength="500",
            gencode="universal",
            mode="primers",
            clustype="protein",
            amptype="dna_GTRG",
            email="youremail@email.com",
        )

    @responses.activate
    def test_request_primers(self):
        url = "http://floresta.eead.csic.es/primers4clades/primers4clades.cgi"
        with open(RESPONSE, 'r') as handle:
            response_html_body = handle.read()

        responses.add(responses.POST, url,
                      body=response_html_body,
                      status=200,
                      content_type='application/text',
                      )
        resp = self.pd.request_primers(ALIGNMENT)
        assert resp.content.decode('ascii') == response_html_body
