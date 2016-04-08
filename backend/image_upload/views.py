# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from fitu.utils import JSONResponse
from fitu_backend.models import CustomUser
from fitu_backend.serializers import UserSerializer
from models import PhotoRecord
import time
import boto3

photo_bucket = u'fituuserphoto'
avatar_bucket = u'fituuseravatar'
base_s3_url = u'https://s3.amazonaws.com/'

class AvatarUpload(APIView):
    parser_classes = (MultiPartParser, FormParser,)
    def post(self, request, format=None):
		curr_avatar = request.FILES['avatar']
		username = request.POST['username']
		file_id =  username + '-avatar.jpg'
		s3 = boto3.client('s3')
		s3.put_object(Bucket = avatar_bucket, 
			Key = file_id, Body = curr_avatar)
		avatar_url = base_s3_url + avatar_bucket + u'/' + file_id
		# print avatar_url
		curr_user = CustomUser.objects.get(username = username)
		serializer = UserSerializer(curr_user, 
			data={u'username' : username,u'avatarUrl' : avatar_url })
		if serializer.is_valid():
			serializer.save()
			return JSONResponse({'avatarUrl' : avatar_url })
		else:
			print serializer.errors
			return JSONResponse(serializer.errors, status = 400)
	    
class PhotoUpload(APIView):
	parser_classes = (MultiPartParser, FormParser,)
	def get(self, request, format=None):
		ret = []
		for record in PhotoRecord.objects.order_by('-photoId').all():
			temp_dict = {
				'brand' : record.brand, 
				'photoUrl' : record.photoUrl, 
				'buylink' : record.buyLink
			}
			ret.append(temp_dict)

		return JSONResponse({'data' : ret})

	def post(self, request, format=None):
		curr_photo = request.FILES['photo']
		username = request.POST['username']
		buy_link = request.POST['buylink']
		brand = request.POST['brand']
		photo_id = str(int(time.time() * 1000)) + '-' + username + '.jpg'
		s3 = boto3.client('s3')
		s3.put_object(Bucket = photo_bucket, 
			Key = photo_id, Body = curr_photo)
		photo_url = base_s3_url + photo_bucket + u'/' + photo_id
		print photo_url

		photo_record = PhotoRecord(username = username, photoId=photo_id, 
			photoUrl = photo_url ,buyLink = buy_link, brand = brand)
		photo_record.save()
		return JSONResponse({ 'photoUrl' : photo_url })    	

class UserPhotoList(APIView):
	def get_objects(self, username):
		try:
			return PhotoRecord.objects.order_by('-photoId').filter(username = username)
		except PhotoRecord.DoesNotExist:
			return None

	def get(self, request, username, format=None):
		ret = []
		recordlist = self.get_objects(username)
		if recordlist == None:
			return Response('Invalid username!', status = 400)
		else:
			for record in recordlist:
				temp_dict = {
					'brand' : record.brand,  
					'photoUrl' : record.photoUrl, 
					'buylink' : record.buyLink
				}
				ret.append(temp_dict)
			return JSONResponse({'data' : ret})




