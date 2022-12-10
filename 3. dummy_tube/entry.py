from PyInquirer import prompt

from dummy_server.dbConn import DbConn
from dummy_client.initSeq import initial_seq
from dummy_client.chanlistSeq import chanlist_seq
from dummy_client.feedSeq import feed_seq

from dummy_client.chanInfoSeq import my_chen_info_seq

from dummy_server.services.userService import *
from dummy_server.services.channelService import *
from dummy_server.services.videoService import *
from dummy_server.services.plService import *


def main():
    # initializing services
    db = DbConn()
    current_user = {}
    services = {
        "userService": UserService(db),
        "channelService": ChannelService(db),
        "videoService": VideoService(db),
        "plService": PlService(db)
    }

    # test boilerplate
    # end of boilerplate

    # do initial sequence
    # includes sing in, sign up
    # when sign up ends successfully.
    # move to next sequence
    init_res = initial_seq(services)
    if init_res == 0:
        return 0

    # set current user id token
    current_user["userId"] = init_res

    # channel list sequence
    cl_res = chanlist_seq(services, current_user)
    if cl_res == 0:
        return 0

    # set current channel id token
    current_user["channelId"] = cl_res

    # main sequence
    while True:
        q_name = "selected_menu"
        answer = prompt([{
            "type": "list",
            "name": q_name,
            "message": "Choose menu you want.",
            "choices": ["Feed", "My channel", "Create video", "Quit"]
        }])

        fet_answer = answer.get(q_name)

        if fet_answer == "Feed":
            feed_seq(services, current_user)
            continue

        elif fet_answer == "My channel":
            print(current_user["channelId"])
            my_chen_info_seq(services, current_user["channelId"])
            continue

        elif fet_answer == "Create video":
            video_service = services["videoService"]
            chen_id = current_user["channelId"]

            answer = prompt([{
                "type": "input",
                "name": "video_title",
                "message": "type your title"
            }, {
                "type": "input",
                "name": "video_detail",
                "message": "describe your video"
            }])

            video_title = answer.get("video_title")
            video_detail = answer.get("video_detail")

            res = video_service.create_video(chen_id, video_title, video_detail)
            if res == 0:
                print("Failed to create video.")

            print("Created video successfully.")
            continue
        else:
            break

    print("Hope to see you again ;)")


if __name__ == "__main__":
    main()



