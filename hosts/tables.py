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

from horizon import forms
from horizon import tables
from openstack_dashboard import api


class HostsTable(tables.DataTable):
    name = tables.WrappingColumn('name',
                                 # link="horizon:ceph:hosts:detail",
                                 verbose_name=_('Host Name'))

    class Meta(object):
        name = "hosts"
        verbose_name = _("Ceph Hosts")
        # row_actions = (EditUserLink, ChangePasswordLink, ToggleEnabled,
                       # DeleteUsersAction)
        # table_actions = (UserFilterAction, CreateUserLink, ImportUsersLink, DeleteUsersAction)
        # row_class = UpdateRow
