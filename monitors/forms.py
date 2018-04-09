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

from django import http
from django.conf import settings
from django.forms import ValidationError  # noqa
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables  # noqa

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import functions as utils
from horizon.utils import validators

from openstack_dashboard import api

from django.core.urlresolvers import reverse
# import socket
# import struct
# import ConfigParser
LOG = logging.getLogger(__name__)
PROJECT_REQUIRED = api.keystone.VERSIONS.active < 3


# #Check whether the given mon_public_ip is in the public network segment.
# def check_monitor_ip(mon_public_ip=None):
#     if mon_public_ip:
#       with open("/opt/atstorage/ceph_cluster/ceph.conf", "r") as ceph_config:
#         config = ConfigParser.ConfigParser()
#         config.readfp(ceph_config)
#         public_network = config.get("global", "public_network")

#     ip = public_network.split('/')[0]
#     prefix = public_network.split('/')[1]

#     public_ip = socket.ntohl(struct.unpack("I",socket.inet_aton(str(ip)))[0])

#     mon_ip = socket.ntohl(struct.unpack("I",socket.inet_aton(str(mon_public_ip)))[0])

#     if (public_ip >> (32- int(prefix))) == (mon_ip >> (32- int(prefix))):
#       return True

#     return False

class AddMonitorForm(forms.SelfHandlingForm):
    host = forms.CharField(label=_("Host"),
                           max_length=8,
                           help_text=_("Name of the new monitor."),
                           required=True)
    # mon_public_ip = forms.IPField(
    #     label=_("Monitor Public IP Address"),
    #     required=True,
    #     initial="",
    #     help_text=_("The Public IP address of the new monitor IP (e.g. 202.2.3.4). "
    #                 "You need to specify a public address which is under "
    #                 "the public network CIDR (e.g. 202.2.3.0/24)."),
    #     mask=False)

    def clean(self):
        cleaned_data = super(AddMonitorForm, self).clean()
        host = cleaned_data.get('host')
        if not host.startswith('host'):
            msg = _('The host %s is not known host.' % host)
            self._errors['host'] = self.error_class([msg])
        return cleaned_data

    def handle(self, request, data):
        host = data['host']
        # mon_public_ip = data['mon_public_ip']
        # try:          
        #     api.storageinstaller.add_monitor(host, mon_public_ip)
        # except:
        #     redirect = reverse('horizon:ceph:monitors:index')
        #     messages.error(request, _("Failed to add monitor %(host)s!") % dict(host=host))
        #     exceptions.handle(request, redirect=redirect)
        #     return False

        next_url = reverse('horizon:ceph:monitors:config', args=(host,))
        return http.HttpResponseRedirect(next_url)
        # return True


class ConfigMonitorForm(forms.SelfHandlingForm):
    host = forms.CharField(label=_("Host"),
                           max_length=8,
                           help_text=_("Name of the monitor to config."),
                           required=True)

    def handle(self, request, data):
        return True
