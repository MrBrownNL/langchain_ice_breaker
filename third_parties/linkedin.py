import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = os.environ.get("LINKEDIN_DEBUG_URL")
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        headers = {'Authorization': 'Bearer ' + os.environ.get("PROXYCURL_API_KEY")}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'linkedin_profile_url': linkedin_profile_url,
            'extra': 'include',
            'github_profile_id': 'include',
            'facebook_profile_id': 'include',
            'twitter_profile_id': 'include',
            'personal_contact_number': 'include',
            'personal_email': 'include',
            'inferred_salary': 'include',
            'skills': 'include',
            'use_cache': 'if-present',
            'fallback_to_cache': 'on-error',
        }
        response = requests.get(
            api_endpoint,
            params=params,
            headers=headers,
            timeout=10,
        )

    data = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", '', None)
           and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/jeroendebruijnnl/",
            mock=True,
        )
    )
