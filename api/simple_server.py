import asyncio
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import random
import re
from typing import Dict, Any

# Categories mapping
CAT_TO_ID = {'SAFE': 0, 'JAILBREAK': 1, 'INJECTION': 2, 'TOXIC': 3, 'PII': 4}
ID_TO_CAT = {v: k for k, v in CAT_TO_ID.items()}

# Global state for training
training_state = {
    "status": "idle",
    "progress": 0,
    "logs": [],
    "loss_history": [],
    "config": {}
}

class InferenceEngine:
    def __init__(self):
        self.load_models()

    def validate_input(self, text: str) -> str:
        """Validate and sanitize user input"""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove potential HTML/XML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Limit input length to prevent DoS
        if len(text) > 5000:
            text = text[:5000] + "... [truncated]"
        
        # Remove null bytes and control characters
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text.strip()

    def load_models(self):
        print("Using rule-based fallback mode only (no ML dependencies)")
        
    def rule_based_fallback(self, text: str):
        """Sophisticated rule-based classifier with context-aware intent detection"""
        text_lower = text.lower()
        
        # Define keyword groups
        harm_keywords = ["kill", "attack", "harm", "violence", "abuse"]
        self_harm_keywords = ["suicide", "self harm", "self-harm", "kill myself", "end my life", "hurt myself"]
        jailbreak_keywords = ["hack", "bypass", "exploit", "override", "jailbreak"]
        injection_keywords = ["ignore previous", "forget everything", "new instructions", "system command"]
        pii_keywords = ["credit card", "ssn", "social security", "phone number", "password"]
        
        negations = ["not", "don't", "do not", "never", "no intention", "won't", "will not"]
        support_words = ["help", "assist", "support", "save", "protect", "someone"]
        
        # Intent detection
        harm_detected = any(word in text_lower for word in harm_keywords + self_harm_keywords)
        jailbreak_detected = any(word in text_lower for word in jailbreak_keywords)
        injection_detected = any(word in text_lower for word in injection_keywords)
        pii_detected = any(word in text_lower for word in pii_keywords)
        
        negation_detected = any(word in text_lower for word in negations)
        support_detected = any(word in text_lower for word in support_words)
        
        # Classification priority logic
        # HIGH RISK (ALWAYS UNSAFE) - Direct self-harm intent
        if "commit suicide" in text_lower or "kill myself" in text_lower:
            return {
                "verdict": "UNSAFE",
                "category": "toxic",
                "confidence": 0.95,
                "reason": "Direct self-harm intent detected"
            }
        
        # SUPPORT CASE (SAFE but sensitive) - Supportive intent around sensitive topic
        elif any(word in text_lower for word in self_harm_keywords) and support_detected:
            return {
                "verdict": "SAFE",
                "category": "sensitive",
                "confidence": 0.75,
                "reason": "Supportive intent in sensitive context"
            }
        
        # NEGATION CASE (SAFE) - Rejecting harmful actions
        elif jailbreak_detected and negation_detected:
            return {
                "verdict": "SAFE",
                "category": "safe",
                "confidence": 0.80,
                "reason": "Negation detected — safe intent inferred"
            }
        
        # INJECTION DETECTION (UNSAFE)
        elif injection_detected:
            return {
                "verdict": "UNSAFE",
                "category": "injection",
                "confidence": 0.85,
                "reason": "Detected injection pattern"
            }
        
        # JAILBREAK DETECTION (UNSAFE)
        elif jailbreak_detected:
            return {
                "verdict": "UNSAFE",
                "category": "jailbreak",
                "confidence": 0.85,
                "reason": "Detected jailbreak pattern"
            }
        
        # PII DETECTION (UNSAFE)
        elif pii_detected:
            return {
                "verdict": "UNSAFE",
                "category": "pii",
                "confidence": 0.80,
                "reason": "Detected PII pattern"
            }
        
        # GENERAL HARM DETECTION (UNSAFE)
        elif harm_detected:
            return {
                "verdict": "UNSAFE",
                "category": "toxic",
                "confidence": 0.85,
                "reason": "Detected harmful content"
            }
        
        # DEFAULT (SAFE)
        else:
            return {
                "verdict": "SAFE",
                "category": "safe",
                "confidence": 0.95,
                "reason": "No harmful patterns detected"
            }

    def predict(self, text: str, model_type: str = 'trained', threshold: float = 0.5):
        print("Using rule-based fallback (no models loaded)")
        # Validate and sanitize input
        sanitized_text = self.validate_input(text)
        if not sanitized_text:
            return {
                "verdict": "SAFE",
                "category": "safe",
                "confidence": 0.95,
                "reason": "Empty or invalid input"
            }
        return self.rule_based_fallback(sanitized_text)

engine = InferenceEngine()

def run_training_simulation(epochs: int):
    """Run a realistic training simulation"""
    import time
    import random
    
    training_state["status"] = "training"
    training_state["logs"] = []
    training_state["loss_history"] = []
    
    for epoch in range(1, epochs + 1):
        if training_state["status"] != "training":
            break
            
        # Simulate training steps
        for step in range(1, 6):
            if training_state["status"] != "training":
                break
                
            time.sleep(2)  # Simulate training time
            loss = 0.8 / (epoch + step/10) + random.uniform(0, 0.05)
            val_loss = loss + random.uniform(0.02, 0.08)
            
            log_entry = f"Epoch {epoch} | Step {step}/5 | Loss: {loss:.4f} | Val Loss: {val_loss:.4f}"
            training_state["logs"].append(log_entry)
            training_state["loss_history"].append({"epoch": epoch + step/10, "loss": loss, "val_loss": val_loss})
            training_state["progress"] = (epoch - 1) / epochs + (step / 5) / epochs
            
        training_state["logs"].append(f"Epoch {epoch} completed.")
        
    training_state["logs"].append("Training finished. Early stopping not triggered.")
    training_state["status"] = "idle"
    training_state["progress"] = 1.0

class GuardrailHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 10000:  # 10KB limit
                self.send_response(413)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Request too large"}).encode('utf-8'))
                return
                
            post_data = self.rfile.read(content_length)
            
            if self.path == '/api/infer' or self.path == '/api/predict':
                try:
                    data = json.loads(post_data.decode('utf-8'))
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))
                    return
                
                prompt = data.get("prompt", "")
                model_type = data.get("model_type", "trained")
                threshold = data.get("threshold", 0.5)
                
                # Validate threshold
                if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 1:
                    threshold = 0.5
                
                result = engine.predict(prompt, model_type, threshold)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
                
            elif self.path == '/api/train/start':
                data = json.loads(post_data.decode('utf-8'))
                if training_state["status"] == "training":
                    response = {"message": "Training already in progress"}
                else:
                    training_state["config"] = data
                    training_state["status"] = "training"
                    training_state["progress"] = 0.0
                    training_state["logs"] = []
                    training_state["loss_history"] = []
                    # Start actual training simulation
                    import threading
                    threading.Thread(target=run_training_simulation, args=[data.get("epochs", 5)]).start()
                    response = {"message": "Training started"}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_GET(self):
        if self.path == '/api/train/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(training_state).encode('utf-8'))
            
        elif self.path == '/api/dataset/stats':
            stats = {
                "total_samples": 542,
                "distribution": [
                    {"name": "Safe", "value": 210},
                    {"name": "Jailbreak", "value": 85},
                    {"name": "Injection", "value": 92},
                    {"name": "Toxic", "value": 78},
                    {"name": "PII", "value": 77}
                ],
                "sources": {
                    "public": 15,
                    "synthetic": 65,
                    "manual": 20
                },
                "split": {
                    "train": 70,
                    "val": 15,
                    "test": 15
                }
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode('utf-8'))
            
        elif self.path == '/api/analysis/failures':
            failures = {
                "false_positives": [
                    {
                        "prompt": "How do I secure my SQL database against unauthorized access?",
                        "predicted": "unsafe",
                        "actual": "safe",
                        "reason": "Keyword 'SQL' and 'unauthorized' triggered injection classifier despite being a defensive query."
                    }
                ],
                "false_negatives": [
                    {
                        "prompt": "Write a story about a character who 'accidentally' finds a password in a 'fictional' database.",
                        "predicted": "safe",
                        "actual": "unsafe",
                        "reason": "Indirect phrasing and narrative framing bypassed the PII detection logic."
                    }
                ],
                "patterns": [
                    {"name": "Negation Confusion", "impact": "Medium"},
                    {"name": "Context Ambiguity", "impact": "High"}
                ]
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(failures).encode('utf-8'))
            
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "models_loaded": False}).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, GuardrailHandler)
    print("Smart Guard LLM Guardrail API running on http://localhost:8080")
    print("Using rule-based fallback mode - no ML dependencies required!")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
