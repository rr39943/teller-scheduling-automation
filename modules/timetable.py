class Timetable:
    """
    OBJECTIF: Représenter l'horaire global.
    Attributs:
    - schedules: liste des périodes
    """

    def __init__(self):
        """
        OBJECTIF: construire l'horaire vide.
        """
        data = pd.read_excel('Periodes.xlsx')

        self.schedules = []
        rank = 0
        for day in ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']:
            for i in data.index:

                row = data.loc[i]
                if row['Début'].hour == 18 and day == 'vendredi':
                    break

                categories = row['Accueil'] * ['main'] + row['Accueil r.'] * ['main_r'] + row['STM'] * ['stm'] + row['STM r.'] * ['stm_r']
                # print(categories)
                for category in categories:
                    # print(category)
                    self.schedules.append(Schedule(hour_begin=row['Début'],
                                                   hour_end=row['Fin'],
                                                   num_schedule=i,
                                                   day=day,
                                                   category=category,
                                                   rank=rank,
                                                   weight=row['Poids']))
                    rank += 1



    def define_tellers_availability(self, tellers, init=False):
        """
        OBECTIF: Enregistrer les disponibilités des guichetiers dans les périodes
        Le paramètre "init" est utile pour enregistrer l'état d'origine des disponibilité.
        """
        for schedule in self.schedules:
            schedule.available_tellers = {'A':[],'B':[], 'C':[]}
            for teller in tellers:
                availability = teller.test_availability(schedule)
                if availability is not None:

                    schedule.available_tellers[availability].append(teller)

                    if init is True:
                        schedule.available_tellers_orig[availability].append(teller)

            schedule.shuffle_tellers()

            schedule.priority_level = schedule.get_nb_available_tellers()
        self.schedules = sorted(self.schedules, key=lambda schedule:schedule.priority_level, reverse=schedule.reverse)

    def reset_completed_prop(self):
        """
        OBJECTIF: Réinitialiser la propriété "cmpleted" qui empêche qu'on essaie
        plusieurs fois d'attribuer un guichetier à une même periode.
        """
        for schedule in self.schedules:
            schedule.warnings = 0
            if len(schedule.defined_teller) == 0:
                schedule.completed = False


    def define_tellers_schedules(self, tellers):
        """
        OBJECTIF: attribuer des guichetiers aux périodes.
        """
        i = 0
        self.define_tellers_availability(tellers)
        while i < len(self.schedules):
            # print(len(self.schedules))
            if self.schedules[i].completed is False:
                self.schedules[i].define_tellers()
                self.define_tellers_availability(tellers)
                i = 0
            else:
                i += 1

    def export_schedules(self):
        """
        OBJECTIF: exporter les données au format Excel.
        """
        self.schedules = sorted(self.schedules, key=lambda schedule:schedule.rank)
        print(self.schedules[0].__dict__)
