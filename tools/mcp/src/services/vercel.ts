/**
 * Vercel Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv, getEnvOptional } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const VERCEL_API = 'https://api.vercel.com';

function getClient() {
  const token = getEnv('VERCELTOKEN');
  const teamId = getEnvOptional('VERCELTEAMID');

  return createServiceClient(VERCEL_API, {
    'Authorization': `Bearer ${token}`,
    ...(teamId ? { 'x-vercel-team-id': teamId } : {}),
  });
}

export interface VercelProject {
  id: string;
  name: string;
  accountId: string;
  updatedAt: number;
  createdAt: number;
  framework: string | null;
  devCommand: string | null;
  installCommand: string | null;
  buildCommand: string | null;
  outputDirectory: string | null;
  rootDirectory: string | null;
  directoryListing: boolean;
  nodeVersion: string;
  targets: Record<string, unknown>;
  latestDeployments?: VercelDeployment[];
}

export interface VercelDeployment {
  id: string;
  url: string;
  name: string;
  state: string;
  type: string;
  created: number;
  createdAt: number;
  buildingAt: number;
  ready: number;
  readyState: string;
  target: string | null;
  creator: {
    uid: string;
    email: string;
    username: string;
  };
}

export interface VercelProjectsResponse {
  projects: VercelProject[];
  pagination: {
    count: number;
    next: string | null;
    prev: string | null;
  };
}

export async function listProjects(): Promise<VercelProject[]> {
  const client = getClient();
  logger.info('Fetching Vercel projects');
  const teamId = getEnvOptional('VERCELTEAMID');
  const query = teamId ? `?teamId=${teamId}` : '';
  const response = await client.get<VercelProjectsResponse>(`/v9/projects${query}`);
  return response.projects;
}

export async function getProject(projectIdOrName: string): Promise<VercelProject> {
  const client = getClient();
  logger.info('Fetching Vercel project', { project: projectIdOrName });
  const teamId = getEnvOptional('VERCELTEAMID');
  const query = teamId ? `?teamId=${teamId}` : '';
  return client.get<VercelProject>(`/v9/projects/${encodeURIComponent(projectIdOrName)}${query}`);
}

export async function listDeployments(projectId?: string, limit = 10): Promise<VercelDeployment[]> {
  const client = getClient();
  const teamId = getEnvOptional('VERCELTEAMID');

  let query = `limit=${limit}`;
  if (teamId) query += `&teamId=${teamId}`;
  if (projectId) query += `&projectId=${projectId}`;

  logger.info('Fetching Vercel deployments', { projectId, limit });
  const response = await client.get<{ deployments: VercelDeployment[] }>(`/v6/deployments?${query}`);
  return response.deployments;
}
