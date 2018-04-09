# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
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

# from django import shortcuts
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django import http

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from horizon import views
from horizon.utils import memoized

from openstack_dashboard import api
from openstack_dashboard.api import base

from openstack_dashboard.dashboards.ceph.monitors \
    import tables as monitors_tables

from openstack_dashboard.dashboards.ceph.monitors \
    import forms as project_forms

LOG = logging.getLogger(__name__)


class MonitorsLine(base.APIDictWrapper):
    def __init__(self, monitor):
        # id should be unique!
        monitor_dict = {'id': monitor['name'],
                        'name': monitor['name'],
                        'rank': monitor['rank'],
                        'addr': monitor['addr'],
                        'state': monitor['state']}
        super(MonitorsLine, self).__init__(monitor_dict)


class IndexView(tables.DataTableView):
    table_class = monitors_tables.MonitorsTable
    template_name = 'ceph/monitors/index.html'
    page_title = _("Ceph Monitors")

    def needs_filter_first(self, table):
        return self._needs_filter_first

    @memoized.memoized_method
    def get_monitors(self):
        mon_status = {}
        try:
            mon_status = api.ceph.get_ceph_mon_status(self.request)
        except Exception:
            msg = _('Unable to retrieve ceph monitor status.')
            exceptions.handle(self.request, msg)
        return mon_status

    def get_data(self):
        filters = self.get_filters()
        self._needs_filter_first = False

        mon_status = self.get_monitors()
        monitors_list = mon_status.get('mon_list',[])
        monitor_lines = []
        for monitor in monitors_list:
            line = MonitorsLine(monitor)
            monitor_lines.append(line)
        return monitor_lines

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        mon_status = self.get_monitors()
        context["fsid"] = mon_status.get('fsid', None)
        context["leader"] = mon_status.get('leader', None)
        context["epoch"] = mon_status.get('epoch', None)
        context["created"] = mon_status.get('created', None)
        context["modified"] = mon_status.get('modified', None)
        return context


class AddMonitorView(forms.ModalFormView):
    form_class = project_forms.AddMonitorForm
    template_name = 'ceph/monitors/add_monitor.html'
    success_url = "horizon:ceph:monitors:index"
    page_title = _("Add Monitor")
    # submit_label = _("submit")

    # def get_context_data(self, **kwargs):
    #     context = super(UpdateView, self).get_context_data(**kwargs)
    #     context['image'] = self.get_object()
    #     args = (self.kwargs['pool_name'],)
    #     context['success_url'] = reverse(self.success_url, args=args)
    #     return context


class ConfigMonitorView(views.HorizonTemplateView):
    template_name = 'ceph/monitors/config_monitor.html'
    page_title = _("Config Monitor")

    def get_host_nic(self):
        host = self.kwargs['monitor_name']
        # mon_public_ip = None
        try:
            info, msg = api.storageinstaller.get_host_facts(host, "mon_info")
            data = info.get('content', None)
            if data:
                nic_info = []
                for i in data:
                    # ip = i.get('ip', None)
                    # if ip and api.storageinstaller.check_monitor_ip(ip):
                    #     LOG.info("=====> check_monitor_ip ok")
                    #     mon_public_ip = ip 
                    #     i['usage'] = 'public'
                    if not i.get('ip', None):
                        i['ip'] = ''
                    if not i.get('mask', None):
                        i['mask'] = ''
                    nic_info.append(i)
                # if mon_public_ip:
                return nic_info
                # LOG.info("!---->publicIp--------------->:")
                # messages.error(request, _("Failed to add monitor %s. it have no public ip address!") % dict(host=mon_info['host'])) 
            raise
        except:
            messages.error(self.request,
                _("Failed to get current nic information on host %(host)s!") % dict(host=self.kwargs['monitor_name']))
            next_url = reverse("horizon:ceph:monitors:index")
            return http.HttpResponseRedirect(next_url)
    def get_context_data(self, **kwargs):
        data = self.get_host_nic()
        context = super(ConfigMonitorView, self).get_context_data(**kwargs)
        context['host'] = self.kwargs['monitor_name']
        context['nic_data'] = data
        return context

def AddMonitor(request,monitor_name):
    mon_info = request.POST
    host = monitor_name
    if mon_info:
        LOG.info("!---->publicIp:%s" % mon_info['publicIp'])
    
    # if mon_info['publicName'] != mon_info['clusterName']:
    #     try:
    #         res = api.storageinstaller.config_physical_nic(host, mon_info['publicName'], mon_info['publicIp'], mon_info['publicMask'], 'public network', False, False)
    #         LOG.info("%s" % res)
    #     except:
    #         messages.error(request,
    #             _("Failed to set nic %s public ip address!") % dict(host=mon_info['publicName'])) 
    #     try:
    #         res = api.storageinstaller.config_physical_nic(host, mon_info['clusterName'], mon_info['clusterIp'], mon_info['clusterMask'], 'cluster network', False, False)
    #         LOG.info("%s" % res)
    #     except:
    #         messages.error(request,
    #             _("Failed to set nic %s cluster ip address!") % dict(host=mon_info['clusterName'])) 
    # else:
    #     try:
    #         LOG.info("---->publicName:%s" % mon_info['publicName'])
    #         LOG.info("---->publicIp:%s" % mon_info['publicIp'])
    #         LOG.info("---->publicMask:%s" % mon_info['publicMask'])
    #         res = api.storageinstaller.config_physical_nic(host, mon_info['publicName'], mon_info['publicIp'], mon_info['publicMask'], 'public and cluster network', False, False)
    #         LOG.info("[djy]:%s" % res)
    #     except:
    #         messages.error(request,
    #             _("Failed to set nic %s public and cluster ip address!") % dict(host=mon_info['publicName'])) 
    try:
        res = api.storageinstaller.add_monitor(host, mon_info['publicIp'])
        LOG.info("%s" % res)
    except:
        messages.error(request,
            _("Failed to add monitor %s !") % dict(host=mon_info['publicIp'])) 
 
    next_url = reverse("horizon:ceph:monitors:index")
    return http.HttpResponseRedirect(next_url)




