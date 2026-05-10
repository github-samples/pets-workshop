import type { APIRoute } from 'astro';

const API_SERVER_URL = process.env.API_SERVER_URL || 'http://localhost:5100';

export const POST: APIRoute = async ({ request }) => {
  const cookie = request.headers.get('cookie') || '';
  const response = await fetch(`${API_SERVER_URL}/api/auth/logout`, {
    method: 'POST',
    headers: cookie ? { cookie } : {},
  });

  const body = await response.text();
  const headers = new Headers({ 'content-type': 'application/json' });
  const setCookie = response.headers.get('set-cookie');
  if (setCookie) {
    headers.set('set-cookie', setCookie);
  }

  return new Response(body, { status: response.status, headers });
};
