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


class SnapshotsTable(tables.DataTable):
    name = tables.WrappingColumn('name',
                                 # link="horizon:ceph:pools:detail",
                                 verbose_name=_('Snapshot Name'))
    # pool_name = tables.WrappingColumn('pool_name',
    #                              verbose_name=_('Ceph Pool'))
    # size = tables.Column("size",
    #                      filters=(defaultfilters.filesizeformat,),
    #                      attrs=({"data-type": "size"}),
    #                      verbose_name=_("snapshot Size"))
    # snapshot_format = tables.WrappingColumn('snapshot_format',
    #                              verbose_name=_('snapshot Format'))
    # obj_size = tables.Column("obj_size",
    #                      filters=(defaultfilters.filesizeformat,),
    #                      attrs=({"data-type": "size"}),
    #                      verbose_name=_("Object Size"))
    # snap_num = tables.WrappingColumn('snap_num',
    #                              verbose_name=_('SnapShot Num'))

    class Meta(object):
        name = "snapshots"
        verbose_name = _("snapshots")

