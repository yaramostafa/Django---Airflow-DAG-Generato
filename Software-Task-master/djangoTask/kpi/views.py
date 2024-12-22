from django.shortcuts import render
from rest_framework import generics
from .models import KPI, AssetKPI
from .serializers import KPISerializer, AssetKPISerializer
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import KPI
from django.conf import settings
import json

# KPI Endpoints
class KPIListCreateView(generics.ListCreateAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer

# Link Asset to KPI
class AssetKPICreateView(generics.CreateAPIView):
    queryset = AssetKPI.objects.all()
    serializer_class = AssetKPISerializer


class airflowValueView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Accepts kpi_id and value, saves them in a JSON file for further processing.
        """
        try:
            kpi_id = request.data.get('kpi_id')
            value = request.data.get('value')

            if not kpi_id or not value:
                return Response({"detail": "kpi_id and value are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the KPI from the database
            kpi = KPI.objects.filter(id=kpi_id).first()
            if not kpi:
                return Response({"detail": "KPI with the provided ID not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Prepare data to be saved in JSON format
            kpi_data = {
                "kpi_id": kpi_id,
                "value": value
            }
            file_path = os.path.join(settings.BASE_DIR, 'kpi_values.json')

            # Read the existing data from the JSON file if it alr exists
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    existing_data = json.load(file)
            else:
                existing_data = []

            # Append the new kpi_data to the existing data
            existing_data.append(kpi_data)

            # Write the updated data back to the JSON file
            with open(file_path, 'w') as file:
                json.dump(existing_data, file, indent=4)

            return Response({"detail": "KPI value saved successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)