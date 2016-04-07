# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from fitu.utils import JSONResponse
from fitu_backend.models import CustomUser
from fitu_backend.serializers import UserSerializer

import boto3

bucket_name = u'fituuseravatar'
base_s3_url = r'https://s3.amazonaws.com/'

class AvatarUpload(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    def post(self, request, format=None):
		my_file = request.FILES['avatar']
		username = request.POST['username']
		file_id =  username + '-avatar.jpg'
		s3 = boto3.client('s3')
		s3.put_object(Bucket=bucket_name, 
			Key=file_id, Body=my_file)
		userUrl = base_s3_url + bucket_name + r'/' + file_id
		print userUrl
		currUser = CustomUser.objects.get(username=username)
		serializer = UserSerializer(currUser, 
			data={u'username' : username,u'avatarUrl' : userUrl })
		if serializer.is_valid():
			serializer.save()
			return JSONResponse({'avatarUrl' : userUrl})
		else:
			print serializer.errors
			return JSONResponse(serializer.errors, status=400)
	    

