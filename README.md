# FoodAdvisor - AI-Powered Local Dietary Recommendation Platform

## 🎯 Project Overview

FoodAdvisor is an innovative dietary recommendation platform that connects users with personalized nutrition advice while leveraging real-time product data from local Dutch supermarkets. Our platform goes beyond generic meal suggestions by providing actionable, location-specific recommendations that users can immediately act upon.

### Key Features

- **Personalized User Dossiers**: Each user maintains a comprehensive profile including dietary plans, requirements, preferences, and taste profiles
- **AI-Powered Conversational Interface**: Natural language interaction with intelligent agents that understand nutritional needs and local product availability
- **Hyperlocal Recommendations**: Direct integration with Dutch supermarket inventories (currently Jumbo, with plans for Albert Heijn, Action, Lidl and more)
- **Actionable Guidance**: Specific instructions like "Buy product X at Jumbo location Y, prepare using method Z"
- **Comprehensive Planning**: From quick meal suggestions to long-term nutrition strategies
- **Budget & Nutrition Control**: Full transparency and control over costs and nutritional intake

## 🛠️ Technical Architecture

### Current Tech Stack

#### Data Pipeline
- **Web Scraping**: Custom scrapers collect product data from supermarket websites
- **Storage**: Amazon S3 for raw HTML storage
- **ETL Processing**: Python-based ETL pipeline (in progress) transforming HTML to structured data
- **Database**: PostgreSQL on AWS RDS with normalized schema for products, prices, and nutrition data

#### Infrastructure
- **Cloud Provider**: Amazon AWS
- **Network**: VPC configuration for secure internal communication
- **Frontend**: Angular framework (basic structure implemented)

#### Database Schema
- `stores`: Supermarket locations and metadata
- `products`: Product catalog with flexible unit system
- `prices`: Historical price tracking with promotions
- `nutrition`: Standardized nutritional information per 100g/100ml
(Look backend/database/diagram.png for database outline)

### System Architecture (Current)
```
[Web Scrapers] → [S3 Raw Storage] → [ETL Pipeline] → [PostgreSQL RDS]
                                                           ↓
                                                    [Angular Frontend]
```

## 📊 Current Status

### ✅ Completed
- Database schema design and implementation
- Web scraping infrastructure for Jumbo supermarket
- S3 storage pipeline for raw HTML data
- Basic Angular frontend structure
- Global Logger module
- Product data model with flexible unit system (weight/volume/piece/package)

### 🚧 In Progress
- ETL pipeline for HTML parsing and data transformation
- Frontend refinement

### 📋 Ready for Development
- RAG (Retrieval-Augmented Generation) pipeline
- AI agent architecture
- User authentication and profile management
- API Gateway and microservices migration to Amazon EC2. 

## 🚀 Development Roadmap

### Phase 1: Infrastructure Migration & Scalability
**Goal**: Transition from development VPC to production-ready architecture

1. **EC2 Deployment**
   - Migrate application services to EC2 instances
   - Implement auto-scaling groups for demand management
   - Configure load balancers for high availability

2. **API Gateway Implementation**
   - Design RESTful API endpoints for all services
   - Implement rate limiting and authentication
   - Create API documentation with OpenAPI/Swagger

3. **Microservices Architecture**
   - Separate concerns into distinct services:
     - Product Data Service
     - User Management Service
     - Recommendation Engine Service
     - Agent Communication Service

### Phase 2: RAG Pipeline & AI Agent Development
**Goal**: Build intelligent recommendation system with conversational capabilities

1. **RAG Infrastructure Setup**
   - Vector database selection and implementation (consider Pinecone, Weaviate, or pgvector)
   - Embedding generation for product catalog
   - Semantic search capabilities for product matching

2. **Multi-Agent System Architecture**
   
   **Agent 1: Conversational Interface Agent**
   - Primary user interaction point
   - Natural language understanding for dietary preferences
   - Query routing to specialized agents
   - Response synthesis and presentation
   
   **Agent 2: User Profile Management Agent**
   - Dossier creation and maintenance
   - Preference learning and adaptation
   - Historical tracking of user choices
   - Privacy-compliant data handling
   
   **Agent 3: Nutrition & Diet Expert Agent (Future)**
   - Deep knowledge of nutritional science
   - Dietary plan creation and optimization
   - Health goal alignment
   - Medical restriction compliance

3. **Model Context Protocol (MCP) Implementation**
   - Design inter-agent communication protocols
   - Implement shared context management
   - Create agent orchestration layer
   - Build fallback and error handling mechanisms

4. **LLM Selection & Integration**
   - Evaluate options: OpenAI GPT-4, Anthropic Claude, open-source alternatives
   - Implement prompt engineering framework
   - Create evaluation metrics for recommendation quality
   - Set up A/B testing infrastructure

### Phase 3: User Management & Authentication
**Goal**: Secure, scalable user system with personalized experiences

1. **Authentication System**
   - Implement JWT-based authentication
   - OAuth2 integration for social login
   - Multi-factor authentication options
   - Session management

2. **User Profile System**
   - Comprehensive preference storage
   - Dietary restriction management
   - Goal tracking (weight, nutrition, health)
   - Shopping history and patterns

3. **Privacy & Compliance**
   - GDPR compliance implementation
   - Data encryption at rest and in transit
   - User data export capabilities
   - Right to deletion implementation

### Phase 4: Advanced Features & Optimization
**Goal**: Enhanced user experience and system intelligence

1. **Recommendation Engine Enhancements**
   - Collaborative filtering for meal suggestions
   - Seasonal and weather-based adaptations
   - Cultural cuisine preferences
   - Family meal planning capabilities

2. **Budget Optimization Module**
   - Price tracking and alerting
   - Alternative product suggestions
   - Bulk buying recommendations
   - Store promotion integration

3. **Nutritional Knowledge Base**
   - Integration with scientific nutrition databases
   - Allergen and interaction warnings
   - Micronutrient tracking
   - Health condition specific recommendations

4. **Multi-Store Integration**
   - Albert Heijn scraper development
   - Price comparison features
   - Optimal shopping route planning
   - Inventory availability checking

### Phase 5: Scale & Expansion
**Goal**: Platform growth and market expansion

1. **Performance Optimization**
   - Caching strategies implementation
   - Database query optimization
   - CDN integration for static assets
   - Real-time data synchronization

2. **Analytics & Insights**
   - User behavior analytics
   - Recommendation effectiveness metrics
   - A/B testing framework
   - Business intelligence dashboards

3. **Mobile Applications**
   - iOS and Android native apps
   - Offline capability for shopping lists
   - Barcode scanning integration
   - Push notifications for deals

4. **Geographic Expansion**
   - Additional Dutch supermarket chains
   - Belgian market entry preparation
   - Multi-language support
   - Local dietary preference adaptation

## 🏗️ Architecture Decisions to Make

1. **LLM Provider Selection**
   - Cost vs. performance analysis
   - Privacy and data residency requirements
   - Fine-tuning capabilities assessment

2. **Agent Framework Selection**
   - LangChain vs. custom implementation
   - AutoGPT/AutoGen consideration
   - Workflow orchestration tools

3. **Analysis**
   - Gathering user data 
   - visualization and analysis of user preferences

---

**Project Status**: 🟡 Active Development

**Last Updated**: December 2024
