#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.ceph.pools import views


VIEW_MOD = 'openstack_dashboard.dashboards.ceph.pools.views'

urlpatterns = patterns(
    VIEW_MOD,
    url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pool_name>[^/]+)/$', views.DetailView.as_view(),
	name='detail'),   
    url(r'^create$', views.CreateView.as_view(), name='create'),
    # url(POOLS % 'detail(\?tab=pool_tabs__overview)?$',
    #     views.DetailView.as_view(),
    #     name='detail'),
    # url(POOLS % 'detail\?tab=pool_tabs__images_tab$',
    #     views.DetailView.as_view(), name='images_tab'),

    # url(POOLS % 'update', views.UpdateView.as_view(), name='update'),
    # url(POOLS % 'subnets/create', subnet_views.CreateView.as_view(),
    #     name='addsubnet'),
    # url(r'^(?P<network_id>[^/]+)/subnets/(?P<subnet_id>[^/]+)/update$',
    #     subnet_views.UpdateView.as_view(), name='editsubnet'),
    # url(r'^(?P<network_id>[^/]+)/ports/(?P<port_id>[^/]+)/update$',
    #     port_views.UpdateView.as_view(), name='editport'),
    # url(r'^subnets/', include(subnet_urls, namespace='subnets')),
    # url(r'^ports/', include(port_urls, namespace='ports')),    
)

