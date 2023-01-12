"""Route definitions for the main Fietsboek application."""


def includeme(config):
    # pylint: disable=missing-function-docstring
    config.add_static_view("static", "static", cache_max_age=3600)
    config.add_route("home", "/")
    config.add_route("login", "/login")
    config.add_route("logout", "/logout")
    config.add_route("browse", "/track/")

    config.add_route("static-page", "/page/{slug}")

    config.add_route("track-archive", "/track/archive")

    config.add_route("password-reset", "/password-reset")
    config.add_route("use-token", "/token/{uuid}")
    config.add_route("create-account", "/create-account")

    config.add_route("upload", "/upload")
    config.add_route(
        "preview", "/preview/{upload_id}.gpx", factory="fietsboek.models.Upload.factory"
    )
    config.add_route(
        "finish-upload", "/upload/{upload_id}", factory="fietsboek.models.Upload.factory"
    )
    config.add_route(
        "cancel-upload", "/cancel/{upload_id}", factory="fietsboek.models.Upload.factory"
    )

    config.add_route("details", "/track/{track_id}", factory="fietsboek.models.Track.factory")
    config.add_route("edit", "/track/{track_id}/edit", factory="fietsboek.models.Track.factory")
    config.add_route("gpx", "/gpx/{track_id}.gpx", factory="fietsboek.models.Track.factory")
    config.add_route(
        "invalidate-share",
        "/track/{track_id}/invalidate-link",
        factory="fietsboek.models.Track.factory",
    )
    config.add_route(
        "delete-track", "/track/{track_id}/delete", factory="fietsboek.models.Track.factory"
    )
    config.add_route(
        "add-comment", "/track/{track_id}/comment", factory="fietsboek.models.Track.factory"
    )
    config.add_route(
        "image", "/track/{track_id}/images/{image_name}", factory="fietsboek.models.Track.factory"
    )

    config.add_route("badge", "/badge/{badge_id}", factory="fietsboek.models.Badge.factory")

    config.add_route("admin", "/admin")
    config.add_route("admin-badge-add", "/admin/add-badge")
    config.add_route("admin-badge-edit", "/admin/edit-badge")
    config.add_route("admin-badge-delete", "/admin/delete-badge")

    config.add_route("profile", "/me")
    config.add_route("change-profile", "/me/personal-data")
    config.add_route("add-friend", "/me/send-friend-request")
    config.add_route("delete-friend", "/me/delete-friend")
    config.add_route("accept-friend", "/me/accept-friend")
    config.add_route("json-friends", "/me/friends.json")

    config.add_route("tile-proxy", "/tile/{provider}/{z:\\d+}/{x:\\d+}/{y:\\d+}")
