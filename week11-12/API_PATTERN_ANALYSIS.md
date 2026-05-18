# API Pattern Analysis - Stripe va GitHub

## 1. Stripe API Patterns

### a) Resource-oriented REST + CRUD
- Stripe dung resource ro rang: /customers, /payment_intents, /subscriptions
- HTTP methods theo semantics: POST create, GET retrieve/list, DELETE cancel

### b) Idempotency Pattern
- Header Idempotency-Key cho POST de tranh tao duplicate khi retry
- Rat quan trong trong thanh toan

### c) Event-driven + Webhook-first
- Stripe Events la core integration model
- Webhook events: payment_intent.succeeded, invoice.paid, charge.failed
- Khuyen nghi verify signature (Stripe-Signature)

### d) Expand Query Pattern
- `expand[]` cho phep lay nested object trong cung request
- Giam round-trip cho client

## 2. GitHub API Patterns

### a) REST + Hypermedia hints
- Endpoint tuan theo REST conventions
- Co pagination qua Link header (next, prev, first, last)

### b) Query/Search Pattern
- Search API ho tro query syntax manh
- Loc theo type, state, labels, author

### c) Webhook Integration
- Repository/Organization webhooks cho events: push, pull_request, issues
- Signature verification qua X-Hub-Signature-256

### d) Rate Limiting Pattern
- Response headers cho biet quota:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

## 3. Bai hoc ap dung cho week11-12

- Dung CRUD cho product resources
- Dung Query pattern cho list/filter/sort/pagination
- Dung HATEOAS links de discoverability
- Dung Event-driven de tach producer/consumer
- Dung Webhook de tich hop he thong ngoai

## 4. Khi nao dung REST, gRPC, GraphQL

REST:
- Public API, don gian, HTTP-native, cache-friendly

gRPC:
- Internal microservices, high throughput, strongly typed contracts

GraphQL:
- Frontend can aggregate data linh hoat, query shape theo UI

## 5. Design recommendation

- External/public integrations: REST + Webhook (giong Stripe, GitHub)
- Internal service mesh: gRPC cho performance
- Complex client data requirements: GraphQL gateway tren REST/gRPC backend
