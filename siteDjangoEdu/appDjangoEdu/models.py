"""Database tables as classes:
    class Questions(models.Model)
    class Themes(models.Model)

"""
from django.db import models


class Questions(models.Model):
    """
    Table that contains questions.

    question_id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    theme_id = models.IntegerField()

    """
    question_id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    theme_id = models.IntegerField()

    class Meta:
        db_table = 'Questions'

    def __str__(self):
        return f"{self.question_id}, {self.question}, {self.answer}, {self.theme_id}"

    def get_as_dict(self):
        return {"question_id": self.question_id, "question": self.question,
                "answer": self.answer, "theme_id": self.theme_id}


class Themes(models.Model):
    """
    Table that contains themes

    theme_id = models.AutoField(primary_key=True)
    name = models.TextField()
    parent_id = models.IntegerField(blank=True, null=True)
    """
    theme_id = models.AutoField(primary_key=True)
    name = models.TextField()
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'Themes'

    def __str__(self):
        return f"{self.theme_id}, {self.name}, {self.parent_id}"

    def get_as_dict(self):
        return {"theme_id": self.theme_id, "name": self.name, "parent_id": self.parent_id}

    def get_q_count(self):
        questions = Questions.objects.filter(theme_id=self.theme_id)
        count = len(questions)
        return count

    def get_question_dicts(self):
        q_list = []
        questions = Questions.objects.filter(theme_id=self.theme_id)
        for question in questions:
            q_list.append(question.get_as_dict())
        return q_list
