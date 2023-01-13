from typing import Dict
from flask import jsonify
from flask import request
from flask import Blueprint
from katatachi.content import ContentStore
from katatachi.mod_view import ModViewRenderer
from katatachi.mod_view import ModViewStore


def mod_view_blueprint_factory(
        mod_view_store: ModViewStore,
        content_store: ContentStore,
        mod_view_renderer: ModViewRenderer,
):
    blueprint = Blueprint('mod_view', __name__)

    @blueprint.route("", methods=["GET"])
    def _get_boards():
        boards = []
        for (board_id, board_query) in mod_view_store.get_all():
            boards.append(
                {
                    "board_id": board_id,
                    "board_query": board_query.to_dict(),
                    "count": content_store.count(board_query.query),
                }
            )
        return jsonify(boards), 200

    def render_board(board_id: str):
        board_query = mod_view_store.get(board_id)
        return (
            jsonify(
                {
                    "board_query": board_query.to_dict(),
                    "payload": mod_view_renderer.render_as_dict(board_query),
                    "count": content_store.count(board_query.query),
                }
            ),
            200,
        )

    @blueprint.route("render/<string:board_id>", methods=["GET"])
    def _render_board(board_id: str):
        return render_board(board_id)

    @blueprint.route("callback/<string:board_id>/<string:callback_id>", methods=["POST"])
    def _callback_board(board_id: str, callback_id: str):
        document = request.json  # type: Dict
        mod_view_renderer.callback(callback_id, document)
        return render_board(board_id)

    return blueprint
