from rest_framework import generics, serializers

class AccountView(generics.CreateAPIView):

    def perform_create(self, serializer):
        pass
        # serializer.save(username="", email="", password="")