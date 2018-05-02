from rest_framework import serializers
from workouts.models import Workout, Exercise, Set

class SetSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Set
        fields = ('id', 'reps', 'weight')

class ExerciseSerializer(serializers.ModelSerializer):

    sets = SetSerializer(many=True, read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'sets')

class WorkoutSerializer(serializers.ModelSerializer):

    exercises = ExerciseSerializer(many=True, required=False, read_only=True)
    account = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Workout
        fields = ('id', 'date', 'notes', 'account', 'exercises')