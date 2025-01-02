from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from notifications.models import Notification
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer


# @api_view(['POST'])
# def like_post(request, post_id):
#     post = Post.objects.get(id=post_id)
#     Like.objects.create(post=post, user=request.user)
#     return Response({'status': 'liked'}, status=200)

# @api_view(['POST'])
# def unlike_post(request, post_id):
#     post = Post.objects.get(id=post_id)
#     like = Like.objects.get(post=post, user=request.user)
#     like.delete()
#     return Response({'status': 'unliked'}, status=200)

@api_view(['POST'])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        # Create a notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )
        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Post already liked"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()

    if like:
        like.delete()
        return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)
    return Response({"message": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

