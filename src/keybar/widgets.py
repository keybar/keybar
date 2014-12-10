import floppyforms.__future__ as forms
from django.utils.datastructures import MultiValueDict, MergeDict


class Select2Widget(forms.widgets.Input):
    template_name = 'floppyforms/tags.html'
    allow_multiple_selected = True

    class Media:
        js = ('select2/select2.js',)
        css = {'all': ('select2/select2.css', )}

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            retval = []
            for item in data.getlist(name):
                retval.extend([x.strip() for x in item.split(',')])
            return retval
        return data.get(name, None)
