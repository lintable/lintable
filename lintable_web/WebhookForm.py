# Copyright 2015-2016 Capstone Team G
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from wtforms import Form, widgets, SelectMultipleField, SubmitField, Field, Label, FormField, FieldList


class MultiCheckboxField(SelectMultipleField):
    """A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RepoForm(Form):
    repo_full_name = Label('repo_full_name', text='')
    change_webhook = SubmitField('change_webhook')


class WebhookForm(Form):
    webhooks = FieldList(FormField(RepoForm), min_entries=0, max_entries=None)
    #    webhooks = MultiCheckboxField('webhooks', choices=[])
    #   submit = SubmitField()
