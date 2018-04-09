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

# import collections
# import logging
# import chardet

# from django.conf import settings
# from django.forms import ValidationError  # noqa
# from django import http
# from django.utils.translation import ugettext_lazy as _
# from django.views.decorators.debug import sensitive_variables  # noqa

# from horizon import exceptions
# from horizon import forms
# from horizon import messages
# from horizon.utils import functions as utils
# from horizon.utils import validators

# from openstack_dashboard import api

# LOG = logging.getLogger(__name__)
# PROJECT_REQUIRED = api.keystone.VERSIONS.active < 3


# class PasswordMixin(forms.SelfHandlingForm):
#     password = forms.RegexField(
#         label=_("Password"),
#         widget=forms.PasswordInput(render_value=False),
#         regex=validators.password_validator(),
#         error_messages={'invalid': validators.password_validator_msg()})
#     confirm_password = forms.CharField(
#         label=_("Confirm Password"),
#         widget=forms.PasswordInput(render_value=False))
#     no_autocomplete = True

#     def clean(self):
#         '''Check to make sure password fields match.'''
#         data = super(forms.Form, self).clean()
#         if 'password' in data and 'confirm_password' in data:
#             if data['password'] != data['confirm_password']:
#                 raise ValidationError(_('Passwords do not match.'))
#         return data


# class BaseUserForm(forms.SelfHandlingForm):
#     def __init__(self, request, *args, **kwargs):
#         super(BaseUserForm, self).__init__(request, *args, **kwargs)

#         # Populate project choices
#         project_choices = []

#         # If the user is already set (update action), list only projects which
#         # the user has access to.
#         user_id = kwargs['initial'].get('id', None)
#         domain_id = kwargs['initial'].get('domain_id', None)
#         default_project_id = kwargs['initial'].get('project', None)

#         try:
#             if api.keystone.VERSIONS.active >= 3:
#                 projects, has_more = api.keystone.tenant_list(
#                     request, domain=domain_id)
#             else:
#                 projects, has_more = api.keystone.tenant_list(
#                     request, user=user_id)

#             # hide internal projects
#             hidden_projects = getattr(settings, 'HIDDEN_PROJECTS', ())

#             for project in projects:
#                 if (project.enabled and project.name not in hidden_projects):
#                     project_choices.append((project.id, project.name))
#             if not project_choices:
#                 project_choices.insert(0, ('', _("No available projects")))
#             # TODO(david-lyle): if keystoneclient is fixed to allow unsetting
#             # the default project, then this condition should be removed.
#             elif default_project_id is None:
#                 project_choices.insert(0, ('', _("Select a project")))
#             self.fields['project'].choices = project_choices

#         except Exception:
#             LOG.debug("User: %s has no projects" % user_id)


# class AddExtraColumnMixIn(object):
#     def add_extra_fields(self, ordering=None):
#         if api.keystone.VERSIONS.active >= 3:
#             # add extra column defined by setting
#             EXTRA_INFO = getattr(settings, 'USER_TABLE_EXTRA_INFO', {})
#             for key, value in EXTRA_INFO.items():
#                 self.fields[key] = forms.CharField(label=value,
#                                                    required=False)
#                 if ordering:
#                     ordering.append(key)


# ADD_PROJECT_URL = "horizon:identity:projects:create"


# class CreateUserForm(PasswordMixin, BaseUserForm, AddExtraColumnMixIn):
#     # Hide the domain_id and domain_name by default
#     domain_id = forms.CharField(label=_("Domain ID"),
#                                 required=False,
#                                 widget=forms.HiddenInput())
#     domain_name = forms.CharField(label=_("Domain Name"),
#                                   required=False,
#                                   widget=forms.HiddenInput())
#     name = forms.CharField(max_length=255, label=_("User Name"))
#     description = forms.CharField(widget=forms.widgets.Textarea(
#                                   attrs={'rows': 4}),
#                                   label=_("Description"),
#                                   required=False)
#     email = forms.EmailField(label=_("Email"),
#                              required=False)
#     project = forms.ThemableDynamicChoiceField(label=_("Primary Project"),
#                                                required=PROJECT_REQUIRED,
#                                                add_item_link=ADD_PROJECT_URL)
#     role_id = forms.ThemableChoiceField(label=_("Role"),
#                                         required=PROJECT_REQUIRED)
#     enabled = forms.BooleanField(label=_("Enabled"),
#                                  required=False,
#                                  initial=True)

#     def __init__(self, *args, **kwargs):
#         roles = kwargs.pop('roles')
#         super(CreateUserForm, self).__init__(*args, **kwargs)
#         # Reorder form fields from multiple inheritance
#         ordering = ["domain_id", "domain_name", "name",
#                     "description", "email", "password",
#                     "confirm_password", "project", "role_id",
#                     "enabled"]
#         self.add_extra_fields(ordering)
#         self.fields = collections.OrderedDict(
#             (key, self.fields[key]) for key in ordering)
#         role_choices = [(role.id, role.name) for role in roles]
#         self.fields['role_id'].choices = role_choices

#         # For keystone V3, display the two fields in read-only
#         if api.keystone.VERSIONS.active >= 3:
#             readonlyInput = forms.TextInput(attrs={'readonly': 'readonly'})
#             self.fields["domain_id"].widget = readonlyInput
#             self.fields["domain_name"].widget = readonlyInput
#         # For keystone V2.0, hide description field
#         else:
#             self.fields["description"].widget = forms.HiddenInput()

#     # We have to protect the entire "data" dict because it contains the
#     # password and confirm_password strings.
#     @sensitive_variables('data')
#     def handle(self, request, data):
#         domain = api.keystone.get_default_domain(self.request, False)
#         try:
#             LOG.info('Creating user with name "%s"' % data['name'])
#             desc = data["description"]
#             if "email" in data:
#                 data['email'] = data['email'] or None

#             # add extra information
#             if api.keystone.VERSIONS.active >= 3:
#                 EXTRA_INFO = getattr(settings, 'USER_TABLE_EXTRA_INFO', {})
#                 kwargs = dict((key, data.get(key)) for key in EXTRA_INFO)
#             else:
#                 kwargs = {}

#             new_user = \
#                 api.keystone.user_create(request,
#                                          name=data['name'],
#                                          email=data['email'],
#                                          description=desc or None,
#                                          password=data['password'],
#                                          project=data['project'] or None,
#                                          enabled=data['enabled'],
#                                          domain=domain.id,
#                                          **kwargs)
#             messages.success(request,
#                              _('User "%s" was successfully created.')
#                              % data['name'])
#             if data['project'] and data['role_id']:
#                 roles = api.keystone.roles_for_user(request,
#                                                     new_user.id,
#                                                     data['project']) or []
#                 assigned = [role for role in roles if role.id == str(
#                     data['role_id'])]
#                 if not assigned:
#                     try:
#                         api.keystone.add_tenant_user_role(request,
#                                                           data['project'],
#                                                           new_user.id,
#                                                           data['role_id'])
#                     except Exception:
#                         exceptions.handle(request,
#                                           _('Unable to add user '
#                                             'to primary project.'))
#             return new_user
#         except exceptions.Conflict:
#             msg = _('User name "%s" is already used.') % data['name']
#             messages.error(request, msg)
#         except Exception:
#             exceptions.handle(request, _('Unable to create user.'))


# def reset_user_role(request, user, project, new_role_id, enabled):
#     current_roles = api.keystone.roles_for_user(request,
#                                                 user.id,
#                                                 project) or []

#     assigned = [role for role in current_roles if role.id == str(new_role_id)]
#     if not assigned:
#         try:
#             api.keystone.add_tenant_user_role(request,
#                                               project,
#                                               user.id,
#                                               new_role_id)
#         except Exception:
#             exceptions.handle(request,
#                               _('Failed to add role of user to the project.'))

#     removed = [role for role in current_roles if role.id != str(new_role_id)]
#     for role in removed:
#         try:
#             api.keystone.remove_tenant_user_role(request,
#                                                  project,
#                                                  user.id,
#                                                  role.id)
#         except Exception:
#             exceptions.handle(request,
#                               _('Failed to remove role of user to the project.'))

#     if enabled:
#         api.keystone.user_update_enabled(request, user.id, True)


# class ImportUsersForm(forms.SelfHandlingForm):
#     user_list = forms.FileField(label=_("User List File"),
#                                  help_text=_("User list file to import."),
#                                  widget=forms.FileInput(),
#                                  required=True)

#     def __init__(self, request, *args, **kwargs):
#         super(ImportUsersForm, self).__init__(request, *args, **kwargs)

#     def check_project_role(self, project_category, role):
#         valid_roles = ()
#         if project_category == "admin":
#             valid_roles = getattr(settings, 'VALID_ROLES_IN_ADMIN_PROJECT', ())

#         if project_category == "server":
#             valid_roles = getattr(settings, 'VALID_ROLES_IN_SERVER_PROJECT', ())

#         if project_category == "desktop":
#             valid_roles = getattr(settings, 'VALID_ROLES_IN_DESKTOP_PROJECT', ())

#         return role in valid_roles

#     def handle(self, request, data):
#         domain = api.keystone.get_default_domain(self.request)
#         projects, has_more = api.keystone.tenant_list(request, domain=domain.id)
#         roles = api.keystone.role_list(self.request)

#         if data.get('user_list', None):
#             user_list = self.files['user_list']
#             index = 0
#             try:
#                 for line in user_list:
#                     encoding = chardet.detect(line)['encoding']
#                     LOG.info("user line encoding = %s" % encoding)
#                     line = line.decode(encoding)

#                     if index == 0:
#                         index = 1
#                     else:
#                         data = line.split(u",")
#                         # line columns not enough !!!
#                         if len(data) < 10:
#                             msg = _('Invalid user info line: %s' % line)
#                             messages.warning(request,msg)
#                             continue

#                         name = data[0]
#                         password = data[1]
#                         project_category = data[2]
#                         project_name = data[3]
#                         role = data[4]
#                         department = data[5]
#                         position = data[6]
#                         email = data[7]
#                         telephone = data[8]
#                         description = data[9]

#                         project_id = None
#                         category_is_error = False

#                         for p in projects:
#                             if p.name == project_name:
#                                 project_id = p.id
#                                 category_is_error = project_category != getattr(p, "category", "admin")
                        
#                         if project_id == None:
#                             messages.error(request, _('Import "%(user)s" failed: project "%(project_name)s" does not exist!')
#                                                     % {'project_name': project_name, 'user': name})
#                             continue  

#                         if category_is_error:
#                             messages.error(request, _('Import "%(user)s" failed: Project "%(project_name)s" has invalid category "%(project_category)s"!')
#                                                     % {'project_name': project_name, 'project_category': project_category, 'user': name})
#                             continue

#                         if not self.check_project_role(project_category, role):
#                             messages.error(request, _('Import "%(user)s"  failed: "%(project_category)s" project does not have role "%(role)s"!')
#                                                     % {'project_category': project_category, 'role': role, 'user': name})
#                             continue

#                         role_id = None
#                         for r in roles:
#                             if r.name == role:
#                                 role_id = r.id   

#                         if role_id == None:
#                             messages.error(request, _('Import "%(user)s" failed: Role "%(role)s" does not exist!')
#                                                     % {'role':role, 'user':name})  
#                         try:
#                             new_user = api.keystone.user_create(request,
#                                                                 name=name,
#                                                                 department=department,
#                                                                 position=position,
#                                                                 email=email,
#                                                                 telephone=telephone,
#                                                                 description=description,
#                                                                 password=password,
#                                                                 project=project_id,
#                                                                 enabled=False,
#                                                                 domain=domain.id)

#                             reset_user_role(request, new_user, project_id, role_id, True)

#                             messages.success(request,
#                                              _('User "%s" was successfully created.')
#                                              % name)

#                         except exceptions.Conflict:
#                             msg = _('ImportError: User "%s" already exist.') % name
#                             messages.warning(request, msg)
#                         except Exception as e:
#                             msg = _('ImportError: Failed to create user "%(user)s"! %(exc)s') % {'user': name, 'exc': e}
#                             messages.error(request, msg)  

#             except Exception as e:
#                   msg = _('Failed to import user from file!')
#                   messages.error(request, msg)
#         return True
        

# class UpdateUserForm(BaseUserForm, AddExtraColumnMixIn):
#     # Hide the domain_id and domain_name by default
#     domain_id = forms.CharField(label=_("Domain ID"),
#                                 required=False,
#                                 widget=forms.HiddenInput())
#     domain_name = forms.CharField(label=_("Domain Name"),
#                                   required=False,
#                                   widget=forms.HiddenInput())
#     id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
#     name = forms.CharField(max_length=255, label=_("User Name"))
#     department = forms.CharField(label=_("Department"),
#                                  required=False,
#                                  widget=forms.TextInput)
#     position = forms.CharField(label=_("Position"),
#                                required=False,
#                                widget=forms.TextInput)
#     telephone = forms.CharField(label=_("Telephone"),
#                                 required=False,
#                                 widget=forms.TextInput)
#     email = forms.EmailField(label=_("Email"),
#                              required=False)
#     description = forms.CharField(widget=forms.widgets.Textarea(
#                                   attrs={'rows': 4}),
#                                   label=_("Description"),
#                                   required=False)
#     # project = forms.ThemableChoiceField(label=_("Primary Project"),
#     #                                     required=PROJECT_REQUIRED)

#     def __init__(self, request, *args, **kwargs):
#         super(UpdateUserForm, self).__init__(request, *args, **kwargs)
#         self.add_extra_fields()
#         if api.keystone.keystone_can_edit_user() is False:
#             for field in ('name', 'email', 'department', 'position', 'telephone'):
#                 self.fields.pop(field)
#         # For keystone V3, display the two fields in read-only
#         if api.keystone.VERSIONS.active >= 3:
#             readonlyInput = forms.TextInput(attrs={'readonly': 'readonly'})
#             self.fields["domain_id"].widget = readonlyInput
#             self.fields["domain_name"].widget = readonlyInput
#         # For keystone V2.0, hide description field
#         else:
#             self.fields["description"].widget = forms.HiddenInput()

#     def handle(self, request, data):
#         user = data.pop('id')

#         data.pop('domain_id')
#         data.pop('domain_name')

#         # if not PROJECT_REQUIRED and 'project' not in self.changed_data:
#         #     data.pop('project')

#         if 'description' not in self.changed_data:
#             data.pop('description')
#         try:
#             if "department" in data:
#                 data['department'] = data['department'] or None
#             if "position" in data:
#                 data['position'] = data['position'] or None
#             if "telephone" in data:
#                 data['telephone'] = data['telephone'] or None
#             if "email" in data:
#                 data['email'] = data['email'] or None
#             response = api.keystone.user_update(request, user, **data)
#             messages.success(request,
#                              _('User has been updated successfully.'))
#         except exceptions.Conflict:
#             msg = _('User name "%s" is already used.') % data['name']
#             messages.error(request, msg)
#             return False
#         except Exception:
#             response = exceptions.handle(request, ignore=True)
#             messages.error(request, _('Unable to update the user.'))

#         if isinstance(response, http.HttpResponse):
#             return response
#         else:
#             return True


# class ChangePasswordForm(PasswordMixin, forms.SelfHandlingForm):
#     id = forms.CharField(widget=forms.HiddenInput)
#     name = forms.CharField(
#         label=_("User Name"),
#         widget=forms.TextInput(attrs={'readonly': 'readonly'}),
#         required=False)

#     def __init__(self, request, *args, **kwargs):
#         super(ChangePasswordForm, self).__init__(request, *args, **kwargs)

#         if getattr(settings, 'ENFORCE_PASSWORD_CHECK', False):
#             self.fields["admin_password"] = forms.CharField(
#                 label=_("Admin Password"),
#                 widget=forms.PasswordInput(render_value=False))
#             # Reorder form fields from multiple inheritance
#             self.fields.keyOrder = ["id", "name", "admin_password",
#                                     "password", "confirm_password"]

#     @sensitive_variables('data', 'password', 'admin_password')
#     def handle(self, request, data):
#         user_id = data.pop('id')
#         password = data.pop('password')
#         admin_password = None

#         # Throw away the password confirmation, we're done with it.
#         data.pop('confirm_password', None)

#         # Verify admin password before changing user password
#         if getattr(settings, 'ENFORCE_PASSWORD_CHECK', False):
#             admin_password = data.pop('admin_password')
#             if not api.keystone.user_verify_admin_password(request,
#                                                            admin_password):
#                 self.api_error(_('The admin password is incorrect.'))
#                 return False

#         try:
#             response = api.keystone.user_update_password(
#                 request, user_id, password)
#             if user_id == request.user.id:
#                 return utils.logout_with_message(
#                     request,
#                     _('Password changed. Please log in to continue.'),
#                     redirect=False)
#             messages.success(request,
#                              _('User password has been updated successfully.'))
#         except Exception:
#             response = exceptions.handle(request, ignore=True)
#             messages.error(request, _('Unable to update the user password.'))

#         if isinstance(response, http.HttpResponse):
#             return response
#         else:
#             return True
