import math

from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from markdown import markdown
from simplemde.fields import SimpleMDEField


class Article(models.Model):
    image = models.ImageField(
        _("image"), upload_to='uploads/%Y/%m/%d/',  null=True, blank=True)
    subject = models.CharField(_("subject"), max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("accounts.User", verbose_name=_(
        "user"), on_delete=models.CASCADE)

    message = SimpleMDEField(verbose_name='message')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.pbjects.count()
        pages = count / 10
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 5

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.order_by('-created_at')[:10]

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")


class Comment(models.Model):
    user = models.ForeignKey("accounts.User", verbose_name=_(
        "user"), on_delete=models.CASCADE)
    article = models.ForeignKey("articles.Article", verbose_name=_(
        "article"), on_delete=models.CASCADE)
    comment = models.CharField(_("comment"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(
        'Comment', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='replies')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
