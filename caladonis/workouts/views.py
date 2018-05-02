from workouts.models import Workout, Exercise, Set
from workouts.serializers import WorkoutSerializer, ExerciseSerializer, SetSerializer
from rest_framework import serializers, generics, status

from rest_framework.response import Response
import json
import logging

class WorkoutList(generics.ListAPIView):

    serializer_class = WorkoutSerializer

    def get_queryset(self):

        user = self.request.user

        return Workout.objects.filter(account=user)

class WorkoutCreate(generics.CreateAPIView):

    serializer_class = WorkoutSerializer

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

class WorkoutEdit(generics.RetrieveUpdateDestroyAPIView):

    logger = logging.getLogger('workouts.views')
    serializer_class = WorkoutSerializer

    def get_queryset(self):

        user = self.request.user

        return Workout.objects.filter(account=user)

    def update(self, request, *args, **kwargs):
        body = json.loads(request.body)
        exercise_data = body.pop('exercises')

        workout = self.get_queryset().get(pk=kwargs["pk"])

        workout_serializer = WorkoutSerializer(workout, data=body)

        exercises_to_be_deleted = Exercise.objects.filter(workout=workout)

        print(exercises_to_be_deleted)

        for exercise in exercise_data:
            set_data = exercise.pop('sets', None)
            exercise_id = exercise.pop('id', None)
            if exercise_id:
                try:
                    exercise_instance = Exercise.objects.get(pk=exercise_id, workout=workout)
                    exercise_serializer = ExerciseSerializer(exercise_instance, data=exercise)
                    if exercise_serializer.is_valid():
                        exercise_serializer.save()
                        exercises_to_be_deleted = exercises_to_be_deleted.exclude(pk=exercise_id)
                        print(exercises_to_be_deleted)
                    else:
                        self.logger.warning('invalid exercise')
                except ValueError:
                    exercise_instance = Exercise.objects.create(workout=workout, name=exercise.get('name', 'New Exercise'))
                    self.logger.info("saving...", exercise_instance)
                    exercises_to_be_deleted = exercises_to_be_deleted.exclude(pk=exercise_instance.id)
            sets_to_be_deleted = Set.objects.filter(exercise=exercise_instance)
            for set in set_data:
                set_id = set.pop('id', None)
                if set_id:
                    try:
                        set_instance = Set.objects.get(pk=set_id, exercise=exercise_instance)
                        set_serializer = SetSerializer(set_instance, data=set)

                        if set_serializer.is_valid():
                            set_serializer.save()
                            sets_to_be_deleted = sets_to_be_deleted.exclude(pk=set_id)
                        else:
                            print('set not valid')
                    except ValueError:
                        set_instance = Set.objects.create(exercise=exercise_instance, reps=set.get('reps', 0), weight=set.get('weight', 0))
                        sets_to_be_deleted = sets_to_be_deleted.exclude(pk=set_instance.id)
            sets_to_be_deleted.delete()
        print(exercises_to_be_deleted)
        exercises_to_be_deleted.delete()

        print(workout_serializer)
        if workout_serializer.is_valid():
            workout_serializer.save()
        else:
            self.logger.warning('invalid workout')

        return Response(workout_serializer.data, status=status.HTTP_202_ACCEPTED)
