from django.contrib import admin

from evaluation_module.models import Expert, HorseEvaluationRequest, HorseEvaluationReport


# Register your models here.
class EvaluationReportInline(admin.StackedInline):
    model = HorseEvaluationReport
    extra = 0


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'experience_years', 'verified', 'blocked')
    search_fields = ('user__last_name', 'user__first_name')


@admin.register(HorseEvaluationRequest)
class HorseEvaluationRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_created_jalali', 'status')
    list_filter = ('created_at',)
    search_fields = ('horse__name',)

    inlines = [
        EvaluationReportInline
    ]


@admin.register(HorseEvaluationReport)
class HorseEvaluationReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'expert', 'get_created_jalali')
