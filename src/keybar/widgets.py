import floppyforms.__future__ as forms


class Select2Widget(forms.Select):
    template_name = 'floppyforms/tags.html'
    allow_multiple_selected = True

    class Media:
        js = ('select2/select2.js',)
        css = {'all': ('select2/select2.css', )}

    def value_from_datadict(self, data, files, name):
        import ipdb; ipdb.set_trace()
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)
