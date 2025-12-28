/**
 * Supabase Service - Database and project management operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const SUPABASE_API = 'https://api.supabase.com';

function getClient() {
  const token = getEnv('SUPABASEACCESSTOKEN');

  return createServiceClient(SUPABASE_API, {
    'Authorization': `Bearer ${token}`,
  });
}

export interface SupabaseProject {
  id: string;
  ref: string;
  organization_id: string;
  organization_slug: string;
  name: string;
  region: string;
  status: string;
  database: {
    host: string;
    version: string;
    postgres_engine: string;
    release_channel: string;
  };
  created_at: string;
}

export interface SupabaseOrganization {
  id: string;
  slug: string;
  name: string;
  billing_email: string;
}

export interface SupabaseFunction {
  id: string;
  slug: string;
  name: string;
  version: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface SupabaseSecret {
  name: string;
  value?: string;
}

export async function listProjects(): Promise<SupabaseProject[]> {
  const client = getClient();
  logger.info('Fetching Supabase projects');
  return client.get<SupabaseProject[]>('/v1/projects');
}

export async function getProject(projectRef?: string): Promise<SupabaseProject> {
  const client = getClient();
  const ref = projectRef || getEnv('SUPABASEPROJECTREF');
  logger.info('Fetching Supabase project', { project: ref });
  return client.get<SupabaseProject>(`/v1/projects/${ref}`);
}

export async function listOrganizations(): Promise<SupabaseOrganization[]> {
  const client = getClient();
  logger.info('Fetching Supabase organizations');
  return client.get<SupabaseOrganization[]>('/v1/organizations');
}

export async function listFunctions(projectRef?: string): Promise<SupabaseFunction[]> {
  const client = getClient();
  const ref = projectRef || getEnv('SUPABASEPROJECTREF');
  logger.info('Fetching Supabase Edge Functions', { project: ref });
  return client.get<SupabaseFunction[]>(`/v1/projects/${ref}/functions`);
}

export async function listSecrets(projectRef?: string): Promise<SupabaseSecret[]> {
  const client = getClient();
  const ref = projectRef || getEnv('SUPABASEPROJECTREF');
  logger.info('Fetching Supabase secrets', { project: ref });
  return client.get<SupabaseSecret[]>(`/v1/projects/${ref}/secrets`);
}

export async function getProjectApiKeys(projectRef?: string): Promise<{ name: string; api_key: string }[]> {
  const client = getClient();
  const ref = projectRef || getEnv('SUPABASEPROJECTREF');
  logger.info('Fetching Supabase API keys', { project: ref });
  return client.get<{ name: string; api_key: string }[]>(`/v1/projects/${ref}/api-keys`);
}

export async function runSqlQuery(query: string, projectRef?: string): Promise<unknown> {
  const client = getClient();
  const ref = projectRef || getEnv('SUPABASEPROJECTREF');
  logger.info('Running SQL query on Supabase', { project: ref });
  return client.post<unknown>(`/v1/projects/${ref}/database/query`, { query });
}

export async function getProjectHealth(projectRef?: string): Promise<{ status: string }> {
  const client = getClient();
  const ref = projectRef || getEnv('SUPABASEPROJECTREF');
  logger.info('Checking Supabase project health', { project: ref });
  return client.get<{ status: string }>(`/v1/projects/${ref}/health`);
}
