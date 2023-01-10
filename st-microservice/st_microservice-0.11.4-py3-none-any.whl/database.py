from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class AsyncDBMiddleware(BaseHTTPMiddleware):
    """ Will start a DB Session at every request and commit or rollback in the end """
    def __init__(self, app, database_uri: str):
        super().__init__(app)
        self.engine = create_async_engine(database_uri, connect_args={'timeout': 5})

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        async with self.engine.connect() as connection:
            request.state.db = connection

            # Continue with request
            response = await call_next(request)

            if hasattr(request.state, 'errors'):
                await connection.rollback()
            else:
                try:  # Try to commit
                    await connection.commit()
                except SQLAlchemyError:
                    await connection.rollback()
                    return JSONResponse({'errors': 'Error while commiting to Database'}, status_code=500)  # Todo: adopt graphql spec
            return response
