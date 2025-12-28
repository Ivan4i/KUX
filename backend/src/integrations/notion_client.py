"""Notion API Client - manages WhatsApp tasks from Notion database"""

import asyncio
from typing import List, Dict, Optional
from notion_client import AsyncClient
from loguru import logger

from ..config import get_settings


class NotionClient:
    """Manages integration with Notion database"""

    def __init__(self):
        """Initialize Notion client"""
        settings = get_settings()
        self.client = AsyncClient(auth=settings.notion_api_key)
        self.database_id = settings.notion_database_id
        self._cache: Dict[str, Dict] = {}  # Simple cache for tasks

    async def get_pending_tasks(self, limit: int = 10) -> List[Dict]:
        """
        Get pending WhatsApp tasks from Notion database

        Args:
            limit: Maximum number of tasks to fetch

        Returns:
            list: List of pending task dicts
        """
        try:
            logger.info(f"📥 Fetching pending tasks from Notion (limit: {limit})...")

            # Query database for pending tasks sorted by priority
            response = await self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Status",
                    "status": {
                        "equals": "Pending"
                    }
                },
                sorts=[
                    {
                        "property": "Priority",
                        "direction": "descending"
                    }
                ],
                page_size=limit
            )

            tasks = []

            for page in response.get('results', []):
                task = self._parse_notion_page(page)
                if task:
                    tasks.append(task)
                    # Update cache
                    self._cache[task['notion_id']] = task

            logger.success(f"✅ Fetched {len(tasks)} pending tasks from Notion")

            return tasks

        except Exception as e:
            logger.error(f"❌ Error fetching tasks from Notion: {e}")
            return []

    def _parse_notion_page(self, page: Dict) -> Optional[Dict]:
        """
        Parse Notion page into task dict

        Args:
            page: Notion page object

        Returns:
            dict: Parsed task data, or None if invalid
        """
        try:
            properties = page.get('properties', {})

            # Extract fields from Notion properties
            task = {
                'notion_id': page['id'],
                'recipient_name': self._get_text_property(properties, 'Recipient Name'),
                'phone_number': self._get_text_property(properties, 'Phone Number'),
                'message_content': self._get_text_property(properties, 'Message Content'),
                'status': self._get_status_property(properties, 'Status'),
                'device_assignment': self._get_select_property(properties, 'Device Assignment'),
                'priority': self._get_number_property(properties, 'Priority', default=5),
                'created_date': self._get_date_property(properties, 'Created Date'),
                'scheduled_send_time': self._get_date_property(properties, 'Scheduled Send Time'),
                'attempt_count': self._get_number_property(properties, 'Attempt Count', default=0),
                'notes': self._get_text_property(properties, 'Notes')
            }

            return task

        except Exception as e:
            logger.error(f"Error parsing Notion page: {e}")
            return None

    async def update_task_status(
        self,
        notion_id: str,
        status: str,
        sent_date: Optional[str] = None,
        notes: Optional[str] = None
    ) -> bool:
        """
        Update task status in Notion

        Args:
            notion_id: Notion page ID
            status: New status ("Sent", "Failed", etc.)
            sent_date: Sent date (ISO format)
            notes: Additional notes

        Returns:
            bool: True if successful
        """
        try:
            properties = {
                "Status": {
                    "status": {
                        "name": status
                    }
                }
            }

            if sent_date:
                properties["Sent Date"] = {
                    "date": {
                        "start": sent_date
                    }
                }

            if notes:
                properties["Notes"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": notes
                            }
                        }
                    ]
                }

            await self.client.pages.update(
                page_id=notion_id,
                properties=properties
            )

            logger.success(f"✅ Updated Notion task {notion_id}: status={status}")
            return True

        except Exception as e:
            logger.error(f"❌ Error updating Notion task {notion_id}: {e}")
            return False

    async def batch_update_tasks(self, updates: List[Dict]) -> int:
        """
        Batch update multiple tasks (more efficient than individual updates)

        Args:
            updates: List of update dicts with keys: notion_id, status, sent_date, notes

        Returns:
            int: Number of successful updates
        """
        logger.info(f"📤 Batch updating {len(updates)} Notion tasks...")

        # Execute updates concurrently
        tasks = []
        for update in updates:
            task = self.update_task_status(
                notion_id=update['notion_id'],
                status=update.get('status', 'Sent'),
                sent_date=update.get('sent_date'),
                notes=update.get('notes')
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        success_count = sum(1 for r in results if r is True)
        logger.success(f"✅ Batch update completed: {success_count}/{len(updates)} successful")

        return success_count

    def _get_text_property(self, properties: Dict, key: str, default: str = "") -> str:
        """Extract text property from Notion properties"""
        prop = properties.get(key, {})

        if prop.get('type') == 'title':
            title_array = prop.get('title', [])
            if title_array:
                return title_array[0].get('plain_text', default)

        elif prop.get('type') == 'rich_text':
            rich_text_array = prop.get('rich_text', [])
            if rich_text_array:
                return rich_text_array[0].get('plain_text', default)

        return default

    def _get_status_property(self, properties: Dict, key: str, default: str = "Pending") -> str:
        """Extract status property"""
        prop = properties.get(key, {})
        status_obj = prop.get('status', {})
        return status_obj.get('name', default)

    def _get_select_property(self, properties: Dict, key: str, default: str = "Auto") -> str:
        """Extract select property"""
        prop = properties.get(key, {})
        select_obj = prop.get('select', {})
        return select_obj.get('name', default)

    def _get_number_property(self, properties: Dict, key: str, default: int = 0) -> int:
        """Extract number property"""
        prop = properties.get(key, {})
        return prop.get('number', default)

    def _get_date_property(self, properties: Dict, key: str) -> Optional[str]:
        """Extract date property"""
        prop = properties.get(key, {})
        date_obj = prop.get('date', {})
        return date_obj.get('start') if date_obj else None


# Global instance
notion_client = NotionClient()
