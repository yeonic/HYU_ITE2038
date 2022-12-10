from PyInquirer import prompt

from dummy_client.utils.print_table import print_my_playlist_table, print_videos_in_playlist

my_pl_q = [{
    "type": "list",
    "name": "pl_task",
    "message": "Choose task you want.",
    "choices": ["Watch playlist","Create", "Delete",
                "Rename", "Change open scope", "Quit"]
}]

pl_id = {
    "type": "input",
    "name": "pl_id",
    "message": "Type playlist ID to do task with"
}


def my_playlist_seq(service, chen_id):
    pl_service = service["plService"]

    # print playlist
    pl_list = pl_service.get_my_playlists(chen_id)
    print_my_playlist_table(pl_list)

    while True:
        answer = prompt(my_pl_q)
        pl_task = answer.get("pl_task")

        # watch playlist
        if pl_task == "Watch playlist":
            answer = prompt([pl_id])
            to_watch = answer.get("pl_id")

            res = pl_service.watch_playlist(to_watch)
            if res == 0:
                print("Failed to load videos.")
                continue

            print_videos_in_playlist(res)
            print()
            return 0

        # create playlist
        elif pl_task == "Create":
            answer = prompt([{
                "type": "input",
                "name": "pl_name",
                "message": "Type playlist name."
            }])
            pl_name = answer.get("pl_name")
            res = pl_service.create_playlist(chen_id, pl_name)

            if res == 0:
                print("Creation Failed. Try again.")
                continue

            print("Playlist created successfully.")
            return 0

        # delete playlist
        elif pl_task == "Delete":
            answer = prompt([pl_id])
            del_id = answer.get("pl_id")

            res = pl_service.delete_playlist(del_id)
            if res == 0:
                print("Failed to delete playlist.")
                continue

            print("Playlist deleted successfully.")
            return 0

        # rename
        elif pl_task == "Rename":
            answer = prompt([pl_id])

            answer2 = prompt([{
                "type": "input",
                "name": "new_name",
                "message": "Type new name for playlist."
            }])

            ren_id = answer.get("pl_id")
            new_name = answer2.get("new_name")

            res = pl_service.rename_playlist(int(ren_id), new_name)
            if res == 0:
                print("Rename failed.")
                continue

            print("Renamed playlist successfully.")
            return 0

        # change open_code
        elif pl_task == "Change open scope":
            answer = prompt([pl_id, {
                "type": "list",
                "name": "pl_opcode",
                "message": "Choose open scope.",
                "choices": ["global", "private"]
            }])

            list_id = answer.get("pl_id")
            pl_opcode = answer.get("pl_opcode")

            if pl_opcode == "global":
                res = pl_service.change_open_code(0, list_id)
                if res == 0:
                    print("Failed to change scope.")
                    continue

                print("The playlist now set global.")
                return 0

            else:
                res = pl_service.change_open_code(1, list_id)
                if res == 0:
                    print("Failed to change scope.")
                    continue
                print("The playlist now set local.")
                return 0

        # quit
        else:
            print("Return to menu.")
            return 0
