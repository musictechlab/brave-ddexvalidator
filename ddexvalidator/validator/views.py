import requests
from django.shortcuts import render
from lxml import etree

from .forms import UploadXMLForm

from django.conf import settings

print (settings.GOOGLE_ANALYTICS)

def validate_ddex_xml(xml_data, xsd_url, is_file=True):
    """Validate the uploaded or pasted XML file against the selected DDEX XSD schema."""
    try:
        # Fetch the XSD schema from the selected URL
        response = requests.get(xsd_url)
        if response.status_code != 200:
            raise Exception(f"Unable to fetch schema from {xsd_url}")

        # Parse the XSD schema
        schema_root = etree.fromstring(response.content)
        schema = etree.XMLSchema(schema_root)

        # Parse the uploaded XML file or XML text
        if is_file:
            xml_tree = etree.parse(xml_data)  # Treat as file
        else:
            xml_tree = etree.fromstring(xml_data)  # Treat as string

        # Schema validation as before...
        schema.validate(xml_tree)

        # Return validation result, errors, and the XML string (if valid)
        if schema.error_log:
            return False, [schema.error_log], None

        # Return XML content if validation is successful
        xml_content = etree.tostring(xml_tree, pretty_print=True).decode("utf-8")
        return True, None, xml_content

    except etree.XMLSyntaxError as e:
        return False, [str(e)], None


def upload_and_validate_xml(request):
    """Handle XML upload or text paste and validation."""
    is_valid = errors = xml_content = None
    form = UploadXMLForm()

    if request.method == "POST":
        form = UploadXMLForm(request.POST, request.FILES)

        if form.is_valid():
            # Get the selected schema
            selected_schema = form.cleaned_data["schema"]

            # Check if an XML file was uploaded
            if "xml_file" in request.FILES and request.FILES["xml_file"]:
                xml_file = request.FILES["xml_file"]
                is_valid, errors, xml_content = validate_ddex_xml(
                    xml_file, selected_schema, is_file=True
                )

            # Check if XML text was pasted
            elif form.cleaned_data["xml_text"]:
                xml_text = form.cleaned_data["xml_text"]
                is_valid, errors, xml_content = validate_ddex_xml(
                    xml_text, selected_schema, is_file=False
                )

            else:
                errors = ["Please upload an XML file or paste XML text for validation."]

    else:
        form = UploadXMLForm()

    return render(
        request,
        "validator/upload.html",
        {
            "form": form,
            "is_valid": is_valid,
            "errors": errors,
            "xml_content": xml_content,
            "GOOGLE_ANALYTICS": settings.GOOGLE_ANALYTICS
        },
    )
