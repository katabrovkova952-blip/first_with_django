from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from books.models import Book

from .serializers import AssistantAskSerializer
from .services import get_ai_answer


class AssistantAskView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = AssistantAskSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        question = serializer.validated_data['question']
        book_id = serializer.validated_data.get('book_id')

        if book_id:
            try:
                book = Book.objects.get(id=book_id)
            except Book.DoesNotExist:
                return Response({'error': 'Книгу з таким id не знайдено'}, status=status.HTTP_404_NOT_FOUND)
            books = [book]
        else:
            books = (
                Book.objects.filter(title__icontains=question) | Book.objects.filter(description__icontains=question)
            ).distinct()[:5]
            if not books:
                books = Book.objects.order_by('?')[:5]

        try:
            answer = get_ai_answer(question, books=books)
        except Exception as e:
            print(f'AI error: {e}', flush=True)
            return Response({'error': 'AI-сервіс тимчасово недоступний'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({'answer': answer}, status=status.HTTP_200_OK)
