/**
 * Postman Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const POSTMAN_API = 'https://api.getpostman.com';

function getClient() {
  const apiKey = getEnv('POSTMANAPIKEY');
  return createServiceClient(POSTMAN_API, {
    'X-Api-Key': apiKey,
  });
}

export interface PostmanCollection {
  id: string;
  uid: string;
  name: string;
  owner: string;
  createdAt: string;
  updatedAt: string;
  isPublic: boolean;
  fork?: {
    label: string;
    createdAt: string;
    from: string;
  };
}

export interface PostmanCollectionDetail {
  info: {
    _postman_id: string;
    name: string;
    description?: string;
    schema: string;
    updatedAt: string;
    createdAt: string;
    lastUpdatedBy: string;
    uid: string;
  };
  item: PostmanItem[];
  variable?: Array<{
    key: string;
    value: string;
    type: string;
  }>;
}

export interface PostmanItem {
  id: string;
  name: string;
  description?: string;
  item?: PostmanItem[]; // Folders have nested items
  request?: {
    method: string;
    header: Array<{ key: string; value: string }>;
    body?: unknown;
    url: {
      raw: string;
      protocol?: string;
      host?: string[];
      path?: string[];
      query?: Array<{ key: string; value: string }>;
    };
    description?: string;
  };
  response?: unknown[];
}

export interface PostmanWorkspace {
  id: string;
  name: string;
  type: string;
  visibility: string;
  createdBy: string;
  updatedBy: string;
  createdAt: string;
  updatedAt: string;
}

export async function listCollections(): Promise<PostmanCollection[]> {
  const client = getClient();
  logger.info('Fetching Postman collections');
  const response = await client.get<{ collections: PostmanCollection[] }>('/collections');
  return response.collections;
}

export async function getCollection(collectionId: string): Promise<PostmanCollectionDetail> {
  const client = getClient();
  // Handle both UID format (12345678-uuid) and plain ID
  const id = collectionId.includes('-') ? collectionId : collectionId;
  logger.info('Fetching Postman collection', { collectionId: id });
  const response = await client.get<{ collection: PostmanCollectionDetail }>(`/collections/${id}`);
  return response.collection;
}

export async function listWorkspaces(): Promise<PostmanWorkspace[]> {
  const client = getClient();
  logger.info('Fetching Postman workspaces');
  const response = await client.get<{ workspaces: PostmanWorkspace[] }>('/workspaces');
  return response.workspaces;
}

export async function listEnvironments(): Promise<Array<{ id: string; uid: string; name: string; owner: string; createdAt: string; updatedAt: string }>> {
  const client = getClient();
  logger.info('Fetching Postman environments');
  const response = await client.get<{ environments: Array<{ id: string; uid: string; name: string; owner: string; createdAt: string; updatedAt: string }> }>('/environments');
  return response.environments;
}
