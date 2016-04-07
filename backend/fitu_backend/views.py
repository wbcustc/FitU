from models import CustomUser
from serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from fitu.utils import JSONResponse

@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        print serializer.data
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse({'status':'ok'}, status=201)
        return JSONResponse({'status':'failed'}, status=400)

@csrf_exempt
def user_detail(request, username):
  
    try:
        currUser = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(currUser)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(currUser, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        currUser.delete()
        return HttpResponse(status=204)

@csrf_exempt
def check_duplicate(request):
    if request.method == 'GET':
        username = request.GET['username']
        try:
            currUser = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return JSONResponse({'available': True, 'Message': 'Valid username.'})
        return JSONResponse({'available': False, 'Message': 'Duplicate username'})









