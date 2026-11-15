// Forja do Herói · lembrete de treino por notificação (Web Push)
// GET  ?pub=1            -> devolve a chave pública VAPID (gera na primeira vez)
// POST (x-cron: token)   -> roda o envio: avisa quem passou do horário e ainda não treinou hoje
import { createClient } from "npm:@supabase/supabase-js@2";
import webpush from "npm:web-push@3.6.7";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const cors = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Methods": "GET,POST,OPTIONS" };

const INTERVAL_MIN = 30;   // repete a cada 30 min
const MAX_PER_DAY = 6;     // no máximo 6 avisos por dia
const STOP_HOUR = 23;      // não manda depois das 23h

// 1º aviso (na hora do treino), avisos do meio, e o último do dia. {n} = nome do jogador
const FIRST = [
  ["[SISTEMA] Missão diária disponível", "{n}, a missão de hoje foi liberada. Cumpra para receber XP."],
  ["[SISTEMA] Você está próximo do despertar", "{n}, seu corpo está mudando. Treine hoje e o despertar chega mais cedo."],
  ["[SISTEMA] O portal foi aberto", "{n}, a hora do treino chegou. Entre e cumpra a missão."],
  ["[SISTEMA] Nova missão recebida", "{n}, o Sistema escolheu você. Inicie o treino de hoje."],
];
const MID = [
  ["[SISTEMA] Missão pendente", "{n}, o treino de hoje ainda não foi registrado. A sequência está em risco."],
  ["[SISTEMA] Você ainda não está pronto para a Dungeon", "{n}, só quem treina todo dia sobrevive lá dentro. Cumpra a missão."],
  ["[SISTEMA] O despertar está próximo", "{n}, não pare agora. Mais um treino e você sobe de nível."],
  ["[SISTEMA] Jogador inativo detectado", "{n}, o Sistema está esperando. Uma única série já conta."],
  ["[SISTEMA] Os chefes estão ficando mais fortes", "{n}, enquanto você descansa, eles evoluem. Treine hoje."],
  ["[SISTEMA] Recompensa bloqueada", "{n}, o XP e o ouro de hoje só são liberados após o treino."],
];
const LAST = [
  ["[SISTEMA] Aviso de penalidade", "{n}, se a missão não for cumprida, a sequência será zerada à meia-noite."],
  ["[SISTEMA] Último aviso", "{n}, a missão diária expira hoje. O Sistema não aceita desculpas."],
];
// mensagens do Sistema fora do lembrete (deixam o app mais imersivo)
const MORNING = [
  ["[SISTEMA] Bom dia, caçador", "{n}, um novo dia começou. Sua missão diária já está à sua espera."],
  ["[SISTEMA] Hora de acordar, caçador", "{n}, o Sistema detectou o nascer do sol. Beba água e prepare o corpo."],
  ["[SISTEMA] Novo dia registrado", "{n}, as missões foram renovadas. Hoje o treino é às {h}."],
  ["[SISTEMA] Jogador desperto", "{n}, quem acorda com propósito evolui mais rápido. Bom dia."],
  ["[SISTEMA] Status: descansado", "{n}, sua energia foi restaurada durante a noite. Use bem."],
];
const NIGHT_DONE = [
  ["[SISTEMA] Hora de descansar, caçador", "{n}, missão cumprida. O músculo cresce no descanso. Durma bem."],
  ["[SISTEMA] Recuperação iniciada", "{n}, seu corpo está processando o XP de hoje. Desligue a tela e descanse."],
  ["[SISTEMA] Dia concluído com sucesso", "{n}, o Sistema registrou seu esforço. Amanhã você estará mais forte."],
  ["[SISTEMA] Modo regeneração", "{n}, 7 a 8 horas de sono garantem bônus de força amanhã. Boa noite."],
];
const DAY_LORE = [
  ["[SISTEMA] Mensagem do Sistema", "{n}, lembre-se de beber água. Um caçador desidratado perde força."],
  ["[SISTEMA] Rumor na Taverna", "{n}, dizem que um novo chefe foi visto perto da Dungeon. Você está pronto?"],
  ["[SISTEMA] Dica do Sistema", "{n}, proteína em todas as refeições acelera sua evolução."],
  ["[SISTEMA] Você está sendo observado", "{n}, outros caçadores estão subindo no ranking. Não fique para trás."],
  ["[SISTEMA] Fragmento de memória", "{n}, todo caçador lendário começou no nível 1. Continue."],
  ["[SISTEMA] Postura detectada", "{n}, endireite a coluna. Um herói não anda curvado."],
  ["[SISTEMA] O despertar se aproxima", "{n}, sua sequência está construindo algo maior. Não quebre agora."],
];

// ---- versões em espanhol (es) e inglês (en): mesma ordem das listas em português ----
const L10N: Record<string, Record<string, string[][]>> = {
  es: {
    FIRST: [["[SISTEMA] Misión diaria disponible", "{n}, la misión de hoy fue liberada. Cúmplela para recibir XP."],
      ["[SISTEMA] Estás cerca del despertar", "{n}, tu cuerpo está cambiando. Entrena hoy y el despertar llega antes."],
      ["[SISTEMA] El portal se abrió", "{n}, llegó la hora de entrenar. Entra y cumple la misión."],
      ["[SISTEMA] Nueva misión recibida", "{n}, el Sistema te eligió. Inicia el entrenamiento de hoy."]],
    MID: [["[SISTEMA] Misión pendiente", "{n}, el entrenamiento de hoy todavía no se registró. La racha está en riesgo."],
      ["[SISTEMA] Todavía no estás listo para la Mazmorra", "{n}, solo quien entrena todos los días sobrevive ahí dentro. Cumple la misión."],
      ["[SISTEMA] El despertar está cerca", "{n}, no pares ahora. Un entrenamiento más y subes de nivel."],
      ["[SISTEMA] Jugador inactivo detectado", "{n}, el Sistema te está esperando. Una sola serie ya cuenta."],
      ["[SISTEMA] Los jefes se están haciendo más fuertes", "{n}, mientras descansas, ellos evolucionan. Entrena hoy."],
      ["[SISTEMA] Recompensa bloqueada", "{n}, el XP y el oro de hoy solo se liberan después del entrenamiento."]],
    LAST: [["[SISTEMA] Aviso de penalización", "{n}, si la misión no se cumple, la racha se reinicia a medianoche."],
      ["[SISTEMA] Último aviso", "{n}, la misión diaria vence hoy. El Sistema no acepta excusas."]],
    MORNING: [["[SISTEMA] Buenos días, cazador", "{n}, un nuevo día comenzó. Tu misión diaria ya te está esperando."],
      ["[SISTEMA] Hora de despertar, cazador", "{n}, el Sistema detectó el amanecer. Toma agua y prepara el cuerpo."],
      ["[SISTEMA] Nuevo día registrado", "{n}, las misiones se renovaron. Hoy el entrenamiento es a las {h}."],
      ["[SISTEMA] Jugador despierto", "{n}, quien despierta con propósito evoluciona más rápido. Buenos días."],
      ["[SISTEMA] Estado: descansado", "{n}, tu energía se restauró durante la noche. Úsala bien."]],
    NIGHT_DONE: [["[SISTEMA] Hora de descansar, cazador", "{n}, misión cumplida. El músculo crece en el descanso. Duerme bien."],
      ["[SISTEMA] Recuperación iniciada", "{n}, tu cuerpo está procesando el XP de hoy. Apaga la pantalla y descansa."],
      ["[SISTEMA] Día completado con éxito", "{n}, el Sistema registró tu esfuerzo. Mañana estarás más fuerte."],
      ["[SISTEMA] Modo regeneración", "{n}, de 7 a 8 horas de sueño garantizan bono de fuerza mañana. Buenas noches."]],
    DAY_LORE: [["[SISTEMA] Mensaje del Sistema", "{n}, recuerda tomar agua. Un cazador deshidratado pierde fuerza."],
      ["[SISTEMA] Rumor en la Taberna", "{n}, dicen que vieron un nuevo jefe cerca de la Mazmorra. ¿Estás listo?"],
      ["[SISTEMA] Consejo del Sistema", "{n}, proteína en todas las comidas acelera tu evolución."],
      ["[SISTEMA] Te están observando", "{n}, otros cazadores están subiendo en el ranking. No te quedes atrás."],
      ["[SISTEMA] Fragmento de memoria", "{n}, todo cazador legendario empezó en el nivel 1. Sigue."],
      ["[SISTEMA] Postura detectada", "{n}, endereza la espalda. Un héroe no camina encorvado."],
      ["[SISTEMA] El despertar se acerca", "{n}, tu racha está construyendo algo más grande. No la rompas ahora."]],
    DUEL: [["[SISTEMA] Te desafiaron a un duelo", "{a} te desafió: quien haga {w} {q}. ¿Aceptas?"],
      ["[SISTEMA] Duelo aceptado", "{a} aceptó tu desafío. Que gane el más fuerte."],
      ["[SISTEMA] Duelo rechazado", "{a} rechazó el desafío. Tal vez tiene miedo."]],
    WORDS: [["mais XP", "más XP"], ["mais repetições de", "más repeticiones de"], ["hoje", "hoy"], ["amanhã", "mañana"], ["Um caçador", "Un cazador"], ["Jogador", "Jugador"]],
  },
  en: {
    FIRST: [["[SYSTEM] Daily quest available", "{n}, today's quest has been unlocked. Complete it to earn XP."],
      ["[SYSTEM] You are close to awakening", "{n}, your body is changing. Train today and the awakening comes sooner."],
      ["[SYSTEM] The portal has opened", "{n}, it's time to train. Step in and complete the quest."],
      ["[SYSTEM] New quest received", "{n}, the System has chosen you. Start today's workout."]],
    MID: [["[SYSTEM] Quest pending", "{n}, today's workout hasn't been logged yet. Your streak is at risk."],
      ["[SYSTEM] You're not ready for the Dungeon yet", "{n}, only those who train every day survive in there. Complete the quest."],
      ["[SYSTEM] The awakening is near", "{n}, don't stop now. One more workout and you level up."],
      ["[SYSTEM] Inactive player detected", "{n}, the System is waiting. A single set counts."],
      ["[SYSTEM] The bosses are getting stronger", "{n}, while you rest, they evolve. Train today."],
      ["[SYSTEM] Reward locked", "{n}, today's XP and gold only unlock after your workout."]],
    LAST: [["[SYSTEM] Penalty warning", "{n}, if the quest isn't completed, your streak resets at midnight."],
      ["[SYSTEM] Final warning", "{n}, the daily quest expires today. The System accepts no excuses."]],
    MORNING: [["[SYSTEM] Good morning, hunter", "{n}, a new day has begun. Your daily quest is already waiting."],
      ["[SYSTEM] Time to wake up, hunter", "{n}, the System detected sunrise. Drink some water and get your body ready."],
      ["[SYSTEM] New day logged", "{n}, your quests have reset. Today's workout is at {h}."],
      ["[SYSTEM] Player awake", "{n}, those who wake up with purpose level up faster. Good morning."],
      ["[SYSTEM] Status: rested", "{n}, your energy was restored overnight. Use it well."]],
    NIGHT_DONE: [["[SYSTEM] Time to rest, hunter", "{n}, quest complete. Muscle grows while you rest. Sleep well."],
      ["[SYSTEM] Recovery started", "{n}, your body is processing today's XP. Put the screen down and rest."],
      ["[SYSTEM] Day completed", "{n}, the System logged your effort. Tomorrow you'll be stronger."],
      ["[SYSTEM] Regeneration mode", "{n}, 7 to 8 hours of sleep guarantees a strength bonus tomorrow. Good night."]],
    DAY_LORE: [["[SYSTEM] Message from the System", "{n}, remember to drink water. A dehydrated hunter loses strength."],
      ["[SYSTEM] Rumor at the Tavern", "{n}, they say a new boss was spotted near the Dungeon. Are you ready?"],
      ["[SYSTEM] System tip", "{n}, protein in every meal speeds up your progress."],
      ["[SYSTEM] You are being watched", "{n}, other hunters are climbing the leaderboard. Don't fall behind."],
      ["[SYSTEM] Memory fragment", "{n}, every legendary hunter started at level 1. Keep going."],
      ["[SYSTEM] Posture detected", "{n}, straighten your back. A hero doesn't slouch."],
      ["[SYSTEM] The awakening approaches", "{n}, your streak is building something bigger. Don't break it now."]],
    DUEL: [["[SYSTEM] You've been challenged to a duel", "{a} challenged you: whoever does {w} {q}. You in?"],
      ["[SYSTEM] Duel accepted", "{a} accepted your challenge. May the strongest win."],
      ["[SYSTEM] Duel declined", "{a} declined the challenge. Maybe they're scared."]],
    WORDS: [["mais XP", "the most XP"], ["mais repetições de", "the most reps of"], ["hoje", "today"], ["amanhã", "tomorrow"], ["Um caçador", "A hunter"], ["Jogador", "Player"]],
  },
};
const PT_POOLS: Record<string, string[][]> = { FIRST, MID, LAST, MORNING, NIGHT_DONE, DAY_LORE };
function pools(lang: string) { return (L10N[lang] ? L10N[lang] : PT_POOLS) as Record<string, string[][]>; }
function words(lang: string, t: string) { for (const [a, b] of (L10N[lang]?.WORDS || [])) t = t.replaceAll(a, b); return t; }
function appBase(lang: string) { return L10N[lang] ? `/${lang}/app/` : "/app/"; }
function seedOf(str: string) { return [...str].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7); }
function fill(t: [string, string], n: string, h: string, lang = "pt") { return [t[0], t[1].replace("{n}", n || words(lang, "Jogador")).replace("{h}", h)]; }
async function push(s: any, title: string, body: string, url: string, tag: string) {
  await webpush.sendNotification({ endpoint: s.endpoint, keys: { p256dh: s.p256dh, auth: s.auth } },
    JSON.stringify({ title, body, url, tag }), { TTL: 3600 });
}

function pickMsg(sent: number, day: string, name: string, lang = "pt") {
  const seed = [...day].reduce((a, c) => a + c.charCodeAt(0), 0);
  const P = pools(lang);
  const pool = sent === 0 ? P.FIRST : sent >= MAX_PER_DAY - 1 ? P.LAST : P.MID;
  const [t, b] = pool[(seed + sent) % pool.length];
  return [t, b.replace("{n}", name || words(lang, "Jogador"))];
}

async function cfg(k: string) {
  const { data } = await db.from("fh_push_config").select("v").eq("k", k).maybeSingle();
  return data?.v as string | undefined;
}
async function vapid() {
  let pub = await cfg("vapid_public"), priv = await cfg("vapid_private");
  if (!pub || !priv) {
    const k = webpush.generateVAPIDKeys();
    await db.from("fh_push_config").upsert([{ k: "vapid_public", v: k.publicKey }, { k: "vapid_private", v: k.privateKey }]);
    pub = k.publicKey; priv = k.privateKey;
  }
  return { pub, priv };
}
function localNow(tz: string) {
  const p = Object.fromEntries(new Intl.DateTimeFormat("en-CA", { timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date()).map((x) => [x.type, x.value]));
  return { day: `${p.year}-${p.month}-${p.day}`, mins: +p.hour * 60 + +p.minute };
}

const J = (o: unknown, st = 200) => new Response(JSON.stringify(o), { status: st, headers: { ...cors, "Content-Type": "application/json" } });
async function adminSend(req: Request, authz: string) {
  const user = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, { global: { headers: { Authorization: authz } } });
  const { data: isAdmin } = await user.rpc("fh_is_admin");
  if (!isAdmin) return J({ error: "acesso negado" }, 403);
  const { data: me } = await user.auth.getUser();
  const b = await req.json().catch(() => ({}));
  const title = String(b.title || "").slice(0, 80), body = String(b.body || "").slice(0, 240), target = String(b.target || "all");
  if (!title || !body) return J({ error: "título e mensagem são obrigatórios" }, 400);
  const { data: subs } = await db.from("fh_push").select("*").eq("enabled", true);
  let list = subs || [];
  if (target === "users") list = list.filter((s) => (b.user_ids || []).includes(s.user_id));
  else if (target.startsWith("lang:")) list = list.filter((s) => String(s.lang || "pt") === target.slice(5));
  else if (target !== "all") {
    const ids = list.map((s) => s.user_id);
    const { data: saves } = await db.from("fh_saves").select("user_id,data").in("user_id", ids.length ? ids : ["00000000-0000-0000-0000-000000000000"]);
    const { data: users } = await db.auth.admin.listUsers({ perPage: 1000 });
    const emailOf = new Map((users?.users || []).map((u) => [u.id, (u.email || "").toLowerCase()]));
    const { data: orders } = await db.from("fh_orders").select("email,plan,status").eq("status", "pago");
    const planOf = (uid: string) => { const e = emailOf.get(uid); const os = (orders || []).filter((o) => o.email === e); return os.some((o) => o.plan === "elite") ? "elite" : os.length ? "recruta" : ""; };
    const lastDay = (uid: string) => { const l = ((saves || []).find((x) => x.user_id === uid)?.data?.log || []) as { d: string }[]; return l.reduce((m, e) => (e.d > m ? e.d : m), ""); };
    list = list.filter((s) => {
      const { day } = localNow(s.tz || "America/Sao_Paulo"); const ld = lastDay(s.user_id);
      if (target === "notToday") return ld !== day;
      if (target === "inactive3") { const d = new Date(day + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - 3); return !ld || ld < d.toISOString().slice(0, 10); }
      if (target === "never") return !ld;
      if (target === "elite") return planOf(s.user_id) === "elite";
      if (target === "recruta") return planOf(s.user_id) === "recruta";
      return true;
    });
  }
  const { pub, priv } = await vapid();
  webpush.setVapidDetails("mailto:suporte@forjadoheroi.app", pub, priv);
  let sent = 0, failed = 0;
  for (const s of list) {
    try {
      const { data: sv } = await db.from("fh_saves").select("data").eq("user_id", s.user_id).maybeSingle();
      const nome = String(sv?.data?.name || "Jogador").split(/[\s,]+/)[0];
      await webpush.sendNotification({ endpoint: s.endpoint, keys: { p256dh: s.p256dh, auth: s.auth } },
        JSON.stringify({ title: title.replaceAll("{nome}", nome), body: body.replaceAll("{nome}", nome), url: b.url || appBase(String(s.lang || "pt")), tag: "fh-admin-" + Date.now() }), { TTL: 86400 });
      sent++;
    } catch (e: any) {
      failed++;
      if (e?.statusCode === 404 || e?.statusCode === 410) await db.from("fh_push").delete().eq("user_id", s.user_id);
    }
  }
  await db.from("fh_push_log").insert({ by_email: me?.user?.email, title, body, target, sent, failed });
  return J({ ok: true, sent, failed, total: list.length });
}

async function duelNotify(b: any, authz: string) {
  const user = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, { global: { headers: { Authorization: authz } } });
  const { data: { user: me } } = await user.auth.getUser();
  if (!me) return J({ error: "login" }, 401);
  const { data: d } = await db.from("fh_duels").select("*").eq("code", String(b.duel).toUpperCase()).maybeSingle();
  if (!d) return J({ error: "duelo" }, 404);
  let to = "", title = "", body = "";
  const nameOf = async (uid: string) => { const { data } = await db.from("fh_saves").select("data").eq("user_id", uid).maybeSingle(); return String(data?.data?.name || "Um caçador").split(/[\s,]+/)[0]; };
  const what = d.kind === "xp" ? "mais XP" : `mais repetições de ${String(b.exn || "um exercício").slice(0, 40)}`;
  const quando = b.when === "amanhã" ? "amanhã" : "hoje";
  if (b.event === "invite" && d.creator === me.id && d.opponent && d.status === "invited") {
    to = d.opponent; title = "[SISTEMA] Você foi desafiado para um duelo"; body = `${await nameOf(me.id)} desafiou você: quem faz ${what} ${quando}. Aceita?`;
  } else if (b.event === "accepted" && d.opponent === me.id && d.status === "active") {
    to = d.creator; title = "[SISTEMA] Duelo aceito"; body = `${await nameOf(me.id)} aceitou seu desafio. Que vença o mais forte.`;
  } else if (b.event === "declined" && d.opponent === me.id && d.status === "declined") {
    to = d.creator; title = "[SISTEMA] Duelo recusado"; body = `${await nameOf(me.id)} recusou o desafio. Talvez esteja com medo.`;
  } else return J({ ok: true, skipped: true });
  const { data: sub } = await db.from("fh_push").select("*").eq("user_id", to).eq("enabled", true).maybeSingle();
  if (!sub) return J({ ok: true, noPush: true });
  const lg = String(sub.lang || "pt");
  if (L10N[lg]) {
    const k = b.event === "invite" ? 0 : b.event === "accepted" ? 1 : 2;
    const [t2, b2] = L10N[lg].DUEL[k];
    title = t2; body = b2.replace("{a}", words(lg, await nameOf(me.id))).replace("{w}", words(lg, what)).replace("{q}", words(lg, quando));
  }
  const { pub, priv } = await vapid();
  webpush.setVapidDetails("mailto:suporte@forjadoheroi.app", pub, priv);
  try { await push(sub, title, body, `${appBase(String(sub.lang || "pt"))}?duelo=${d.code}`, "fh-duel-" + d.code); } catch (e: any) { if (e?.statusCode === 404 || e?.statusCode === 410) await db.from("fh_push").delete().eq("user_id", to); }
  return J({ ok: true });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const url = new URL(req.url);
  if (req.method === "GET" && url.searchParams.has("pub")) {
    const { pub } = await vapid();
    return new Response(JSON.stringify({ publicKey: pub }), { headers: { ...cors, "Content-Type": "application/json" } });
  }
  // envio manual pela Central de Admin (precisa estar logado como admin)
  const authz = req.headers.get("Authorization") || "";
  if (req.method === "POST" && !req.headers.get("x-cron") && authz.startsWith("Bearer ")) {
    const peek = await req.clone().json().catch(() => ({}));
    if (peek && peek.duel) return duelNotify(peek, authz);
    return adminSend(req, authz);
  }
  if (req.method !== "POST" || req.headers.get("x-cron") !== (await cfg("cron_token"))) return new Response("forbidden", { status: 403 });

  const { pub, priv } = await vapid();
  webpush.setVapidDetails("mailto:suporte@forjadoheroi.app", pub, priv);
  const { data: subs } = await db.from("fh_push").select("*").eq("enabled", true);
  const out: string[] = [];
  for (const s of subs || []) {
    try {
      const { day, mins } = localNow(s.tz || "America/Sao_Paulo");
      const [h, m] = s.train_time.split(":").map(Number);
      // ---- mensagens ambiente (1 de cada tipo por dia) ----
      const amb: string[] = s.amb_day === day ? (s.amb_sent || []) : [];
      const sd = seedOf(s.user_id + day);
      let ambKind = "";
      if (mins >= 7 * 60 && mins < 8 * 60 + 30 && h * 60 + m - mins > 60 && !amb.includes("am")) ambKind = "am";
      else if (mins >= 21 * 60 + 30 && mins < 22 * 60 + 30 && !amb.includes("pm")) ambKind = "pm";
      else { const at = 10 * 60 + (sd % 600); if (mins >= at && mins < at + 30 && Math.abs(mins - (h * 60 + m)) > 60 && !amb.includes("day")) ambKind = "day"; }
      if (ambKind) {
        const { data: sv0 } = await db.from("fh_saves").select("data").eq("user_id", s.user_id).maybeSingle();
        const nome = String(sv0?.data?.name || "").split(/[\s,]+/)[0];
        const trained = ((sv0?.data?.log || []) as { d: string }[]).some((e) => e.d === day);
        let msg: string[] | null = null;
        const lg = String(s.lang || "pt"), PP = pools(lg);
        if (ambKind === "am") msg = fill(PP.MORNING[sd % PP.MORNING.length] as [string, string], nome, s.train_time, lg);
        if (ambKind === "pm" && trained) msg = fill(PP.NIGHT_DONE[sd % PP.NIGHT_DONE.length] as [string, string], nome, s.train_time, lg);
        if (ambKind === "day") msg = fill(PP.DAY_LORE[sd % PP.DAY_LORE.length] as [string, string], nome, s.train_time, lg);
        const sentAmb = [...amb, ambKind];
        if (msg) { try { await push(s, msg[0], msg[1], appBase(String(s.lang || "pt")), "fh-amb-" + ambKind); out.push(`amb ${ambKind} ${s.user_id}`); } catch (e: any) { if (e?.statusCode === 404 || e?.statusCode === 410) { await db.from("fh_push").delete().eq("user_id", s.user_id); continue; } } }
        await db.from("fh_push").update({ amb_day: day, amb_sent: sentAmb }).eq("user_id", s.user_id);
      }
      if (mins < h * 60 + m || mins >= STOP_HOUR * 60) continue;
      const sent = s.last_day === day ? s.sent_today : 0;
      if (sent >= MAX_PER_DAY) continue;
      if (s.last_day === day && s.last_sent_at && Date.now() - new Date(s.last_sent_at).getTime() < (INTERVAL_MIN - 2) * 60000) continue;
      const { data: sv } = await db.from("fh_saves").select("data").eq("user_id", s.user_id).maybeSingle();
      const log = (sv?.data?.log || []) as { d: string }[];
      if (log.some((e) => e.d === day)) continue; // já treinou hoje
      const [title, body] = pickMsg(sent, day, String(sv?.data?.name || "").split(/[\s,]+/)[0], String(s.lang || "pt"));
      try {
        await webpush.sendNotification({ endpoint: s.endpoint, keys: { p256dh: s.p256dh, auth: s.auth } },
          JSON.stringify({ title, body, url: appBase(String(s.lang || "pt")) + "?tab=treinar", tag: "fh-treino" }), { TTL: 1800 });
        await db.from("fh_push").update({ last_day: day, sent_today: sent + 1, last_sent_at: new Date().toISOString() }).eq("user_id", s.user_id);
        out.push(`sent ${s.user_id}`);
      } catch (e: any) {
        if (e?.statusCode === 404 || e?.statusCode === 410) { await db.from("fh_push").delete().eq("user_id", s.user_id); out.push(`gone ${s.user_id}`); }
        else out.push(`err ${s.user_id} ${e?.statusCode || e}`);
      }
    } catch (e) { out.push(`fail ${s.user_id} ${e}`); }
  }
  return new Response(JSON.stringify({ ok: true, checked: subs?.length || 0, out }), { headers: { "Content-Type": "application/json" } });
});
