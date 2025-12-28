/**
 * Figma Service - Read-only operations
 */

import { createServiceClient } from '../utils/http-client.js';
import { getEnv, getEnvOptional } from '../utils/env.js';
import { logger } from '../utils/logger.js';

const FIGMA_API = 'https://api.figma.com/v1';

function getClient() {
  const token = getEnv('FIGMATOKEN');
  return createServiceClient(FIGMA_API, {
    'X-Figma-Token': token,
  });
}

export interface FigmaFile {
  name: string;
  lastModified: string;
  thumbnailUrl: string;
  version: string;
  document: {
    id: string;
    name: string;
    type: string;
    children: unknown[];
  };
  components: Record<string, FigmaComponent>;
  styles: Record<string, unknown>;
}

export interface FigmaComponent {
  key: string;
  name: string;
  description: string;
  componentSetId?: string;
  documentationLinks: string[];
}

export interface FigmaComponentsResponse {
  meta: {
    components: FigmaComponent[];
  };
}

export async function getFile(fileKey: string): Promise<FigmaFile> {
  const client = getClient();
  logger.info('Fetching Figma file', { fileKey });
  return client.get<FigmaFile>(`/files/${fileKey}`);
}

export async function listComponents(fileKey?: string): Promise<FigmaComponent[]> {
  const client = getClient();
  const targetFile = fileKey || getEnvOptional('FIGMAFILEKEY');

  if (!targetFile) {
    throw new Error('No Figma file key provided. Set FIGMAFILEKEY env or pass fileKey parameter.');
  }

  logger.info('Fetching Figma components', { fileKey: targetFile });
  const response = await client.get<FigmaComponentsResponse>(`/files/${targetFile}/components`);
  return response.meta.components;
}

export async function getFileStyles(fileKey: string): Promise<Record<string, unknown>> {
  const client = getClient();
  logger.info('Fetching Figma styles', { fileKey });
  const file = await client.get<FigmaFile>(`/files/${fileKey}`);
  return file.styles;
}
