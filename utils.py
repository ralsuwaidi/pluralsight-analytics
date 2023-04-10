import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from models.user import User, Skill

from api.plural import PluralSight
from api.codershq import Codershq


def main():
    chq = Codershq()
    auth = {"email": os.getenv("ADMIN_EMAIL"), "password": os.getenv("ADMIN_PASSWORD")}

    chq.login(auth)

    all_chq_users = chq.all_users()["data"]

    all_skills = PluralSight.all_skills()
    all_users = PluralSight.all_p_users()
    print("all users", len(all_users))

    # add psid
    for user in all_chq_users:
        for p_user in all_users:
            p_user_id = p_user["email"].split("@")[0]
            try:
                if int(p_user_id) == user["fields"]["user"]:
                    user["ps_id"] = p_user["id"]
            except:
                pass

    # get skill for every user based on ps_id
    for user in all_chq_users:
        for p_user in all_users:
            p_user_id = p_user["email"].split("@")[0]
            try:
                if int(p_user_id) == user["fields"]["user"]:
                    # user['skills'] = PluralSight.get_user_skill(int(p_user_id))
                    user["ps_id"] = p_user["id"]
                    user["skills"] = PluralSight.get_user_skill_psid(user["ps_id"])

            except:
                pass

    # fix dict
    for user in all_chq_users:
        try:
            user["skills"] = user["skills"]["data"]["skillAssessmentResults"]["nodes"]
        except:
            pass

    # remove anyone without a test
    only_skills = []
    for user in all_chq_users:
        try:
            user["skills"][0]
            only_skills.append(user)
        except:
            pass

    for user in only_skills:
        user["pk"] = user["fields"]["user"]

    json_object = json.dumps(only_skills, indent=4)

    # Writing to sample.json
    with open("users.json", "w") as outfile:
        outfile.write(json_object)


def json_to_user(data):
    """
    convert json list to user
    """
    user_list = []
    for user_item in data:
        skill_list = []
        for skill_item in user_item["skills"]:
            skill = Skill(**skill_item)
            skill_list.append(skill)
        user = User(**user_item["fields"], skills=skill_list)
        user_list.append(user)
    return user_list


def flatten_json(json_list):
    """
    make skill per user
    """

    user_list = []
    for user in json_list:
        # loop over every skill
        for skill in user["skills"]:
            data = {**user["fields"], **skill}
            data["pk"] = user["pk"]
            data["ps_id"] = user["ps_id"]
            user_list.append(data)

    return user_list


if __name__ == "__main__":
    main()
