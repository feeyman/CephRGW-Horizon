# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy
from django.utils.translation import pgettext_lazy

from horizon import forms
from horizon import tables
from openstack_dashboard import api

class AddMonitor(tables.LinkAction):
    name = "add_monitor"
    verbose_name = _("Add Monitor")
    url = "horizon:ceph:monitors:add_monitor"
    classes = ("ajax-modal","btn-primary","btn-launch",)
    icon = "plus"

class MonitorsTable(tables.DataTable):
    name = tables.WrappingColumn('name',
                                 # link="horizon:ceph:monitors:detail",
                                 verbose_name=_('Name'))
    rank = tables.Column('rank', verbose_name=pgettext_lazy('ceph monitor attribute','Rank'))
    addr = tables.Column('addr', verbose_name=pgettext_lazy('ceph monitor attribute','Address'))
    state = tables.Column('state', verbose_name=_('State'))

    class Meta(object):
        name = "monitors"
        verbose_name = _("Ceph Monitors")
        table_actions = (tables.FilterAction, AddMonitor)
        # row_actions = (EditUserLink, ChangePasswordLink, ToggleEnabled,
                       # DeleteUsersAction)
        # table_actions = (UserFilterAction, CreateUserLink, ImportUsersLink, DeleteUsersAction)
        # row_class = UpdateRow
