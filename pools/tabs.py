# Copyright 2016 Mirantis Inc.
# All Rights Reserved.
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

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs
from horizon.utils import memoized

from openstack_dashboard import api
# from openstack_dashboard.dashboards.ceph.pools.images imort tabs \
#     as images_tabs
from openstack_dashboard.dashboards.ceph.pools \
    import tables as project_tables
from openstack_dashboard.utils import filters

import logging
LOG = logging.getLogger(__name__)

class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("ceph/pools/_detail_overview.html")
    preload = False

    @memoized.memoized_method
    def _get_data(self):
        pool = self.tab_group.kwargs['pool']
        LOG.error("------>pool %s" % pool)
        return pool

    def get_context_data(self, request, **kwargs):
        context = super(OverviewTab, self).get_context_data(request, **kwargs)
        pool = self._get_data()
        context["pool"] = pool
        if pool['type'] == 1:
            pool.type_label = 'replicated'
        else:
            pool.type_label = 'erasure'
        return context


class PoolDetailsTabs(tabs.DetailTabsGroup):
    slug = "pool_tabs"
    # tabs = (OverviewTab, pools_tabs_tabs.SubnetsTab, pools_tabs.PoolsTab, )
    tabs = (OverviewTab, )
    sticky = True
