import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone

class ClassifyNameView(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        
        if not name or name.strip() == "":
            return Response(   
	            {
		            "status": "error",
		            "message": "Missing or empty name parameter"
	            },
	            status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(name, str):
            return Response(   
                {
                    "status": "error",
                    "message": "name must be a string"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
             
        try:
            res = requests.get(
                f"https://api.genderize.io/?name={name}",
                timeout=3
            )

            if res.status_code != 200:
                return Response(
                    {
                        "status": "error",
                        "message": "Upstream API error"
                    },
                    status=status.HTTP_502_BAD_GATEWAY
                )
                
            data = res.json()
            
            gender = data.get("gender")
            probability = data.get("probability")
            count = data.get("count")
            
            if gender is None or count == 0:
                return Response(
                    {
                        "status": "error",
                        "message": "No prediction available for the provided name"
                    },
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

            sample_size = count
            is_confident = (probability >= 0.7 and sample_size >= 100)
            processed_at = (
                datetime.now(timezone.utc)
                .isoformat()
                .replace("+00:00", "Z")
            )
            
            return Response(
                {
                    "status": "success",
                    "data": {
                        "name": name,
                        "gender": gender,
                        "probability": probability,
                        "sample_size": sample_size,
                        "is_confident": is_confident,
                        "processed_at": processed_at
                    }
                },
                status=status.HTTP_200_OK
            )
        except requests.exceptions.RequestException:
            return Response(
                {
                    "status": "error",
                    "message": "Upstream API failure"
                },
                status=status.HTTP_502_BAD_GATEWAY
            )

        except Exception:
            return Response(
                {
                    "status": "error",
                    "message": "Server error"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )