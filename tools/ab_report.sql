-- Resultado do teste A/B Brasil (quiz x página nova), desde o início do teste
with ini as (select timestamptz '2026-11-25 21:10:00+00' t),
vis as (
  select ab, count(distinct sid) visitas
  from fh_quiz_events, ini
  where ab in ('quiz','pag') and created_at >= ini.t and coalesce(utm_source,'') <> 'teste'
    and ((ab='quiz' and ev='view') or (ab='pag' and step='pag'))
  group by ab),
ven as (
  select substring(raw->'tracking'->>'url' from 'fh_ab=([a-z]+)') ab,
         count(*) vendas, sum((raw->'order'->>'amount')::numeric) faturamento
  from fh_orders, ini
  where status='pago' and updated_at >= ini.t
  group by 1)
select v.ab, v.visitas, coalesce(n.vendas,0) vendas,
       round(100.0*coalesce(n.vendas,0)/nullif(v.visitas,0),2) conversao_pct,
       coalesce(n.faturamento,0) faturamento,
       round(coalesce(n.faturamento,0)/nullif(v.visitas,0),2) receita_por_visita
from vis v left join ven n using (ab) order by ab;
