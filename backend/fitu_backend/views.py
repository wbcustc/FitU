from models import CustomUser
from serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from fitu.utils import JSONResponse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    # parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'user': UserSerializer(user).data, 'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()




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










