"""tip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.static import serve
from django.conf.urls import url
from addUser import views as addviews
from plan1 import views as plan1views
from final import views as finalviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', addviews.index),
    path('add', addviews.add_User),
    path('login', addviews.login),
    path('plan_1', plan1views.plan_1),
    path('plan_2', plan1views.plan_2),
    path('plan_3', plan1views.plan_3),
    path('plan_4', plan1views.plan_4),
    path('final_it', finalviews.show),
    path('final2', finalviews.show2),
    path('final3', finalviews.show3),
    path('prev', finalviews.itin_list),
    path('del', finalviews.delete),
    path('edit', finalviews.edit),
    path('USA', finalviews.USA),
    path('Canada', finalviews.Canada),
    path('India', finalviews.India),
    path('England', finalviews.England),
    path('Spain', finalviews.Spain),
    path('Italy', finalviews.Italy),
    path('France', finalviews.France),
    path('Russia', finalviews.Russia),
    path('Sweden', finalviews.Sweden),
    path('Germany', finalviews.Germany),
    path('Norway', finalviews.Norway),
    path('Switzerland', finalviews.Switzerland),
    path('Netherlands', finalviews.Netherlands),
    path('Belgium', finalviews.Belgium),
    path('Denmark', finalviews.Denmark),
    path('Japan', finalviews.Japan),
    path('China', finalviews.China),
    path('Singapore', finalviews.Singapore),
    path('UAE', finalviews.UAE),
    path('Egypt', finalviews.Egypt),
    path('Morocco', finalviews.Morocco),
    path('Mexico', finalviews.Mexico),
    path('Australia', finalviews.Australia),
    path('NewZealand', finalviews.NZ),
    path('USA_edit', finalviews.USA_edit),
    path('Canada_edit', finalviews.Canada_edit),
    path('India_edit', finalviews.India_edit),
    path('England_edit', finalviews.England_edit),
    path('Spain_edit', finalviews.Spain_edit),
    path('Italy_edit', finalviews.Italy_edit),
    path('France_edit', finalviews.France_edit),
    path('Russia_edit', finalviews.Russia_edit),
    path('Sweden_edit', finalviews.Sweden_edit),
    path('Germany_edit', finalviews.Germany_edit),
    path('Norway_edit', finalviews.Norway_edit),
    path('Switzerland_edit', finalviews.Switzerland_edit),
    path('Netherlands_edit', finalviews.Netherlands_edit),
    path('Belgium_edit', finalviews.Belgium_edit),
    path('Denmark_edit', finalviews.Denmark_edit),
    path('Japan_edit', finalviews.Japan_edit),
    path('China_edit', finalviews.China_edit),
    path('Singapore_edit', finalviews.Singapore_edit),
    path('UAE_edit', finalviews.UAE_edit),
    path('Egypt_edit', finalviews.Egypt_edit),
    path('Morocco_edit', finalviews.Morocco_edit),
    path('Mexico_edit', finalviews.Mexico_edit),
    path('Australia_edit', finalviews.Australia_edit),
    path('NewZealand_edit', finalviews.NZ_edit),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
