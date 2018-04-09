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


class AddOsd(tables.LinkAction):
    name = "add_osd"
    verbose_name = _("Add Osd")
    url = "horizon:ceph:osds:add_osd"
    classes = ("ajax-modal","btn-primary","btn-launch",)
    icon = "plus"
'''
class DeleteOsd(tables.LinkAction):
    name = "delete_osd"
    verbose_name = _("Delete OSD")
    url = "horizon:ceph:osds:add_osd"
    classes = ("ajax-modal","","btn-danger",)
    icon = "minus"
'''

class DeleteOsd(tables.DeleteAction):
    # NOTE: The bp/add-batchactions-help-text
    # will add appropriate help text to some batch/delete actions.
    help_text = _("Deleted ods objects are not recoverable.")

    @staticmethod
    def action_present(count):
        return ungettext_lazy(
            u"Delete OSD",
            u"Delete OSD",
            count
        )

    @staticmethod
    def action_past(count):
        return ungettext_lazy(
            u"Deleted OSD",
            u"Deleted OSD",
            count
        )

    #policy_rules = (("image", "delete_image"),)

    def allowed(self, request, image=None):
        return True

    def delete(self, request, obj_id):
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print obj_id
        api.ceph.delete_osd(obj_id)
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        #api.glance.image_delete(request, obj_id)
        pass


def get_osd_parent(osd):
    parent = osd.get('parent', None)
    if parent:
        return parent.get('name', '')
    return ''


class OsdsTable(tables.DataTable):
    id = tables.Column('id',
                       # link="horizon:ceph:osds:detail",
                       verbose_name=_('ID'))
    name = tables.Column('name', verbose_name=_('OSD Name'))
    parent = tables.Column(get_osd_parent, verbose_name=_('Host'))
    exists = tables.Column('exists', verbose_name=pgettext_lazy('ceph osd attribute','exists'))
    reweight = tables.Column('reweight', verbose_name=pgettext_lazy('ceph osd attribute','reweight'))
    crush_weight = tables.Column('crush_weight', verbose_name=pgettext_lazy('ceph osd attribute','crush_weight'))
    primary_affinity = tables.Column('primary_affinity', verbose_name=pgettext_lazy('ceph osd attribute','primary_affinity'))
    depth = tables.Column('depth', verbose_name=pgettext_lazy('ceph osd attribute','depth'))
    status = tables.Column('status', verbose_name=_('Status'))

    class Meta(object):
        name = "Osds"
        verbose_name = _("Ceph Osds")
        # row_actions = (EditUserLink, ChangePasswordLink, ToggleEnabled,
                       # DeleteUsersAction)
        table_actions = (tables.FilterAction, AddOsd, DeleteOsd)
        # row_class = UpdateRow
