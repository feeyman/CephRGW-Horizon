# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 OpenStack Foundation
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
from django.utils.datastructures import SortedDict

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import views
from horizon import forms
from horizon import tables
from horizon import messages
from horizon.utils import memoized
from openstack_dashboard import api

LOG = logging.getLogger(__name__)


class IndexView(views.HorizonTemplateView):
    template_name = 'ceph/crushmap/index.html'
    page_title = _("Crushmap")

    @memoized.memoized_method
    def get_crushmap(self):
        crushmap = None
        try:
            crushmap = api.ceph.get_ceph_crushmap(self.request)
        except Exception:
            msg = _('Unable to retrieve ceph crushmap.')
            exceptions.handle(self.request, msg)

        LOG.info("crushmap type= %s" % type(crushmap))
        LOG.info("crushmap = %s" % crushmap)
        return crushmap

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['crushmap'] = self.get_crushmap()
        return context
  

