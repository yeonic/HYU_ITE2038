from PyInquirer import prompt
from cli_tables.cli_tables import *

chan_action_q = [{
    "type": "list",
    "name": "action",
    "message": "What action do you want to do?",
    "choices": ["Select", "Delete"]
}, {
    "type": "input",
    "name": "chanId",
    "message": "Select ID of a channel to join DummyTube:"
}]


def chanlist_seq(services, current_user):
    user_service = services["userService"]
    user_id = current_user["userId"]

    # fetch channel_list first
    channel_list = user_service.get_channel_list(user_id)

    if channel_list == 0:
        return 0

    print_channel_as_table(channel_list)

    # Print inquire, and resolve
    answer = prompt(chan_action_q)
    selected_id = answer.get("chanId")

    if answer.get("action") == "Select":
        return selected_id

    else:
        res = 0
        if len(channel_list) > 1:
            res = user_service.delete_channel()
        else:
            print('[Deletion fail]At least 1 channel should be exist.')
            chanlist_seq(services, current_user)

        if res == 0:
            print('[Deletion fail]Something has gone wrong.')
        chanlist_seq(services, current_user)


def print_channel_as_table(channel_list):
    # Print channel list as table.
    table = [['ID', 'Channel_name']]
    for channel in channel_list:
        table.append([str(channel["chanId"]), channel["channelName"]])

    print("\nCHANNEL LISTS")
    print_table(table)
