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

"""
Views for managing images.
"""

from django.conf import settings
from django.core import validators
from django.forms import ValidationError  # noqa
from django.forms.widgets import HiddenInput  # noqa
from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
import six

from horizon import exceptions
from horizon import forms
from horizon import messages

from openstack_dashboard import api
from openstack_dashboard import policy



# def get_linux_choices():
#     return [(image.get('distribution', ''), image.get('verbose_name', '')) \
#            for image in IMAGE_OS_LINUX_SETTINGS]


# def get_windows_choices():
#     return [(image.get('distribution', ''), image.get('verbose_name', '')) \
#            for image in IMAGE_OS_WINDOWS_SETTINGS]


# class ImageURLField(forms.URLField):
#     default_validators = [validators.URLValidator(schemes=["http", "https"])]


# def create_image_metadata(data):
#     """Use the given dict of image form data to generate the metadata used for
#     creating the image in glance.
#     """
#     # Glance does not really do anything with container_format at the
#     # moment. It requires it is set to the same disk_format for the three
#     # Amazon image types, otherwise it just treats them as 'bare.' As such
#     # we will just set that to be that here instead of bothering the user
#     # with asking them for information we can already determine.
#     disk_format = data['disk_format']
#     if disk_format in ('ami', 'aki', 'ari',):
#         container_format = disk_format
#     elif disk_format == 'docker':
#         # To support docker containers we allow the user to specify
#         # 'docker' as the format. In that case we really want to use
#         # 'raw' as the disk format and 'docker' as the container format.
#         disk_format = 'raw'
#         container_format = 'docker'
#     elif disk_format == 'ova':
#         # If the user wishes to upload an OVA using Horizon, then
#         # 'ova' must be the container format and 'vmdk' must be the disk
#         # format.
#         container_format = 'ova'
#         disk_format = 'vmdk'
#     else:
#         container_format = 'bare'

#     meta = {'protected': data['protected'],
#             'disk_format': disk_format,
#             'container_format': container_format,
#             'min_disk': (data['minimum_disk'] or 0),
#             'min_ram': (data['minimum_ram'] or 0),
#             'name': data['name']}

#     is_public = data.get('is_public', data.get('public', False))
#     properties = {}
#     # NOTE(tsufiev): in V2 the way how empty non-base attributes (AKA metadata)
#     # are handled has changed: in V2 empty metadata is kept in image
#     # properties, while in V1 they were omitted. Skip empty description (which
#     # is metadata) to keep the same behavior between V1 and V2
#     if data.get('description'):
#         properties['description'] = data['description']
#     if data.get('kernel'):
#         properties['kernel_id'] = data['kernel']
#     if data.get('ramdisk'):
#         properties['ramdisk_id'] = data['ramdisk']
#     if data.get('architecture'):
#         properties['architecture'] = data['architecture']

#     # astute: add os_type & os_distribution property
#     if data.get('os_type'):
#         properties['os_type'] = data['os_type']
#         if data['os_type'] == 'windows':
#             properties['os_distribution'] = data['os_windows_distribution']
#         elif data['os_type'] == 'linux':
#             properties['os_distribution'] = data['os_linux_distribution']

#     if api.glance.VERSIONS.active < 2:
#         meta.update({'is_public': is_public, 'properties': properties})
#     else:
#         meta['visibility'] = 'public' if is_public else 'private'
#         meta.update(properties)

#     return meta


# if api.glance.get_image_upload_mode() == 'direct':
#     FileField = forms.ExternalFileField
#     CreateParent = six.with_metaclass(forms.ExternalUploadMeta,
#                                       forms.SelfHandlingForm)
# else:
#     FileField = forms.FileField
#     CreateParent = forms.SelfHandlingForm


class CreatePoolForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=255, label=_("Name"))

    # pool_type = forms.ThemableChoiceField(
    #     label=_('Pool Ruleset Type'),
    #     initial='replicated',
    #     required=True,
    #     choices=[('replicated', _('replicated')),
    #              ('erasure', _('erasure'))],
    #     widget=forms.ThemableSelectWidget(attrs={
    #         'class': 'switchable',
    #         'data-slug': 'pool_type'}),)
    # xxx = ''

    # ruleset = forms.ThemableChoiceField(
    #     label=_('Pool Ruleset'),
    #     initial= xxx,
    #     required=True,
    #     choices=[('replicated', _('replicated')),
    #              ('erasure', _('erasure'))],
    #     widget=forms.ThemableSelectWidget(attrs={
    #         'class': 'switchable',
    #         'data-slug': 'pool_type'}),)   

    # pg_num = forms.IntegerField(
    #     label=_("Placement Group Number"),
    #     min_value=1,
    #     help_text=_('number of placement groups mapped to an OSD.'),
    #     required=True)

    # pg_placement_num = forms.IntegerField(
    #     label=_("Placement Group for Placement Purpose Number"),
    #     min_value=1,
    #     help_text=_('number of placement groups mapped to an OSD for Placement purpose. ')
    #     required=True)

    # pool_size = forms.IntegerField(
    #     label=_("Pool Size (GB)"),
    #     min_value=0,
    #     help_text=_('The pool size is required to create the pool. '
    #                 'If unspecified, this value defaults to 0.'),
    #     required=False)

    # min_size = forms.IntegerField(
    #     label=_("Minimum Replicated Size"),
    #     min_value=1,
    #     help_text=_('The minimum replicated size is required to create the pool. '
    #                 'If unspecified, this value is default.'),
    #     required=False)

    # size = forms.IntegerField(
    #     label=_("Replicated Size"),
    #     min_value=1,
    #     help_text=_('The minimum disk size is required to create the pool. '
    #                 'If unspecified, this value is deault.'),
    #     required=False)

    def __init__(self, request, *args, **kwargs):
        super(CreatePoolForm, self).__init__(request, *args, **kwargs)

    def handle(self, request, data):
        meta = create_image_metadata(data)
        return ''
        # # Add image source file or URL to metadata
        # if (api.glance.get_image_upload_mode() != 'off' and
        #         policy.check((("image", "upload_image"),), request) and
        #         data.get('image_file', None)):
        #     meta['data'] = data['image_file']
        # elif data.get('is_copying'):
        #     meta['copy_from'] = data['image_url']
        # else:
        #     meta['location'] = data['image_url']

        # try:
        #     image = api.glance.image_create(request, **meta)
        #     messages.info(request,
        #                   _('Your image %s has been queued for creation.') %
        #                   meta['name'])
        #     return image
        # except Exception as e:
        #     msg = _('Unable to create new image.')
        #     # TODO(nikunj2512): Fix this once it is fixed in glance client
        #     if hasattr(e, 'code') and e.code == 400:
        #         if "Invalid disk format" in e.details:
        #             msg = _('Unable to create new image: Invalid disk format '
        #                     '%s for image.') % meta['disk_format']
        #         elif "Image name too long" in e.details:
        #             msg = _('Unable to create new image: Image name too long.')
        #         elif "not supported" in e.details:
        #             msg = _('Unable to create new image: URL scheme not '
        #                     'supported.')

        #     exceptions.handle(request, msg)

        #     return False


class UpdatePoolForm(forms.SelfHandlingForm):
    # image_id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=255, label=_("Name"))

    # pool_type = forms.ThemableChoiceField(
    #     label=_('Pool Ruleset Type'),
    #     initial='replicated',
    #     required=True,
    #     choices=[('replicated', _('replicated')),
    #              ('erasure', _('erasure'))],
    #     widget=forms.ThemableSelectWidget(attrs={
    #         'class': 'switchable',
    #         'data-slug': 'pool_type'}),)
    # xxx = ''

    # ruleset = forms.ThemableChoiceField(
    #     label=_('Pool Ruleset'),
    #     initial= xxx,
    #     required=True,
    #     choices=[('replicated', _('replicated')),
    #              ('erasure', _('erasure'))],
    #     widget=forms.ThemableSelectWidget(attrs={
    #         'class': 'switchable',
    #         'data-slug': 'pool_type'}),)   

    # pg_num = forms.IntegerField(
    #     label=_("Placement Group Number"),
    #     min_value=1,
    #     help_text=_('number of placement groups mapped to an OSD.'),
    #     required=True)

    # pg_placement_num = forms.IntegerField(
    #     label=_("Placement Group for Placement Purpose Number"),
    #     min_value=1,
    #     help_text=_('number of placement groups mapped to an OSD for Placement purpose. ')
    #     required=True)

    # pool_size = forms.IntegerField(
    #     label=_("Pool Size (GB)"),
    #     min_value=0,
    #     help_text=_('The pool size is required to create the pool. '
    #                 'If unspecified, this value defaults to 0.'),
    #     required=False)

    # min_size = forms.IntegerField(
    #     label=_("Minimum Replicated Size"),
    #     min_value=1,
    #     help_text=_('The minimum replicated size is required to create the pool. '
    #                 'If unspecified, this value is default.'),
    #     required=False)

    # size = forms.IntegerField(
    #     label=_("Replicated Size"),
    #     min_value=1,
    #     help_text=_('The minimum disk size is required to create the pool. '
    #                 'If unspecified, this value is deault.'),
    #     required=False)
                  

    def __init__(self, request, *args, **kwargs):
        super(UpdatePoolForm, self).__init__(request, *args, **kwargs)
        # self.fields['disk_format'].choices = [(value, name) for value,
        #                                       name in IMAGE_FORMAT_CHOICES
        #                                       if value]
        # if not policy.check((("image", "publicize_image"),), request):
        #     self.fields['public'].widget = forms.CheckboxInput(
        #         attrs={'readonly': 'readonly', 'disabled': 'disabled'})
        #     self.fields['public'].help_text = _(
        #         'Non admin users are not allowed to make images public.')

    def handle(self, request, data):
    	pass
        # image_id = data['image_id']
        # error_updating = _('Unable to update image "%s".')
        # meta = create_image_metadata(data)

        # try:
        #     image = api.glance.image_update(request, image_id, **meta)
        #     messages.success(request, _('Image was successfully updated.'))
        #     return image
        # except Exception:
        #     exceptions.handle(request, error_updating % image_id)
			
