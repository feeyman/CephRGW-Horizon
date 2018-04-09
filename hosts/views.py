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

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from horizon import views
from horizon.utils import memoized

from openstack_dashboard import api
from openstack_dashboard.api import base

from openstack_dashboard.dashboards.ceph.hosts \
    import forms as hosts_forms
from openstack_dashboard.dashboards.ceph.hosts \
    import tables as hosts_tables


LOG = logging.getLogger(__name__)

class HostsLine(base.APIDictWrapper):
    def __init__(self, host):
        # id should be unique!
        host_dict = {'id': host['name'],
                     'name': host['name'],}
        super(HostsLine, self).__init__(host_dict)


class IndexView(tables.DataTableView):
    table_class = hosts_tables.HostsTable
    template_name = 'ceph/hosts/index.html'
    page_title = _("Ceph Hosts")

    def needs_filter_first(self, table):
        return self._needs_filter_first

    def get_data(self):
        filters = self.get_filters()

        self._needs_filter_first = False

        hosts_list = []
        try:
            hosts_list = api.ceph.get_ceph_hosts(self.request)
        except Exception:
            msg = _('Failed to get ceph hosts list!')
            exceptions.handle(self.request, msg)

        host_lines = []
        for host in hosts_list:
            line = HostsLine(host)
            host_lines.append(line)
        return host_lines


