import datetime

class Schedule:
    """
    Classe servant à représenter de manière générique une période.
    """

    @staticmethod
    def create_schedules_from_txt(schedules_txt, day, category):
        """
        Transforme le texte en "Schedule".

        Params:
            - txt_schedules (string): texte des périodes de guichet
            - day (string): jour
            - type_schedules (string): type des périodes

        Return: liste de "Schedule"
        """

        if schedules_txt.startswith('ABSENT'):
            return []
        schedules = schedules_txt.split('/')
        schedules = [Schedule(datetime.datetime.strptime(schedule.split('-')[0], '%H:%M').time(),
                              datetime.datetime.strptime(schedule.split('-')[1], '%H:%M').time(),
                              day,
                              category) for schedule in schedules]

        return schedules


    def __init__(self, hour_begin, hour_end, day, category):
        """
        Construit un objet "Schedule".

        Params:
            - hour_begin (datetime.time): heure du début de la période
            - hour_end (datetime.time): heure de la fin de la période
            - day ('Mon', 'Tue', 'Wed', 'Thu', 'Fri'): jour de la semaine
            - category (string): catégorie de la période
        """
        self.hour_begin = hour_begin
        self.hour_end = hour_end
        self.day = day
        self.category = category
        self.set_weight()

    def set_weight(self):
        """
        Définit le poids en heures de la période et le place dans l'argument "weight".
        """
        self.weight = int(((self.hour_end.hour - self.hour_begin.hour) * 60 + self.hour_end.minute - self.hour_begin.minute) / 60)

    def test_overlaping(self, schedule_to_test):
        """
        Teste si une période chevauche la période passée en argument.
        """

        if self.day == schedule_to_test.day:
            # Les périodes sont la même journée
            if self.hour_begin < schedule_to_test.hour_end and self.hour_end > schedule_to_test.hour_begin:
                return True

        return False

    def test_inclusion(self, schedule_to_test):
        """Teste si une période est incluse dans la période passée en argument."""

        if self.day == schedule_to_test.day:
            # Les périodes sont la même journée
            if self.hour_begin <= schedule_to_test.hour_begin and self.hour_end >= schedule_to_test.hour_end:
                return True

        return False

class TellerSchedule(Schedule):
    """Classe servant à représenter une période de guichet."""

    def __init__(self, hour_begin, hour_end, day, category, rank, num_schedule):
        """
        Construit un objet "TellerSchedule".

        Params:
            - hour_begin (datetime.time): heure du début de la période
            - hour_end (datetime.time): heure de la fin de la période
            - day ('Mon', 'Tue', 'Wed', 'Thu', 'Fri'): jour de la semaine
            - category (string): catégorie de la période
        """
        self.hour_begin = hour_begin
        self.hour_end = hour_end
        self.day = day
        self.category = category
        self.set_weight()
        self.rank = rank
        self.num_schedule = num_schedule
        self.completed = False
        self.optimize_schedules = True
        self.defined_teller = []
        self.available_tellers = []
