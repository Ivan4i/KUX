/**
 * Shared HTTP client with timeouts, retries, and normalized errors
 */

interface HttpClientOptions {
  timeout?: number;
  retries?: number;
  retryDelay?: number;
}

interface HttpResponse<T = unknown> {
  ok: boolean;
  status: number;
  statusText: string;
  data: T;
  headers: Headers;
}

export class HttpError extends Error {
  constructor(
    message: string,
    public status: number,
    public statusText: string,
    public data?: unknown
  ) {
    super(message);
    this.name = 'HttpError';
  }
}

const DEFAULT_TIMEOUT = 30000;
const DEFAULT_RETRIES = 2;
const DEFAULT_RETRY_DELAY = 1000;

async function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export async function httpRequest<T = unknown>(
  url: string,
  options: RequestInit & HttpClientOptions = {}
): Promise<HttpResponse<T>> {
  const {
    timeout = DEFAULT_TIMEOUT,
    retries = DEFAULT_RETRIES,
    retryDelay = DEFAULT_RETRY_DELAY,
    ...fetchOptions
  } = options;

  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        ...fetchOptions,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      let data: T;
      const contentType = response.headers.get('content-type') || '';

      if (contentType.includes('application/json')) {
        data = await response.json() as T;
      } else {
        data = await response.text() as unknown as T;
      }

      if (!response.ok) {
        throw new HttpError(
          `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          response.statusText,
          data
        );
      }

      return {
        ok: response.ok,
        status: response.status,
        statusText: response.statusText,
        data,
        headers: response.headers,
      };
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      // Don't retry on 4xx errors (client errors)
      if (error instanceof HttpError && error.status >= 400 && error.status < 500) {
        throw error;
      }

      // Retry on network errors or 5xx errors
      if (attempt < retries) {
        await sleep(retryDelay * (attempt + 1)); // Exponential backoff
        continue;
      }
    }
  }

  throw lastError || new Error('Unknown HTTP error');
}

export function createServiceClient(baseUrl: string, defaultHeaders: Record<string, string> = {}) {
  return {
    async get<T = unknown>(path: string, options: HttpClientOptions = {}): Promise<T> {
      const response = await httpRequest<T>(`${baseUrl}${path}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          ...defaultHeaders,
        },
        ...options,
      });
      return response.data;
    },

    async post<T = unknown>(path: string, body?: unknown, options: HttpClientOptions = {}): Promise<T> {
      const response = await httpRequest<T>(`${baseUrl}${path}`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          ...defaultHeaders,
        },
        body: body ? JSON.stringify(body) : undefined,
        ...options,
      });
      return response.data;
    },
  };
}
