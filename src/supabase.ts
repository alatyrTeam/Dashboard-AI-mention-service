import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

export const hasSupabaseConfig = Boolean(supabaseUrl && supabaseAnonKey);
export const initialAuthRedirectHref = typeof window === "undefined" ? "" : window.location.href;

export const supabase = createClient(
  supabaseUrl || "https://example.invalid",
  supabaseAnonKey || "missing-anon-key",
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      storageKey: "rankberry-dashboard-supabase-auth",
    },
  },
);
