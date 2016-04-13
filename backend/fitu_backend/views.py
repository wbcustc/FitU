from models import CustomUser
from serializers import UserSerializer, CreateUserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from fitu.utils import JSONResponse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView



class ObtainAuthToken(APIView):
    # throttle_classes = ()
    # permission_classes = ()
    parser_classes = (JSONParser,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return JSONResponse({'user': UserSerializer(user).data, 'token': token.key})


class user_list(APIView):
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        print serializer.data
        return JSONResponse(serializer.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = CreateUserSerializer(data=data)
        if serializer.is_valid():
            #print serializer.data, type(serializer.data)
            #CustomUser.objects.create_user(dict(serializer.data))
            serializer.save()
            return JSONResponse({'status':'ok'}, status=201)
        return JSONResponse({'status':'failed'}, status=400)


class check_duplicate(APIView):
    def get(self, request, format=None):
        username = request.GET['username']
        try:
            currUser = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return JSONResponse({'available': True, 'Message': 'Valid username.'})
        return JSONResponse({'available': False, 'Message': 'Duplicate username'})










