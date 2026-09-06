import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;

const supabasePublishableKey =
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;

console.log("SUPABASE URL EXISTS:", Boolean(supabaseUrl));
console.log(
  "SUPABASE PUBLISHABLE KEY EXISTS:",
  Boolean(supabasePublishableKey)
);

if (!supabaseUrl) {
  throw new Error(
    "Missing NEXT_PUBLIC_SUPABASE_URL in frontend/.env.local"
  );
}

if (!supabasePublishableKey) {
  throw new Error(
    "Missing NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY in frontend/.env.local"
  );
}

export const supabase = createClient(
  supabaseUrl,
  supabasePublishableKey
);