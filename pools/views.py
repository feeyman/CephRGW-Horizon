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
from horizon import tabs
from horizon import views
from horizon.utils import memoized

from openstack_dashboard import api
from openstack_dashboard.api import base

# from openstack_dashboard.dashboards.ceph.pools \
#     import forms as pools_forms
from openstack_dashboard.dashboards.ceph.pools \
    import tabs as pool_tables
from openstack_dashboard.dashboards.ceph.pools \
    import tables as project_tables
from openstack_dashboard.dashboards.ceph.pools \
    import forms as project_forms

LOG = logging.getLogger(__name__)

class PoolsLine(base.APIDictWrapper):
    def __init__(self, pool):
        # id should be unique!
        pool_dict = {'id': pool['pool_name'],
                     'name': pool['pool_name'],
                     'auid': pool['auid'],
                     'type': pool['type'],
                     'size': pool['size'],
                     'min_size': pool['min_size'],
                     'crush_ruleset': pool['crush_ruleset'],
                     'pg_num': pool['pg_num'],
                     'pg_placement_num': pool['pg_placement_num'],
                     'quota_max_bytes': pool['quota_max_bytes'],
                     'quota_max_objects': pool['quota_max_objects'],
                     'expected_num_objects': pool['expected_num_objects'],
                     'flags_names': pool['flags_names'],}
        super(PoolsLine, self).__init__(pool_dict)

class IndexView(tables.DataTableView):
    table_class = project_tables.PoolsTable
    template_name = 'ceph/pools/index.html'
    page_title = _("Ceph Pools")

    def needs_filter_first(self, table):
        return self._needs_filter_first

    def get_data(self):
        filters = self.get_filters()

        self._needs_filter_first = False

        pools_list = []
        try:
            pools_list = api.ceph.get_ceph_pools(self.request)
        except Exception:
            msg = _('Failed to get ceph pools list!')
            exceptions.handle(self.request, msg)

        pool_lines = []
        for pool in pools_list:
            line = PoolsLine(pool)
            pool_lines.append(line)
        return pool_lines


class DetailView(tabs.TabbedTableView):
    tab_group_class = pool_tables.PoolDetailsTabs
    template_name = 'horizon/common/_detail.html'
    page_title = '{{ pool.name | default:pool.id }}'

    @staticmethod
    def get_redirect_url():
        return reverse('horizon:ceph:pools:index')

    @memoized.memoized_method
    def _get_data(self):
        pool_name = self.kwargs['pool_name']
        pools_list = []
        try:
            pools_list = api.ceph.get_ceph_pools(self.request)
        except Exception:
            msg = _('Failed to get ceph pools list!')
            exceptions.handle(self.request, msg)

        for pool in pools_list:
            if pool['pool_name'] == pool_name:
                line = PoolsLine(pool)
                break
        return line

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        pool = self._get_data()
        context["pool"] = pool
        table = project_tables.PoolsTable(self.request)
        context["url"] = self.get_redirect_url()
        context["actions"] = table.render_row_actions(pool)
        # pool.pg_num_label = 'tables.pg_num'
        # pool.name = 'tables.name'
        # pool.id = '1912'
        # pool.pg_num_label = (
        #     filters.get_display_label(choices, pool.pg_num_label))
        # choices = project_tables.DISPLAY_CHOICES
        # network.admin_state_label = (
        #     filters.get_display_label(choices, network.admin_state))
        return context

    def get_tabs(self, request, *args, **kwargs):
        pool = self._get_data()
        return self.tab_group_class(request, pool=pool, **kwargs)


class CreateView(forms.ModalFormView):
    form_class = project_forms.CreatePoolForm
    form_id = "create_pool_form"
    # submit_label = _("Create Pool")
    submit_url = reverse_lazy('horizon:ceph:pools:create')
    template_name = 'ceph/pools/create.html'
    context_object_name = 'pool'
    success_url = reverse_lazy("horizon:ceph:pools:index")
    page_title = _("Create Pool")

    def get_initial(self):
        initial = {}
        for name in [
            'name',
            # 'description',
            # 'image_url',
            # 'source_type',
            # 'architecture',
            # 'disk_format',
            # 'minimum_disk',
            # 'minimum_ram'
        ]:
            tmp = self.request.GET.get(name)
            if tmp:
                initial[name] = tmp
        return initial

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        # upload_mode = api.glance.get_image_upload_mode()
        # context['image_upload_enabled'] = upload_mode != 'off'
        # context['images_allow_location'] = getattr(settings,
        #                                            'IMAGES_ALLOW_LOCATION',
        #                                            False)
        return context

