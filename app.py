from fitbit import fitbit
import argparse
import datetime
import json
import os

parser = argparse.ArgumentParser(
    prog="fitbit", 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

subprasers = parser.add_subparsers(
    title="Available commands", 
    dest="command", 
    required=True, 
    help="<Required> Select the command to run"
)

unauth = subprasers.add_parser(
    "unauth", 
    help="unauth", 
    aliases=["u"], 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
authd = subprasers.add_parser(
    "authd", 
    help="authd", 
    aliases=["a"], 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

args = parser.parse_args()
if args.command == "unauth" or args.command == "u":
    # unauthenticated client
    fitbit_obj = fitbit.Fitbit("23BJ8J", "3dfa10d04abfa792e90d8316cccb9991")
    url, _ = fitbit_obj.client.authorize_token_url()
    # Step 1: the url is for authorization
    print(url)
    # then the fitbit returns something like this:
    # https://cap.gura.ch/fitbit_callback?code=4e326bc35f6dc001e0344ec044495d78b2f32e30&state=CItaLg1tzKAsYbKpQTUxYXfAw1qlIx#_=_
    url = input("Paste the url here: ")
    code = url.split("code=")[1].split("&")[0]
    # Step 2: acquire the code from the url
    fitbit_obj.client.fetch_access_token(code)
    print("You are authorized to access data for the user: {}".format(fitbit_obj.user_profile_get()["user"]["fullName"]))
    print("TOKEN\n=====\n")
    token_dict = json.dumps(fitbit_obj.client.session.token, indent=4)
    with open("token_dict.json", "w") as f:
        f.write(token_dict)
    print(token_dict)
elif args.command == "authd" or args.command == "a":
    # if revoked, InvalidGrantError will be raised
    def token_updater(token_dict):
        # should save the updated token for the user
        with open("token_dict.json", "w") as f:
            json.dump(token_dict, f, indent=4)
    with open('token_dict.json') as f:
        token_dict = json.load(f)
    # set the expire time to the past to update the token
    # Note here: typically the token expires in 8 hours, the system should use cron job to update the token
    token_dict["expires_at"] = datetime.datetime.now().timestamp() - 1
    fitbit_obj = fitbit.Fitbit(
        "23BJ8J",
        "3dfa10d04abfa792e90d8316cccb9991",
        access_token=token_dict["access_token"],
        refresh_token=token_dict["refresh_token"],
        expires_at=token_dict["expires_at"],
        refresh_cb=token_updater
    )
    """
        Data to use:
        - User profile
        - Activity
        - Heartrate
        - Sleep
    """
    """
        User profile
    """
    print("========USER PROFILE========")
    profile = json.dumps(fitbit_obj.user_profile_get(), indent=4)
    with open("profile.json", "w") as f:
        f.write(profile)
    print(profile)
    """
        Activity
    """
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========ACTIVITY========")
    # Get Activity Daily Goals
    print("========Get Activity Daily Goals========")
    activities_daily_goal = json.dumps(fitbit_obj.activities_daily_goal(), indent=4)
    with open("activities_daily_goal.json", "w") as f:
        f.write(activities_daily_goal)
    print(activities_daily_goal)
    # Get Activity Weekly Goals
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Activity Weekly Goals========")
    activities_weekly_goal = json.dumps(fitbit_obj.activities_weekly_goal(), indent=4)
    with open("activities_weekly_goal.json", "w") as f:
        f.write(activities_weekly_goal)
    print(activities_weekly_goal)
    # Get Activity Stats
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Activity Stats========")
    activity_stats = json.dumps(fitbit_obj.activity_stats(), indent=4)
    with open("activity_stats.json", "w") as f:
        f.write(activity_stats)
    print(activity_stats)
    # Get Activities List
    # What data is this?
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Activities List========")
    activities_list = json.dumps(fitbit_obj.activities_list(), indent=4)
    with open("activities_list.json", "w") as f:
        f.write(activities_list)
    print(activities_list)
    # Get Activity Detail
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Activity Detail========")
    id = input("Enter the activity id: ")
    activity_detail = json.dumps(fitbit_obj.activity_detail(id), indent=4)
    with open("activity_detail" + id + ".json", "w") as f:
        f.write(activity_detail)
    print(activity_detail)
    # Get Activity Time Series
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Activity Time Series========")
    activity_time_series = json.dumps(fitbit_obj.time_series("activities/tracker/steps", period="1y"), indent=4)
    # dump to file
    with open("activity_time_series.json", "w") as f:
        f.write(activity_time_series)
    print(activity_time_series)
    # Get Intraday Activity Time Series
    # No Access to intra day data as of 2021-11-25
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Intraday Activity Time Series========")
    activity_intraday_time_series = json.dumps(fitbit_obj.intraday_time_series("activities/steps"), indent=4)
    # dump to file
    with open("activity_intraday_time_series.json", "w") as f:
        f.write(activity_intraday_time_series)
    print(activity_intraday_time_series)
    """
        Heartrate
    """
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    # Get Heart Rate Time Series
    print("========Get Heart Rate Time Series========")
    heart_rate_time_series = json.dumps(fitbit_obj.time_series("activities/heart", period="1y"), indent=4)
    # dump to file
    with open("heart_rate_time_series.json", "w") as f:
        f.write(heart_rate_time_series)
    print(heart_rate_time_series)
    # Get Heart Rate Intraday Time Series
    # No Access to intra day data as of 2021-11-25
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Heart Rate Intraday Time Series========")
    heart_rate_intraday_time_series = json.dumps(fitbit_obj.intraday_time_series("activities/heart"), indent=4)
    # dump to file
    with open("heart_rate_intraday_time_series.json", "w") as f:
        f.write(heart_rate_intraday_time_series)
    print(heart_rate_intraday_time_series)
    """
        Sleep
    """
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    # Get Sleep
    print("========Get Sleep========")
    get_sleep = json.dumps(fitbit_obj.get_sleep(date=datetime.date.fromisoformat("2021-11-11")), indent=4)
    # dump to file
    with open("get_sleep.json", "w") as f:
        f.write(get_sleep)
    print(get_sleep)
    # Get Sleep Log List
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Sleep Log List========")
    get_sleep_log_list = json.dumps(fitbit_obj.get_sleep_log_list(date=datetime.date.fromisoformat("2021-11-11")), indent=4)
    # dump to file
    with open("get_sleep_log_list.json", "w") as f:
        f.write(get_sleep_log_list)
    print(get_sleep_log_list)
    # Get Sleep Time Series
    input("Press Enter to show next page")
    os.system("cls" if os.name == "nt" else "clear")
    print("========Get Sleep Time Series========")
    # Only supports date range
    get_sleep_time_series = json.dumps(fitbit_obj.time_series("sleep", base_date="2021-10-10", end_date="2021-11-24"), indent=4)
    # dump to file
    with open("get_sleep_time_series.json", "w") as f:
        f.write(get_sleep_time_series)
    print(get_sleep_time_series)
