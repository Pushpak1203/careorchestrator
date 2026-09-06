create extension if not exists pgcrypto;

create table if not exists public.patients (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid unique,
  full_name text not null,
  date_of_birth date,
  phone text not null,
  preferred_language text not null default 'en' check (preferred_language in ('en','es')),
  assigned_clinician text,
  clinician_phone text,
  chronic_conditions text[] not null default '{}',
  risk_level text not null default 'LOW' check (risk_level in ('LOW','MEDIUM','HIGH','CRITICAL')),
  last_check_in_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.vitals (
  id uuid primary key default gen_random_uuid(),
  patient_id uuid not null references public.patients(id) on delete cascade,
  blood_glucose numeric,
  systolic_bp integer,
  diastolic_bp integer,
  heart_rate integer,
  oxygen_saturation numeric,
  weight_kg numeric,
  source text not null default 'manual',
  recorded_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create index if not exists vitals_patient_recorded_idx on public.vitals(patient_id, recorded_at desc);

create table if not exists public.alerts (
  id uuid primary key default gen_random_uuid(),
  patient_id uuid not null references public.patients(id) on delete cascade,
  severity text not null check (severity in ('LOW','MEDIUM','HIGH','CRITICAL')),
  status text not null default 'OPEN' check (status in ('OPEN','ACKNOWLEDGED','RESOLVED')),
  title text not null,
  message text not null,
  source_agent text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  acknowledged_at timestamptz,
  resolved_at timestamptz
);

create index if not exists alerts_patient_created_idx on public.alerts(patient_id, created_at desc);

create table if not exists public.caregivers (
  id uuid primary key default gen_random_uuid(),
  patient_id uuid not null references public.patients(id) on delete cascade,
  full_name text not null,
  relationship text not null,
  phone text not null,
  preferred_language text not null default 'en' check (preferred_language in ('en','es')),
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create unique index if not exists caregivers_patient_phone_idx on public.caregivers(patient_id, phone);

create table if not exists public.care_plans (
  id uuid primary key default gen_random_uuid(),
  patient_id uuid not null references public.patients(id) on delete cascade,
  name text not null,
  goals text not null,
  medications jsonb not null default '[]'::jsonb,
  monitoring_rules jsonb not null default '{}'::jsonb,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.audit_log (
  id uuid primary key default gen_random_uuid(),
  patient_id uuid references public.patients(id) on delete set null,
  actor text not null,
  action text not null,
  entity_type text not null,
  entity_id uuid,
  details jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

alter table public.patients enable row level security;
alter table public.vitals enable row level security;
alter table public.alerts enable row level security;
alter table public.caregivers enable row level security;
alter table public.care_plans enable row level security;
alter table public.audit_log enable row level security;

drop policy if exists "authenticated read patients" on public.patients;
create policy "authenticated read patients" on public.patients for select to authenticated using (true);
drop policy if exists "authenticated read vitals" on public.vitals;
create policy "authenticated read vitals" on public.vitals for select to authenticated using (true);
drop policy if exists "authenticated read alerts" on public.alerts;
create policy "authenticated read alerts" on public.alerts for select to authenticated using (true);
drop policy if exists "authenticated read caregivers" on public.caregivers;
create policy "authenticated read caregivers" on public.caregivers for select to authenticated using (true);

alter publication supabase_realtime add table public.alerts;
