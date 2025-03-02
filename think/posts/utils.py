class DataMixin:
    title_page = None
    extra_context = {}
    error_message = None

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if not self.error_message:
            self.extra_context['error_message'] = self.error_message

    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context