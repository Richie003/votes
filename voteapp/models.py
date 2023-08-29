from typing import Iterable, Optional
from django.db import models
from appauth.models import UserBio
from django.conf import settings
from django.utils.timezone import now

class Role(models.Model):
    role = models.CharField(default='', blank=False, max_length=255)

    def __str__(self):
        return str(self.role)

class Election(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.role)

class Candidate(models.Model):
    candidate_name = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    display_image = models.ImageField(upload_to="candidates/", blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    bio = models.ForeignKey(UserBio, on_delete=models.CASCADE)
    added = models.DateTimeField(default=now)

    def __str__(self):
        return str(f'{self.candidate_name.first_name} {self.candidate_name.last_name}')
    
    @property
    def get_vote_count(self):
        query_VoteTable = VoteTable.objects.filter(candidates_id=self.id)
        return query_VoteTable.count()

class VoteTable(models.Model):
    voted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    role_name = models.ForeignKey(Role, on_delete=models.CASCADE)
    candidates = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    voted = models.DateTimeField(auto_now_add=True)

class VoteCheck(models.Model):
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)