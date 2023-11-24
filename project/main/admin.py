from django.contrib import admin
from .models import *

class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'group']
    list_filter = ['name']
    search_fields = ['name']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'from_user', 'created_at','is_read']

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
