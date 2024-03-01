from django.contrib import admin
from .models import News, Tours, Booking,User
from django.utils.html import mark_safe
from django import forms
from django.urls import path
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.template.response import TemplateResponse
from django.db.models import Count, Sum,F,DecimalField
from django.forms import DateInput
from django.db.models.functions import ExtractYear,ExtractMonth
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class AdminSite(admin.AdminSite):
    site_header = "abcc"

    class MyCustomForm(forms.Form):
        # Define your form fields here
        # Example:
        start_date = forms.DateField(
            widget=DateInput(attrs={'type': 'date'}),
            label='Start Date'
        )
        end_date = forms.DateField(
            widget=DateInput(attrs={'type': 'date'}),
            label='End Date'
        )


    form = MyCustomForm

    def get_urls(self):
        #
        return [
            path('tour-stats/', self.tour_stats)
        ] + super().get_urls()

    def tour_stats(self, request):
        yearly_revenue = None
        if request.method == 'POST':
            form = self.MyCustomForm(request.POST)
            if form.is_valid():
                # Process the form data here
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                # Perform operations based on form data
                yearly_revenue = Tours.objects.filter(booking__active=True,booking__create_date__range=[start_date, end_date]).annotate(year=ExtractYear('booking__create_date')).values('name_tour', 'year').annotate(total_revenue=Sum('booking__total_price')).order_by('total_revenue')
                # month_revenue = Tours.objects.filter(booking__active=True,booking__create_date__range=[start_date, end_date]).annotate(
                #     month=ExtractMonth('booking__create_date')).values('name_tour', 'month').annotate(
                #     total_revenue=Sum('booking__total_price')).order_by('total_revenue')
        else:
            form = self.MyCustomForm()

        tour_counts = Tours.objects.values('name_tour').annotate(tour_count=Count('name_tour'))
        # booking_counts = Tours.objects.annotate(count = Sum('booking__tour')).values("name_tour","count").order_by("count")
        # b = Tours.objects.filter(booking__active=True).annotate(total_revenue=Sum('booking__total_price')).values("name_tour","total_revenue")

        return TemplateResponse(request, 'admin/tour-stats.html', {
            'tour_counts': tour_counts,
            # 'b': b,
            'form': form,
            'yearly_revenue':yearly_revenue,
            # 'month_revenue':month_revenue
        })


admin_site = AdminSite("mycourse")

class DateForm(forms.Form):
    from_date = forms.DateField
    to_date = forms.DateField
class ToursAdmin(admin.ModelAdmin):
    list_display = ["id", "name_tour", "create_date"]
    search_fields = ["name_tour", "create_date"]
    readonly_fields = ['avatar']

    def avatar(self, tours):
        return mark_safe("<img src='/static/{img_url}' alt='{alt}' width='120px'/> ".format(img_url=tours.image.name,
                                                                                            alt=tours.name_tour))


class UserInline(admin.StackedInline):
    model = User
    pk_name = 'user'


# class UserAdmin(admin.ModelAdmin):
#     inlines = (UserInline,)
#     # list_display = ["user","create_date"]
#     search_fields = ["username","create_date"]

class StaffAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user"]
class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = News
        fields = '__all__'
class UserAdmin(admin.ModelAdmin):
    list_display = ["username","email","password"]
    search_fields = ["username", "create_date"]

    def save_model(self, request, obj, form, change):
        # Nếu là việc tạo mới user hoặc mật khẩu được thay đổi, hãy băm mật khẩu
        if not change or form.cleaned_data["password"]:
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "content", "create_date"]
    search_fields = ["name","content","create_date"]
    form = NewsForm
# admin.site.unregister(User)
admin_site.register(User,UserAdmin)

# admin_site.register(Staff,StaffAdmin)
admin_site.register(News, NewsAdmin)
admin_site.register(Tours, ToursAdmin)
