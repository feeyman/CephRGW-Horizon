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

from openstack_dashboard.dashboards.ceph.overview import views

VIEW_MOD = 'openstack_dashboard.dashboards.ceph.overview.views'

urlpatterns = patterns(
    VIEW_MOD,
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^ceph_health_status/$', views.ceph_health_status, name='ceph_health_status'),
    url(r'^ceph_warning_num/$', views.ceph_warning_num, name='ceph_warning_num'),
    url(r'^ceph_disk_status/$', views.ceph_disk_status, name='ceph_disk_status'),
    url(r'^ceph_pg_status/$', views.ceph_pg_status, name='ceph_pg_status'),
    url(r'^ceph_pool_status/$', views.ceph_pool_status, name='ceph_pool_status'),
    url(r'^ceph_host_status/$', views.ceph_host_status, name='ceph_host_status'),
    url(r'^ceph_mon_status/$', views.ceph_mon_status, name='ceph_mon_status'),
    url(r'^ceph_osd_status/$', views.ceph_osd_status, name='ceph_osd_status'),
    url(r'^ceph_mds_status/$', views.ceph_mds_status, name='ceph_mds_status'),
    url(r'^ceph_iops/$', views.ceph_iops, name='ceph_iops'),
)

