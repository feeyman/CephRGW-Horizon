# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 OpenStack Foundation
# Copyright 2012 Nebula, Inc.
#
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

import logging

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.datastructures import SortedDict

from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse

from horizon import exceptions
from horizon import views
from horizon import messages
from horizon.utils import memoized
from openstack_dashboard import api

LOG = logging.getLogger(__name__)


class IndexView(views.HorizonTemplateView):
    template_name = 'ceph/RGWBuckets/index.html'
    page_title = _("RGWBuckets")

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['buckets'] = api.ceph.get_cephrgw_buckets()
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     context['users'] = api.ceph.get_cephrgw_user()
    #     return context


def ceph_health_status(request):
    value = ''
    try:
    	value = api.ceph.get_ceph_health(request)
        # LOG.info("ceph_health_status = %s" % value)
    except:
        # msg = _('Unable to get cluster health.')
        # messages.warning(request,msg)
        pass
    # response health_status
    # LOG.info("ceph_health_status = %s" % value)
    return JsonResponse(value, safe=False)


def ceph_warning_num(request):
    value = ''
    try:
    	value = api.ceph.get_ceph_warning_num(request)
    except:
        # msg = _('Unable to get warning num.')
        # messages.warning(request,msg)
        pass
    # response ceph_warning_num
    return JsonResponse(value, safe=False)
    

def ceph_disk_status(request):
    value = ''
    try:
    	value = api.ceph.get_ceph_disk_status(request)
    except:
        # msg = _('Unable to get disk status.')
        # messages.warning(request,msg)
        pass
    # response ceph_disk_status
    return JsonResponse(value, safe=False)


def ceph_pg_status(request):
    value = ''
    try:
    	value = api.ceph.get_ceph_pg_status(request)
    except:
        # msg = _('Unable to get pg status.')
        # messages.warning(request,msg)
        pass
    # response ceph_pg_status
    return JsonResponse(value, safe=False)


def ceph_pool_status(request):
    value = ''
    try:
    	value = api.ceph.get_ceph_pool_status(request)
    except:
        # msg = _('Unable to get pool status.')
        # messages.warning(request,msg)
        pass
    # response ceph_pool_status
    return JsonResponse(value, safe=False)


def ceph_host_status(request):
    value = ''
    try:
    	value = api.ceph.get_ceph_host_status(request)
    except:
        # msg = _('Unable to get host health.')
        # messages.warning(request,msg)
        pass
    # response ceph_host_status
    return JsonResponse(value, safe=False)


def ceph_mon_status(request):
    value = ''
    try:
        value = api.ceph.get_ceph_mon_status(request)
        # LOG.info("ceph_mon_status, value = %s" % value)
    except:
        # msg = _('Unable to get mon status.')
        # messages.warning(request,msg)
        pass
    # response ceph_mon_status
    return JsonResponse(value, safe=False)


def ceph_osd_status(request):
    value = ''
    try:
        value = api.ceph.get_ceph_osd_status(request)
    except:
        # msg = _('Unable to get osd status.')
        # messages.warning(request,msg)
        pass
    # response health_status
    return JsonResponse(value, safe=False)


def ceph_mds_status(request):
    value = ''
    try:
        value = api.ceph.get_ceph_mds_status(request)
    except:
        # msg = _('Unable to get mds status.')
        # messages.warning(request,msg)
        pass
    # response health_status
    return JsonResponse(value, safe=False)


def ceph_iops(request):
    ceph_iops = [{"write_net": [], "time": [], "read_net": [], "read_iops": [], "write_iops": []}]
    try:
        ceph_iops = api.zabbix.ceph_iops()
        #LOG.info("ceph_iops = %s" % ceph_iops)
    except:
        # msg = _('Unable to retrieve data from zabbix.')
        # messages.warning(request,msg)
        pass
    return JsonResponse(ceph_iops, safe=False)
	
