# #!/usr/bin/python
# #-*- coding: UTF-8 -*-
# # Copyright 2012 United States Government as represented by the
# # Administrator of the National Aeronautics and Space Administration.
# # All Rights Reserved.
# #
# # Copyright 2012 Nebula, Inc.
# #
# #    Licensed under the Apache License, Version 2.0 (the "License"); you may
# #    not use this file except in compliance with the License. You may obtain
# #    a copy of the License at
# #
# #         http://www.apache.org/licenses/LICENSE-2.0
# #
# #    Unless required by applicable law or agreed to in writing, software
# #    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# #    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# #    License for the specific language governing permissions and limitations
# #    under the License.

import collections
import logging
import chardet

from django.conf import settings
from django.forms import ValidationError  # noqa
from django import http
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables  # noqa

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import functions as utils
from horizon.utils import validators

from openstack_dashboard import api

from django.core.urlresolvers import reverse

LOG = logging.getLogger(__name__)
PROJECT_REQUIRED = api.keystone.VERSIONS.active < 3



class AddOsdForm(forms.SelfHandlingForm):
    host = forms.CharField(label=_("Host"),
                           max_length=8,
                           help_text=_("Name of the new osd."),
                           required=True)

    def handle(self, request, data):
        host = data['host']
        try:
            api.storageinstaller.add_osd(host)
        except:
            redirect = reverse('horizon:ceph:osds:index')
            messages.error(request, _("Failed to add osd %(host)s!") % dict(host=host))
            exceptions.handle(request, redirect=redirect)
            return False

        return True
