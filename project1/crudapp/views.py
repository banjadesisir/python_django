from django.shortcuts import render
from .models import Student
from django.contrib import messages
from django.db.models import Q

def index(request):
    students = Student.objects.all()
    search_query = ""
    
    if request.method == "POST":
        if "create" in request.POST:
            name = request.POST.get("name")
            email = request.POST.get("email")
            
            # Check if the email already exists
            if Student.objects.filter(email=email).exists():
                messages.error(request, "Email is already in use.")
            else:
                Student.objects.create(
                    name=name,
                    email=email
                )
                messages.success(request, "Student added successfully")
        
        elif "update" in request.POST:
            id = request.POST.get("id")
            name = request.POST.get("name")
            email = request.POST.get("email")
            student = Student.objects.get(id=id)
            student.name = name
            student.email = email
            student.save()
            messages.success(request, "Student updated successfully")
        
        elif "delete" in request.POST:
            id = request.POST.get("id")
            Student.objects.get(id=id).delete()
            messages.success(request, "Student deleted successfully")
        
        elif "search" in request.POST:
            search_query = request.POST.get("query")
            students = Student.objects.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))
    
    # Enumerate the students, starting from 1
    enumerated_students = list(enumerate(students, start=1))
    
    context = {
        "enumerated_students": enumerated_students, 
        "search_query": search_query
    }
    return render(request, "index.html", context=context)
