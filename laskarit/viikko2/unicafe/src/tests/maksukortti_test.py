import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_rahan_lataaminen_kasvattaa_saldoa(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(str(self.maksukortti), "saldo: 10.1")

    def test_ei_voi_ladata_neg_arvoa(self):
        ''' hox! tämä testi ei mene läpi >> -9.9 != 0.1 '''
        self.maksukortti.lataa_rahaa(-1000)
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_rahan_ottaminen_pienentaa_saldoa(self):
        self.maksukortti.lataa_rahaa(500)
        self.maksukortti.ota_rahaa(225)
        self.assertEqual(str(self.maksukortti), "saldo: 2.85")

    def test_saldo_ei_muutu_jos_liian_vahan_rahaa(self):
        self.maksukortti.ota_rahaa(300)
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_rahat_riittivat_palauttaa_true(self):
        self.assertEqual(self.maksukortti.ota_rahaa(10), True)

    def test_rahat_ei_riittanyt_palauttaa_false(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1000), False)