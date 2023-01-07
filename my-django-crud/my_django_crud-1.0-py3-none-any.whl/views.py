from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


#Building the views


def crudcreate(Model):
    
    class CrudSerializer(serializers.ModelSerializer):
        class Meta:
            model = Model
            fields = '__all__'
        

    @api_view(['POST'])
    def Create(request):

            if request.method == "POST":

                serializer = CrudSerializer(data=request.data)
                
            if serializer.is_valid():
                    
                serializer.save()

            return Response(serializer.data)
    return Create




