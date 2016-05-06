# Create your views here.
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from fitu.utils import JSONResponse
from fitu_backend.models import CustomUser
from fitu_backend.serializers import UserSerializer
from models import PhotoRecord
from rest_framework.permissions import IsAuthenticated
import time
import boto3
import csv
import math

class PhotoProfile(APIView):
	def get(self, request, format=None):
		profile = []
		with open('./image_upload/profile.csv', 'r') as csvfile:
			reader = csv.reader(csvfile.read().splitlines())
			for row in reader:
				profile.append(row)

		objs = PhotoRecord.objects.all()
		for index in xrange(len(profile)):
			obj = objs[index]
			obj.brand = profile[index][0]
			obj.height = float(profile[index][1])
			obj.weight = float(profile[index][2])
			obj.shape = profile[index][3]
			obj.gender = profile[index][4]
			obj.buyLink = profile[index][5]
			obj.save(force_update=True)
			index += 1
		return JSONResponse({'status':'finish'})

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

class f_user():
		def __init__(self, height = 181.0, weight = 75.0):
			self.height = height
			self.weight = weight

	    
class PhotoUpload(APIView):
	parser_classes = (MultiPartParser, FormParser,)
	#permission_classes = (IsAuthenticated,)
	
	
	def get_sim(self, user, record):
		BMI_1 = float(user.weight)/((user.height/100.0)**2)
		BMI_2 = float(record.weight)/((record.height/100.0)**2)
		delta = math.fabs(BMI_1 - BMI_2)
		# print delta,BMI_1
		sim = (BMI_1 - delta) * 100/ BMI_1
		return sim

	def get(self, request, format=None):
		ret = []
		user1 = f_user() 
		for record in PhotoRecord.objects.order_by('-photoId').all():
			if math.fabs(record.height - user1.height) > 5.0: 
				continue
			sim = self.get_sim(user1, record)
			
			#print sim
			temp_dict = {
				'brand' : record.brand, 
				'photoUrl' : record.photoUrl, 
				'buylink' : record.buyLink,
				'height' : record.height,
				'weight' : record.weight,
				'sim' : sim
			}
			ret.append(temp_dict)

		ret = sorted(ret, key=lambda k: k['sim'], reverse=True)
		for record in ret:
			record['sim'] = ('%.1f' % record['sim']) + '%'

		return JSONResponse({'data' : ret})

	def post(self, request, format=None):
		curr_photo = request.FILES['photo']
		username = request.POST['username']
		buy_link = request.POST['buylink']
		brand = request.POST['brand']
		loc_x = request.POST['x']
		loc_y = request.POST['y']
		photo_id = str(int(time.time() * 1000)) + '-' + username + '.jpg'
		s3 = boto3.client('s3')
		s3.put_object(Bucket = photo_bucket, 
			Key = photo_id, Body = curr_photo)
		photo_url = base_s3_url + photo_bucket + u'/' + photo_id
		print photo_url

		photo_record = PhotoRecord(username = username, photoId=photo_id, 
			photoUrl = photo_url ,buyLink = buy_link, brand = brand, x = loc_x, y = loc_y)
		photo_record.save()
		return JSONResponse({ 'photoUrl' : photo_url })    	




class UserPhotoList(APIView):
	#permission_classes = (IsAuthenticated,)

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
					'buylink' : record.buyLink,
					'x': record.x,
					'y': record.y
				}
				ret.append(temp_dict)
			return JSONResponse({'data' : ret})




