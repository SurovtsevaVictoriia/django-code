from django.db import models


class Questions(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    theme_id = models.IntegerField()

    class Meta:
        db_table = 'Questions'

    def __str__(self):
        return f"{self.question_id}, {self.question}, {self.answer}, {self.theme_id}"


class Themes(models.Model):
    theme_id = models.AutoField(primary_key=True)
    name = models.TextField()
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Themes'

    def __str__(self):
        return f"{self.theme_id}, {self.name}, {self.parent_id}"
