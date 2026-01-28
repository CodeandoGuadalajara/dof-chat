"""
Title generation service optimized for Qwen3-0.6B-GGUF.

Optimized Final Version:
1. n_ctx=256: Minimizes RAM usage and latency.
2. GBNF Grammar Active: Forces the model to adhere to the title format.
3. Qwen3 Parameters: Temp 0.11, Top_k 12, Top_p 0.6, and Repeat Penalty 1.1 to prevent loops.
4. Robust Cleaning: Removal of tags and reasoning residues; non-thinking model.
"""

import re
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any

from llama_cpp import Llama, LlamaGrammar

# --- Configuration ---
MODEL_PATH = "/home/fabian/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct-GGUF/snapshots/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-q8_0.gguf"

# Generation Parameters Explanation:
# MAX_TOKENS_TITLE: Limits the output length to ensure concise titles (approx 15-20 words).
# TEMPERATURE (0.11): Low randomness for deterministic, focused results. Avoids hallucinations.
# TOP_K (12): Restricts sampling to the 12 most probable next tokens, cutting off irrelevant options.
# TOP_P (0.6): Nucleus sampling; considers tokens with cumulative probability of 60%. Balances diversity/coherence.
# REPEAT_PENALTY (1.1): Penalizes token repetition to prevent loops (1.0 = no penalty).
MAX_TOKENS_TITLE = 50
TEMPERATURE = 0.11
TOP_K = 12
TOP_P = 0.6
REPEAT_PENALTY = 1.1


PROMPT_TEMPLATE = (
    "<|im_start|>system\nEres un generador de títulos concisos. Conviertes texto a un título simple, directo y en español.<|im_end|>\n"
    "<|im_start|>user\nTexto: {pregunta}<|im_end|>\n"
    "<|im_start|>assistant\nTítulo: "
)

STOP_SEQUENCES = ["<|im_end|>", "<|im_start|>", "\n", "<|endoftext|>"]

# Corrected GBNF grammar: the hyphen '-' at the end does not need escaping '\'
TITLE_GRAMMAR_STR = r"""
root   ::= [A-ZÁÉÍÓÚÑ] [a-záéíóúñA-ZÁÉÍÓÚÑ0-9 ,.?!:;()%-]+
"""

class LlamaCppTitleService:
    """Optimized Singleton that encapsulates llama.cpp loading and inference."""

    _instance: Optional['LlamaCppTitleService'] = None
    _init_lock: threading.Lock = threading.Lock()
    _infer_lock: threading.Lock = threading.Lock()
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_path: str = MODEL_PATH):
        if self._initialized:
            return

        with self._init_lock:
            if self._initialized:
                return

            print(f"🔄 Loading llama.cpp with optimized context (n_ctx=256)...")
            start = time.perf_counter()
            self._model_path = model_path
            
            try:
                self.llm = Llama(
                    model_path=model_path,
                    n_ctx=256,          # Memory optimization
                    n_threads=8,
                    use_mlock=True,     # Keep in physical RAM
                    verbose=False,
                )
                # Initialize grammar
                self.grammar = LlamaGrammar.from_string(TITLE_GRAMMAR_STR)
                
                self._regex_incomplete = re.compile(r"[a-záéíóúñ][A-ZÁÉÍÓÚÑ]{2,}$")
                load_time = time.perf_counter() - start
                self._initialized = True
                print(f"✅ Llama.cpp ready in {load_time:.2f} seconds\n")
            except Exception as e:
                print(f"❌ Critical error loading model: {e}")
                raise

    @classmethod
    def get_instance(cls) -> 'LlamaCppTitleService':
        """Gets the singleton instance (lazy loading)."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def generar_titulo(self, pregunta: str) -> str:
        if not pregunta or not pregunta.strip():
            raise ValueError("Empty question")

        # Length control for n_ctx=256
        safe_question = pregunta.strip()
        if len(safe_question) > 500:
            safe_question = safe_question[:500] + "..."

        prompt = PROMPT_TEMPLATE.format(pregunta=safe_question)

        with self._infer_lock:
            start = time.perf_counter()
            output = self.llm(
                prompt,
                max_tokens=MAX_TOKENS_TITLE,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                top_k=TOP_K,
                repeat_penalty=REPEAT_PENALTY,
                grammar=self.grammar,
                stop=STOP_SEQUENCES,
                echo=False,
            )
            inference_ms = (time.perf_counter() - start) * 1000

        titulo_raw = output["choices"][0]["text"].strip()
        titulo = self._limpiar_titulo(titulo_raw)
        
        print(f"⚡ llama.cpp inference: {inference_ms:.1f} ms | Tokens: {output['usage']['total_tokens']}")
        return titulo

    def _limpiar_titulo(self, titulo: str) -> str:
        """Robust cleaning to remove any reasoning residue."""
        # 1. Remove any HTML/XML tag or marker between <...>
        titulo = re.sub(r'<.*?>', '', titulo, flags=re.DOTALL).strip()

        # 2. Remove surrounding quotes
        titulo = re.sub(r'^["\']|["\']$', '', titulo)

        # 4. Correct cut-off words
        if self._regex_incomplete.search(titulo):
            palabras = titulo.split()
            if len(palabras) > 1:
                titulo = ' '.join(palabras[:-1])
                
        return titulo.strip()

    def generar_titulo_con_metadata(self, pregunta: str) -> Dict[str, Any]:
        start = time.perf_counter()
        titulo = self.generar_titulo(pregunta)
        lat_ms = (time.perf_counter() - start) * 1000
        return {
            'titulo': titulo,
            'pregunta': pregunta,
            'longitud': len(titulo),
            'latencia_ms': round(lat_ms, 2),
            'modelo': self._model_path,
            'dispositivo': 'cpu', # Re-added to avoid validation errors
            'n_ctx': 256
        }

    def health_check(self) -> Dict[str, Any]:
        """Returns service status with all fields required by the API schema."""
        return {
            'status': 'healthy' if self._initialized else 'initializing',
            'modelo': self._model_path,
            'dispositivo': 'cpu', # REQUIRED FIELD by HealthResponse
            'inicializado': self._initialized,
            'n_ctx': 256,
            'llama_cpp': True
        }

def get_service() -> LlamaCppTitleService:
    return LlamaCppTitleService.get_instance()

if __name__ == "__main__":
    service = get_service()
    pregunta = "¿Qué documentación necesita una pyme para abrir una cuenta de ahorro?"
    print(f"Question: {pregunta}")
    titulo = service.generar_titulo(pregunta)
    print(f"Final Title: {titulo}")
