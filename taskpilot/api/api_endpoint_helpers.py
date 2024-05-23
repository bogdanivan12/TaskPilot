"""File containing helper functions for the endpoints of the API service."""
from taskpilot.api import db_operations as db
from taskpilot.api import api_models as models
from taskpilot.common import config_info
from taskpilot.api import api_response_classes as api_resp
from taskpilot.api import api_request_classes as api_req


logger = config_info.get_logger()


def get_user(user_id: str) -> api_resp.Response:
    """
    Get a user by id
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    db_get_result = db.get_item(index, user_id)

    if not db_get_result:
        response = api_resp.Response(
            message=f"User with id '{user_id}' not found",
            code=404,
            result=False
        )
        logger.error(response.message)
        return response

    user = models.User.parse_obj(db_get_result)
    response = api_resp.Response(
        message=f"User with id '{user_id}' retrieved successfully",
        data=user
    )
    logger.info(response.message)
    return response


def create_user(user_req: api_req.CreateUserRequest) -> api_resp.Response:
    """
    Create a user
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    user_dict = user_req.dict()
    password = user_dict.pop("password")
    hashed_password = config_info.hash_password(password)
    user_dict["hashed_password"] = hashed_password
    user = models.User.parse_obj(user_dict)

    db_create_result = db.create_item(index, user.dict(), user.username)

    if not db_create_result:
        response = api_resp.Response(
            message="Failed to create user with id '{user_req.username}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{db_create_result}' created successfully",
        data={
            "username": db_create_result
        }
    )
    logger.info(response.message)
    return response
