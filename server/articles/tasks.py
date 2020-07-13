from .models import Comment

from server.celery import app


@app.task(name="save_comment")
def save_comment(comment, article_id, user_id, parent_id=None):
    if parent_id:
        try:
            parent_obj = Comment.objects.get(id=parent_id)
        except Comment.DoesNotExist:
            parent_obj = None
        if parent_obj:
            Comment.objects.create(
                article_id=article_id,
                user_id=user_id, comment=comment, reply=parent_obj)
    else:
        Comment.objects.create(article_id=article_id,
                               comment=comment, user_id=user_id)
    return "Saved"
