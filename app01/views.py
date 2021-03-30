from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.


def index(request):
    # logic
    # Test ORM
    res = models.User.objects.all()
    for i in res:
        print(i, i.username, i.password, type(i.username))
    print(res, type(res))
    return render(request, 'index.html')  # Return a HTML page


def login(request):
    if request.method == 'POST':
        # The logic of dealing with POST request
        # Obtain the user name and pwd users input
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        # To validate the input value via database
        # if user == 'alex' and pwd == '123':
        if models.User.objects.filter(username=user, password=pwd):
            # If validation successes, inform the success of login
            return redirect('/index/')
    # Else return the original page
    return render(request, 'login.html')


def publisher_list(request):
    # Logic
    # Obtain all the information of Publishers
    # Return a page which contains the information
    all_publishers = models.Publisher.objects.all().order_by('id')
    return render(request, 'publisher_list.html', {'all_Publishers': all_publishers})


# Add new publishers
def publisher_add(request):
    if request.method == 'POST':
        # Post request
        # Obtain the data user input
        pub_name = request.POST.get('pub_name')
        print(pub_name)

        # If there are duplicated names already in database
        if models.Publisher.objects.filter(name=pub_name):
            return render(request, 'publisher_add.html', {'error': 'Name already exits!'})

        # If the name is empty
        if not pub_name:
            return render(request, 'publisher_add.html', {'error': 'Name cannot be empty!'})

        # Add the data into database
        res = models.Publisher.objects.create(name=pub_name)
        print(res, type(res))
        # return a new page containing new data
        return redirect('/publisher_list/')
    # Get request returns a page containing Form
    return render(request, 'publisher_add.html')


# Delete publishers
def publisher_del(request):
    # Obtain the id of the object
    pk = request.GET.get('pk')
    print(pk)
    # Delete the id from database
    models.Publisher.objects.get(pk=pk).delete()
    # Redirect to the original page
    return redirect('/publisher_list/')


# Edit Publishers
def publisher_edit(request):
    pk = request.GET.get('pk')
    pub_obj = models.Publisher.objects.get(pk=pk)

    # Get Request: return a page containing Form, and input the original data
    if request.method == 'GET':
        return render(request, 'publisher_edit.html', {'pub_obj': pub_obj})

    # Post Request:
    else:
        # Get the name of publisher user submitted
        pub_name = request.POST.get('pub_name')

        # If there are duplicated names already in database
        if models.Publisher.objects.filter(name=pub_name):
            return render(request, 'publisher_edit.html', {'error': 'Name already exits!'})

        # If the name is empty
        if not pub_name:
            return render(request, 'publisher_edit.html', {'error': 'Name cannot be empty!'})

        # Manipulate the data in database
        pub_obj.name = pub_name
        # Submit the change
        pub_obj.save()
        # Redirect to the original page in Publisher_list
        return redirect('/publisher_list')


def book_list(request):
    # Query all the books:
    all_books = models.Book.objects.all()
    # for book in books:
    #     print(book)
    #     print(book.name)
    #     print(book.publisher, book.publisher.pk, book.publisher.name)  # The corresponding publisher obj
    #     print(book.publisher_id)  # The publisher_id of a book

    # Return a page including book data
    # return HttpResponse('books')
    return render(request, 'book_list.html', {'all_books': all_books})


# Newly added books
def book_add(request):
    error = ''
    # If the request is a POST, then get the data user input
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')

        # Error handle:
        if not book_name:
            # Book_name cannot be empty
            error = "Book name cannot be empty"
        elif models.Book.objects.filter(name=book_name):
            # If there are duplicated book_name in the databass
            error = "Book already exists"
        else:
            # Insert the book info into database
            models.Book.objects.create(name=book_name, publisher=models.Publisher.objects.get(pk=pub_id))
            # return to the original page to show all the books
            return redirect('/book_list/')

    # If the query is a GET request, return the page with all the entities
    # query all the publishers
    all_publishers = models.Publisher.objects.all()
    # GET request, return a page containing a form
    return render(request, 'book_add.html', {'all_publishers': all_publishers, 'error': error})


# Delete a book
def book_del(request):
    # Obtain the book id user input
    pk = request.GET.get('id')
    # Obtain the object in database, and delete it
    models.Book.objects.filter(pk=pk).delete()
    # Redirect to the original page
    return redirect('/book_list/')


# Edit a book
def book_edit(request):

    # Obtain the obj to be edited
    pk = request.GET.get('id')
    book_obj = models.Book.objects.get(pk=pk)

    if request.method == 'POST':
        # POST request
        # Obtain the data user input
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub_id')
        # # Edit the corresponding obj
        # book_obj.name = book_name
        # book_obj.publisher_id = pub_id
        # # Save the data to database
        # book_obj.save()

        # Method 2
        models.Book.objects.filter(pk=pk).update(name=book_name,publisher_id=pub_id)
        return redirect('/book_list/')
        # Redirect to the new book_list page

    # GET request
    # Edit the obj according to the result
    # return a page containing the manipulated data

    all_publisher = models.Publisher.objects.all()

    return render(request, 'book_edit.html', {'book_obj': book_obj, 'all_publishers': all_publisher})