import functions_framework
import requests
from google.auth.transport.requests import Request
from google.auth import exceptions
import os

# GCP Endpoint details
PROJECT = "770798022283"
ENDPOINT_ID = "5769824705708032000"
LOCATION = "us-central1"
PREDICT_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}:predict"

# Replace with your authentication method (e.g., using service account JSON key)
GOOGLE_CLOUD_AUTH_TOKEN = os.environ.get("AUTH_KEY")
#"ya29.c.c0ASRK0GYHei0U5ZenuyzCWlef34fWfPhCNGWa5LXBFyMMKXCXHpv56SrqVj5i83vM5WwSOe-7y6aYM8OKqfM4EJ8N3oz7Bs7Jjw4Vn1L6Lhx5ExdaQcjHgdc4rOmh5MdoUfIKRPN3pz-1Fm0FF3rrtgNKDJD5oJ-a4R-wzTjaPe0pGGEptXcr12oqp7CFf5yE4tm9WskBIuM4DvAYU2ocwYDB6Plco8d75zFGWZDgZ0_gseS2ADji0kh03gOIebQ0WzOqaIhQuabtJ6zcFA4PD9_dqWMQqVfFK7Rh4jtfbvZmM7iSdKIJlhTRJBW9z6r1O5RtS-CKvNVYIkh0ErNd7XM2f2gq4n0wH5-QOABOp_54zQCY129BhNA2MgL387Dbz2zwxOFOxV_YZwwWzZvF1sbB5F9t5zWbsSzfr0Y6wt7p3gO0yIxwI7kdVU6acx3zhaQgnc0436X-2BBamwWIfqsVBSux60uqmr601g7_ZOSIMnjS82u151r1JWtuBeOyku6mv8kq_mvS660R590YwRIQtjsIQofkUfmr4l9MWYi53R8QB8quQ34bx1k2d5dutR0SvlMb9MJ2loRspzjqiq1aryc75_kRMF1zJZUmqJ2F8QXwMOIFopV1V6xuubrh8kysOzoy93MpQpU2n_mdx6FqscFVnnsof_pVQvUy299zdVpYagsuXOZmf7yXrX9aQW-6bcdenl0RjxeZ-JyB1x9s-Xz4ZfQwlZMYh7Y6-8OWStS82JtrBI-yorazsZF-mx8eRjwqw8m4Mw64e7wiFStOpX74_borXdlaw8I-osrXllqMsyZk19pf6zFfm9km9t-vmnvhFt3Jm89csVBMadM9OajUmpJwJ4sbXB2Vt-mvWdi7SX_6ht7kSB_resdQltaijxQ_r5l7Mg7tUwIliM_OBV20VlvS5WR0r3in96bmve9enZ9tFkuYb-09_VrqJ5J-4wnglaeqk68B6fwxiJ60_9YnviFb3Q19he5SknSuXO1BwwcYeb1"


@functions_framework.http
def generate_image(request):
    """HTTP Cloud Function to interact with GCP endpoint for image generation.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text or a JSON object.
    """
    request_json = request.get_json(silent=True)
    
    # Validate incoming request
    if not request_json or 'text' not in request_json:
        return 'Invalid request. "text" key is required.', 400

    text_prompt = request_json['text']
    
    # Prepare the request payload for the GCP endpoint
    payload = {
        "instances": [{"text": text_prompt}]
    }

    # Set the headers with authentication
    headers = {
        "Authorization": f"Bearer {GOOGLE_CLOUD_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        # Send request to the GCP endpoint
        response = requests.post(PREDICT_URL, json=payload, headers=headers)
        response_data = response.json()

        # Check for errors
        if response.status_code != 200:
            return response_data, response.status_code

        # Extract the base64 image from the response
        predictions = response_data.get("predictions", [])
        if not predictions:
            return {"error": "No predictions returned."}, 500

        base64_image = predictions[0].get("output", "")
        return {
            "text": text_prompt,
            "image_base64": base64_image
        }

    except exceptions.GoogleAuthError as auth_error:
        return {"error": str(auth_error)}, 500
    except Exception as e:
        return {"error": str(e)}, 500
