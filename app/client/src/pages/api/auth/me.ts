import type { APIRoute } from 'astro';

const API_SERVER_URL = process.env.API_SERVER_URL || 'http://localhost:5100';

export const GET: APIRoute = async ({ request }) => {
  const cookie = request.headers.get('cookie') || '';
  const response = await fetch(`${API_SERVER_URL}/api/auth/me`, {
    headers: cookie ? { cookie } : {},
  });

  return new Response(await response.text(), {
    status: response.status,
    headers: { 'content-type': 'application/json' },
  });
};
