import time, os, errno
from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings

class Overview(models.Model):
    text = models.TextField()

    class Meta:
        verbose_name_plural = "Overview"

    def __unicode__(self):
        return self.text[0:40] + '...'

class PersonalInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    locality = models.CharField(max_length=255, help_text="e.g. city such as Boston")
    region = models.CharField(max_length=255, help_text="e.g. state such as Massachusetts")
    region_shorthand = models.CharField(max_length=64, help_text="e.g. shorthand (abbr), MA for Massachusetts")
    email = models.EmailField()
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = "Personal Info"
    
    def full_name(self):
        return " ".join([self.first_name, self.last_name])
    
    def __unicode__(self):
        return self.full_name()

class Education(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    school_url = models.URLField('School URL')
    start_date = models.DateField()
    completion_date = models.DateField()
    summary = models.TextField()
    is_current = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Education"

    def edu_date_range(self):
        return ''.join(['(', self.formatted_start_date(), 
            '-', self.formatted_end_date(), ')'])

    def full_start_date(self):
        return self.start_date.strftime("%Y-%m-%d")

    def full_end_date(self):
        if (self.is_current == True):
            return time.strftime("%Y-%m-%d", time.localtime())
        else:
            return self.completion_date.strftime("%Y-%m-%d")

    def formatted_start_date(self):
        return self.start_date.strftime("%b %Y")

    def formatted_end_date(self):
        if (self.is_current == True):
            return "Current"
        else:
            return self.completion_date.strftime("%b %Y")

    def __unicode__(self):
        return ' '.join([self.name, self.edu_date_range()])


class Job(models.Model):
    company = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    company_url = models.URLField('Company URL', blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    completion_date = models.DateField()
    is_current = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    company_image = models.CharField(max_length=250, blank=True, 
        help_text='path to company image, local or otherwise')

    class Meta:
        db_table = 'jobs'
        ordering = ['-completion_date','-start_date']
        
    def job_date_range(self):
        return ''.join(['(', self.formatted_start_date(),'-', 
            self.formatted_end_date(), ')'])
    
    def full_start_date(self):
        return self.start_date.strftime("%Y-%m-%d")

    def full_end_date(self):
        if (self.is_current == True):
            return time.strftime("%Y-%m-%d", time.localtime())
        else:
            return self.completion_date.strftime("%Y-%m-%d")

    def formatted_start_date(self):
        return self.start_date.strftime("%b %Y")
        
    def formatted_end_date(self):
        if (self.is_current == True):
            return "Current"
        else:
            return self.completion_date.strftime("%b %Y")

    def __unicode__(self):
        return ' '.join([self.company, self.job_date_range()])

class Accomplishment(models.Model):
    description = models.TextField()
    job = models.ForeignKey(Job)
    order = models.IntegerField()

    class Meta:
        db_table = 'accomplishments'
        ordering = ['order']

    def __unicode__(self):
        return ''.join([self.job.company, '-', self.description[0:50], '...'])


def maintain_project_media_folder(sender, **kwargs):
    """
    This is a superfluous function I made that stands as a Set of Refactors tbd
    TODO: remove project media dirs on post_delete instead of create
    TODO: refactor the project specific part out to it's own function
    Maintains the 'resume_projects' folder under settings.MEDIA_ROOT
    """
    instance = None
    for key in kwargs:
        if key == 'instance':
            instance = kwargs['instance']
            
    media_dir = os.path.join(settings.RESUME_PROJECTS_MEDIA_ROOT, instance.name, 'pics')
    try:
        if pics_dir != '/':
            os.makedirs(media_dir)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

class Project(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    repository = models.URLField('Project Repository', blank=True)
    
    def __unicode__(self):
        return self.name

#pre_save.connect(maintain_project_media_folder, sender=Project)


def get_save_path(instance, filename):
    """
    dynamically generates the save path for a ProjectPic
    """
    return os.path.join(instance.project.name, 'pics', filename)

class ProjectPic(models.Model):
    project = models.ForeignKey(Project)
    pic_file = models.FileField(upload_to=get_save_path)
    
    def __unicode__(self):
        return self.pic_file.path

class Skillset(models.Model):
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name

class Skill(models.Model):
    name =  models.CharField(max_length=250)
    skill_url = models.URLField('Skill URL', blank=True)
    skillset = models.ForeignKey(Skillset)
    
    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return ''.join([self.skillset.name, '-', self.name])
