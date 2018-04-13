import pandas as pd
import numpy as np
import re

class Tellers:
    """
    Classe servant à représenter la liste des guichetiers.

    Méthodes statiques:
    - clean_schedule: nettoyer les indictions de disponibilité

    Méthodes:
    - Constructeur
    - clean_group: nettoyer la valeur de la colonne groupe
    """

    @staticmethod
    def clean_schedule(schedule):
        """
        Méthode statique servant à nettoyer les indications d'heures
        - params: texte du temps à nettoyer
        - return: texte du temps uniformisé
        """

        def clean_time(time_to_clean):
            """
            OBJECTIF: Méthode interne servant à uniformiser le format des heures en rajoutant un 0
            avant le premier chiffre si nécesssaire.
            - params: texte du temps à nettoyer
            - return: texte avec les "0" supplémentaires si nécessaire
            """
            return time_to_clean.zfill(2)

        r = r'([210]?\d)[:h]?\.?(\d{1,2})? ?- ?([210]?\d)[:h]?\.?(\d{1,2})? ?(?: ?[\/;] ?([210]?\d)[:h]?\.?(\d{1,2})? ?- ?([210]?\d)[:h]?\.?(\d{1,2})?)?'

        if schedule is np.nan:
            schedule = ''

        m = re.match(r, schedule)
        if m is not None:
            cleaned_schedule = '{}:{}-{}:{}'.format(clean_time(m.group(1)),
                                                    clean_time(m.group(2)) if m.group(2) is not None else '00',
                                                    clean_time(m.group(3)),
                                                    clean_time(m.group(4)) if m.group(4) is not None else '00')
            if m.group(5) is not None:
                cleaned_schedule += '/{}:{}-{}:{}'.format(clean_time(m.group(5)),
                                                          clean_time(m.group(6)) if m.group(6) is not None else '00',
                                                          clean_time(m.group(7)),
                                                          clean_time(m.group(8)) if m.group(8) is not None else '00')

            return cleaned_schedule
        return 'ABSENT : {}'.format(schedule)

    @staticmethod
    def clean_group(txt):
        """
        Nettoie les données de la colonne "groupe" de la liste Excel
        - params: texte de la colonne
        - return: "0" ou "1" en fonction de la présence du mot "oui"
        """
        return 1 if 'oui' in str(txt).lower() else 0

    def __init__(self):
        data = {}
        data['quotas'] = pd.read_excel('data/quota_guichet.xlsx')
        data['horaires'] = pd.read_excel('data/horaires.xlsx')

        for day in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']:
            data['horaires'][day] = data['horaires'][day].apply(Tellers.clean_schedule)

        data['horaires']['groupe'] = data['horaires']['groupe'].apply(Tellers.clean_group)
        data['horaires'] = data['horaires'].drop(['Prénom', 'Nom', 'Remarques'], axis=1)
        data['global'] = data['quotas'].merge(data['horaires'], on='Sciper', how='inner')
        self.tellers = []

        for teller in data['global'].index:
            self.tellers.append(Teller(data['global'].loc[teller]))


class Teller:
    """
    OBJECTIF: Représenter un guichetier.

    Méthode statique:
    - create_schedules_from_txt: transformer le texte en période temporelle

    Méthodes:
    - Constructeur
    - test_availability: Vérifier si pour une catégorie donnée, un guichetier est disponible.
    """

    @staticmethod
    def create_schedules_from_txt(txt):
        """
        OBJECTIF: transformer le texte en période temporelle.
        - params: texte des périodes de guichet
        - return: liste de périodes avec un début, une fin et un type de disponibilité
        """
        if txt.startswith('ABSENT'):
            return []
        schedules = txt.split('/')
        schedules = [{'hour_begin':datetime.datetime.strptime(schedule.split('-')[0], '%H:%M').time(),
                      'hour_end':datetime.datetime.strptime(schedule.split('-')[1], '%H:%M').time(),
                      'type_availability':'A'} for schedule in schedules]
        return schedules


    def __init__(self, row):
        self.sciper = row['Sciper']
        self.name = row['Nom affiché']

        # self.group_schedule = row['groupe']
        # self.quotas = {'total':row['Nb guichet fixe'],
        #                'stm_max':(row['Nb guichet fixe']) // 2,
        #                'total_r': row['Nb remplacements'],
        #                'stm_max_r': row['Nb remplacements'] // 2}
        #
        # self.defined_schedules = []
        #
        # self.availability = {'seances':Seances.seances_participation(row['Secteur'], row['BL'], row['Direction']),
        #                      'lundi':self.create_schedules_from_txt(row['lundi']),
        #                      'mardi':self.create_schedules_from_txt(row['mardi']),
        #                      'mercredi':self.create_schedules_from_txt(row['mercredi']),
        #                      'jeudi':self.create_schedules_from_txt(row['jeudi']),
        #                      'vendredi':self.create_schedules_from_txt(row['vendredi'])}
        #
        # self.create_schedule_B_C(row['disponible 18h'], datetime.time(16, 0), datetime.time(18, 0))
        # self.create_schedule_B_C(row['disponible 8h'], datetime.time(8, 0), datetime.time(9, 0))
        # self.create_schedule_B_C(row['disponible 20h'], datetime.time(18, 0), datetime.time(20, 0))

    def create_schedule_B_C(self, days_str, hour_begin, hour_end):
        """
        OBJECTIF: A partir des abréviations de jour, revenir à des périodes.
        - params: day_str (txt avec des abbréviations de jour), hour_begin (datetime.time), hour_end (datetime.time), day, category
        """

        if days_str is not np.nan:

            days = [{'lu':'lundi',
                     'ma':'mardi',
                     'me':'mercredi',
                     'je':'jeudi',
                     've':'vendredi'}[day] for day in days_str.split('-')]
            type_availability = 'B' if hour_begin.hour > 12 else 'C'

            for day in days:

                is_schedule_larger = True
                for schedule in self.availability[day]:
                    if type_availability == 'B' and hour_end <= schedule['hour_end']:
                        is_schedule_larger = False
                    if type_availability == 'C' and hour_begin >= schedule['hour_begin']:
                        is_schedule_larger = False


                if is_schedule_larger is True:
                    self.availability[day].append({'hour_begin':hour_begin,
                                                   'hour_end':hour_end,
                                                   'type_availability':type_availability})

    def test_quotas(self):
        """
        OBJECTIF: Vérfier si les quotas sont respectés.
        - return: True/False
        """
        def test_counter_day(counter_day):
            for day in counter_day:
                if counter_day[day] > 2:
                    return False

            return True

        counter_total = 0
        counter_r = 0
        counter_stm_r = 0
        counter_stm = 0
        counter_B = 0
        counter_C = 0
        counter_day = {'lundi':0,
                       'mardi':0,
                       'mercredi':0,
                       'jeudi':0,
                       'vendredi':0}

        for schedule_defined in self.defined_schedules:

            if self in schedule_defined.available_tellers_orig['B']:
                counter_B += 0
            if self in schedule_defined.available_tellers_orig['C']:
                counter_C += 1
            if schedule_defined.category == 'main':
                counter_day[schedule_defined.day] += schedule_defined.weight
                counter_total += schedule_defined.weight
            if schedule_defined.category == 'main_r':
                counter_r += schedule_defined.weight
            if schedule_defined.category == 'stm':
                counter_day[schedule_defined.day] += schedule_defined.weight
                counter_stm += schedule_defined.weight
                counter_total += schedule_defined.weight
            if schedule_defined.category == 'stm_r':
                counter_r += schedule_defined.weight
                counter_stm_r += schedule_defined.weight

        if counter_total > self.quotas['total'] \
           or counter_r > self.quotas['total_r'] \
           or counter_stm > self.quotas['stm_max'] \
           or counter_stm_r > self.quotas['stm_max_r'] \
           or counter_B > 1 \
           or counter_C > 1 \
           or test_counter_day(counter_day) is False:
            if self.name == '--Raphaël R.':
                print(counter_total)
                print(counter_r)
                print(counter_stm)
                print(counter_stm_r)
                print(counter_B)
                print(counter_C)
                print(counter_day)
            return False

        return True


    def test_availability(self, schedule):
        """
        OBJECTIF: Vérifier si pour une catégorie donnée, un guichetier est disponible.
        - params: object schedule à tester
        - return: None s'il n'y a pas de disponibilité, sinon une lettre correspondant à la disponibilité la plus favorable.
        """

        for seance in self.availability['seances']:
            if seance.test_overlapping(schedule.hour_begin, schedule.hour_end, schedule.day) is True:
                return None

        for defined_schedule in self.defined_schedules:
            if schedule.test_overlapping(defined_schedule.hour_begin, defined_schedule.hour_end, defined_schedule.day) is True:
                return None


        for time_available in self.availability[schedule.day]:

            if schedule.hour_begin >= time_available['hour_begin'] and schedule.hour_end <= time_available['hour_end']:

                self.defined_schedules.append(schedule)
                if self.test_quotas() is True:
                    del self.defined_schedules[-1]
                    return time_available['type_availability']
                else:
                    del self.defined_schedules[-1]
                    return None

        return None

class Quotas:
    """Classe représentant les quotas des guichetiers."""

    def __init__(self, total, total_r):
        """Constructeur définissant un quostas pour les gichetiers."""
        self.init = {'total': total,
                     'total_r': total_r,
                     'stm_max': total // 2,
                     'stm_max_r': total_r // 2,
                     'Mon': 2,
                     'Tue': 2,
                     'Wed': 2,
                     'Thu': 2,
                     'Fri': 2}

        self.reset_quotas()

    def reset_quotas(self):
        """Définit l'attribut "current" à l'identique avec "init"."""
        self.current = {}
        for key, value in self.init.items():
            self.current[key] = value

    def test_schedule(self, schedule_to_test):
        """Teste si une période à ajouter respecte les quotas."""
        if self.current[schedule_to_test.day] > 0:
            if schedule_to_test.category == 'accueil':
                return True if self.current['total'] > 0 else False
            if schedule_to_test.category == 'stm':
                return True if self.current['stm_max'] > 0 and self.current['total'] > 0 else False
            if schedule_to_test.category == 'accueil_r':
                return True if self.current['total_r'] > 0 else False
            if schedule_to_test.category == 'stm_r':
                return True if self.current['stm_max_r'] > 0 and self.current['total_r'] > 0 else False

        return False
