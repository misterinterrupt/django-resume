from django.contrib import admin
from models import Overview, PersonalInfo, Education, Job,\
    Accomplishment, Project, ProjectPic, Skillset, Skill 

class AccomplishmentInline(admin.StackedInline):
    model = Accomplishment

class SkillInline(admin.StackedInline):
    model = Skill

class ProjectPicInline(admin.StackedInline):
    model = ProjectPic

class JobAdmin(admin.ModelAdmin):
    inlines = [
        AccomplishmentInline,
    ]


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectPicInline,
    ]

class AccomplishmentAdmin(admin.ModelAdmin):
    list_select_related = True
    ordering = ['job__company','order']

class SkillsetAdmin(admin.ModelAdmin):
    inlines = [
        SkillInline,
    ]

class SkillAdmin(admin.ModelAdmin):
    list_select_related = True
    ordering = ['skillset__name','name']

admin.site.register(PersonalInfo)
admin.site.register(Overview)
admin.site.register(Education)
admin.site.register(Job, JobAdmin)
admin.site.register(Accomplishment, AccomplishmentAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skillset, SkillsetAdmin)
admin.site.register(Skill, SkillAdmin)