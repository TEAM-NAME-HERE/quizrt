from __future__ import unicode_literals

import uuid

from django.db import models

from . import Quiz

class Question(models.Model):
    prompt = models.CharField(max_length=255, unique=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    uuid = models.SlugField(default=uuid.uuid4, editable=False)


    # def get_correct_answers(self):
    #     pass

    def __str__(self):
        return self.prompt