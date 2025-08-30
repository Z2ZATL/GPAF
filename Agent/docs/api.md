# GPAF API Documentation

This document describes the GPAF API endpoints and usage.

## Authentication

### API Keys

- Required for all endpoints
- Set in environment variables
- Configure in settings
- Rotate regularly

### Headers

```
Authorization: Bearer <api_key>
Content-Type: application/json
```

## Endpoints

### Chat

#### POST /api/chat

Send a message to GPAF.

**Request:**
```json
{
  "message": "string",
  "context": "string",
  "options": {
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

**Response:**
```json
{
  "response": "string",
  "context": "string",
  "metadata": {
    "tokens": 100,
    "time": 1.5
  }
}
```

### Memory

#### GET /api/memory

Retrieve memory entries.

**Response:**
```json
{
  "entries": [
    {
      "id": "string",
      "content": "string",
      "timestamp": "string",
      "metadata": {}
    }
  ]
}
```

#### POST /api/memory

Add memory entry.

**Request:**
```json
{
  "content": "string",
  "metadata": {}
}
```

### Tools

#### GET /api/tools

List available tools.

**Response:**
```json
{
  "tools": [
    {
      "name": "string",
      "description": "string",
      "parameters": {}
    }
  ]
}
```

#### POST /api/tools/{name}

Execute tool.

**Request:**
```json
{
  "parameters": {}
}
```

## Error Handling

### Status Codes

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

### Error Response

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

## Rate Limiting

- 100 requests per minute
- 1000 requests per hour
- Custom limits configurable

## Resources

- [Documentation](https://github.com/frdel/gpaf/docs)
- [Discord Community](https://discord.gg/Z2tun2N3)
- [Skool](https://www.skool.com/gpaf)
- [Issue Tracker](https://github.com/frdel/gpaf/issues)

For API questions, contact the maintainers. 