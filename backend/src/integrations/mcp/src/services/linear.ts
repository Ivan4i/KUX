/**
 * Linear Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv } from '../utils/env.js';
import { logger } from '../utils/logger.js';

function getClient() {
  const token = getEnv('LINEARTOKEN');
  return createServiceClient('https://api.linear.app', {
    'Authorization': token,
    'Content-Type': 'application/json',
  });
}

export interface LinearIssue {
  id: string;
  identifier: string;
  title: string;
  description: string | null;
  state: {
    id: string;
    name: string;
    type: string;
  };
  priority: number;
  priorityLabel: string;
  url: string;
  createdAt: string;
  updatedAt: string;
  assignee: {
    id: string;
    name: string;
    email: string;
  } | null;
  labels: {
    nodes: Array<{
      id: string;
      name: string;
      color: string;
    }>;
  };
  project: {
    id: string;
    name: string;
  } | null;
}

interface LinearGraphQLResponse<T> {
  data: T;
  errors?: Array<{ message: string }>;
}

async function graphql<T>(query: string, variables?: Record<string, unknown>): Promise<T> {
  const client = getClient();
  const response = await client.post<LinearGraphQLResponse<T>>('/graphql', {
    query,
    variables,
  });

  if (response.errors?.length) {
    throw new Error(`Linear API error: ${response.errors.map(e => e.message).join(', ')}`);
  }

  return response.data;
}

export async function listIssues(limit = 50): Promise<LinearIssue[]> {
  logger.info('Fetching Linear issues', { limit });

  const query = `
    query Issues($first: Int) {
      issues(first: $first, orderBy: updatedAt) {
        nodes {
          id
          identifier
          title
          description
          state { id name type }
          priority
          priorityLabel
          url
          createdAt
          updatedAt
          assignee { id name email }
          labels { nodes { id name color } }
          project { id name }
        }
      }
    }
  `;

  const data = await graphql<{ issues: { nodes: LinearIssue[] } }>(query, { first: limit });
  return data.issues.nodes;
}

export async function getIssue(issueIdOrKey: string): Promise<LinearIssue> {
  logger.info('Fetching Linear issue', { issue: issueIdOrKey });

  // Check if it's an identifier (like "ENG-123") or a UUID
  const isIdentifier = /^[A-Z]+-\d+$/.test(issueIdOrKey);

  if (isIdentifier) {
    const query = `
      query IssueByIdentifier($identifier: String!) {
        issueSearch(query: $identifier, first: 1) {
          nodes {
            id
            identifier
            title
            description
            state { id name type }
            priority
            priorityLabel
            url
            createdAt
            updatedAt
            assignee { id name email }
            labels { nodes { id name color } }
            project { id name }
          }
        }
      }
    `;

    const data = await graphql<{ issueSearch: { nodes: LinearIssue[] } }>(query, { identifier: issueIdOrKey });
    const issues = data.issueSearch.nodes;

    if (issues.length === 0) {
      throw new Error(`Issue not found: ${issueIdOrKey}`);
    }

    return issues[0];
  }

  const query = `
    query Issue($id: String!) {
      issue(id: $id) {
        id
        identifier
        title
        description
        state { id name type }
        priority
        priorityLabel
        url
        createdAt
        updatedAt
        assignee { id name email }
        labels { nodes { id name color } }
        project { id name }
      }
    }
  `;

  const data = await graphql<{ issue: LinearIssue }>(query, { id: issueIdOrKey });
  return data.issue;
}

export async function searchIssues(searchQuery: string, limit = 25): Promise<LinearIssue[]> {
  logger.info('Searching Linear issues', { query: searchQuery, limit });

  const query = `
    query SearchIssues($query: String!, $first: Int) {
      issueSearch(query: $query, first: $first) {
        nodes {
          id
          identifier
          title
          description
          state { id name type }
          priority
          priorityLabel
          url
          createdAt
          updatedAt
          assignee { id name email }
          labels { nodes { id name color } }
          project { id name }
        }
      }
    }
  `;

  const data = await graphql<{ issueSearch: { nodes: LinearIssue[] } }>(query, {
    query: searchQuery,
    first: limit
  });
  return data.issueSearch.nodes;
}
