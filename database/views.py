"""Database related view functions."""


import re
import textwrap
from io import StringIO
from Bio import SeqIO
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from .models import PesticidalProteinDatabase, UserUploadData, Description


def home(request):
    """Loads the homepage."""

    return render(request, 'database/home.html')


def categorize_database(request, category=None):
    """Categorize the protein database with unqiue, first three letter pattern."""

    context = \
        {'proteins': PesticidalProteinDatabase.objects.filter(
            name__istartswith=category),
         'descriptions': Description.objects.filter(
             name__istartswith=category)
         }
    return render(request, 'database/category_update.html', context)


def database(request):
    """Returns the protein list for the categories from the database."""

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name').distinct()
    category_prefixes = []
    for category in categories:
        prefix = category[0][:3]
        if prefix not in category_prefixes:
            category_prefixes.append(prefix)

    context = \
        {'category_prefixes': category_prefixes,
         'descriptions': Description.objects.all()}
    return render(request, 'database/database.html', context)


def search_database(request):
    """Returns the results based on the search query."""

    if request.method == 'POST':
        search_term = request.POST['search_term']
        search_term = search_term.strip()
        searches = re.split(r':|, ?|\s |\- |_ |. |; |\*|\n',
                            search_term)

        q_objects = Q()
        for search in searches:
            q_objects.add(Q(name__icontains=search), Q.OR)

        proteins = PesticidalProteinDatabase.objects.filter(q_objects)
        if proteins:
            return render(request, 'database/search_results.html',
                          {'proteins': proteins})

    return render(request, 'database/search_page.html')


def add_cart(request):
    """Add the profiles to the cart."""

    if request.method == 'POST':
        selected_values = request.POST.getlist('name', [])
        previously_selected_values = request.session.get('list_names', [])
        previously_selected_values.extend(selected_values)

        request.session['list_names'] = previously_selected_values
        profile_length = len(selected_values)
        message_profile = \
            "Selected {} proteins added to the cart".format(profile_length)
        messages.success(request, message_profile)

    return redirect("search_database")


def clear_session_database(request):
    """Clear the database session."""

    session_key = list(request.session.keys())

    for key in session_key:
        del request.session[key]
    return redirect("view_cart")


def remove_cart(request, database_id):
    """Remove the selected proteins one by one from the cart."""

    protein = PesticidalProteinDatabase.objects.get(id=database_id)

    selected_values = request.session.get('list_names')
    selected_values.remove(protein.name)
    request.session.modified = True

    if selected_values:
        return redirect("view_cart")
    message_profile = "Please add sequences to the cart"
    messages.success(request, message_profile)
    return redirect("search_database")


def view_cart(request):
    """View the selected proteins in the session and user uploaded sequences."""

    selected_values = request.session.get('list_names')

    userdata = \
        UserUploadData.objects.filter(session_key=request.session.session_key)

    context = {'proteins': PesticidalProteinDatabase.objects.all(),
               'selected_groups': selected_values, 'userdata': userdata}

    return render(request, 'database/search_user_data.html', context)


def clear_session_user_data(request):
    """Remove all the user uploaded proteins from the cart."""

    UserUploadData.objects.filter(
        session_key=request.session.session_key).delete()

    return redirect("view_cart")


def user_data_remove(request, database_id):
    """Remove the user uploaded proteins individually"""

    instance = \
        UserUploadData.objects.get(session_key=request.session.session_key,
                                   id=database_id)
    instance.delete()

    return redirect("view_cart")


def user_data(request):
    """A user will upload the protein sequences in fasta format
    and stored temporarily using the session."""

    if request.method == 'POST':
        file = request.POST['fulltextarea']
        if not file:
            message_profile = "Please add some sequences"
            messages.success(request, message_profile)
            return redirect("view_cart")

        content = ContentFile(file)
        content = filter(None, content)

        for rec in SeqIO.parse(content, "fasta"):
            name = rec.id
            sequence = str(rec.seq)
            UserUploadData.objects.create(
                session_key=request.session.session_key,
                name=name, fastasequence=sequence)
        message_profile = "Added the sequence"
        messages.success(request, message_profile)

    return redirect("view_cart")


@csrf_exempt
def download_sequences(request):
    """Download the selected and/or user uploaded protein sequences."""

    selected_values = request.session.get('list_names', [])
    userdata = \
        UserUploadData.objects.filter(session_key=request.session.session_key)

    if not selected_values and not userdata.exists():
        message_profile = "Please add sequences to the cart"
        messages.success(request, message_profile)
        return redirect("view_cart")

    file = StringIO()
    data = \
        PesticidalProteinDatabase.objects.filter(name__in=selected_values)
    for item in data:
        fasta = textwrap.fill(item.fastasequence, 80)
        str_to_write = f">{item.name}\n{fasta}\n"
        file.write(str_to_write)

    for record in userdata:
        fasta = textwrap.fill(record.fastasequence, 80)
        str_to_write = f">{record.name}\n{fasta}\n"
        file.write(str_to_write)

    response = HttpResponse(file.getvalue(), content_type="text/plain")
    response['Content-Disposition'] = \
        'attachment;filename=data_fasta.txt'
    response['Content-Length'] = file.tell()
    return response


def download_data(request):
    """List the categories for download."""

    categories = \
        PesticidalProteinDatabase.objects.order_by(
            'name').values_list('name').distinct()
    category_prefixes = []
    for category in categories:
        prefix = category[0][:3]
        if prefix not in category_prefixes:
            category_prefixes.append(prefix)

    context = {
        'proteins': PesticidalProteinDatabase.objects.all(),
        'category_prefixes': category_prefixes
    }
    return render(request, 'database/download_category.html', context)


def download_category(request, category=None):
    """Download all fasta sequences for the category."""

    context = {
        'proteins': PesticidalProteinDatabase.objects.all()
    }
    category = category.title()
    file = StringIO()
    data = list(context.get('proteins'))

    for item in data:
        if category in item.name:
            fasta = textwrap.fill(item.fastasequence, 80)
            str_to_write = f">{item.name}\n{fasta}\n"
            file.write(str_to_write)
        else:
            pass

    if 'All' in category:
        for item in data:
            fasta = textwrap.fill(item.fastasequence, 80)
            str_to_write = f">{item.name}\n{fasta}\n"
            file.write(str_to_write)

    response = HttpResponse(file.getvalue(), content_type="text/plain")
    download_file = f"{category}_fasta_sequences.txt"
    response['Content-Disposition'] = 'attachment;filename='+download_file
    response['Content-Length'] = file.tell()
    return response
