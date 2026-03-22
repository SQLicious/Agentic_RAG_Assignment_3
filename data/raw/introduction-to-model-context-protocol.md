---
title: Introduction to Model Context Protocol
doc_type: academy_course
credential_type: course_completion_certificate
source_url: https://anthropic.skilljar.com/introduction-to-model-context-protocol
---

This course provides comprehensive coverage of the Model Context Protocol (MCP), focusing on building both MCP servers and clients using the Python SDK. You'll learn about MCP's three core primitives—tools, resources, and prompts—and understand how they integrate with Claude AI to create powerful applications without writing extensive integration code.

## What you'll learn

-   Understand MCP architecture and how it shifts tool definition and execution burden from your server to specialized MCP servers
-   Learn about MCP's transport-agnostic communication system and the message types used between clients and servers
-   Explore the complete request-response flow from user queries through MCP clients to external services and back to Claude
-   Build MCP servers using the Python SDK with decorators to define tools instead of writing JSON schemas manually
-   Implement document management functionality with tools for reading and editing documents using Field descriptions and type hints
-   Use the built-in MCP Server Inspector to test and debug your server functionality in a browser-based interface
-   Define resources for exposing read-only data, including both direct resources with static URIs and templated resources with parameters
-   Implement resource reading functionality in clients with proper MIME type handling for JSON and text content
-   Build prompts that provide pre-crafted, high-quality instructions for common workflows like document formatting
-   Understand when to use each MCP primitive: tools (model-controlled), resources (app-controlled), and prompts (user-controlled)
-   Examine practical integration patterns including autocomplete functionality and context injection for AI conversations

## Prerequisites

-   Working knowledge of Python programming
-   Basic understanding of JSON and HTTP request-response patterns

## Who this course is for

-   Developers looking to create MCP servers

## Course Overview

### Introduction
* Welcome to the course
* Introducing MCP
* MCP clients

### Hands-on with MCP servers
* Project setup
* Defining tools with MCP
* The server inspector
* Course satisfaction survey

### Connecting with MCP clients
* Implementing a client
* Defining resources
* Accessing resources
* Defining prompts
* Prompts in the client

### Assessment and wrap Up
* Final assessment on MCP
* MCP review

### About this course