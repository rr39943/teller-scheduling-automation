import unittest
import datetime
from modules.tellers import Quotas
from modules.schedules import Schedule

class QuotasTest(unittest.TestCase):

    def test_reset_quotas(self):
        """Teste la création d'un quotas et son initialisation"""

        quotas = Quotas(5, 4)
        quotas.current['total'] -= 1
        quotas.reset_quotas()
        self.assertEqual(quotas.current['total'], 5)

    def test_schedule_1(self):
        """Teste la capacité à vérifier si l'ajout d'une période respecte les quotas"""
        quotas = Quotas(5, 4)
        schedule = Schedule(datetime.time(10,0),
                            datetime.time(11,0),
                            'Mon',
                            'stm_r')
        self.assertTrue(quotas.test_schedule(schedule))

    def test_schedule_2(self):
        """Teste la capacité à vérifier si l'ajout d'une période respecte les quotas"""
        quotas = Quotas(3, 0)
        schedule = Schedule(datetime.time(10,0),
                            datetime.time(11,0),
                            'Mon',
                            'accueil_r')
        self.assertFalse(quotas.test_schedule(schedule))
