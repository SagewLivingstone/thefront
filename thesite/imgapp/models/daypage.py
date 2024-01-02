from django.db import models

class DayPage(models.Model):
    date = models.DateField()
    caption = models.TextField()

    def get_next_day(self):
        next = DayPage.objects.filter(
            date__gt=self.date
        ).order_by('date') .first()
        if next:
            return next.date

    def get_prev_day(self):
        prev = DayPage.objects.filter(
            date__lt=self.date
        ).order_by('date') .last()
        if prev:
            return prev.date
    
    @property
    def caption_inline(self):
        return self.caption.replace('\n', ' | ')

    def __str__(self) -> str:
        return f"Day: {str(self.date)} ({self.image_set.count()} image{'s' if self.image_set.count() > 1 else ''})   \"{self.caption_inline}\""