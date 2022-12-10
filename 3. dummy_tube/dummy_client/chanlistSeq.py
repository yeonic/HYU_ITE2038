from PyInquirer import prompt
from cli_tables.cli_tables import *

chan_action_q = [{
    "type": "list",
    "name": "action",
    "message": "What action do you want to do?",
    "choices": ["Select", "Create", "Delete"]
}]

chen_id_dict = {
    "type": "input",
    "name": "chanId",
    "message": "Select ID of a channel to join DummyTube:"
}


def chanlist_seq(services, current_user):
    user_service = services["userService"]
    channel_service = services["channelService"]
    user_id = current_user["userId"]

    while True:
        # fetch channel_list first
        channel_list = user_service.get_channel_list(user_id)

        if channel_list == 0:
            return 0

        print_channel_as_table(channel_list)

        # Print inquire, and resolve
        answer = prompt(chan_action_q)
        action = answer.get("action")

        if action == "Select":
            answer = prompt([chen_id_dict])
            selected_id = answer.get("chanId")
            return int(selected_id)

        elif action == "Create":
            answer = prompt([{
                "type": "input",
                "name": "new_name",
                "message": "Type your new channel name."
            }])
            new_name = answer.get("new_name")
            # do name check
            overlap = channel_service.check_name_overlap(new_name)
            if overlap is not None:
                print("Name is overlapped. Try other name.")
                continue

            chan_count_dict = channel_service.get_channel_count(user_id)
            chan_count = chan_count_dict["chanCount"]
            res = channel_service.create_channel(new_name, user_id, chan_count)

            if res == 0:
                print("Failed to create new channel.")

            print("Created new channel successfully.")

        else:
            answer = prompt([chen_id_dict])
            chen_id = int(answer.get("chanId"))

            res = 0
            if len(channel_list) > 1:
                res = user_service.delete_channel(user_id, chen_id)
                if res == 0:
                    print("Channel deletion failed.")
                    continue
            else:
                print('[Deletion fail]At least 1 channel should be exist.')
                continue

            if res == 0:
                print('[Deletion fail]Something has gone wrong.')

            print("Channel deleted successfully.")
            continue


def print_channel_as_table(channel_list):
    # Print channel list as table.
    table = [['ID', 'Channel_name']]
    for channel in channel_list:
        table.append([str(channel["chanId"]), channel["channelName"]])

    print("\nCHANNEL LISTS")
    print_table(table)
