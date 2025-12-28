/**
 * Cloudflare Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv, getEnvOptional } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const CLOUDFLARE_API = 'https://api.cloudflare.com/client/v4';

function getClient() {
  const token = getEnv('CLOUDFLAREAPITOKEN');
  return createServiceClient(CLOUDFLARE_API, {
    'Authorization': `Bearer ${token}`,
  });
}

export interface CloudflareZone {
  id: string;
  name: string;
  status: string;
  paused: boolean;
  type: string;
  development_mode: number;
  name_servers: string[];
  original_name_servers: string[];
  modified_on: string;
  created_on: string;
  activated_on: string;
  plan: {
    id: string;
    name: string;
  };
}

export interface CloudflareResponse<T> {
  success: boolean;
  errors: Array<{ code: number; message: string }>;
  messages: string[];
  result: T;
  result_info?: {
    page: number;
    per_page: number;
    count: number;
    total_count: number;
  };
}

export interface CloudflareZoneDetails extends CloudflareZone {
  meta: {
    step: number;
    custom_certificate_quota: number;
    page_rule_quota: number;
    phishing_detected: boolean;
    multiple_railguns_allowed: boolean;
  };
  owner: {
    id: string;
    type: string;
    email?: string;
  };
  account: {
    id: string;
    name: string;
  };
  permissions: string[];
}

export async function listZones(): Promise<CloudflareZone[]> {
  const client = getClient();
  logger.info('Fetching Cloudflare zones');
  const response = await client.get<CloudflareResponse<CloudflareZone[]>>('/zones?per_page=50');

  if (!response.success) {
    throw new Error(`Cloudflare API error: ${response.errors.map(e => e.message).join(', ')}`);
  }

  return response.result;
}

export async function getZoneDetails(zoneIdOrName?: string): Promise<CloudflareZoneDetails> {
  const client = getClient();
  let zoneId = zoneIdOrName || getEnvOptional('CLOUDFLAREZONEID');

  // If it looks like a domain name, find the zone ID first
  if (zoneId && zoneId.includes('.')) {
    logger.info('Looking up zone by name', { name: zoneId });
    const zones = await listZones();
    const zone = zones.find(z => z.name === zoneId);
    if (!zone) {
      throw new Error(`Zone not found: ${zoneId}`);
    }
    zoneId = zone.id;
  }

  if (!zoneId) {
    throw new Error('No zone ID provided. Set CLOUDFLARE_ZONE_ID env or pass zoneId parameter.');
  }

  logger.info('Fetching zone details', { zoneId });
  const response = await client.get<CloudflareResponse<CloudflareZoneDetails>>(`/zones/${zoneId}`);

  if (!response.success) {
    throw new Error(`Cloudflare API error: ${response.errors.map(e => e.message).join(', ')}`);
  }

  return response.result;
}

export async function getZoneDnsRecords(zoneId: string): Promise<unknown[]> {
  const client = getClient();
  logger.info('Fetching DNS records', { zoneId });
  const response = await client.get<CloudflareResponse<unknown[]>>(`/zones/${zoneId}/dns_records?per_page=100`);

  if (!response.success) {
    throw new Error(`Cloudflare API error: ${response.errors.map(e => e.message).join(', ')}`);
  }

  return response.result;
}
