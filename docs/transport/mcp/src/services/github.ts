/**
 * GitHub Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv, getEnvOptional } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const GITHUB_API = 'https://api.github.com';

function getClient() {
  const token = getEnv('GITHUBTOKEN');
  return createServiceClient(GITHUB_API, {
    'Authorization': `Bearer ${token}`,
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'MCP-SaaS-Gateway/1.0',
  });
}

export interface GitHubRepo {
  id: number;
  name: string;
  full_name: string;
  description: string | null;
  private: boolean;
  html_url: string;
  default_branch: string;
  language: string | null;
  stargazers_count: number;
  forks_count: number;
  updated_at: string;
}

export interface GitHubIssue {
  id: number;
  number: number;
  title: string;
  state: string;
  body: string | null;
  html_url: string;
  user: { login: string } | null;
  labels: Array<{ name: string; color: string }>;
  created_at: string;
  updated_at: string;
}

export interface GitHubSearchResult {
  total_count: number;
  incomplete_results: boolean;
  items: GitHubIssue[];
}

export async function listRepos(owner?: string): Promise<GitHubRepo[]> {
  const client = getClient();
  const targetOwner = owner || getEnvOptional('GITHUBOWNER');

  if (!targetOwner) {
    // List repos for authenticated user
    logger.info('Fetching repos for authenticated user');
    return client.get<GitHubRepo[]>('/user/repos?per_page=100&sort=updated');
  }

  logger.info('Fetching repos', { owner: targetOwner });

  // Check if it's an org or user
  try {
    return await client.get<GitHubRepo[]>(`/orgs/${targetOwner}/repos?per_page=100&sort=updated`);
  } catch {
    // Fallback to user repos
    return client.get<GitHubRepo[]>(`/users/${targetOwner}/repos?per_page=100&sort=updated`);
  }
}

export async function getIssue(owner: string, repo: string, issueNumber: number): Promise<GitHubIssue> {
  const client = getClient();
  logger.info('Fetching issue', { owner, repo, issueNumber });
  return client.get<GitHubIssue>(`/repos/${owner}/${repo}/issues/${issueNumber}`);
}

export async function searchIssues(query: string): Promise<GitHubSearchResult> {
  const client = getClient();
  const owner = getEnvOptional('GITHUBOWNER');

  let fullQuery = query;
  if (owner && !query.includes('org:') && !query.includes('user:')) {
    fullQuery = `${query} org:${owner}`;
  }

  logger.info('Searching issues', { query: fullQuery });
  return client.get<GitHubSearchResult>(`/search/issues?q=${encodeURIComponent(fullQuery)}&per_page=50`);
}
