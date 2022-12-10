from PyInquirer import prompt

edit_act_q = [{
    "type": "list",
    "name": "edit_act",
    "message": "Choose your action",
    "choices": ["Edit name", "Edit intro"]
}]


def edit_info_seq(service, chan_id):
    chan_service = service["channelService"]

    while True:
        answer = prompt(edit_act_q)

        if answer.get("edit_act") == "Edit name":
            # Edit name
            answer = prompt([{
                "type": "input",
                "name": "new_name",
                "message": "Type your new name.",
            }])
            new_name = answer.get("new_name")

            # name overlap check
            overlap = chan_service.check_name_overlap(new_name)
            if overlap is not None:
                print("Name already exists.\n")
                continue

            # rename query
            res = chan_service.update_name(new_name, chan_id)
            if res == 0:
                print("Rename failed.\n")
                continue

            print("Rename succeed.\n")
            return 0

        else:
            # edit channel intro
            answer = prompt([{
                "type": "input",
                "name": "new_intro",
                "message": "Type your new intro."
            }])
            new_intro = answer.get("new_intro")
            res = chan_service.update_intro(new_intro, chan_id)

            if res == 0:
                print("Failed to update intro.\n")
                continue

            print("Update intro succeed.\n")
            return 0
