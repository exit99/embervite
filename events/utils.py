import datetime


class EventDateHelper(object):
    """Helps convert Event fields to human readable, and usable datetimes."""
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        super(EventDateHelper, self).__init__(*args, **kwargs)
        self.now = datetime.datetime.now()

    def calc_invite_date(self):
        return self.calc_date(int(self.model.invite_day),
                              self.model.invite_time)

    def calc_event_date(self):
        return self.calc_date(int(self.model.days), self.model.time)

    def calc_date(self, day, time):
        return self.update_time(self.calc_day(day), time)

    def calc_day(self, day):
        """We save with 1-7 not 0-6 like datetime.weekday()."""
        weekday = self.now.weekday() + 1
        if weekday > day:
            days = 6 - weekday + day
        else:
            days = day - weekday
        return self.now + datetime.timedelta(days=days)

    def update_time(self, date, time):
        return datetime.datetime(date.year, date.month, date.day, time.hour,
                                 time.minute)
