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

# from openstack_dashboard.dashboards.ceph.osds \
#     import forms as osds_forms
from openstack_dashboard.dashboards.ceph.osds \
    import tables as osds_tables

from openstack_dashboard.dashboards.ceph.osds \
    import forms as project_forms

LOG = logging.getLogger(__name__)

class OsdsLine(base.APIDictWrapper):
    def __init__(self, osd):
        # id should be unique!
        osd_dict = {'id': osd['id'],
                    'name': osd['name'],
                    'exists': osd['exists'],
                    'type_id': osd['type_id'],
                    'reweight': osd['reweight'],
                    'crush_weight': osd['crush_weight'],
                    'primary_affinity': osd['primary_affinity'],
                    'depth': osd['depth'],
                    'type': osd['type'],
                    'status': osd['status'],
                    'parent': osd.get('parent', None)}
        super(OsdsLine, self).__init__(osd_dict)


class IndexView(tables.DataTableView):
    table_class = osds_tables.OsdsTable
    template_name = 'ceph/osds/index.html'
    page_title = _("Ceph Osds")

    def needs_filter_first(self, table):
        return self._needs_filter_first

    @memoized.memoized_method
    def get_osd_list(self):
        osd_tree = {}
        try:
            osd_tree = api.ceph.get_ceph_osd_tree(self.request)
        except Exception:
            msg = _('Unable to retrieve ceph osd tree.')
            exceptions.handle(self.request, msg)

        if not osd_tree:
            return []

        nodes = osd_tree.get('nodes',[])
        osd_list = [ node for node in nodes if node.get('type') == 'osd' ]
        non_osd_list = [ node for node in nodes if node.get('type') != 'osd' ]

        for osd in osd_list:
            for parent in non_osd_list:
                if osd['id'] in parent.get('children',[]):
                    osd['parent'] = parent

        return osd_list

    def get_data(self):
        filters = self.get_filters()        
        self._needs_filter_first = False

        osd_list = self.get_osd_list()
        osd_lines = []
        for osd in osd_list:
            line = OsdsLine(osd)
            osd_lines.append(line)
        return osd_lines

class AddOsd(forms.ModalFormView):
    form_class = project_forms.AddOsdForm
    template_name = 'ceph/osds/add_osd.html'
    success_url = reverse_lazy("horizon:ceph:osds:index")
    page_title = _("Add Osd")
    # submit_label = _("submit")


