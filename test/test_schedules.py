import unittest
import datetime
from modules.schedules import Schedule

class ScheduleTest(unittest.TestCase):

    def test_weight_1(self):
        """Teste le poids d'une période d'une heure"""
        schedule = Schedule(datetime.time(10,0),
                            datetime.time(11,0),
                            'Mon',
                            'test')
        self.assertEqual(schedule.weight, 1)

    def test_weight_2(self):
        """Teste le poids d'une période de deux heures"""
        schedule = Schedule(datetime.time(10,0),
                            datetime.time(12,0),
                            'Mon',
                            'test')

        self.assertEqual(schedule.weight, 2)

    def test_overlaping_1(self):
        """Teste le chevauchement de deux périodes: chevauchement"""
        schedule_a = Schedule(datetime.time(10,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        schedule_b = Schedule(datetime.time(11,30),
                              datetime.time(12,30),
                              'Mon',
                              'test')

        self.assertTrue(schedule_a.test_overlaping(schedule_b))

    def test_overlaping_2(self):
        """Teste le chevauchement de deux périodes: jour différent"""
        schedule_a = Schedule(datetime.time(10,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        schedule_b = Schedule(datetime.time(11,30),
                              datetime.time(12,30),
                              'Tue',
                              'test')

        self.assertFalse(schedule_a.test_overlaping(schedule_b))

    def test_overlaping_3(self):
        """Teste le chevauchement de deux périodes: périodes successives"""
        schedule_a = Schedule(datetime.time(10,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        schedule_b = Schedule(datetime.time(12,0),
                              datetime.time(13,0),
                              'Mon',
                              'test')

        self.assertFalse(schedule_a.test_overlaping(schedule_b))

    def test_inclusion_1(self):
        """Teste l'inclusion d'une période dans une autre: effectif"""
        schedule_a = Schedule(datetime.time(10,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        schedule_b = Schedule(datetime.time(11,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        self.assertTrue(schedule_a.test_inclusion(schedule_b))

    def test_inclusion_2(self):
        """Teste l'inclusion d'une période dans une autre: chevauchement"""
        schedule_a = Schedule(datetime.time(10,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        schedule_b = Schedule(datetime.time(11,0),
                              datetime.time(12,30),
                              'Mon',
                              'test')

        self.assertFalse(schedule_a.test_inclusion(schedule_b))

    def test_inclusion_3(self):
        """Teste l'inclusion d'une période dans une autre: chevauchement"""
        schedule_a = Schedule(datetime.time(10,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        schedule_b = Schedule(datetime.time(9,30),
                              datetime.time(10,30),
                              'Mon',
                              'test')

        self.assertFalse(schedule_a.test_inclusion(schedule_b))

    def test_inclusion_4(self):
        """Teste l'inclusion d'une période dans une autre: jour différent"""
        schedule_a = Schedule(datetime.time(10,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        schedule_b = Schedule(datetime.time(10,0),
                              datetime.time(10,30),
                              'Tue',
                              'test')

        self.assertFalse(schedule_a.test_inclusion(schedule_b))

    def test_inclusion_5(self):
        """Teste l'inclusion d'une période dans une autre: juxtaposition"""
        schedule_a = Schedule(datetime.time(10,0),
                              datetime.time(12,0),
                              'Mon',
                              'test')

        schedule_b = Schedule(datetime.time(12,0),
                              datetime.time(12,30),
                              'Mon',
                              'test')

        self.assertFalse(schedule_a.test_inclusion(schedule_b))

    def test_create_schedules_from_txt_1(self):
        """Teste la création de périodes via un txt: nb"""

        schedules = Schedule.create_schedules_from_txt('08:00-12:00/14:00-17:00', 'Mon', 'test')
        self.assertEqual(len(schedules), 2)

    def test_create_schedules_from_txt_2(self):
        """Teste la création de périodes via un txt: '08:00-12:00', 'Mon', teste le jour."""

        schedules = Schedule.create_schedules_from_txt('08:00-12:00', 'Mon', 'test')
        self.assertEqual(schedules[0].day, 'Mon')

    def test_create_schedules_from_txt_3(self):
        """Teste la création de périodes via un txt: '08:00-12:00', 'Mon', teste l'heure de fin."""

        schedules = Schedule.create_schedules_from_txt('08:00-12:00', 'Mon', 'test')
        self.assertEqual(schedules[0].hour_end.hour, 12)
