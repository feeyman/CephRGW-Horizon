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

import time
import logging

from django.core import urlresolvers
from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from horizon import forms
from horizon import tables
from horizon.utils import filters

from openstack_dashboard import api


LOG = logging.getLogger(__name__)


def get_used_by_link(datum):
    if datum.used_by == "cinder":
        return urlresolvers.reverse("horizon:admin:volumes:volumes:detail",
                                    args=(datum.os_image_id,))
    if datum.used_by == "glance":
        return urlresolvers.reverse("horizon:admin:images:detail",
                                    args=(datum.os_image_id,))


def get_project_link(datum):
    if datum.project_id:
        return urlresolvers.reverse("horizon:identity:projects:detail",
                                    args=(datum.project_id,))


class ImagesTable(tables.DataTable):
    name = tables.WrappingColumn("name",
                                 # link="horizon:ceph:pools:detail",
                                 verbose_name=_('Image Name'))
    pool_name = tables.WrappingColumn('pool',
                                 verbose_name=_('Ceph Pool'))
    image_format = tables.WrappingColumn('format',
                                 verbose_name=_('Image Format'))
    size = tables.Column("size",
                         filters=(defaultfilters.filesizeformat,),
                         attrs=({"data-type": "size"}),
                         verbose_name=_("Image Size"))
    obj_size = tables.Column("obj_size",
                         filters=(defaultfilters.filesizeformat,),
                         attrs=({"data-type": "size"}),
                         verbose_name=_("Object Size"))
    snap_num = tables.WrappingColumn('snap_num',
                                 verbose_name=_('SnapShot Num'))
    project_name = tables.WrappingColumn('project_name',
                                 link=get_project_link,
                                 verbose_name=_('Project Name'))
    used_by = tables.WrappingColumn('used_by',
                                 # link=get_used_by_link,
                                 verbose_name=_('Used By'))
    created_at = tables.Column("created_at",
                            verbose_name=_("Created Time"),
                            filters=(filters.parse_isotime_local,))

    class Meta(object):
        name = "images"
        verbose_name = _("Images")

