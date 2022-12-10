from PyInquirer import prompt

from dummy_client.utils.print_table import print_history_as_table


history_q = [{
    "type": "list",
    "name": "history_act",
    "message": "choose your action",
    "choices": ['Delete', 'Quit']
}]

hist_id_q = [{
    "type": "input",
    "name": "hist_id",
    "message": "Type history ID to delete."
}]


def history_seq(service, my_channel_num):
    chan_service = service["channelService"]

    # fetch history watched by user has my_channel_num as chanId
    res = chan_service.watch_history(my_channel_num)

    if res == 0:
        print('Failed to fetch history. Try again.')
        return 0

    while True:
        # print history as table
        print_history_as_table(res)

        # inquire
        answer = prompt(history_q)

        if answer.get("history_act") == "Delete":
            answer = prompt(hist_id_q)
            hist_id = answer.get("hist_id")
            res = chan_service.delete_history(hist_id)

            if res == 0:
                print("Deletion failed.")
                continue

            return 0

        else:
            print("Return to main menu.")
            return 0
