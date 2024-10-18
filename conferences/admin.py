from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import conference 
from django.utils import timezone
from users.models import reservation
from django.db.models import Count


# Inline model to show reservations within the conference admin
class ReservationInline(admin.TabularInline):
    model = reservation
    extra = 1
    readonly_fields = ('reservation_date',)
    can_delete = True

# Custom filter for conferences based on their dates
class ConferenceDateFilter(admin.SimpleListFilter):
    title = "Conference Date Filter"
    parameter_name = "conference_date"

    def lookups(self, request, model_admin):
        return (
            ('past', ('Past Conferences')),
            ('today', ('Today\'s Conferences')),
            ('upcoming', ('Upcoming Conferences')),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'past':
            return queryset.filter(end_date__lt=today)
        if self.value() == 'today':
            return queryset.filter(start_date__lte=today, end_date__gte=today)
        if self.value() == 'upcoming':
            return queryset.filter(start_date__gt=today)
        return queryset

# Custom filter for conferences based on the number of participants (reservations)
class ParticipantFilter(admin.SimpleListFilter):
    title = "Participants Filter"
    parameter_name = "participants"

    def lookups(self, request, model_admin):
        return (
            ('0', ('No Participants')),
            ('more', ('With Participants')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        if self.value() == 'more':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        return queryset

# Admin model customization for conference
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date', 'price')
    search_fields = ('title',)
    list_per_page = 2
    ordering = ('start_date', 'title')

    fieldsets = (
        ('Description', {
            'fields': ('title', 'description', 'category', 'location', 'price', 'capacity')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Documents', {
            'fields': ('program',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ReservationInline]
    autocomplete_fields = ('category',)
    list_filter = ('title', ParticipantFilter, ConferenceDateFilter)

# Registering the Conference model with custom admin
admin.site.register(conference, ConferenceAdmin)

