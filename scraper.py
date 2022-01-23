from linkedin_api import Linkedin, linkedin
from requests.cookies import cookiejar_from_dict
import re


def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


def get_linkedin_data(user_id):
    # Authenticate using any Linkedin account credentials
    cookies = cookiejar_from_dict(
        {
            "liap": "true",
            "li_at": 'AQEDATiU6vsCs2AqAAABfY6ajFQAAAF9sqcQVE4AOmhPSIJiVzoQODl2-6GPb_Evoww4DnE3VJVuR-MW5Hn36YpsBNBegEQInAAJnYaQEj52bLjzOYlY-jOtHgBGWdu791dFnSaHpC2TmkbXDIdLX8Mu',
            "JSESSIONID": "ajax:1921697886900276652",
        }
    )
    # api = Linkedin("ab1jidge@gmail.com", "Asj@1998")
    api = Linkedin("", "", cookies=cookies)
    # GET a profile
    profile = api.get_profile(user_id)
    # Extract details
    data = {}
    # data['name'] = profile['firstName'] +' '+ profile['lastName']
    # data['headline'] = profile['headline']
    # data['location'] = profile['geoLocationName']

    try:
      data['summary'] = deEmojify(profile['summary'])

    except:
      data['summary'] = ''

    try:
        data['name'] = deEmojify(profile['firstName'] +' '+ profile['lastName'])
    except:
        data['name'] = ""

    try:
        data['headline'] = deEmojify(profile['headline'])
    except:
        data['headline'] = ""

    try:
        data['location'] = deEmojify(profile['geoLocationName'])
    except:
        data['location'] = ""


    experiences = profile['experience']
    experience_data = []
    for experience in experiences:
        temp_dict = {}
        if 'locationName' in experience:
            temp_dict['locationName'] = deEmojify(experience['locationName']),
        else:
            print('locationName not found')
        if 'companyName' in experience:
            temp_dict['companyName'] = deEmojify(experience['companyName']),
        else:
            print('companyName not found')
        if 'title' in experience:
            temp_dict['title'] = deEmojify(experience['title']),
        else:
            print('title not found')
        experience_data.append(temp_dict)
    try:
        data['current_company'] = deEmojify(experience_data[0]['companyName'][0])
        data['current_role'] = deEmojify(experience_data[0]['title'][0])
    except:
        data['current_company'] = ''
        data['current_role'] = ''
    return(data)