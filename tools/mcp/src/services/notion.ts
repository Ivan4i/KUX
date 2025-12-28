/**
 * Notion Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const NOTION_API = 'https://api.notion.com/v1';

function getClient() {
  const token = getEnv('NOTIONTOKEN');
  return createServiceClient(NOTION_API, {
    'Authorization': `Bearer ${token}`,
    'Notion-Version': '2022-06-28',
  });
}

export interface NotionPage {
  id: string;
  object: 'page';
  created_time: string;
  last_edited_time: string;
  created_by: { object: string; id: string };
  last_edited_by: { object: string; id: string };
  parent: {
    type: 'database_id' | 'page_id' | 'workspace';
    database_id?: string;
    page_id?: string;
  };
  archived: boolean;
  properties: Record<string, unknown>;
  url: string;
  public_url: string | null;
}

export interface NotionSearchResponse {
  object: 'list';
  results: NotionPage[];
  next_cursor: string | null;
  has_more: boolean;
}

export interface NotionBlock {
  id: string;
  object: 'block';
  type: string;
  created_time: string;
  last_edited_time: string;
  has_children: boolean;
  [key: string]: unknown;
}

export interface NotionBlocksResponse {
  object: 'list';
  results: NotionBlock[];
  next_cursor: string | null;
  has_more: boolean;
}

export async function searchPages(query: string): Promise<NotionPage[]> {
  const client = getClient();
  logger.info('Searching Notion pages', { query });

  const response = await client.post<NotionSearchResponse>('/search', {
    query,
    filter: {
      value: 'page',
      property: 'object',
    },
    page_size: 50,
  });

  return response.results;
}

export async function getPage(pageId: string): Promise<NotionPage> {
  const client = getClient();
  // Remove dashes if present
  const cleanId = pageId.replace(/-/g, '');
  logger.info('Fetching Notion page', { pageId: cleanId });
  return client.get<NotionPage>(`/pages/${cleanId}`);
}

export async function getPageBlocks(pageId: string): Promise<NotionBlock[]> {
  const client = getClient();
  const cleanId = pageId.replace(/-/g, '');
  logger.info('Fetching Notion page blocks', { pageId: cleanId });

  const response = await client.get<NotionBlocksResponse>(`/blocks/${cleanId}/children?page_size=100`);
  return response.results;
}

export async function searchDatabases(query: string): Promise<unknown[]> {
  const client = getClient();
  logger.info('Searching Notion databases', { query });

  const response = await client.post<NotionSearchResponse>('/search', {
    query,
    filter: {
      value: 'database',
      property: 'object',
    },
    page_size: 50,
  });

  return response.results;
}
