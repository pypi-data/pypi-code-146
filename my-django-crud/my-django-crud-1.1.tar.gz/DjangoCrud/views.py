from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


#Building the views


def create(Model):
    
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



def update(Model):
    
    class CrudSerializer(serializers.ModelSerializer):
        class Meta:
            model = Model
            fields = '__all__'
        

    @api_view(['PUT'])
    def Update(request, pk):
        items = Model.objects.get(id=pk)
        if request.method == 'PUT':

            serializer = CrudSerializer(instance=items, data=request.data, many = False, partial=True)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    return Update



def detail(Model):
    
    class CrudSerializer(serializers.ModelSerializer):
        class Meta:
            model = Model
            fields = '__all__'

    @api_view(['GET'])
    def Detail(request, pk):
        items = Model.objects.get(id=pk)
        serializer = CrudSerializer(items, many=False)
        return Response(serializer.data)

    return Detail




def list(Model):
    
    class CrudSerializer(serializers.ModelSerializer):
        class Meta:
            model = Model
            fields = '__all__'

    @api_view(['GET'])
    def List(request):
        items = Model.objects.all()
        serializer = CrudSerializer(items, many=True)
        return Response(serializer.data)

    return List





def delete(Model):

    @api_view(['DELETE'])
    def Delete(request, pk):
        items = Model.objects.get(id=pk)
        items.delete()
        return Response('item deleted successfuly')

    return Delete




