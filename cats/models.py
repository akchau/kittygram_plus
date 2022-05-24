from django.db import models
from django.contrib.auth import get_user_model


CHOICES = (
    ('Gray', 'Серый'),
    ('Black', 'Черный'),
    ('White', 'Белый'),
    ('Ginger', 'Рыжий'),
    ('Mixed', 'Смешанный')
)

User = get_user_model()

'''
class Owner(models.Model):
    """Модель владельца кота."""
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
'''


class Achievement(models.Model):
    """Модель достижений кота."""
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Cat(models.Model):
    """Модель кота."""
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(User, related_name='cats', on_delete=models.CASCADE )
    achievements = models.ManyToManyField(Achievement, through='AchievementCat')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'owner'],
                name='unique_name_owner'
            )
        ]
        # этот метод является устаревшим
        # unique_together = ('name', 'owner')

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    """Модель для связи many-to-many"""
    achievement = models.ForeignKey(Achievement, on_delete = models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'




