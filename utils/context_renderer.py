"""Context rendering utilities for DOF Chat accordion display.

ACCORDION SYSTEM FLOW:
======================

This module is responsible for converting document data retrieved by the RAG 
system into an interactive HTML accordion structure using Air framework components.

ACCORDION STRUCTURE (3 LEVELS):
-------------------------------
Level 1: Main Container
└── Consulted sources (N documents) 
    └── Level 2: Individual Document  
        └── Document title (statistics)
            └── Metadata (date, URL)
            └── Level 3: Individual Fragment
                └── ▪ Fragment N - Header
                    └── Text content with Markdown formatting

DATA FLOW:
----------
DocumentSource + ChunkData → Air Components → HTML String → Frontend JSON


MAIN FUNCTIONS:
--------------
1. render_embedded_sources() → Main entry point
2. _format_document_section() → Renders a complete document
3. _format_chunk_collapsible() → Renders an individual fragment
4. _process_markdown_to_components() → Converts Markdown to Air components
"""

import html
import re
import time
from typing import List
from air import Details, Summary, Div, Strong, A, Span, Br, H1, H2, H3, H4, Em
from schemas import DocumentSource, ChunkData

# Pre-compile regex patterns for better performance
_BOLD_PATTERN = re.compile(r'\*\*(.*?)\*\*')
_ITALIC_PATTERN = re.compile(r'(?<!\*)\*([^*]+?)\*(?!\*)')


def render_embedded_sources(sources: List[DocumentSource], query_id: str = None) -> Div:
    """Converts RAG document sources into interactive Air accordion components.
    
    Args:
        sources: List of documents with fragments
        query_id: Unique query ID (optional)
        
    Returns:
        Div: Main Air container component
    """
    if not sources:
        return Div("")
    
    if query_id is None:
        query_id = f"q{int(time.time())}"
    
    num_docs = len(sources)
    sources_content = _render_sources_content(sources)
    
    # Main container with sources accordion
    embedded_component = Div(
        Details(
            Summary(
                "📚 ",
                Strong(f"Fuentes consultadas ({num_docs} documentos)"),
                class_="embedded-sources-summary"
            ),
            Div(
                *sources_content,
                class_="embedded-sources-content"
            ),
            class_="embedded-sources"
        ),
        class_="embedded-sources-container",
        **{"data-query-id": query_id}
    )
    
    return embedded_component


def _render_sources_content(sources: List[DocumentSource]) -> List:
    """Processes list of documents and generates Air components."""
    content_components = []
    
    for index, source in enumerate(sources):
        document_component = _format_document_section(source, index + 1)
        content_components.append(document_component)
    
    return content_components


def _format_document_section(source: DocumentSource, index: int) -> Details:
    """Creates accordion component for a complete document with metadata and fragments.
    
    Args:
        source: Document with chunks and metadata
        index: Document number
        
    Returns:
        Details: Air component of document accordion
    """
    title = source.title or "Documento sin título"
    chunks = source.chunks or []
    url = source.url or ""
    
    # Calculate document statistics
    num_chunks = len(chunks)
    
    age_text = _get_age_text(source)
    content_components = []
    
    # Temporal metadata
    content_components.append(
        Div(
            f"📅 {age_text}",
            class_="document-metadata"
        )
    )
    
    # URL if available
    if url:
        content_components.append(
            Div(
                "🔗 ",
                A(url, href=url, target="_blank", class_="document-metadata-link"),
                class_="document-metadata"
            )
        )
    
    # Add chunks
    for i, chunk in enumerate(chunks, 1):
        chunk_component = _format_chunk_collapsible(chunk, i)
        content_components.append(chunk_component)
    
    # Create document Details component
    document_component = Details(
        Summary(
            f"📄 {title}",
            Span(
                f"({num_chunks} fragmentos)",
                class_="document-stats"
            ),
            class_="document-summary"
        ),
        Div(
            *content_components,
            class_="document-content"
        ),
        class_="document-details"
    )
    
    return document_component


def _format_chunk_collapsible(chunk: ChunkData, index: int) -> Details:
    """Creates accordion component for a document fragment.
    
    Args:
        chunk: Fragment with text and header
        index: Fragment number
        
    Returns:
        Details: Air component of fragment accordion
    """
    text = chunk.text or ""
    header = chunk.header or ""
    
    # Process markdown content
    formatted_text_components = _process_markdown_to_components(text)
    
    # Build chunk title
    chunk_title = f"Fragmento {index}"
    if header:
        chunk_title += f" - {header}"
    
    chunk_component = Details(
        Summary(
            f"▪ {chunk_title}",
            class_="chunk-summary"
        ),
        Div(
            Div(
                *formatted_text_components,
                class_="chunk-content"
            ),
            class_="chunk-content-wrapper"
        ),
        class_="chunk-details"
    )
    
    return chunk_component


def _process_markdown_to_components(text: str) -> List:
    """Converts markdown text to Air components supporting headers, bold and italic formatting.
    
    Args:
        text: Text with Markdown markup
        
    Returns:
        List: Air components (H1-H4, Strong, Em, Br, strings)
    """
    if not text:
        return [text]
    
    components = []
    lines = text.split('\n')
    
    for line in lines:
        # Process headers (order matters: most specific first)
        if line.startswith('#### '):
            components.append(H4(html.escape(line[5:])))
        elif line.startswith('### '):
            components.append(H3(html.escape(line[4:])))
        elif line.startswith('## '):
            components.append(H2(html.escape(line[3:])))
        elif line.startswith('# '):
            components.append(H1(html.escape(line[2:])))
        else:
            # Process inline formatting for regular lines
            line_components = _process_inline_formatting(line)
            components.extend(line_components)
        
        # Add line break except for last line
        if line != lines[-1]:
            components.append(Br())
    
    return components


def _process_inline_formatting(text: str) -> List:
    """Processes bold and italic markdown formatting within a text line.
    
    Args:
        text: Line of text without headers
        
    Returns:
        List: Mix of strings and components (Strong, Em)
    """
    if not text.strip():
        return [text] if text else []
    
    components = []
    
    # Process bold patterns first (**text**)
    parts = _BOLD_PATTERN.split(text)
    
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Even indices are regular text, check for italic
            italic_parts = _ITALIC_PATTERN.split(part)
            for j, italic_part in enumerate(italic_parts):
                if j % 2 == 0:
                    # Regular text - escape HTML entities for security
                    if italic_part:
                        components.append(html.escape(italic_part))
                else:
                    # Italic text - escape content for security
                    components.append(Em(html.escape(italic_part)))
        else:
            # Odd indices are bold text - escape content for security
            components.append(Strong(html.escape(part)))
    
    return components if components else [html.escape(text)]


def _get_age_text(source: DocumentSource) -> str:
    """Returns formatted document age text with date and description if available.
    
    Args:
        source: DocumentSource with temporal metadata
        
    Returns:
        str: Formatted age text with emoji
    """
    # Use provided metadata if available
    if source.age_description and source.age_emoji:
        publication_date = source.publication_date or "Fecha no especificada"
        return f"{publication_date} ({source.age_description}) {source.age_emoji}"
    
    # Fallback for missing age information
    if source.publication_date:
        return f"{source.publication_date} ❓"
    
    return "Fecha no disponible ❓"