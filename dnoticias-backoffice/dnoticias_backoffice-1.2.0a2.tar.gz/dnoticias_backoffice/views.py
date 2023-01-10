from django.views.generic import CreateView, FormView, UpdateView, View
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q

from dnoticias_utils.views import GenericDeleteView, Select2View
from dnoticias_tables.columns import ColumnMethod, Column
from dnoticias_tables.datatable import Datatable
from flags.models import FlagState

from dnoticias_backoffice.forms import FlagStateForm, PermissionForm, GroupForm
from dnoticias_backoffice.serializers import PermissionSerializer

User = get_user_model()


class PermissionsSelect2View(Select2View):
    SEARCH_PARAMS = ["name", "codename"]
    SEARCH_TYPE = "icontains"
    ORDER_BY_PARAMS = ["codename"]
    MODEL = Permission
    MODEL_VERBOSE_NAMES = {
        Permission.__name__ : _("Permissões"),
    }


class UsersSelect2View(Select2View):
    SEARCH_PARAMS = ["email"]
    SEARCH_TYPE = "icontains"
    ORDER_BY_PARAMS = ["email"]
    MODEL = User
    MODEL_VERBOSE_NAMES = {
        User.__name__ : _("Utilizador"),
    }


@method_decorator(permission_required("flags.view_flagstate", raise_exception=True), name="dispatch")
class FlagStateListView(Datatable):
    id = Column(visible=False, searchable=True, url_name="perk-detail")
    name = Column(name="Nome", orderable=True, width=300, searchable=True)
    condition = Column(
        name="Condição",
        orderable=True,
        width=200,
        searchable=True,
        align="center",
    )
    value = Column(
        name="Valor necessãrio",
        orderable=True,
        width=200,
        searchable=True,
        align="center",
    )
    required = ColumnMethod(
        name="Obrigatório",
        orderable=True,
        width=100,
        searchable=True,
        align="center",
    )

    model = FlagState
    table_id = "flag-state"
    table_name = "Ativação de funcionalidades"

    class Meta:
        sortable = True

        create_url_name = "flag-state-create-view"
        update_url_name = "flag-state-wildcard-view"
        delete_url_name = "flag-state-delete-view"

    def get_required(self, obj: FlagState):
        return "Sim" if obj.required else "Não"


@method_decorator(permission_required("flags.add_flagstate", raise_exception=True), name="dispatch")
class FlagStateCreateView(CreateView):
    template_name = "backoffice/flags/form.html"
    model = FlagState
    queryset = FlagState.objects.all()
    form_class = FlagStateForm
    success_url = reverse_lazy("flag-state-list-view")

    def form_valid(self, form):
        messages.success(self.request, _("A regra foi criada correctamente."), fail_silently=True)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, _("Nao foi possível criar a regra."), fail_silently=True)
        return super().form_invalid(form)


@method_decorator(permission_required("flags.change_flagstate", raise_exception=True), name="dispatch")
class FlagStateEditView(UpdateView):
    template_name = 'backoffice/flags/form.html'
    model = FlagState
    queryset = FlagState.objects.all()
    form_class = FlagStateForm
    success_url = reverse_lazy("flag-state-list-view")

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        pk = self.kwargs.get("pk")
        context["instance"] = FlagState.objects.get(pk=pk)
        return context

    def form_valid(self, form):
        messages.success(self.request, _("A regra foi atualizada correctamente."), fail_silently=True)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, _("Nao foi possível atualizar a regra."), fail_silently=True)
        return super().form_invalid(form)


@method_decorator(permission_required("flags.delete_flagstate", raise_exception=True), name="dispatch")
class FlagStateDeleteView(GenericDeleteView):
    model = FlagState

    def add_message(self, request):
        messages.info(request, _("Foi eliminada a regra de funcionalidade."), fail_silently=True)


class PermissionsView(FormView):
    template_name = 'backoffice/permissions/form.html'
    form_class = PermissionForm
    success_url = reverse_lazy("permissions")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Os grupos e as permissões do utilizador foram atualizadas com sucesso."), fail_silently=True)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, _("Nao foi possível atualizar os grupos e as permissões."), fail_silently=True)
        return super().form_invalid(form)


class UserPermissionsView(View):
    def get(self, request, *args, **kwargs):
        from django.db import connection
        user_pk = request.GET.get("pk", None)

        groups_pks = request.GET.getlist("groups[]", [])
        groups = Group.objects.filter(pk__in=groups_pks)

        try:
            user = User.objects.get(pk=user_pk)
        except Exception:
            user = None

        queryset = Permission.objects.filter(
            Q(group__id__in=groups_pks) | Q(user=user)
        ).prefetch_related("content_type")

        serializer = PermissionSerializer(
            queryset,
            many=True
        )

        return JsonResponse(
            serializer.data,
            safe=False
        )


class GroupPermissionsView(View):
    def get(self, request, *args, **kwargs):
        from django.db import connection
        group_pk = request.GET.get("pk", None)

        try:
            group = Group.objects.get(pk=group_pk)
        except Group.DoesNotExist:
            group = None

        queryset = Permission.objects.filter(group=group).prefetch_related("content_type")
        print(queryset.query)
        print(connection.queries)
        serializer = PermissionSerializer(
            queryset,
            many=True
        )

        return JsonResponse(serializer.data, safe=False)


class UserGroupsView(View):
    def get(self, request, *args, **kwargs):
        user_pk = request.GET.get("pk", None)

        try:
            user = User.objects.get(pk=user_pk)
        except Exception:
            user = None

        groups = Group.objects.all()
        user_groups_ids = set(user.groups.values_list("id", flat=True)) if user else []

        context = []
        for group in groups:
            context.append({
                "pk" : group.pk,
                "name" : group.name,
                "in_group" : group.pk in user_groups_ids
            })

        return JsonResponse(context, safe=False)


@method_decorator(permission_required("auth.view_group", raise_exception=True), name="dispatch")
class GroupListView(Datatable):
    name = Column(name="Nome", orderable=True, width=300, searchable=True)

    model = Group
    table_id = "flag-state"
    table_name = "Ativação de funcionalidades"

    class Meta:
        sortable = True

        create_url_name = "group-create-view"
        update_url_name = "group-detail-view"
        delete_url_name = "group-delete-view"


@method_decorator(permission_required("auth.add_group", raise_exception=True), name="dispatch")
class GroupCreateView(CreateView):
    template_name = "backoffice/groups/form.html"
    model = Group
    queryset = Group.objects.all()
    form_class = GroupForm
    success_url = reverse_lazy("group-list-view")

    def form_valid(self, form):
        messages.success(self.request, _("A regra foi criada correctamente."), fail_silently=True)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _("Nao foi possível criar a regra."), fail_silently=True)
        return super().form_invalid(form)


@method_decorator(permission_required("auth.change_group", raise_exception=True), name="dispatch")
class GroupEditView(UpdateView):
    template_name = 'backoffice/groups/form.html'
    model = Group
    queryset = Group.objects.all()
    form_class = GroupForm
    success_url = reverse_lazy("group-list-view")

    def get_form_kwargs(self):
        context = super().get_form_kwargs()
        pk = self.kwargs.get("pk")
        context["instance"] = Group.objects.get(pk=pk)
        return context

    def form_valid(self, form):
        messages.success(self.request, _("O grupo foi atualizado correctamente."), fail_silently=True)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _("Nao foi possível atualizar o grupo."), fail_silently=True)
        return super().form_invalid(form)


@method_decorator(permission_required("auth.delete_group", raise_exception=True), name="dispatch")
class GroupDeleteView(GenericDeleteView):
    model = Group

    def add_message(self, request):
        messages.info(request, _("O grupo foi eliminado com sucesso"), fail_silently=True)
