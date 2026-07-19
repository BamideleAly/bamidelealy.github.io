export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return cors(new Response(null, { status: 204 }), request);
    if (request.method !== 'POST') return cors(new Response('Method Not Allowed', { status: 405 }), request);
    const origin = request.headers.get('Origin') || '';
    if (!allowedOrigin(origin, env)) return new Response('Forbidden', { status: 403 });
    let payload;
    try {
      payload = await request.json();
    } catch (_) {
      return cors(new Response('Bad Request', { status: 400 }), request);
    }
    const event = sanitize(payload.event, 64);
    const path = sanitize(payload.path, 240);
    if (!event || !path) return cors(new Response('Bad Request', { status: 400 }), request);
    const day = new Date().toISOString().slice(0, 10);
    const key = `${day}:${event}:${path}`;
    if (env.ANALYTICS_KV) {
      const current = Number(await env.ANALYTICS_KV.get(key)) || 0;
      await env.ANALYTICS_KV.put(key, String(current + 1), { expirationTtl: 60 * 60 * 24 * 400 });
    }
    return cors(Response.json({ ok: true }), request);
  }
};

function allowedOrigin(origin, env) {
  const allowed = (env.ALLOWED_ORIGINS || 'https://bamidelealy.com,http://127.0.0.1:8081,http://localhost:8081').split(',');
  return allowed.includes(origin);
}

function cors(response, request) {
  const origin = request.headers.get('Origin') || 'https://bamidelealy.com';
  response.headers.set('Access-Control-Allow-Origin', origin);
  response.headers.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type');
  response.headers.set('Cache-Control', 'no-store');
  return response;
}

function sanitize(value, limit) {
  return String(value || '').replace(/[^a-zA-Z0-9_:\/.#?&=-]/g, '').slice(0, limit);
}
