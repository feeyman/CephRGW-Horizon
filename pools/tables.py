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


POOL_TYPES = {1:_('replicated'),3:_('erasure')}

def get_pool_type(pool):
    return POOL_TYPES.get(pool['type'],_("unknown"))

# class DeletePool(tables.DeleteAction):
    # # NOTE: The bp/add-batchactions-help-text
    # # will add appropriate help text to some batch/delete actions.
    # help_text = _("Deleted images are not recoverable.")

    # @staticmethod
    # def action_present(count):
    #     return ungettext_lazy(
    #         u"Delete Image",
    #         u"Delete Images",
    #         count
    #     )

    # @staticmethod
    # def action_past(count):
    #     return ungettext_lazy(
    #         u"Deleted Image",
    #         u"Deleted Images",
    #         count
    #     )

    # policy_rules = (("image", "delete_image"),)

    # def allowed(self, request, image=None):
    #     # Protected images can not be deleted.
    #     if image and image.protected:
    #         return False
    #     if image:
    #         return image.owner == request.user.tenant_id
    #     # Return True to allow table-level bulk delete action to appear.
    #     return True

    # def delete(self, request, obj_id):
    #     api.glance.image_delete(request, obj_id)


class CreatePool(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Pool")
    url = "horizon:ceph:pools:create"
    classes = ("ajax-modal", "btn-launch")
    icon = "plus"
    policy_rules = (("pool", "add_pool"),)


# class EditPool(tables.LinkAction):
    # name = "edit"
    # verbose_name = _("Edit Image")
    # url = "horizon:project_desktop:images:images:update"
    # classes = ("ajax-modal",)
    # icon = "pencil"
    # policy_rules = (("image", "modify_image"),)

    # def allowed(self, request, image=None):
    #     if image:
    #         return image.status in ("active",) and \
    #             image.owner == request.user.tenant_id
    #     # We don't have bulk editing, so if there isn't an image that's
    #     # authorized, don't allow the action.
    #     return False

class PoolsTable(tables.DataTable):
    name = tables.Column('name',link="horizon:ceph:pools:detail", verbose_name=_('Pool Name'))
    pool_type = tables.Column(get_pool_type, verbose_name=_('Pool Type'))
    pg_num = tables.Column('pg_num', verbose_name=_('Placement Groups'))
    pg_placement_num = tables.Column('pg_placement_num', verbose_name=_('Placement Group for Placement'))
    size = tables.Column('size', verbose_name=_('Replicated Num'))
    min_size = tables.Column('min_size', verbose_name=_('Minimal Replicated Num'))

    class Meta(object):
        name = "pools"
        verbose_name = _("Ceph Pools")
        # table_actions = (CreatePool, )#, EditPool, DeletePool,)
        # row_class = UpdateRow


