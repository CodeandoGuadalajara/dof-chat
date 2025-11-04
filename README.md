# DOF Chat

> Your intelligent assistant for navigating Mexico's official legal documents

![Python Version](https://img.shields.io/badge/python-3.14%2B-blue)
<!--
TODO: Check license type
 ![License](https://img.shields.io/badge/license-MIT-green) -->

DOF Chat is a web application that enables natural language querying of the Diario Oficial de la Federación (DOF), Mexico's official government publication. By leveraging AI, it transforms complex legal documents into accessible, conversational information for citizens, legal professionals, and researchers.

---

## About

The **Diario Oficial de la Federación (DOF)** is the official publication organ of the Mexican federal government, managed by the Secretaría de Gobernación. It publishes laws, regulations, decrees, agreements, circulars, orders, treaties, and other acts issued by federal authorities.

### The Problem
Navigating thousands of legal documents published in the DOF is time-consuming and requires expertise in legal terminology. Citizens and professionals alike need quick, accurate answers to legal questions without reading through dense documentation.

### The Solution
DOF Chat provides an AI-powered conversational interface that understands natural language questions in Spanish, retrieves relevant information from DOF documents, and delivers clear, contextual answers.

### Target Audience
- **Citizens** seeking to understand laws and regulations that affect them
- **Legal professionals** researching case precedents and regulatory changes
- **Journalists and researchers** investigating government policies and legal frameworks
- **Government employees** needing quick reference to official publications

---

## Planned Key Features


### DOF Document Types

| Document Type | Spanish Name | Description |
|--------------|--------------|-------------|
| Laws | Leyes | Legislative acts passed by Congress |
| Regulations | Reglamentos | Administrative rules implementing laws |
| Decrees | Decretos | Executive orders and presidential decisions |
| Agreements | Acuerdos | Inter-agency or international agreements |
| Circulars | Circulares | Administrative directives |
| Orders | Órdenes | Official commands and instructions |
| Treaties | Tratados | International agreements and conventions |

---

## Getting Started

### Prerequisites

- Python 3.14 or higher
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - Fast Python package installer
- [gh](https://github.com/cli/cli#installation) - GitHub CLI (for contributors)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/CodeandoGuadalajara/dof-chat.git
cd dof-chat
```

2. Create and activate the virtual environment:
```bash
uv sync --frozen
```

3. Run the application:
```bash
uv run fastapi dev
```

---

## Usage

Once the application is running, navigate to `http://localhost:8000` in your web browser.

**Example queries:**
- "¿Cuáles son los requisitos para abrir una empresa en México?"
- "Reformas fiscales de 2024"

---

## Technology Stack

| Technology | Purpose | Description |
|-----------|---------|-------------|
| **Python** | Core Language | High-level programming language |
| **FastAPI** | Web Framework | Modern, fast web framework for building APIs |
| **Air** | Development Framework | Modern Python web framework built with FastAPI, Starlette, and Pydantic |
| **AI/ML** | Natural Language Processing | Vector embeddings and LLM integration for intelligent query handling |

---

## Roadmap

We're actively developing DOF Chat. Here's what's planned:

- **Natural Language Q&A** - Ask questions in plain Spanish
- **Comprehensive Coverage** - Access to laws, regulations, decrees, agreements, and more
- **Smart Search** - AI-powered semantic search finds relevant documents even with imprecise queries
- **Web-Based Interface** - Access from any device with a browser

<!-- 
TODO: Check any missing items for the roadmap
- **Fast Responses** - Optimized retrieval and generation for quick answers
- **Source Citations** - Every answer includes references to original DOF documents -->

**Note:** This is a new project and we're actively discussing the architecture through [GitHub Issues](https://github.com/CodeandoGuadalajara/dof-chat/issues). Your input is welcome!

---

## Contributing

We welcome contributions from the community! DOF Chat is an open-source project built to serve the public good.

To contribute, please read our [Contributing Guidelines](CONTRIBUTING.md) for detailed instructions on:
- Setting up your development environment
- Creating feature branches
- Submitting pull requests
- Code style and commit conventions

For questions or discussions about the project architecture, check out our [GitHub Issues](https://github.com/CodeandoGuadalajara/dof-chat/issues).

---

<!-- 
TODO: Create LICENSE
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. -->

---

## Contact

- **Project Repository**: [https://github.com/CodeandoGuadalajara/dof-chat](https://github.com/CodeandoGuadalajara/dof-chat)
- **Issue Tracker**: [https://github.com/CodeandoGuadalajara/dof-chat/issues](https://github.com/CodeandoGuadalajara/dof-chat/issues)
<!--
TODO: Enable discussions channel
- **Discussions**: [https://github.com/CodeandoGuadalajara/dof-chat/discussions](https://github.com/CodeandoGuadalajara/dof-chat/discussions) -->

---

## Acknowledgments

- The Secretaría de Gobernación for maintaining the DOF public archives
- The open-source community for the amazing tools that make this project possible
- Codeando Guadalajara for hosting and supporting this civic tech initiative

---

## Disclaimer

DOF Chat is an independent project and is not officially affiliated with or endorsed by the Mexican federal government or the Secretaría de Gobernación. The information provided by this application is for informational purposes only and should not be considered legal advice. Always refer to the official DOF publications for authoritative legal information.