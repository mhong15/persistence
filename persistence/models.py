from otree.api import models

class PlayerResponse(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    question_number = models.PositiveIntegerField()
    response = models.IntegerField()

    def __str__(self):
        return f'Player {self.player.id} Response to Question {self.question_number}'
