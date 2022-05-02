from .models import Article, Tag, Scope
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            print(form.cleaned_data)
            if not form.cleaned_data:
                continue
            if form.cleaned_data['main_tag'] == True:
                count += 1
            if form.cleaned_data['DELETE'] == True and form.cleaned_data['main_tag'] == True:
                raise ValidationError('Выбирете другой главный тег (нельзя удалить главный тег)')
        if count > 1:
            raise ValidationError('Не допускается более одного главного тега')
        if count == 0:
            raise ValidationError('Необходимо выбрать главный тег.')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
   inlines = [ScopeInline]


@admin.register(Tag)
class TegAdmin(admin.ModelAdmin):
    pass