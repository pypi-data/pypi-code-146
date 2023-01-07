"""FastApi server."""
from typing import List
from io import BytesIO

from fastapi import FastAPI, UploadFile
from fastapi.responses import Response, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ..storage import Client


class Server:
    """API server."""

    def __init__(self):
        """Initialize the FastApi server."""
        self.app = FastAPI()



        self.client = None
        self.bucket = None

    def init_obs(self, access_key, secret_key, endpoint, bucket):
        """Initialize OBS backend.

        Args:
            access_key(str): OBS access key.
            secret_key (str): OBS secret access key.
            endpoint (str): OBS server address. e.g. https://obs.cn-north-1.myhwclouds.com
        """
        self.client = Client(access_key, secret_key, endpoint)
        self.bucket = bucket


    def set_router(self):
        """Initialize the FastApi server."""
        self.app = FastAPI()

        @self.app.get("/image/{image_name}")
        async def image(image_name):
            """Get image.

            Args:
                image_name (str): image id.

            returns:
                Response : image response.
            """
            # get image
            result = self.client.get_object(self.bucket, image_name)

            if result.status < 300:
                content_type = result.body['contentType']

                # change bytes to stream
                stream = BytesIO(result.body.buffer)

                return StreamingResponse(stream, media_type=content_type)

            # return not found
            return Response(status_code=404)

        @self.app.get("/markdown")
        async def markdown(id):
            """Get markdown.

            Args:
                id (str): markdown id.

            returns:
                Response : markdown response.
            """
            return Response(b"markdown binary data", media_type="text/markdown")

        @self.app.post("/upload/")
        async def upload(files: List[UploadFile]):
            """Upload files.

            Args:
                files ( List[UploadFile] ): file to upload.
            """
            all_success = True

            for file in files:
                filename = file.filename
                content_type = file.content_type
                result = self.client.add(self.bucket, filename, content_type, file.file)
                if not result:
                    all_success = False

            return {"result": all_success}

        # **must** after all router, set cors middleware can work
        self._set_cors()

    def _set_cors(self):
        """Set CORS."""
        # set cors
        origins = [
            "*"
        ]

        # add cors middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def run(self, host, port):
        """Run the server.

        Args:
            host (str): server host.
            port (int): server port.
        """
        uvicorn.run(self.app, host=host, port=port)



