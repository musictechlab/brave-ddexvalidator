from django import forms

from .utils import fetch_xsd_schemas


class UploadXMLForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UploadXMLForm, self).__init__(*args, **kwargs)

        # Fetch the XSD schemas dynamically
        xsd_schemas = fetch_xsd_schemas()

        # Populate the schema choices
        self.fields["schema"] = forms.ChoiceField(
            choices=xsd_schemas,
            label="Select DDEX Schema",
            required=True,
            initial="https://service.ddex.net/xml/ern/382/release-notification.xsd",  # Set default value here
            widget=forms.Select(
                attrs={
                    "class": "appearance-none rounded-none relative block w-full px-3 py-2 mb-4 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                }
            ),
        )

    xml_file = forms.FileField(label="Upload DDEX XML File", required=False)
    xml_text = forms.CharField(
        widget=forms.Textarea, label="Or Paste DDEX XML Text", required=False
    )
