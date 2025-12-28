#!/usr/bin/env node
/**
 * MCP SaaS Gateway Server
 *
 * A unified MCP server providing read-only access to multiple SaaS services.
 * All operations are read-only by design.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';

import { logger } from './utils/logger.js';
import { listConfiguredServices } from './utils/env.js';

// Service imports
import * as github from './services/github.js';
import * as figma from './services/figma.js';
import * as cloudflare from './services/cloudflare.js';
import * as vercel from './services/vercel.js';
import * as notion from './services/notion.js';
import * as linear from './services/linear.js';
import * as sentry from './services/sentry.js';
import * as cloudinary from './services/cloudinary.js';
import * as postman from './services/postman.js';
import * as monitoring from './services/monitoring.js';
import * as stubs from './services/stubs.js';
import * as supabase from './services/supabase.js';
import * as mongodb from './services/mongodb.js';

// Check for health check mode
if (process.argv.includes('--health-check')) {
  const services = listConfiguredServices();
  console.log('\n=== MCP SaaS Gateway Health Check ===\n');

  let allConfigured = 0;
  let partiallyConfigured = 0;
  let notConfigured = 0;

  for (const service of services) {
    if (service.enabled) {
      console.log(`✅ ${service.name}: Configured`);
      allConfigured++;
    } else if (service.missingVars.length < service.envVars.length) {
      console.log(`⚠️  ${service.name}: Partially configured (missing: ${service.missingVars.join(', ')})`);
      partiallyConfigured++;
    } else {
      console.log(`❌ ${service.name}: Not configured (need: ${service.envVars.join(', ')})`);
      notConfigured++;
    }
  }

  console.log('\n--- Summary ---');
  console.log(`Configured: ${allConfigured}`);
  console.log(`Partially: ${partiallyConfigured}`);
  console.log(`Not configured: ${notConfigured}`);
  console.log('');

  process.exit(0);
}

// Tool definitions
const tools: Tool[] = [
  // Health Check
  {
    name: 'health_check',
    description: 'Check which SaaS services are configured and available',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },

  // GitHub Tools
  {
    name: 'github_list_repos',
    description: 'List GitHub repositories for the configured owner/org or authenticated user',
    inputSchema: {
      type: 'object',
      properties: {
        owner: {
          type: 'string',
          description: 'GitHub username or organization (optional, uses GITHUB_OWNER env if not provided)',
        },
      },
      required: [],
    },
  },
  {
    name: 'github_get_issue',
    description: 'Get details of a specific GitHub issue',
    inputSchema: {
      type: 'object',
      properties: {
        owner: { type: 'string', description: 'Repository owner' },
        repo: { type: 'string', description: 'Repository name' },
        issue_number: { type: 'number', description: 'Issue number' },
      },
      required: ['owner', 'repo', 'issue_number'],
    },
  },
  {
    name: 'github_search_issues',
    description: 'Search GitHub issues using query syntax',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query (GitHub search syntax)' },
      },
      required: ['query'],
    },
  },

  // Figma Tools
  {
    name: 'figma_get_file',
    description: 'Get Figma file details including document structure',
    inputSchema: {
      type: 'object',
      properties: {
        file_key: { type: 'string', description: 'Figma file key (from URL)' },
      },
      required: ['file_key'],
    },
  },
  {
    name: 'figma_list_components',
    description: 'List components in a Figma file',
    inputSchema: {
      type: 'object',
      properties: {
        file_key: {
          type: 'string',
          description: 'Figma file key (optional, uses FIGMA_FILE_KEY env if not provided)',
        },
      },
      required: [],
    },
  },

  // Cloudflare Tools
  {
    name: 'cloudflare_list_zones',
    description: 'List all Cloudflare zones (domains)',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'cloudflare_get_zone_details',
    description: 'Get details for a specific Cloudflare zone',
    inputSchema: {
      type: 'object',
      properties: {
        zone_id: {
          type: 'string',
          description: 'Zone ID or domain name (optional, uses CLOUDFLARE_ZONE_ID env if not provided)',
        },
      },
      required: [],
    },
  },

  // Vercel Tools
  {
    name: 'vercel_list_projects',
    description: 'List all Vercel projects',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'vercel_get_project',
    description: 'Get details for a specific Vercel project',
    inputSchema: {
      type: 'object',
      properties: {
        project: { type: 'string', description: 'Project ID or name' },
      },
      required: ['project'],
    },
  },

  // Notion Tools
  {
    name: 'notion_search_pages',
    description: 'Search Notion pages by query',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query' },
      },
      required: ['query'],
    },
  },
  {
    name: 'notion_get_page',
    description: 'Get a Notion page by ID',
    inputSchema: {
      type: 'object',
      properties: {
        page_id: { type: 'string', description: 'Page ID (with or without dashes)' },
      },
      required: ['page_id'],
    },
  },

  // Linear Tools
  {
    name: 'linear_list_issues',
    description: 'List Linear issues',
    inputSchema: {
      type: 'object',
      properties: {
        limit: { type: 'number', description: 'Maximum number of issues to return (default: 50)' },
      },
      required: [],
    },
  },
  {
    name: 'linear_get_issue',
    description: 'Get a Linear issue by ID or identifier (e.g., ENG-123)',
    inputSchema: {
      type: 'object',
      properties: {
        issue: { type: 'string', description: 'Issue ID or identifier (e.g., ENG-123)' },
      },
      required: ['issue'],
    },
  },

  // Sentry Tools
  {
    name: 'sentry_list_projects',
    description: 'List Sentry projects',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'sentry_get_issue',
    description: 'Get a Sentry issue by ID',
    inputSchema: {
      type: 'object',
      properties: {
        issue_id: { type: 'string', description: 'Sentry issue ID' },
      },
      required: ['issue_id'],
    },
  },

  // Cloudinary Tools
  {
    name: 'cloudinary_list_resources',
    description: 'List Cloudinary resources (images, videos, etc.)',
    inputSchema: {
      type: 'object',
      properties: {
        type: {
          type: 'string',
          enum: ['image', 'video', 'raw'],
          description: 'Resource type (default: image)',
        },
        prefix: { type: 'string', description: 'Filter by public ID prefix (folder path)' },
      },
      required: [],
    },
  },
  {
    name: 'cloudinary_get_resource',
    description: 'Get details for a specific Cloudinary resource',
    inputSchema: {
      type: 'object',
      properties: {
        public_id: { type: 'string', description: 'Resource public ID' },
        type: {
          type: 'string',
          enum: ['image', 'video', 'raw'],
          description: 'Resource type (default: image)',
        },
      },
      required: ['public_id'],
    },
  },

  // Postman Tools
  {
    name: 'postman_list_collections',
    description: 'List Postman collections',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'postman_get_collection',
    description: 'Get a Postman collection by ID',
    inputSchema: {
      type: 'object',
      properties: {
        collection_id: { type: 'string', description: 'Collection ID or UID' },
      },
      required: ['collection_id'],
    },
  },

  // Datadog Tools
  {
    name: 'datadog_list_dashboards',
    description: 'List Datadog dashboards',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'datadog_search_logs',
    description: 'Search Datadog logs',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query' },
        from: { type: 'string', description: 'Start time (ISO 8601)' },
        to: { type: 'string', description: 'End time (ISO 8601)' },
        limit: { type: 'number', description: 'Maximum results (default: 100)' },
      },
      required: ['query', 'from', 'to'],
    },
  },

  // CloudWatch Tools
  {
    name: 'cloudwatch_describe_operations',
    description: 'Describe available CloudWatch operations and their required parameters',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },

  // ELK Tools
  {
    name: 'elk_list_indices',
    description: 'List Elasticsearch indices',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'elk_search_logs',
    description: 'Search Elasticsearch logs',
    inputSchema: {
      type: 'object',
      properties: {
        index: { type: 'string', description: 'Index name or pattern' },
        query: { type: 'string', description: 'Query string' },
        size: { type: 'number', description: 'Maximum results (default: 100)' },
        time_field: { type: 'string', description: 'Timestamp field name (default: @timestamp)' },
        time_gte: { type: 'string', description: 'Start time (ISO 8601)' },
        time_lte: { type: 'string', description: 'End time (ISO 8601)' },
      },
      required: ['index', 'query'],
    },
  },

  // Stub Tools
  {
    name: 'box_list_files',
    description: 'List Box files (NOT YET IMPLEMENTED)',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'canva_list_designs',
    description: 'List Canva designs (NOT YET IMPLEMENTED)',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'clarity_get_dashboard',
    description: 'Get Microsoft Clarity dashboard data (NOT YET IMPLEMENTED)',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },

  // Supabase Tools
  {
    name: 'supabase_list_projects',
    description: 'List all Supabase projects',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'supabase_get_project',
    description: 'Get details for a specific Supabase project',
    inputSchema: {
      type: 'object',
      properties: {
        project_ref: { type: 'string', description: 'Project reference ID (optional, uses SUPABASE_PROJECT_REF env if not provided)' },
      },
      required: [],
    },
  },
  {
    name: 'supabase_list_organizations',
    description: 'List all Supabase organizations',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'supabase_list_functions',
    description: 'List Edge Functions for a Supabase project',
    inputSchema: {
      type: 'object',
      properties: {
        project_ref: { type: 'string', description: 'Project reference ID (optional)' },
      },
      required: [],
    },
  },
  {
    name: 'supabase_run_sql',
    description: 'Run a SQL query on the Supabase database',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'SQL query to execute' },
        project_ref: { type: 'string', description: 'Project reference ID (optional)' },
      },
      required: ['query'],
    },
  },
  {
    name: 'supabase_get_api_keys',
    description: 'Get API keys for a Supabase project',
    inputSchema: {
      type: 'object',
      properties: {
        project_ref: { type: 'string', description: 'Project reference ID (optional)' },
      },
      required: [],
    },
  },

  // MongoDB Atlas Tools
  {
    name: 'mongodb_list_organizations',
    description: 'List MongoDB Atlas organizations',
    inputSchema: {
      type: 'object',
      properties: {},
      required: [],
    },
  },
  {
    name: 'mongodb_list_projects',
    description: 'List MongoDB Atlas projects (groups)',
    inputSchema: {
      type: 'object',
      properties: {
        org_id: { type: 'string', description: 'Organization ID (optional, lists all accessible projects if not provided)' },
      },
      required: [],
    },
  },
  {
    name: 'mongodb_list_clusters',
    description: 'List clusters in a MongoDB Atlas project',
    inputSchema: {
      type: 'object',
      properties: {
        project_id: { type: 'string', description: 'Project (group) ID' },
      },
      required: ['project_id'],
    },
  },
  {
    name: 'mongodb_get_cluster',
    description: 'Get details of a specific MongoDB Atlas cluster',
    inputSchema: {
      type: 'object',
      properties: {
        project_id: { type: 'string', description: 'Project (group) ID' },
        cluster_name: { type: 'string', description: 'Cluster name' },
      },
      required: ['project_id', 'cluster_name'],
    },
  },
];

// Tool handler
async function handleToolCall(
  name: string,
  args: Record<string, unknown>
): Promise<unknown> {
  logger.info('Tool called', { name, args: Object.keys(args) });

  try {
    switch (name) {
      // Health Check
      case 'health_check': {
        const services = listConfiguredServices();
        return {
          services: services.map(s => ({
            name: s.name,
            configured: s.enabled,
            missingEnvVars: s.missingVars,
          })),
          summary: {
            configured: services.filter(s => s.enabled).length,
            total: services.length,
          },
        };
      }

      // GitHub
      case 'github_list_repos':
        return github.listRepos(args.owner as string | undefined);
      case 'github_get_issue':
        return github.getIssue(
          args.owner as string,
          args.repo as string,
          args.issue_number as number
        );
      case 'github_search_issues':
        return github.searchIssues(args.query as string);

      // Figma
      case 'figma_get_file':
        return figma.getFile(args.file_key as string);
      case 'figma_list_components':
        return figma.listComponents(args.file_key as string | undefined);

      // Cloudflare
      case 'cloudflare_list_zones':
        return cloudflare.listZones();
      case 'cloudflare_get_zone_details':
        return cloudflare.getZoneDetails(args.zone_id as string | undefined);

      // Vercel
      case 'vercel_list_projects':
        return vercel.listProjects();
      case 'vercel_get_project':
        return vercel.getProject(args.project as string);

      // Notion
      case 'notion_search_pages':
        return notion.searchPages(args.query as string);
      case 'notion_get_page':
        return notion.getPage(args.page_id as string);

      // Linear
      case 'linear_list_issues':
        return linear.listIssues(args.limit as number | undefined);
      case 'linear_get_issue':
        return linear.getIssue(args.issue as string);

      // Sentry
      case 'sentry_list_projects':
        return sentry.listProjects();
      case 'sentry_get_issue':
        return sentry.getIssue(args.issue_id as string);

      // Cloudinary
      case 'cloudinary_list_resources':
        return cloudinary.listResources(
          (args.type as 'image' | 'video' | 'raw') || 'image',
          args.prefix as string | undefined
        );
      case 'cloudinary_get_resource':
        return cloudinary.getResource(
          args.public_id as string,
          (args.type as 'image' | 'video' | 'raw') || 'image'
        );

      // Postman
      case 'postman_list_collections':
        return postman.listCollections();
      case 'postman_get_collection':
        return postman.getCollection(args.collection_id as string);

      // Datadog
      case 'datadog_list_dashboards':
        return monitoring.datadogListDashboards();
      case 'datadog_search_logs':
        return monitoring.datadogSearchLogs(
          args.query as string,
          args.from as string,
          args.to as string,
          (args.limit as number) || 100
        );

      // CloudWatch
      case 'cloudwatch_describe_operations':
        return monitoring.cloudwatchDescribeOperations();

      // ELK
      case 'elk_list_indices':
        return monitoring.elkListIndices();
      case 'elk_search_logs':
        return monitoring.elkSearchLogs(
          args.index as string,
          args.query as string,
          0,
          (args.size as number) || 100,
          (args.time_field as string) || '@timestamp',
          args.time_gte && args.time_lte
            ? { gte: args.time_gte as string, lte: args.time_lte as string }
            : undefined
        );

      // Stubs
      case 'box_list_files':
        return stubs.boxListFiles();
      case 'canva_list_designs':
        return stubs.canvaListDesigns();
      case 'clarity_get_dashboard':
        return stubs.clarityGetDashboard();

      // Supabase
      case 'supabase_list_projects':
        return supabase.listProjects();
      case 'supabase_get_project':
        return supabase.getProject(args.project_ref as string | undefined);
      case 'supabase_list_organizations':
        return supabase.listOrganizations();
      case 'supabase_list_functions':
        return supabase.listFunctions(args.project_ref as string | undefined);
      case 'supabase_run_sql':
        return supabase.runSqlQuery(
          args.query as string,
          args.project_ref as string | undefined
        );
      case 'supabase_get_api_keys':
        return supabase.getProjectApiKeys(args.project_ref as string | undefined);

      // MongoDB Atlas
      case 'mongodb_list_organizations':
        return mongodb.listOrganizations();
      case 'mongodb_list_projects':
        return mongodb.listProjects(args.org_id as string | undefined);
      case 'mongodb_list_clusters':
        return mongodb.listClusters(args.project_id as string);
      case 'mongodb_get_cluster':
        return mongodb.getCluster(
          args.project_id as string,
          args.cluster_name as string
        );

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    logger.error('Tool error', { name, error: message });
    throw error;
  }
}

// Create and run server
async function main() {
  logger.info('Starting MCP SaaS Gateway server');

  const server = new Server(
    {
      name: 'saas-gateway',
      version: '1.0.0',
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // List tools handler
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools };
  });

  // Call tool handler
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    try {
      const result = await handleToolCall(name, args || {});
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({ error: message }),
          },
        ],
        isError: true,
      };
    }
  });

  // Connect via stdio
  const transport = new StdioServerTransport();
  await server.connect(transport);

  logger.info('MCP SaaS Gateway server running');
}

main().catch((error) => {
  logger.error('Server error', { error: error.message });
  process.exit(1);
});
