/**
 * MongoDB Atlas Service - Cluster and project management operations
 * Uses HTTP Digest Authentication
 */

import { getEnv } from '../utils/env.js';
import { logger } from '../utils/logger.js';
import AxiosDigestAuthModule from '@mhoc/axios-digest-auth';
const AxiosDigestAuth = AxiosDigestAuthModule.default || AxiosDigestAuthModule;

const MONGODB_API = 'https://cloud.mongodb.com/api/atlas/v2';

function getClient() {
  const publicKey = getEnv('MONGODBPUBLICKEY');
  const privateKey = getEnv('MONGODBPRIVATEKEY');

  return new AxiosDigestAuth({
    username: publicKey,
    password: privateKey,
  });
}

const ATLAS_HEADERS = {
  'Accept': 'application/vnd.atlas.2023-01-01+json',
  'Content-Type': 'application/json',
};

export interface MongoDBOrganization {
  id: string;
  name: string;
  isDeleted: boolean;
  links: Array<{ href: string; rel: string }>;
}

export interface MongoDBProject {
  id: string;
  name: string;
  orgId: string;
  clusterCount: number;
  created: string;
  links: Array<{ href: string; rel: string }>;
}

export interface MongoDBCluster {
  id: string;
  name: string;
  clusterType: string;
  mongoDBVersion: string;
  stateName: string;
  paused: boolean;
  connectionStrings?: {
    standard?: string;
    standardSrv?: string;
  };
  replicationSpecs?: Array<{
    regionConfigs: Array<{
      providerName: string;
      regionName: string;
      priority: number;
      electableSpecs?: {
        instanceSize: string;
        nodeCount: number;
      };
    }>;
  }>;
}

export interface MongoDBDatabase {
  databaseName: string;
  links: Array<{ href: string; rel: string }>;
}

async function request<T>(method: 'GET' | 'POST' | 'PUT' | 'DELETE', path: string, data?: unknown): Promise<T> {
  const client = getClient();
  const url = `${MONGODB_API}${path}`;

  logger.info(`MongoDB Atlas ${method} ${path}`);

  const response = await client.request({
    method: method as 'GET' | 'POST' | 'PUT' | 'DELETE',
    url,
    headers: ATLAS_HEADERS,
    data,
  });

  return response.data as T;
}

export async function listOrganizations(): Promise<MongoDBOrganization[]> {
  const response = await request<{ results: MongoDBOrganization[] }>('GET', '/orgs');
  return response.results;
}

export async function listProjects(orgId?: string): Promise<MongoDBProject[]> {
  const path = orgId ? `/orgs/${orgId}/groups` : '/groups';
  const response = await request<{ results: MongoDBProject[] }>('GET', path);
  return response.results;
}

export async function getProject(projectId: string): Promise<MongoDBProject> {
  return request<MongoDBProject>('GET', `/groups/${projectId}`);
}

export async function listClusters(projectId: string): Promise<MongoDBCluster[]> {
  const response = await request<{ results: MongoDBCluster[] }>('GET', `/groups/${projectId}/clusters`);
  return response.results;
}

export async function getCluster(projectId: string, clusterName: string): Promise<MongoDBCluster> {
  return request<MongoDBCluster>('GET', `/groups/${projectId}/clusters/${clusterName}`);
}

export async function listDatabases(projectId: string, clusterName: string): Promise<MongoDBDatabase[]> {
  // Note: This requires the cluster to be running
  const response = await request<{ results: MongoDBDatabase[] }>(
    'GET',
    `/groups/${projectId}/clusters/${clusterName}/databases`
  );
  return response.results;
}

export async function getClusterStatus(projectId: string, clusterName: string): Promise<{ status: string; state: string }> {
  const cluster = await getCluster(projectId, clusterName);
  return {
    status: cluster.paused ? 'PAUSED' : 'RUNNING',
    state: cluster.stateName,
  };
}
