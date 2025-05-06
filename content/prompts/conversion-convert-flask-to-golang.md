# Flask to Go Server Migration Project

## Objective

Convert the existing Python Flask server implementation to a Go-based server with identical functionality and API endpoints. The Go implementation should maintain the same request handling, routes, data processing, and response formats as the original Flask server.

The Python Flask is stored in #folder:server 

## Requirements
1. Create a functionally equivalent Go server implementation
2. Match all existing API endpoints, query parameters, and HTTP methods
3. Preserve all current data processing logic and response formats
4. Implement the same error handling and status codes
5. Maintain any authentication mechanisms present in the Flask implementation
6. Use only the Go standard library where possible, with minimal external dependencies
7. Include appropriate comments explaining the code and any implementation decisions

## Deliverables
1. Complete Go source code organized in a folder named `go_server`
2. A main.go file with server initialization and configuration
3. Separate handler files for different API endpoint groups
4. Any utility or helper functions required
5. A README.md with setup and usage instructions

