from django.db import models
from datetime import date

class DishRotation(models.Model):
    YOU = "You"
    SISTER = "Sister"
    PEOPLE = [YOU, SISTER]

    today_index = models.IntegerField(default=0)
    last_updated = models.DateField(default=date.today)

    def today(self):
        return self.PEOPLE[self.today_index]

    def tomorrow(self):
        return self.PEOPLE[(self.today_index + 1) % len(self.PEOPLE)]

    def rotate_by(self, steps=1):
        """Rotate the index forward by `steps` (modulo people length)."""
        self.today_index = (self.today_index + steps) % len(self.PEOPLE)
        self.last_updated = date.today()
        self.save()

    def set_today(self, person):
        """Force-set who washes today."""
        idx = self.PEOPLE.index(person)
        self.today_index = idx
        self.last_updated = date.today()
        self.save()

    def auto_rollover(self):
        """If multiple days passed since last_updated, advance accordingly."""
        days_passed = (date.today() - self.last_updated).days
        if days_passed <= 0:
            return
        # rotate by number of days passed (so schedule stays continuous even if no one opened the app)
        self.rotate_by(days_passed)

class WashHistory(models.Model):
    person = models.CharField(max_length=50)
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.person} — {self.date.isoformat()}"
