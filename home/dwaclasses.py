from datetime import datetime

from django.http import HttpResponseRedirect


class DwaCommon:
    # override default form_valid to set updateby and lastupdate
    def form_valid(self, form):
        print("DwaCommon::dwa_form_valid")
        print(f"form in dwa_form_valid_save: {form.cleaned_data}")
        model = form.save(commit=False)
        model.updateby = f"{self.request.user}"
        model.lastupdate = datetime.now()
        model.save()
        self.object = model
        return HttpResponseRedirect(self.get_success_url())


class DwaCommon:

    def dwa_form_valid_save_model(self, form, model):
        print("DwaCommon::dwa_is_valid_save2")
        model.updateby = f"{self.request.user}"
        model.lastupdate = datetime.now()
        model.save()
        self.object = model
        print(f"type(model): {type(model)}")
        print(f"model: {model}")
        print(f"self.object: {self.object}")
        return HttpResponseRedirect(self.get_success_url())

    def dwa_form_valid_save(self, form):
        print("DwaCommon::dwa_is_valid_save1")
        print(f"form in dwa_form_valid_save: {form.cleaned_data}")
        model = form.save(commit=False)
        model.updateby = f"{self.request.user}"
        model.lastupdate = datetime.now()
        model.save()
        self.object = model
        print(f"type(model): {type(model)}")
        print(f"model: {model}")
        print(f"self.object: {self.object}")
        return HttpResponseRedirect(self.get_success_url())

    def dwa_get_limited(self, request, *args, **kwargs):
        print(f"self: {self}")
        print(f"request: {request}")
        print(f"request.GET: {request.GET}")
        self.name_filter = request.GET.get('name_filter', 'A')
        self.active = request.GET.get('filter', 'Y')
        if (self.active == 'N'): self.active = ''
        print(f"request.GET.name: {self.name_filter}; filter: {self.active}")

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['name_filter'] = self.name_filter
        context['filter'] = self.active
        #        print (f"object_list: {self.object_list}\n")
        #        print (f"*****context: {context}*****")
        return self.render_to_response(context)
