import express from "express";
import { createServer as createViteServer } from "vite";
import { spawn } from "child_process";
import path from "path";
import axios from "axios";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // Start FastAPI server as a child process
  console.log("Starting FastAPI server...");
  const pythonProcess = spawn("py", ["api/simple_server.py"]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`FastAPI: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`FastAPI Error: ${data}`);
  });

  // Proxy endpoints to FastAPI
  const proxyEndpoints = [
    "/api/predict",
    "/api/infer", 
    "/api/train/start",
    "/api/train/stop",
    "/api/train/status",
    "/api/dataset/stats",
    "/api/analysis/failures",
    "/api/health"
  ];

  proxyEndpoints.forEach(endpoint => {
    const method = endpoint.includes("start") || endpoint.includes("stop") || endpoint.includes("predict") || endpoint.includes("infer") ? "post" : "get";
    app[method](endpoint, async (req, res) => {
      try {
        const fastApiUrl = `http://127.0.0.1:8080${endpoint}`;
        console.log(`Proxying ${method.toUpperCase()} ${endpoint} to ${fastApiUrl}`);
        console.log(`Request body:`, req.body);
        const config = {
          method,
          url: fastApiUrl,
          data: req.body,
          proxy: false as const,
          headers: {
            'Content-Type': 'application/json'
          }
        };
        const response = await axios(config);
        console.log(`Response from backend:`, response.data);
        res.json(response.data);
      } catch (error) {
        console.error(`Proxy Error for ${endpoint}:`, error.message);
        console.error(`Full error:`, error);
        res.status(500).json({ error: `Failed to connect to inference engine for ${endpoint}` });
      }
    });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
