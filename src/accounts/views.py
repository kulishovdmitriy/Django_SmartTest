from django.views.generic import ListView

from accounts.models import User


class UserListView(ListView):

    model = User
    template_name = "user_list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        params = {
            "first_name": "__icontains",
            "last_name": "__icontains",
            "email": "__icontains",

            "birthdate": "",
        }
        for param, lookup in params.items():
            value = request.GET.get(param)
            if value:
                if lookup:
                    qs = qs.filter(**{f"{param}{lookup}": value})
                else:
                    qs = qs.filter(**{param: value})

        return qs
