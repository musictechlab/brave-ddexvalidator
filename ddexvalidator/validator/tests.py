import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import UploadXMLForm

@pytest.mark.django_db
def test_upload_xml_file(client):
    """
    Test valid XML file upload and validation.
    """
    # Simulate uploading an XML file
    xml_file_content = b'<xml><data>Sample</data></xml>'
    xml_file = SimpleUploadedFile("test.xml", xml_file_content, content_type="text/xml")

    # Post data to the form with a file
    response = client.post(reverse('your_view_name'), {
        'schema': 'https://service.ddex.net/xml/ern/382/release-notification.xsd',
        'xml_file': xml_file,
    })

    # Check that the response is valid and the form processes successfully
    assert response.status_code == 200
    assert b'Success' in response.content  # Check for success message


@pytest.mark.django_db
def test_upload_xml_text(client):
    """
    Test valid XML text submission and validation.
    """
    # Simulate submitting XML text instead of a file
    xml_text_content = '<xml><data>Sample</data></xml>'

    # Post data to the form with text
    response = client.post(reverse('your_view_name'), {
        'schema': 'https://service.ddex.net/xml/ern/382/release-notification.xsd',
        'xml_text': xml_text_content,
    })

    # Check that the response is valid and the form processes successfully
    assert response.status_code == 200
    assert b'Success' in response.content  # Check for success message


@pytest.mark.django_db
def test_missing_xml_submission(client):
    """
    Test that form fails validation when neither file nor text is provided.
    """
    # Post data without file or text
    response = client.post(reverse('your_view_name'), {
        'schema': 'https://service.ddex.net/xml/ern/382/release-notification.xsd',
    })

    # Check that the response shows errors
    assert response.status_code == 200
    assert b'Please upload an XML file or paste XML text for validation.' in response.content


@pytest.mark.django_db
def test_invalid_xml_file(client):
    """
    Test invalid XML file upload.
    """
    # Simulate uploading an invalid XML file
    invalid_xml_content = b'Invalid XML Content'
    xml_file = SimpleUploadedFile("test.xml", invalid_xml_content, content_type="text/xml")

    # Post data to the form with invalid XML file
    response = client.post(reverse('your_view_name'), {
        'schema': 'https://service.ddex.net/xml/ern/382/release-notification.xsd',
        'xml_file': xml_file,
    })

    # Check that the response shows validation errors
    assert response.status_code == 200
    assert b'The XML file is invalid.' in response.content  # Check for error message