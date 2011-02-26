from django.contrib import admin
from models import Overview, PersonalInfo, Education, Job,\
    Accomplishment, Project, Skillset, Skill 

class AccomplishmentInline(admin.StackedInline):
    model = Accomplishment

class SkillInline(admin.StackedInline):
    model = Skill

class JobAdmin(admin.ModelAdmin):
    inlines = [
        AccomplishmentInline,
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
admin.site.register(Project)
admin.site.register(Skillset, SkillsetAdmin)
admin.site.register(Skill, SkillAdmin)