import requests


def post_tasks(time, url, app_id, user_id="1", algorithm="1", coverage_switch="0"):
    data = dict()
    data["app_id"] = app_id
    data["user_id"] = user_id
    data["algorithm"] = algorithm
    data["coverage_switch"] = coverage_switch
    data["time"] = time
    response = requests.post(url=url, data=data)
    # json = response.json()
    print(response.status_code)
    print(response)


if __name__ == "__main__":
    url = "http://114.212.86.174:9002/run_app"
    for i in range(100):
        post_tasks(time=1800, url=url, app_id=4)
