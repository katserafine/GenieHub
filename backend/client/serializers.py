from rest_framework import serializers
from .models import  client, project, projectWorker, leadContact

#add validation?

class clientSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields = ('id', 'name', )'street', 'city', 'zipcode', 'state', 'country')



class projectSerializer(serializers.ModelSerializer):
    class Meta:
        model = project
        fields = ('id', 'name')


class leadContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = leadContact
        fields = ('id', 'name', 'phone', 'email')


class projectWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = projectWorker
        fields = ('id', 'pName', 'wName')