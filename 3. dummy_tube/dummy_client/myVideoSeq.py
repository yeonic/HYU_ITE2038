from PyInquirer import prompt

from dummy_client.utils.print_table import print_video_as_table, print_playlist_as_table


my_videos_q = [{
    "type": "list",
    "name": "mv_action",
    "message": "Choose your action.",
    "choices": ["Edit video details.", "Add to playlist",
                "Delete Video", "Quit"]
}]

video_id_q = {
    "type": "input",
    "name": "video_id",
    "message": "Type video id to do task."
}


def my_video_seq(service, chen_id):
    # print video list
    video_service = service["videoService"]
    pl_service = service["plService"]

    video_list = video_service.get_others_videos_to_feed(chen_id)

    while True:
        print_video_as_table(video_list)

        # inquire
        answer = prompt(my_videos_q)
        mv_action = answer.get("mv_action")

        if mv_action == "Edit video details.":
            answer = prompt([video_id_q])
            answer1 = prompt([{
                "type": "input",
                "name": "new_detail",
                "message": "Type new video detail you want."
            }])

            video_id = answer.get("video_id")
            new_detail = answer1.get("new_detail")

            res = video_service.update_video_detail(video_id, new_detail)
            if res == 0:
                print("Update detail failed.")
                continue

            print("Updated detail successfully.\n")
            return 0

        elif mv_action == "Add to playlist":
            list_pl = pl_service.get_my_playlist(chen_id)
            if list_pl is None:
                print("No playlist exists. Create it first.")
                continue

            print_playlist_as_table(list_pl)
            answer = prompt([video_id_q, {
                "type": "input",
                "name": "added_to",
                "message": "Type playlist ID to add video."
            }])

            pl_id = answer.get("added_to")
            vid_id = answer.get("video_id")
            res = video_service.add_to_playlist(pl_id, vid_id)

            if res == 0:
                print("Failed to add to playlist.")
                continue

            print("Added to playlist successfully.\n")
            return 0

        elif mv_action == "Delete Video":
            answer = prompt([video_id_q])
            video_id = answer.get("video_id")

            res = video_service.delete_video(video_id)
            if res == 0:
                print("Failed to delete the video")
                continue

            print("Deleted video successfully.\n")
            return 0

        else:
            print("Return to menu\n")
            return 0
