from django.contrib import admin
from .models import * # Import your model here


class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'firstUser', 'botAnswer', 'created_at', 'updated_at']  # Customize this as needed
    list_filter = ['username', 'firstUser']  # Add filters if necessary
    search_fields = ['username', 'botAnswer']  # Add search fields if necessary

# Register your model with the admin site
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Patient)
