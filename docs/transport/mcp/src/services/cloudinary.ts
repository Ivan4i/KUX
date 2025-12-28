/**
 * Cloudinary Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv, getEnvOptional } from '../utils/env.js';
import { logger } from '../utils/logger.js';

function getConfig() {
  // Support both CLOUDINARY_URL format and individual vars
  const cloudinaryUrl = getEnvOptional('CLOUDINARYURL');

  if (cloudinaryUrl) {
    // Parse cloudinary://API_KEY:API_SECRET@CLOUD_NAME
    const match = cloudinaryUrl.match(/cloudinary:\/\/(\w+):(\w+)@(\w+)/);
    if (match) {
      return {
        cloudName: match[3],
        apiKey: match[1],
        apiSecret: match[2],
      };
    }
  }

  return {
    cloudName: getEnv('CLOUDINARYCLOUDNAME'),
    apiKey: getEnv('CLOUDINARYAPIKEY'),
    apiSecret: getEnv('CLOUDINARYAPISECRET'),
  };
}

function getClient() {
  const config = getConfig();
  const credentials = Buffer.from(`${config.apiKey}:${config.apiSecret}`).toString('base64');

  return {
    config,
    client: createServiceClient(`https://api.cloudinary.com/v1_1/${config.cloudName}`, {
      'Authorization': `Basic ${credentials}`,
    }),
  };
}

export interface CloudinaryResource {
  asset_id: string;
  public_id: string;
  format: string;
  version: number;
  resource_type: string;
  type: string;
  created_at: string;
  bytes: number;
  width?: number;
  height?: number;
  folder: string;
  url: string;
  secure_url: string;
  tags?: string[];
}

export interface CloudinaryResourcesResponse {
  resources: CloudinaryResource[];
  next_cursor?: string;
  rate_limit_allowed: number;
  rate_limit_reset_at: string;
  rate_limit_remaining: number;
}

export interface CloudinaryResourceDetails extends CloudinaryResource {
  derived?: Array<{
    transformation: string;
    format: string;
    bytes: number;
    url: string;
    secure_url: string;
  }>;
  colors?: Array<[string, number]>;
  predominant?: {
    google: Array<[string, number]>;
  };
  context?: Record<string, unknown>;
}

export async function listResources(
  resourceType: 'image' | 'video' | 'raw' = 'image',
  prefix?: string,
  maxResults = 50
): Promise<CloudinaryResource[]> {
  const { client } = getClient();

  let url = `/resources/${resourceType}?max_results=${maxResults}`;
  if (prefix) {
    url += `&prefix=${encodeURIComponent(prefix)}`;
  }

  logger.info('Fetching Cloudinary resources', { resourceType, prefix, maxResults });
  const response = await client.get<CloudinaryResourcesResponse>(url);
  return response.resources;
}

export async function getResource(publicId: string, resourceType: 'image' | 'video' | 'raw' = 'image'): Promise<CloudinaryResourceDetails> {
  const { client } = getClient();
  logger.info('Fetching Cloudinary resource', { publicId, resourceType });
  return client.get<CloudinaryResourceDetails>(`/resources/${resourceType}/upload/${encodeURIComponent(publicId)}`);
}

export async function searchResources(expression: string, maxResults = 50): Promise<CloudinaryResource[]> {
  const { client } = getClient();
  logger.info('Searching Cloudinary resources', { expression, maxResults });

  const response = await client.post<{ resources: CloudinaryResource[] }>('/resources/search', {
    expression,
    max_results: maxResults,
  });

  return response.resources;
}

export async function listFolders(rootFolder?: string): Promise<Array<{ name: string; path: string }>> {
  const { client } = getClient();
  const path = rootFolder ? `/folders/${encodeURIComponent(rootFolder)}` : '/folders';
  logger.info('Fetching Cloudinary folders', { rootFolder });

  const response = await client.get<{ folders: Array<{ name: string; path: string }> }>(path);
  return response.folders;
}
