from django.db import models

class Problem(models.Model):
    DIFFICULTIES = (
        ('Easy','Easy'),
        ('Medium','Medium'),
        ('Hard','Hard'),
        ('Very Hard','Very Hard'),
    )

    name = models.CharField(max_length=40)
    name_slug = models.SlugField(unique=True)
    description = models.TextField()
    init_memory = models.CharField('Initial Memory', max_length=200, help_text= \
        "Separate by a space. Use '*' to represent empty spots.")
    difficulty = models.CharField(max_length=9, choices=DIFFICULTIES)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['difficulty', 'name']


class Test(models.Model):
    problem = models.ForeignKey(Problem)
    inbox = models.CharField(max_length=200)
    outbox = models.CharField(max_length=200)

    def __str__(self):
        return self.problem.name


class Score(models.Model):
    problem = models.ForeignKey(Problem)
    user = models.CharField(max_length=40)
    size = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)

    def __str__(self):
        return "{}: {}/{}".format(self.user, self.size, self.speed)

    class Meta:
        ordering = ['problem', 'size']
