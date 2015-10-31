import sublime
import nimlime_core
from nimlime_core import settings
from nimlime_core.utils.output import (
    get_output_view, write_to_view, show_view, format_tag
)


class NimLimeMixin(object):
    def __init__(self, *args, **kwargs):
        self.enabled = True
        if hasattr(self, 'load_settings'):
            self.reload_settings()

    def reload_settings(self):
        self.load_settings()
        settings.add_on_change('reload', self.load_settings)

    def get_setting(self, key, default):
        formatted_key = key.format(self.settings_selector)
        result = settings.get(formatted_key, default)
        return result

    def load_settings(self):
        self.enabled = self.get_setting('{0}.enabled', True)

    def is_enabled(self, *args, **kwargs):
        return self.enabled

    def is_visible(self):
        return self.is_enabled()

    def description(self, *args, **kwargs):
        return self.__doc__


class NimLimeOutputMixin(NimLimeMixin):
    def load_settings(self):
        get = self.get_setting

        self.enabled = get('{0}.enabled', True)
        self.clear_output = get('{0}.output.clear', True)
        self.output_method = get('{0}.output.method', 'grouped')
        self.send_output = get('{0}.output.send', True)
        self.show_output = get('{0}.output.show', True)
        self.output_tag = get('{0}.output.tag', 'nimlime')
        self.raw_output = get('{0}.output.raw', True)
        self.output_name = get('{0}.output.name', 'nimlime')

    def write_to_output(self, content, source_window, source_view):
        tag = format_tag(self.output_tag, source_window, source_view)
        output_window, output_view = get_output_view(
            tag, self.output_method, self.output_name, self.show_output,
            source_window
        )

        write_to_view(output_view, content, self.clear_output)

        if self.show_output:
            output_view.settings().set('output_tag', tag)
            is_console = (self.output_method == 'console')
            show_view(output_window, output_view, is_console)
