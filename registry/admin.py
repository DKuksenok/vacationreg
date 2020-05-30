from django.contrib import admin

from .models import Employee, Vacation, VacationReview

class VacationInLine(admin.TabularInline):
    model = Vacation
    extra = 1

class VacationReviewInLine(admin.TabularInline):
    model = VacationReview
    extra = 1

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username')
    search_fields = ['last_name', 'first_name', 'middle_name']
    inlines = [VacationInLine, VacationReviewInLine]

class VacationAdmin(admin.ModelAdmin):
    pass

class VacationReviewAdmin(admin.ModelAdmin):
    pass

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Vacation, VacationAdmin)
admin.site.register(VacationReview, VacationReviewAdmin)
