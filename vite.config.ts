import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  envDir: "backend/app",
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    allowedHosts: ["meatal-lanora-thornily.ngrok-free.dev"],
    proxy: {
      "/api": "http://localhost:3001",
    },
  },
});
