"""Mock data for development and testing."""

# =============================================================================
# MOCK DATA - ESTRUCTURA PARA PRODUCCIÓN
# =============================================================================
# En producción, cada conversación viene de SQLite (conversations.db)
# con la siguiente estructura:
#
# {
#     "id": str,              # UUID único de la conversación
#     "title": str,           # Título de la conversación (max ~50 chars para UI)
#     "created_at": str,      # ISO 8601 timestamp: "2026-01-06T14:30:00"
#     "updated_at": str,      # ISO 8601 timestamp de última actualización
# }
#
# El agrupamiento por fecha (HOY, AYER, ÚLTIMOS 7 DÍAS, etc.) se calcula
# en conversation_service.py comparando 'created_at' con datetime.now()
# =============================================================================

MOCK_CONVERSATIONS = {
    "HOY": [
        {
            "id": "conv-001",
            "title": "Ley de Protección de Datos",
            "created_at": "2026-01-06T10:30:00",
        }
    ],
    "AYER": [
        {
            "id": "conv-002", 
            "title": "Normas de Comercio Exterior",
            "created_at": "2026-01-05T15:45:00",
        }
    ],
    "ÚLTIMOS 7 DÍAS": [
        {
            "id": "conv-003",
            "title": "Reforma Fiscal 2026",
            "created_at": "2026-01-02T09:00:00",
        },
        {
            "id": "conv-004",
            "title": "Reglamento de Construcción",
            "created_at": "2026-01-01T11:20:00",
        },
        {
            "id": "conv-005",
            "title": "Ley General de Salud",
            "created_at": "2025-12-31T16:00:00",
        }
    ],
    "ÚLTIMOS 30 DÍAS": [
        {
            "id": "conv-006",
            "title": "Código de Comercio",
            "created_at": "2025-12-20T14:00:00",
        },
        {
            "id": "conv-007",
            "title": "Ley Federal del Trabajo",
            "created_at": "2025-12-15T10:30:00",
        }
    ]
}
