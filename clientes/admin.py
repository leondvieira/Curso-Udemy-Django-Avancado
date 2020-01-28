from django.contrib import admin

from .models import Person, Documento


class PersonAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Dados Pessoas', {'fields': ('first_name', 'last_name', 'doc')}),
        ('Dados Complementares', {
            'classes': ('collapse',),
            'fields': ('age', 'salary', 'photo', 'bio')})
    )
    # fields = [('doc', 'first_name', 'last_name'), ('age', 'salary'), 'bio', 'photo']
    # exclude = ['bio']
    list_display = ['first_name', 'doc', 'last_name', 'age', 'salary', 'bio', 'tem_foto']
    list_filter = ('age', 'salary')
    search_fields = ('id', 'first_name')
    autocomplete_fields = ('doc',)

    def tem_foto(self, object):
        if object.photo:
            return 'Sim'
        else:
            return 'Não'

    tem_foto.short_description = 'Possui Foto'


class NomeProdutoListFilter(admin.SimpleListFilter):
    title = ('Filtrar pelo Nome',)

    parameter_name = 'descricao'

    def lookups(self, request, model_admin):

        return (
            ('az', ('De A a Z')),
            ('za', ('De Z a A')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'az':
            return queryset.filter().order_by('descricao')
        if self.value() == 'za':
            return queryset.filter().order_by('descricao').reverse()


class DocumentoAdmin(admin.ModelAdmin):
    search_fields = ('num_doc',)


admin.site.register(Person, PersonAdmin)
admin.site.register(Documento, DocumentoAdmin)

