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
from horizon import workflows
from horizon import views
from horizon.utils import memoized

from openstack_dashboard import api
from openstack_dashboard.api import base

from openstack_dashboard.dashboards.ceph.snapshots \
    import tables as snapshot_tables


LOG = logging.getLogger(__name__)


class SnapshotsLine(base.APIDictWrapper):
    def __init__(self, snapshot):
        # id should be unique!
        snapshot_dict = {'id': snapshot['pool'] + "/" + snapshot['name'],
                        'name': snapshot['name'],
                        'pool_name': snapshot['pool'],
                        'size':snapshot['size'],
                        'snapshot_format':snapshot['format'],
                        'obj_size': snapshot['object_size'],
                        'snap_num': len(snapshot['snaps'])}
        super(SnapshotsLine, self).__init__(snapshot_dict)


class IndexView(tables.DataTableView):
    table_class = snapshot_tables.SnapshotsTable
    template_name = 'ceph/snapshots/index.html'
    page_title = _("Ceph Snapshots")

    def needs_filter_first(self, table):
        return self._needs_filter_first

    def get_data(self):
        snapshots = []
        filters = self.get_filters()

        self._needs_filter_first = False

        snapshots_list = []
        # try:
        #     #snapshots_list = api.ceph.get_ceph_snapshots(self.request)
        # except Exception:
        #     msg = _('Failed to get ceph snapshots !')
        #     exceptions.handle(self.request, msg)

        snapshot_lines = []
        for snapshot in snapshots_list:
            line = SnapshotsLine(snapshot)
            snapshot_lines.append(line)
        return snapshot_lines

