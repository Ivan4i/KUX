/**
 * Sentry Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv, getEnvOptional } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const SENTRY_API = 'https://sentry.io/api/0';

function getClient() {
  const token = getEnv('SENTRYAUTHTOKEN');
  return createServiceClient(SENTRY_API, {
    'Authorization': `Bearer ${token}`,
  });
}

export interface SentryProject {
  id: string;
  slug: string;
  name: string;
  platform: string | null;
  dateCreated: string;
  isBookmarked: boolean;
  isMember: boolean;
  features: string[];
  firstEvent: string | null;
  firstTransactionEvent: boolean;
  access: string[];
  hasAccess: boolean;
  hasCustomMetrics: boolean;
  hasMinifiedStackTrace: boolean;
  hasMonitors: boolean;
  hasProfiles: boolean;
  hasReplays: boolean;
  hasSessions: boolean;
  isInternal: boolean;
  organization: {
    id: string;
    slug: string;
    name: string;
  };
}

export interface SentryIssue {
  id: string;
  shortId: string;
  title: string;
  culprit: string;
  permalink: string;
  level: string;
  status: string;
  statusDetails: Record<string, unknown>;
  isPublic: boolean;
  platform: string | null;
  project: {
    id: string;
    name: string;
    slug: string;
    platform: string | null;
  };
  type: string;
  metadata: {
    value?: string;
    type?: string;
    filename?: string;
    function?: string;
  };
  numComments: number;
  assignedTo: unknown | null;
  isBookmarked: boolean;
  isSubscribed: boolean;
  subscriptionDetails: unknown | null;
  hasSeen: boolean;
  annotations: string[];
  isUnhandled: boolean;
  count: string;
  userCount: number;
  firstSeen: string;
  lastSeen: string;
}

export async function listProjects(): Promise<SentryProject[]> {
  const client = getClient();
  const org = getEnvOptional('SENTRYORG');

  if (org) {
    logger.info('Fetching Sentry projects for org', { org });
    return client.get<SentryProject[]>(`/organizations/${org}/projects/`);
  }

  logger.info('Fetching all Sentry projects');
  return client.get<SentryProject[]>('/projects/');
}

export async function getIssue(issueId: string): Promise<SentryIssue> {
  const client = getClient();
  logger.info('Fetching Sentry issue', { issueId });
  return client.get<SentryIssue>(`/issues/${issueId}/`);
}

export async function listIssues(project?: string, limit = 25): Promise<SentryIssue[]> {
  const client = getClient();
  const org = getEnvOptional('SENTRYORG');
  const targetProject = project || getEnvOptional('SENTRYPROJECT');

  if (!org) {
    throw new Error('SENTRY_ORG environment variable is required to list issues');
  }

  let url = `/organizations/${org}/issues/?limit=${limit}`;
  if (targetProject) {
    url += `&project=${targetProject}`;
  }

  logger.info('Fetching Sentry issues', { org, project: targetProject, limit });
  return client.get<SentryIssue[]>(url);
}

export async function searchIssues(query: string, limit = 25): Promise<SentryIssue[]> {
  const client = getClient();
  const org = getEnvOptional('SENTRYORG');

  if (!org) {
    throw new Error('SENTRY_ORG environment variable is required to search issues');
  }

  logger.info('Searching Sentry issues', { org, query, limit });
  return client.get<SentryIssue[]>(
    `/organizations/${org}/issues/?limit=${limit}&query=${encodeURIComponent(query)}`
  );
}
