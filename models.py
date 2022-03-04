from django.db import models
from CareeYour import settings
from skill.models import Skill

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'job_seeker_profile'
        verbose_name = 'Job Seeker Profile'
        verbose_name_plural = 'Job Seeker Profiles'

    def __str__(self):
        return '{}-{}'.format(self.first_name, self.user.email)


class EducationDetail(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    school_name = models.CharField("School/College Name", max_length=250)
    certificate_degree_name = models.CharField("Certificate/Degree Name", max_length=50)
    major_subject = models.CharField(max_length=20, blank=True, null=True)
    school_address = models.CharField(max_length=50, blank=True, null=True)
    date_start = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'job_seeker_education_detail'
        verbose_name = 'Job Seeker Education Detail'
        verbose_name_plural = 'Job Seeker Education Details'


class ExperienceDetail(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)
    is_current_job = models.BooleanField(default=False)
    date_start = models.DateField()
    date_end = models.DateField()
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'job_seeker_experience_detail'
        verbose_name = 'Job Seeker Experience Detail'
        verbose_name_plural = 'Job Seeker Experience Details'


class SkillSet(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skill')
    skill_set = models.ForeignKey(Skill, on_delete=models.PROTECT)

    class Meta:
        db_table = 'job_seeker_skill_set'
        verbose_name = 'Job Seeker Skill'
        verbose_name_plural = 'Job Seeker Skills'




