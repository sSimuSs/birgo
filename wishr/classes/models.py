from django.utils import timezone
from django.utils.translation import get_language
from django.contrib.humanize.templatetags.humanize import naturalday

class BaseModelInterface:
    """ Base model interface for all models """
    @property
    def created_at(self):
        """ Requiring 'created_at' to be implemented in head model classes '"""
        raise NotImplementedError("Model must implement 'created_at'")

    def natural_created_at(self) -> str:
        """ Method for getting natural creation date """
        lang = get_language()
        today = timezone.now().date()
        created_at = timezone.make_naive(self.created_at)
        result = naturalday(created_at)
        if created_at.year == today.year:
            if lang == "en":
                result = naturalday(created_at, "N j")
            else:
                result = naturalday(created_at, "j N").lower()
        result += f" {str(created_at.strftime("%H:%M"))}"
        return result
