from django.contrib import admin

# Register your models here.
from models import PropertyType, RealEstate, Skill, PersonSkill, PropertyInventory, Person, CurrentDate


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    exclude = ["join_date", "date_of_birth","uptime"]
    list_display = ["id","first_name", "last_name", "gender", "date_of_birth" ,"join_date", "parent_mother", "parent_father", "dead"]

    # admin.site.register(Person)