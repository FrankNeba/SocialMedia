from django.db import models
from authenticate.models import User

# Create your models here.
class Image(models.Model):
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=200)
    image = models.ImageField(upload_to='images/posts', null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    like = models.PositiveIntegerField(default = 0)
    comment = models.PositiveBigIntegerField(default=0)
    images = models.ManyToManyField(Image)
    video = models.FileField(upload_to='videos', null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        name = f'{self.user.username}: {self.text[:20]}'
        # pass
        return name
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} : {self.post.text[:20]}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    replies = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} : {self.text[:20]}'
    
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_user')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply')
    text = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user.username} replied to {self.comment.text[:10]} by {self.comment.user.username} with {self.text[:20]}'


class CommentLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentlike')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likecomments')
    created = models.DateTimeField(auto_now_add=True)

    class META:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user} liked {self.comment.text[:20]}'

