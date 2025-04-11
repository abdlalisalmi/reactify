from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom


def index(request):
    chat_room = ChatRoom.objects.filter(is_active=True).first()
    print(chat_room, flush=True)
    if not chat_room:
        return render(
            request,
            "reactify/room.html",
            {"chat_room": None, "messages": None},
        )
    # Add user to participants if not already there
    # if (
    #     request.user.is_authenticated
    #     and request.user not in chat_room.participants.all()
    # ):
    #     chat_room.participants.add(request.user)

    messages = chat_room.messages.all().order_by("timestamp")
    return render(
        request, "reactify/room.html", {"chat_room": chat_room, "messages": messages}
    )


# def room(request, room_id):
#     chat_room = get_object_or_404(ChatRoom, id=room_id)
#     # Add user to participants if not already there
#     if request.user not in chat_room.participants.all():
#         chat_room.participants.add(request.user)

#     messages = chat_room.messages.all().order_by("timestamp")
#     return render(
#         request, "reactify/room.html", {"chat_room": chat_room, "messages": messages}
#     )
