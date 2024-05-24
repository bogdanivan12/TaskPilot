"""File containing helper functions for the endpoints of the API service."""
from taskpilot.api import db_operations as db
from taskpilot.api import api_models as models
from taskpilot.common import config_info
from taskpilot.api import api_response_classes as api_resp
from taskpilot.api import api_request_classes as api_req


logger = config_info.get_logger()


def get_user(user_id: str) -> api_resp.GetUserResponse:
    """
    Get a user by id
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    db_get_result = db.get_item(index, user_id)

    if not db_get_result:
        response = api_resp.GetUserResponse(
            message=f"User with id '{user_id}' not found",
            code=404,
            result=False
        )
        logger.error(response.message)
        return response

    user = models.User.parse_obj(db_get_result)
    response = api_resp.GetUserResponse(
        message=f"User with id '{user_id}' retrieved successfully",
        user=user
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
        message=f"User with id '{db_create_result}' created successfully"
    )
    logger.info(response.message)
    return response


def update_user(user_id: str,
                user_req: api_req.UpdateUserRequest) -> api_resp.Response:
    """
    Update a user
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    user_dict = user_req.dict()
    password = user_dict.pop("password")
    hashed_password = config_info.hash_password(password)
    user_dict["hashed_password"] = hashed_password
    user_dict["username"] = user_id
    user = models.User.parse_obj(user_dict)

    db_update_result = db.update_item(index, user_id, user.dict())

    if not db_update_result:
        response = api_resp.Response(
            message=f"Failed to update user with id '{user_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user_id}' updated successfully"
    )
    logger.info(response.message)
    return response


def delete_user(user_id: str) -> api_resp.Response:
    """
    Delete a user
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    db_delete_result = db.delete_item(index, user_id)

    if not db_delete_result:
        response = api_resp.Response(
            message=f"Failed to delete user with id '{user_id}'",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    response = api_resp.Response(
        message=f"User with id '{user_id}' deleted successfully"
    )
    logger.info(response.message)
    return response


def get_all_users() -> api_resp.GetAllUsersResponse:
    """
    Get all users
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    db_get_all_result = db.get_all_items(index)

    if db_get_all_result is None:
        response = api_resp.GetAllUsersResponse(
            message="Failed to retrieve all users",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    users = [models.User.parse_obj(user)
             for user in db_get_all_result.values()]
    response = api_resp.GetAllUsersResponse(
        message="All users retrieved successfully",
        users=users
    )
    logger.info(response.message)
    return response


def search_users(search_req: api_req.SearchUsersRequest
                 ) -> api_resp.GetAllUsersResponse:
    """
    Search for users
    """
    index = config_info.DB_INDEXES[config_info.Entities.USER]
    query_dict = search_req.dict()
    query_dict = {
        field: value
        for field, value in query_dict.items()
        if value is not None
    }

    db_search_result = db.search_items(index, query_dict)

    if db_search_result is None:
        response = api_resp.GetAllUsersResponse(
            message="Failed to search for users",
            code=424,
            result=False
        )
        logger.error(response.message)
        return response

    users = [models.User.parse_obj(user)
             for user in db_search_result.values()]
    response = api_resp.GetAllUsersResponse(
        message="Users retrieved successfully",
        users=users
    )
    logger.info(response.message)
    print(response)
    return response
