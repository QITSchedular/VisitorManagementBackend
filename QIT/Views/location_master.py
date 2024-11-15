from rest_framework.views import APIView 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from QIT.models import QitCompany, QitUsermaster, QitVisitorinout,QitLocation
from QIT.serializers import LocationSerializer
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from QIT.utils.APICode import APICodeClass

@csrf_exempt
@api_view(["POST"])
def SaveLocation(request):
    try:
        reqData = request.data
        cid = reqData["company_id"]
        cmpEntry = QitCompany.objects.filter(transid=cid).first()
        if not cmpEntry:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Location_Add.value
            })
        
        loc_name = reqData["loc_name"]
        # Check if the location with the same name already exists for the given company (case-insensitive)
        existing_loc = QitLocation.objects.filter(cmptransid=cmpEntry, locationname__iexact=loc_name).first()
        if existing_loc:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Location with the same name already exists",
                'APICode':APICodeClass.Location_Add.value
            },status=400)

        print(loc_name)
        res = QitLocation.objects.create(locationname=loc_name, cmptransid=cmpEntry)
        if res:
            return Response({
                'is_save': "Y",
                'Status': 200,
                'StatusMsg': "Location data saved",
                'APICode':APICodeClass.Location_Add.value,
                "locId": res.transid
            })
        else:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Error while saving data",
                'APICode':APICodeClass.Location_Add.value
            },status=400)
    except Exception as e:
        return Response({
            'is_save': "N",
            'Status': 400,
            'StatusMsg': str(e),
            'APICode':APICodeClass.Location_Add.value
        },status=400)


@csrf_exempt
@api_view(["GET"])
def GetAllLocationByCId(request,cid):
    try:
        if not cid:
            locData = LocationSerializer(QitLocation.objects.all(),many=True)
            return Response({
                'Data':locData.data,
                'APICode':APICodeClass.Location_Get.value
            })
        else:
            cmpEntry = QitCompany.objects.filter(transid=cid).first()
            if not cmpEntry:
                raise NotFound(detail="Company data not found",code=400)
            serializedData = QitLocation.objects.filter(cmptransid=cmpEntry)
            if not serializedData:
                raise NotFound(detail="Data not found",code=400)
            res = LocationSerializer(serializedData,many=True)
            return Response({
                'Data':res.data,
                'APICode':APICodeClass.Location_Get.value
            })
    except NotFound as e:
        return Response({'Status': 400, 'StatusMsg': str(e)}, status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e,
            'APICode':APICodeClass.Location_Get.value
        },status=400)
    

@csrf_exempt
@api_view(["PUT"])
def EditLocation(request):
    try:
        reqData = request.data
        if not reqData.get("transid"):
            raise NotFound(detail="transid is required",code=400)
        if not reqData.get("locationname"):
            raise NotFound(detail="location name is required",code=400)
        if not reqData.get("cmptransid"):
            raise NotFound(detail="cmptransid is required",code=400)
        
        cmpEntry = QitCompany.objects.filter(transid=reqData["cmptransid"]).first()
        if not cmpEntry:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Location_Edit.value
            })
        
        # Check if the location with the same name already exists for the given company (case-insensitive)
        existing_loc = QitLocation.objects.filter(cmptransid=reqData["cmptransid"], locationname__iexact=reqData["locationname"]).first()
        if existing_loc:
            return Response({
                'is_save': "N",
                'Status': 400,
                'StatusMsg': "Location with the same name already exists",
                'APICode':APICodeClass.Location_Edit.value
            },status=400)
        
        locData = QitLocation.objects.filter(transid = reqData["transid"],cmptransid=reqData["cmptransid"]).first()
        if not locData:
            raise NotFound(detail="Location data not found",code=400)
        serialized_data = LocationSerializer(locData, data=reqData, partial=True)
        print(serialized_data)
        if serialized_data.is_valid():
            serialized_data.save()
        return Response({
            'is_save':"Y",
            'Status':200,
            'StatusMsg':"Location data updated",
            'APICode':APICodeClass.Location_Edit.value
        })
    except NotFound as e:
        return Response({
            'Status': 400, 
            'StatusMsg': str(e),
            'APICode':APICodeClass.Location_Edit.value
        }, status=400)
    except Exception as e:
        return Response({
            'Status':400,
            'StatusMsg':e,
            'APICode':APICodeClass.Location_Edit.value
        },status=400)


@csrf_exempt
@api_view(["DELETE"])
def DeleteLocation(request, did, cid):
    try:
        if not did:
            raise NotFound(detail="Location Id is required")
        if not cid:
            raise NotFound(detail="Company Id is required")

        try:
            cmpEntry = QitCompany.objects.get(transid=cid)
        except QitCompany.DoesNotExist:
            return Response({
                'Status': 400, 
                'StatusMsg': "Company not found",
                'APICode':APICodeClass.Location_Delete.value
            }, status=400)

        try:
            locEntry = QitLocation.objects.get(transid=did, cmptransid=cmpEntry)
        except QitLocation.DoesNotExist:
            return Response({
                'Status': 400, 
                'StatusMsg': "Location not found",
                'APICode':APICodeClass.Location_Delete.value
            }, status=400)

        try:
            locEntry.delete()
            return Response({
                'Status': 200,
                'StatusMsg': "Location deleted",
                'APICode':APICodeClass.Location_Delete.value
            }, status=200)
        except IntegrityError as e:
            # Check if the error is due to foreign key constraint violation
            if 'foreign key constraint fails'.upper() in str(e).upper():
                return Response({
                    'Status': 400,
                    'StatusMsg': "Location already in use",
                    'APICode':APICodeClass.Location_Delete.value
                }, status=400)
            else:
                return Response({
                    'Status': 400,
                    'StatusMsg': str(e),
                    'APICode':APICodeClass.Location_Delete.value
                }, status=400)
    except NotFound as e:
        return Response({
            'Status': 400, 
            'StatusMsg': str(e),
            'APICode':APICodeClass.Location_Delete.value
        }, status=400)
    except Exception as e:
        return Response({
            'Status': 400,
            'StatusMsg': str(e),
            'APICode':APICodeClass.Location_Delete.value
        }, status=400)
