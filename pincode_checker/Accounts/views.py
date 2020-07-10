from rest_framework import generics
from .models import *
from .serializers import *
import json
import requests
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class CreateUser(generics.CreateAPIView):
    def post(self, request):
        request_data = json.loads(request.body)
        name = request_data.get('name', "")
        pincode = request_data.get('pincode', "")
        addobj = UserAddress.objects.filter(pincode=pincode).first()
        if not addobj:

            ret = requests.get(
                f"https://api.postalpincode.in/pincode/{pincode}")
            details = ret.json()
            details = details[0]['PostOffice'][0]
            city = details['Region']
            state = details['State']
            district = details['District']
            division = details['Division']
            dic = {
                'pincode': pincode,
                'city': city,
                'state': state,
                'district': district,
                'division': division,
            }

            serializer = UserAddressSerializer(data=dic)
            if serializer.is_valid():
                serializer.save()
                a = serializer.data
                addressId = a['id']
                dic1 = {'name': name, 'address': addressId}
                serializers = UserSerializer(data=dic1)
                if serializers.is_valid():
                    serializers.save()
                    return Response({"Type": "Success",
                                     "Message": "Added User Successfully",
                                     "Address": serializer.data,
                                     "User": serializers.data},
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response({"Type": "Failed",
                                     "Message": "Cannot add the user",
                                     "Errors": serializers.errors},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Type": "Failed",
                                 "Message": "Cannot add the address for the following pincode",
                                 "Errors": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            dic1 = {'name': name, 'address': addobj.id}
            pincode = addobj.pincode
            city = addobj.city
            state = addobj.state
            district = addobj.district
            division = addobj.division
            address = {
                'pincode': pincode,
                'city': city,
                'state': state,
                'district': district,
                'division': division,
            }
            serializers = UserSerializer(data=dic1)
            if serializers.is_valid():
                serializers.save()
                return Response({"Type": "Success",
                                 "Message": "Added User Successfully to the existing address",
                                 "User": serializers.data,
                                 "Address": address},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"Type": "Failed",
                                 "Message": "Cannot add the user",
                                 "Errors": serializers.errors},
                                status=status.HTTP_400_BAD_REQUEST)


class GetAddress(generics.ListAPIView):
    def get(self, request):
        addressList = UserAddress.objects.all()
        serializer = UserAddressSerializer(addressList, many=True)
        if serializer.data:
            return Response({"type": "success",
                             "Message": "Fetched all the address successfully",
                             "Address": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"Type": "Failed",
                             "Message": "No address to display"},
                            status=status.HTTP_200_OK)


class getUsers(generics.ListAPIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        if serializer.data:
            return Response({"type": "success",
                             "Message": "Fetched all the users successfully",
                             "Address": serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({"Type": "Failed",
                             "Message": "No user to display"},
                            status=status.HTTP_200_OK)


# class CreateAddress(generics.CreateAPIView):
#     def post(self, request):

#         request_data = json.loads(request.body)
#         pincode = request_data.get('pincode')
#         ret = requests.get(f"https://api.postalpincode.in/pincode/{pincode}")
#         details = ret.json()
#         details = details[0]['PostOffice'][0]
#         city = details['Region']
#         state = details['State']
#         district = details['District']
#         division = details['Division']
#         dic = {
#             'pincode': pincode,
#             'city': city,
#             'state': state,
#             'district': district,
#             'division': division,
#         }
#         print(dic)
#         serializer = UserAddressSerializer(data=dic)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"Type": "Success",
#                              "Message": "Added the address Successfully",
#                              "Address": serializer.data}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"Type": "Failed",
#                              "Message": "Cannot add the address for the following pincode",
#                              "Address": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
