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

import datetime
import logging
import operator
import pytz

# from django import shortcuts
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator  # noqa
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters  # noqa

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon import tables
from horizon import workflows
from horizon import views
from horizon.utils import memoized

from openstack_dashboard import api
from openstack_dashboard.api import base

from openstack_dashboard.dashboards.ceph.images \
    import tables as image_tables


LOG = logging.getLogger(__name__)


class ImagesLine(base.APIDictWrapper):
    def __init__(self, image):
        def convert_iso_time(timestr):
            dt = datetime.datetime.strptime(str(timestr),"%a %b %d %H:%M:%S %Y")
            tz = pytz.timezone('Asia/Shanghai')
            dt_localized = tz.localize(dt)
            return dt_localized.isoformat()

        image_dict = {'id': image['pool'] + '/' + image['name'],
                      'name': image['name'],
                      'pool': image['pool'],
                      'format': image['format'],
                       'size':image['size'],
                       'obj_size': image['object_size'],
                       'snap_num': len(image['snaps']),
                       'os_image_id': image['os_image_id'],
                       'project_id': image['usage'].get('project_id', None),
                       'project_name': image['project_name'],
                       'used_by': image['usage'].get('used_by', None),
                       # 'created_at':convert_iso_time(image['create_timestamp'])}
                        'created_at':image['usage'].get('created_at', None)}
        super(ImagesLine, self).__init__(image_dict)


class IndexView(tables.DataTableView):
    table_class = image_tables.ImagesTable
    template_name = 'ceph/images/index.html'
    page_title = _("Ceph Images")

    def has_prev_data(self, table):
        return getattr(self, "_prev", False)

    def has_more_data(self, table):
        return getattr(self, "_more", False)

    def needs_filter_first(self, table):
        return self._needs_filter_first

    def get_data(self):
        images = []
        prev_marker = self.request.GET.get(
            image_tables.ImagesTable._meta.prev_pagination_param,
            None)

        if prev_marker is not None:
            # paginating backward in this table
            marker = prev_marker
        else:
            # paginating forward in this table
            marker = self.request.GET.get(
                image_tables.ImagesTable._meta.pagination_param,
                None)

        reversed_order = prev_marker is not None
        filters = self.get_filters()

        self._needs_filter_first = False

        images_list = []
        try:
            images_list, self._more, self._prev = api.ceph.get_ceph_images_paged(self.request, marker, reversed_order)
        except Exception:
            msg = _('Failed to get ceph images !')
            exceptions.handle(self.request, msg)

        image_lines = []
        for image in images_list:
            line = ImagesLine(image)
            image_lines.append(line)
        return image_lines

