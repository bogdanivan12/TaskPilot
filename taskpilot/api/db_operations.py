"""Database operations for the application"""
import uuid

from typing import Any, Dict, Optional
from elasticsearch import Elasticsearch

from taskpilot.common import config_info


logger = config_info.get_logger()


def get_connection() -> Optional[Elasticsearch]:
    """Get connection to the database"""
    try:
        conn = Elasticsearch(config_info.DB_URL)
        logger.info("Generated Elasticsearch client")
    except Exception as exception:
        logger.error(f"Failed to generate Elasticsearch client: {exception}")
        conn = None
    return conn


def get_item(index: str, item_id: str) -> Dict[str, Any]:
    """Get an item from the database"""
    conn = get_connection()
    try:
        item = conn.get(index=index, id=item_id)
        item_dict = item.body["_source"]
        logger.info(
            f"Retrieved item with id {item_id} from index {index}: {item_dict}"
        )
    except Exception as exception:
        logger.error(
            f"Failed to retrieve item with id {item_id} from index {index}:"
            f" {exception}"
        )
        item_dict = {}
    return item_dict


def get_all_items(index: str) -> Dict[str, Dict[str, Any]]:
    """Get all items from the database"""
    conn = get_connection()
    try:
        items = conn.search(index=index)
        items_dict = {
            item["_id"]: item["_source"]
            for item in items["hits"]["hits"]
        }
        logger.info(f"Retrieved all items from index {index}: {items_dict}")
    except Exception as exception:
        logger.error(
            f"Failed to retrieve all items from index {index}: {exception}"
        )
        items_dict = {}
    return items_dict


def create_item(index: str,
                item: Dict[str, Any],
                item_id: Optional[str] = None) -> Optional[str]:
    """Create an item in the database"""
    if not item_id:
        item_id = str(uuid.uuid4())
    conn = get_connection()
    try:
        response = conn.index(
            index=index,
            id=item_id,
            body=item,
            op_type="create"
        )
    except Exception as exception:
        logger.error(
            f"Failed to create item with id {item_id} in index {index}:"
            f" {exception}"
        )
        return None
    logger.info(f"Created item with id {item_id} in index {index}: {item}")
    return response["_id"] if response["result"] == "created" else None


def update_item(index: str, item_id: str, item: Dict[str, Any]) -> bool:
    """Update an item in the database"""
    conn = get_connection()
    try:
        response = conn.update(
            index=index,
            id=item_id,
            body={
                "doc": item
            }
        )
    except Exception as exception:
        logger.error(
            f"Failed to update item {item_id} in index {index}: {exception}"
        )
        return False
    logger.info(f"Updated item {item_id} in index {index}: {item}")
    return response["result"] == "updated"


def delete_item(index: str, item_id: str) -> bool:
    """Delete an item from the database"""
    conn = get_connection()
    try:
        response = conn.delete(index=index, id=item_id)
    except Exception as exception:
        logger.error(
            f"Failed to delete item {item_id} from index {index}: {exception}"
        )
        return False
    logger.info(f"Deleted item {item_id} from {index}")
    return response["result"] == "deleted"


def search_items(index: str,
                 query_dict: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Search for items in the database"""
    if not query_dict:
        return get_all_items(index)
    conn = get_connection()
    try:
        query_body = {
            "query": {
                "bool": {
                    "filter": [
                        {"match": {field: value}}
                        for field, value in query_dict.items()
                    ]
                }
            }
        }
        items = conn.search(index=index, body=query_body)
        items_dict = {
            item["_id"]: item["_source"]
            for item in items["hits"]["hits"]
        }
        logger.info(f"Retrieved items from index {index} that satisfy the"
                    f" query {query_dict}: {items_dict}")
    except Exception as exception:
        logger.error(
            f"Failed to retrieve items from index {index} that satisfy the"
            f" query {query_dict}: {exception}"
        )
        items_dict = {}
    return items_dict
