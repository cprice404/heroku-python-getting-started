from django.forms import formset_factory
from django.shortcuts import render
from hello.forms import PersonForm


def handle_formset_request(request):
    PersonFormSet = formset_factory(PersonForm)
    bunk_initial_data = [
        {'first_name': 'Bill', 'last_name': 'Williams'},
        {'first_name': 'Kim', 'last_name': 'Kimberley'}
    ]

    if request.method == 'POST':
        person_formset = PersonFormSet(request.POST, request.FILES,
                                       initial=bunk_initial_data)
        print("!!!!!! PERSON FORMSET POSTED!")

        if person_formset.is_valid():
            # do something with the formset.cleaned_data
            print("!!!!!! PERSON FORMSET VALID!")
            pass

        if person_formset.has_changed():
            print("!!!!!! PERSON FORMSET CHANGED!")
        else:
            print("!!!!!! PERSON FORMSET NOT CHANGED!!")

        print "NUM FORMS: '%s'" % len(person_formset.forms)
        for form in person_formset.forms:
            print "FORM changed? '%s'" % form.has_changed()
            print "FORM changed data: '%s'" % form.changed_data
    else:
        person_formset = PersonFormSet(initial=bunk_initial_data)
    return render(request, 'formset.html',
                  context={'formset': person_formset})
