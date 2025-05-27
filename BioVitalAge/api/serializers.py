""" 
    Serializer for API.
"""

from rest_framework import serializers
from BioVitalAge.models import TabellaPazienti

class PazienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabellaPazienti
    
        fields = [
            'id',
            'dottore',
            'codice_fiscale',
            'name',
            'surname',
            'dob',
            'gender',
            'chronological_age',
            'lastVisit',
            'upcomingVisit',
        ]