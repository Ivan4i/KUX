"""Notion API Client - manages lead/task data from Notion database with multi-channel support"""

import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime
from notion_client import AsyncClient
from loguru import logger

from ..config import get_settings


class NotionClient:
    """Manages integration with Notion database for leads and multi-channel messaging"""

    # Channel checkbox mappings
    CHANNEL_CHECKBOXES = {
        "whatsapp": "Sent via WhatsApp",
        "sms": "Sent via SMS",
        "max": "Sent via MAX",
        "telegram": "Sent via Telegram"
    }

    def __init__(self):
        """Initialize Notion client"""
        settings = get_settings()
        self.client = AsyncClient(auth=settings.notion_api_key)
        self.database_id = settings.notion_database_id
        self._cache: Dict[str, Dict] = {}  # Simple cache for tasks
        self._lead_cache: Dict[str, Dict] = {}  # Cache for lead data

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
        Parse Notion page into task dict with full lead data

        Args:
            page: Notion page object

        Returns:
            dict: Parsed task data, or None if invalid
        """
        try:
            properties = page.get('properties', {})

            # Extract core task fields
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
                'notes': self._get_text_property(properties, 'Notes'),

                # Extended lead data for personalization
                'company': self._get_text_property(properties, 'Company'),
                'website': self._get_url_property(properties, 'Website'),
                'rusprofile_url': self._get_url_property(properties, 'RusProfile URL'),
                'revenue': self._get_number_property(properties, 'Revenue'),
                'profit': self._get_number_property(properties, 'Profit'),
                'industry': self._get_select_property(properties, 'Industry'),
                'region': self._get_select_property(properties, 'Region'),

                # Channel tracking
                'sent_via_whatsapp': self._get_checkbox_property(properties, 'Sent via WhatsApp'),
                'sent_via_sms': self._get_checkbox_property(properties, 'Sent via SMS'),
                'sent_via_max': self._get_checkbox_property(properties, 'Sent via MAX'),
                'sent_via_telegram': self._get_checkbox_property(properties, 'Sent via Telegram'),

                # Response tracking
                'response_received': self._get_checkbox_property(properties, 'Response Received'),
                'response_date': self._get_date_property(properties, 'Response Date'),
                'conversion_status': self._get_select_property(properties, 'Conversion Status')
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

    def _get_url_property(self, properties: Dict, key: str, default: str = "") -> str:
        """Extract URL property"""
        prop = properties.get(key, {})
        return prop.get('url', default) or default

    def _get_checkbox_property(self, properties: Dict, key: str, default: bool = False) -> bool:
        """Extract checkbox property"""
        prop = properties.get(key, {})
        return prop.get('checkbox', default)

    async def update_channel_sent(
        self,
        notion_id: str,
        channel: str,
        sent: bool = True,
        sent_date: Optional[str] = None
    ) -> bool:
        """
        Update channel-specific sent checkbox in Notion

        Args:
            notion_id: Notion page ID
            channel: Channel type (whatsapp, sms, max, telegram)
            sent: Whether message was sent via this channel
            sent_date: Optional sent date (ISO format)

        Returns:
            bool: True if successful
        """
        try:
            checkbox_name = self.CHANNEL_CHECKBOXES.get(channel.lower())
            if not checkbox_name:
                logger.warning(f"⚠️ Unknown channel: {channel}")
                return False

            properties: Dict[str, Any] = {
                checkbox_name: {
                    "checkbox": sent
                }
            }

            if sent_date:
                properties[f"{channel.capitalize()} Sent Date"] = {
                    "date": {
                        "start": sent_date
                    }
                }

            await self.client.pages.update(
                page_id=notion_id,
                properties=properties
            )

            logger.success(f"✅ Updated Notion: {notion_id} sent via {channel}")
            return True

        except Exception as e:
            logger.error(f"❌ Error updating channel sent in Notion: {e}")
            return False

    async def get_leads_for_channel(
        self,
        channel: str,
        limit: int = 50,
        exclude_sent: bool = True
    ) -> List[Dict]:
        """
        Get leads that haven't been contacted via specific channel

        Args:
            channel: Channel type (whatsapp, sms, max, telegram)
            limit: Maximum leads to fetch
            exclude_sent: Exclude leads already contacted via this channel

        Returns:
            List of leads
        """
        try:
            checkbox_name = self.CHANNEL_CHECKBOXES.get(channel.lower())
            if not checkbox_name:
                logger.warning(f"⚠️ Unknown channel: {channel}")
                return []

            # Build filter
            filter_conditions = {
                "and": [
                    {
                        "property": "Status",
                        "status": {
                            "does_not_equal": "Completed"
                        }
                    }
                ]
            }

            if exclude_sent:
                filter_conditions["and"].append({
                    "property": checkbox_name,
                    "checkbox": {
                        "equals": False
                    }
                })

            response = await self.client.databases.query(
                database_id=self.database_id,
                filter=filter_conditions,
                sorts=[
                    {"property": "Priority", "direction": "descending"},
                    {"property": "Created Date", "direction": "ascending"}
                ],
                page_size=limit
            )

            leads = []
            for page in response.get('results', []):
                lead = self._parse_notion_page(page)
                if lead:
                    leads.append(lead)
                    self._lead_cache[lead['notion_id']] = lead

            logger.info(f"📥 Found {len(leads)} leads for {channel} channel")
            return leads

        except Exception as e:
            logger.error(f"❌ Error fetching leads for channel: {e}")
            return []

    async def get_lead_for_personalization(self, notion_id: str) -> Optional[Dict]:
        """
        Get full lead data for LLM personalization

        Args:
            notion_id: Notion page ID

        Returns:
            Lead data dict with all fields for personalization
        """
        # Check cache first
        if notion_id in self._lead_cache:
            return self._lead_cache[notion_id]

        try:
            page = await self.client.pages.retrieve(page_id=notion_id)
            lead = self._parse_notion_page(page)

            if lead:
                self._lead_cache[notion_id] = lead

            return lead

        except Exception as e:
            logger.error(f"❌ Error fetching lead for personalization: {e}")
            return None

    async def mark_response_received(
        self,
        notion_id: str,
        channel: str,
        response_date: Optional[str] = None
    ) -> bool:
        """
        Mark that a response was received from lead

        Args:
            notion_id: Notion page ID
            channel: Channel where response was received
            response_date: Date of response (ISO format, defaults to now)

        Returns:
            bool: True if successful
        """
        try:
            if not response_date:
                response_date = datetime.utcnow().isoformat()

            properties = {
                "Response Received": {"checkbox": True},
                "Response Date": {"date": {"start": response_date}},
                "Response Channel": {"select": {"name": channel.capitalize()}}
            }

            await self.client.pages.update(
                page_id=notion_id,
                properties=properties
            )

            logger.success(f"✅ Marked response received: {notion_id} via {channel}")
            return True

        except Exception as e:
            logger.error(f"❌ Error marking response: {e}")
            return False

    def clear_cache(self):
        """Clear all caches"""
        self._cache.clear()
        self._lead_cache.clear()
        logger.info("🗑️ Cleared Notion client caches")


# Global instance
notion_client = NotionClient()
