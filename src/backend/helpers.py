def select_sorter(response_data):
    data = []
    for i in response_data:
        data.append([i["Corporation Name"], i["Corporation Ticker value"], i["votes"], i["graphLink"]])
    return data
