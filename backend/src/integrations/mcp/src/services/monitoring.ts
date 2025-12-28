/**
 * Monitoring Services - Datadog, CloudWatch, ELK
 * Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv, getEnvOptional } from '../utils/env.js';
import { logger } from '../utils/logger.js';

// ============================================================================
// DATADOG
// ============================================================================

function getDatadogClient() {
  const apiKey = getEnv('DATADOGAPIKEY');
  const appKey = getEnv('DATADOGAPPKEY');
  const site = getEnvOptional('DATADOGSITE') || 'datadoghq.com';

  return createServiceClient(`https://api.${site}/api/v1`, {
    'DD-API-KEY': apiKey,
    'DD-APPLICATION-KEY': appKey,
  });
}

export interface DatadogDashboard {
  id: string;
  title: string;
  description: string | null;
  layout_type: string;
  is_read_only: boolean;
  url: string;
  created_at: string;
  modified_at: string;
  author_handle: string;
}

export interface DatadogMonitor {
  id: number;
  name: string;
  type: string;
  query: string;
  message: string;
  tags: string[];
  options: Record<string, unknown>;
  overall_state: string;
  created: string;
  modified: string;
  creator: { name: string; email: string };
}

export async function datadogListDashboards(): Promise<DatadogDashboard[]> {
  const client = getDatadogClient();
  logger.info('Fetching Datadog dashboards');
  const response = await client.get<{ dashboards: DatadogDashboard[] }>('/dashboard');
  return response.dashboards;
}

export async function datadogListMonitors(tags?: string[]): Promise<DatadogMonitor[]> {
  const client = getDatadogClient();
  let url = '/monitor';
  if (tags?.length) {
    url += `?monitor_tags=${tags.join(',')}`;
  }
  logger.info('Fetching Datadog monitors', { tags });
  return client.get<DatadogMonitor[]>(url);
}

export async function datadogSearchLogs(query: string, from: string, to: string, limit = 100): Promise<unknown[]> {
  const apiKey = getEnv('DATADOGAPIKEY');
  const appKey = getEnv('DATADOGAPPKEY');
  const site = getEnvOptional('DATADOGSITE') || 'datadoghq.com';

  const client = createServiceClient(`https://api.${site}/api/v2`, {
    'DD-API-KEY': apiKey,
    'DD-APPLICATION-KEY': appKey,
  });

  logger.info('Searching Datadog logs', { query, from, to, limit });

  const response = await client.post<{ data: unknown[] }>('/logs/events/search', {
    filter: {
      query,
      from,
      to,
    },
    page: {
      limit,
    },
  });

  return response.data;
}

// ============================================================================
// CLOUDWATCH (AWS)
// ============================================================================

// Note: CloudWatch requires AWS SDK. For MCP, we provide a describe_supported_operations stub
// as the full AWS SDK integration is more complex

export interface CloudWatchOperationInfo {
  operation: string;
  description: string;
  requiredEnv: string[];
  exampleRequest: Record<string, unknown>;
}

export function cloudwatchDescribeOperations(): CloudWatchOperationInfo[] {
  return [
    {
      operation: 'ListMetrics',
      description: 'List available CloudWatch metrics',
      requiredEnv: ['AWSACCESSKEYID', 'AWSSECRETACCESSKEY', 'AWSREGION'],
      exampleRequest: {
        Namespace: 'AWS/EC2',
        MetricName: 'CPUUtilization',
      },
    },
    {
      operation: 'GetMetricStatistics',
      description: 'Get statistics for a specific metric',
      requiredEnv: ['AWSACCESSKEYID', 'AWSSECRETACCESSKEY', 'AWSREGION'],
      exampleRequest: {
        Namespace: 'AWS/EC2',
        MetricName: 'CPUUtilization',
        StartTime: 'ISO8601 datetime',
        EndTime: 'ISO8601 datetime',
        Period: 300,
        Statistics: ['Average', 'Maximum'],
      },
    },
    {
      operation: 'DescribeAlarms',
      description: 'Get CloudWatch alarms',
      requiredEnv: ['AWSACCESSKEYID', 'AWSSECRETACCESSKEY', 'AWSREGION'],
      exampleRequest: {
        StateValue: 'ALARM',
      },
    },
    {
      operation: 'GetLogEvents',
      description: 'Get log events from a CloudWatch Logs log stream',
      requiredEnv: ['AWSACCESSKEYID', 'AWSSECRETACCESSKEY', 'AWSREGION'],
      exampleRequest: {
        logGroupName: '/aws/lambda/my-function',
        logStreamName: '2024/01/01/[$LATEST]abc123',
        limit: 100,
      },
    },
  ];
}

// ============================================================================
// ELK (Elasticsearch)
// ============================================================================

function getElkClient() {
  const url = getEnv('ELKURL');
  const username = getEnvOptional('ELKUSERNAME');
  const password = getEnvOptional('ELKPASSWORD');
  const apiKey = getEnvOptional('ELKAPIKEY');

  const headers: Record<string, string> = {};

  if (apiKey) {
    headers['Authorization'] = `ApiKey ${apiKey}`;
  } else if (username && password) {
    headers['Authorization'] = `Basic ${Buffer.from(`${username}:${password}`).toString('base64')}`;
  }

  return createServiceClient(url, headers);
}

export interface ElkSearchResult {
  took: number;
  timed_out: boolean;
  _shards: {
    total: number;
    successful: number;
    skipped: number;
    failed: number;
  };
  hits: {
    total: { value: number; relation: string };
    max_score: number | null;
    hits: Array<{
      _index: string;
      _id: string;
      _score: number | null;
      _source: Record<string, unknown>;
    }>;
  };
}

export interface ElkIndexInfo {
  health: string;
  status: string;
  index: string;
  uuid: string;
  pri: string;
  rep: string;
  'docs.count': string;
  'docs.deleted': string;
  'store.size': string;
  'pri.store.size': string;
}

export async function elkListIndices(): Promise<ElkIndexInfo[]> {
  const client = getElkClient();
  logger.info('Fetching ELK indices');
  return client.get<ElkIndexInfo[]>('/_cat/indices?format=json');
}

export async function elkSearchLogs(
  index: string,
  query: string,
  from = 0,
  size = 100,
  timeField = '@timestamp',
  timeRange?: { gte: string; lte: string }
): Promise<ElkSearchResult> {
  const client = getElkClient();

  const must: unknown[] = [
    {
      query_string: {
        query,
      },
    },
  ];

  if (timeRange) {
    must.push({
      range: {
        [timeField]: {
          gte: timeRange.gte,
          lte: timeRange.lte,
        },
      },
    });
  }

  logger.info('Searching ELK logs', { index, query, from, size });

  return client.post<ElkSearchResult>(`/${index}/_search`, {
    from,
    size,
    query: {
      bool: {
        must,
      },
    },
    sort: [{ [timeField]: { order: 'desc' } }],
  });
}

export async function elkGetIndexMapping(index: string): Promise<Record<string, unknown>> {
  const client = getElkClient();
  logger.info('Fetching ELK index mapping', { index });
  return client.get<Record<string, unknown>>(`/${index}/_mapping`);
}
