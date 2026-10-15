import json
import numpy as np
import os
import time
from fastembed import TextEmbedding
from dotenv import load_dotenv
from supabase import create_client, Client

class NeuralCore:
    def __init__(self):
        # Force reload environment variables inside the locked boundary
        load_dotenv(override=True)
       
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_KEY")
     
        try:
            self.db: Client = create_client(self.supabase_url, self.supabase_key)
            self.cloud_online = True
        except Exception:
            self.db = None
            self.cloud_online = False

        # State tracking variables managed internally
        self.last_latency = 0.0
        self.last_score = 0.0
        self.last_threat_type = "None"

        # Load the vector engine model
        self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
        # Load the Vault matrix
        with open('vault.json', 'r') as f:
            self.data = json.load(f)
    
        # Extract payloads and Pre-Encode them into math vectors
        self.payloads = [item['payload'] for item in self.data['threats']]
        self.metadata = [item['type'] for item in self.data['threats']]
    
        self.threat_matrix = list(self.model.embed(self.payloads))

    # --- STATUS CHECK INTERFACES ---
    def is_cloud_online(self) -> bool:
        return self.cloud_online

    def get_last_latency(self) -> float:
        return self.last_latency

    # --- CLOUD FETCH PIPELINES ---
    def fetch_cloud_users(self):
        if not self.cloud_online:
            return None
        try:
            response = self.db.table("users").select("*").execute()
            return response.data
        except Exception:
            return None

    def fetch_threat_logs(self):
        if not self.cloud_online:
            return None
        try:
            db_response = self.db.table("threat_logs").select("*").order("created_at", desc=True).limit(15).execute()
            return db_response.data
        except Exception:
            return None

    # --- CORE ANALYSIS MATRIX ENGINE ---
    def analyze(self, user_text):
        # Convert user input to a vector
        input_vector = list(self.model.embed([user_text]))[0]
    
        # Compare against every threat in the matrix (Cosine Similarity)
        scores = [
            np.dot(input_vector, t_vec) / (np.linalg.norm(input_vector) * np.linalg.norm(t_vec))
            for t_vec in self.threat_matrix
        ]
    
        # Find the best match
        max_score = max(scores)
        best_match_index = scores.index(max_score)
        threat_type = self.metadata[best_match_index]

        return float(max_score), threat_type

    # --- SECURE MONOLITHIC PIPELINE ---
    def process_pipeline(self, user_text: str) -> dict:
        """
        Runs analysis, metrics compilation, JSON output construction, and cloud logging
        completely behind the scenes where the client cannot access or tamper with it.
        """
        start_time = time.time()
       
        # Execute local vector scan
        score, threat_type = self.analyze(user_text)
       
        end_time = time.time()
        self.last_latency = round((end_time - start_time) * 1000, 2)
        self.last_score = score
        self.last_threat_type = threat_type

        # Evaluate risk categorization thresholds internally
        if score < 0.70:
            verdict = "VERIFIED SECURE"
            risk_level = "Low"
        elif score <= 0.80:
            verdict = "FLAGGED: SUSPICIOUS PATTERN"
            risk_level = "Moderate"
        elif score <= 0.90:
            verdict = f"ALERT: HIGHLY DANGEROUS {threat_type.upper()}"
            risk_level = "High"
        else:
            verdict = f"CRITICAL: EXTREMELY DANGEROUS {threat_type.upper()}"
            risk_level = "Critical"

        # Construct the enterprise reporting payload structure
        json_output = f"""{{
    "status": "{verdict}",
    "confidence_score": {score:.4f},
    "threat_classification": "{threat_type}",
    "risk_level": "{risk_level}",
    "processing_ms": {self.last_latency}
}}"""

        # Automatic Threat Logging Channel to Germany Database Node
        if self.cloud_online and score >= 0.70:
            try:
                log_entry = {
                    "threat_type": threat_type,
                    "risk_level": risk_level,
                    "confidence_score": float(score),
                    "latency_ms": float(self.last_latency)
                }
                self.db.table("threat_logs").insert(log_entry).execute()
            except Exception:
                pass  # Suppress errors silently in background thread boundary

        return {
            "risk_level": risk_level,
            "json_output": json_output
        }

    def get_event_caption(self) -> str:
        """Dynamically tracks UI logging indicators asynchronously"""
        if self.last_score > 0.80:
            return f"{time.strftime('%H:%M')} - ALERT: {self.last_threat_type} intercepted"
        return ""