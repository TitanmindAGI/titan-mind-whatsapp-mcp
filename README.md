[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/titanmindagi-titanmind-whatsapp-mcp-badge.png)](https://mseep.ai/app/titanmindagi-titanmind-whatsapp-mcp)

## Titanmind WhatsApp MCP

A WhatsApp marketing and messaging tool MCP (Model Control Protocol) service using [Titanmind](https://www.titanmind.so/). Handles free-form messages (24hr window) and template workflows automatically

## Overview

This service provides all the WhatsApp marketing and messaging functionalities using Titanmind. Includes features like template creation and registration with all components header, body, CTAs.., template broadcast to phone numbers in bulk. Read and send messages in an active conversation.

> This MCP utilizes Titanmind. Titanmind Account is a requirement to use this MCP.
> 
> Titanmind enhances WhatsApp communication by providing powerful features such as **conversation management, scheduling, agentic conversations, content generation etc.**

## Features

#### Conversation Management

**Get Recent Conversations**

*   Retrieve all conversations with messages sent or received in the last 24 hours
*   Returns conversation data with recent activity

**Get Conversation Messages**

*   Fetch all messages from a specific conversation
*   Requires: `conversation_id` (alphanumeric conversation identifier)

**Send WhatsApp Message**

*   Send a message to an existing WhatsApp conversation
*   Requires: `conversation_id` and `message` content

#### Template Management

**Create Message Template**

*   Register new WhatsApp message templates for approval
*   Configure template name (single word, underscores allowed only)
*   Set language (default: "en") and category (MARKETING, UTILITY, AUTHENTICATION)
*   Structure message components including:
    *   **BODY** (required): Main text content
    *   **HEADER** (optional): TEXT, VIDEO, IMAGE, or DOCUMENT format
    *   **FOOTER** (optional): Footer text
    *   **BUTTONS** (optional): QUICK\_REPLY, URL, or PHONE\_NUMBER actions

**Get Templates**

*   Retrieve all created templates with approval status
*   Optional filtering by template name

**Send Bulk Messages**

*   Send messages to multiple phone numbers using approved templates
*   Requires: `template_id` and list of contacts
*   Contact format: country code alpha (e.g., "IN"), country code (e.g., "91"), and phone number

## Installation

### Prerequisites

*   Python 3.10 or higher
*   API Key and Business Code from [Titanmind](https://www.titanmind.so/)

### Usage with MCP Client

In any MCP Client like Claude or Cursor, Titanmind whatsapp MCP config can be added following ways:

#### Using [Titanmind WhatsApp MCP Python package](https://pypi.org/project/titanmind-whatsapp-mcp/0.1.2/)   
1\. Install pipx to install the python package globally

```plaintext
# terminal

# Install pipx first
brew install pipx  # on macOS
# or
sudo apt install pipx  # on Ubuntu/Debian

# Then install Titanmind WhatsApp MCP Python package 
pipx install titanmind-whatsapp-mcp

# Make sure '/[HOME_DIR_OR_USER_PRFILE]/.local/bin' is on your PATH environment variable. Use pipx ensurepath to set it.
pipx ensurepath 
 
```

2\. Set the MCP Config python package script in the MCP Client's MCP Configs Json file.

```plaintext
{
  "mcpServers": {
    "TitanMindMCP": {
      "command": "/[HOME_DIR_OR_USER_PRFILE]/.local/bin/titan-mind-mcp",
      "args": [
      ],
      "env": {
        "api-key": "XXXXXXXXXXXXXXXXXXXXXXXX",
        "bus-code": "XXXXXX"
      }
    }
  }
}

```

#### Use Remote Titanmind MCP server config

1\. Make sure npx is installed in the system  
2\. Then just add the MCP config

```plaintext
{
  "mcpServers": {
    "TitanMindMCP": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.titanmind.so/whatsapp/mcp/",
        "--header",
        "api-key:XXXXXXXXXXXXXXXXXXXXXXX",
        "--header",
        "bus-code:XXXXXX"
      ]
    }
  }
}
```

#### Use local python project config

1\. First Setup project using instructions mentioned in the Setup Project section.  
2\. Then add the MCP config

```plaintext
{
  "mcpServers": {
    "TitanMindMCP": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/[PATH_TO_THE_PROJECT]",
        "python",
        "main.py"
      ],
      "env": {
        "api-key": "XXXXXXXXXXXXXXXXXXXX",
        "bus-code": "XXXXXX"
      }
    }
  }
}
```

### Manual Installation for custom purpose or development

### Install package from PyPI for package use

```plaintext
pip install titanmind-whatsapp-mcp
```

Or use `uv`:

```plaintext
uv pip install titanmind-whatsapp-mcp
```

### Setup Project for development use

1\. Clone the repository:

```plaintext
git clone https://github.com/TitanmindAGI/titanmind-whatsapp-mcp
cd titanmind-whatsapp-mcp
```

2\. Install dependencies:

```plaintext
pip install -e .
# Or
uv pip install -e .
```

3\. Set the auth keys

```plaintext
export api-key="your-titanmind-api-key"
export bus-code="your-titanmind-business-code"
```

## How it Works

TitanMind's WhatsApp messaging system operates under two distinct messaging modes based on timing and conversation status:

## Free-Form Messaging (24-Hour Window)

*   **When Available**: Only after a user has sent a message within the last 24 hours
*   **Content Freedom**: Any content is allowed without pre-approval
*   **Use Case**: Ongoing conversations and immediate responses

## Template Messaging (Outside 24-Hour Window)

*   **When Required**: For new conversations or when the 24-hour window has expired
*   **Content Structure**: Pre-approved, structured message templates only
*   **Use Case**: Initial outreach and re-engagement campaigns

## Messaging Workflow Process

1.  **Check Messaging Window Status**
    *   Verify if receiver's phone number is within the free-form messaging window
    *   A receiver is eligible for free-form messaging if:
        *   A conversation with their phone number already exists AND
        *   The receiver has sent a message within the last 24 hours
2.  **Choose Messaging Method**
    *   **Free-Form**: Send directly if within 24-hour window
    *   **Template**: Register and use approved template if outside window
3.  **Template Approval Process** (if needed)
    *   Submit template for WhatsApp approval
    *   Wait for approval confirmation
    *   Template becomes available for bulk messaging
4.  **Send Message**
    *   Execute message delivery using appropriate method
    *   Monitor delivery status
5.  **Verify Delivery**
    *   Check conversation to confirm receiver successfully received the message
    *   Track message status and engagement

## Usage Notes

*   All tools integrate with Titanmind's WhatsApp channel messaging functionality
*   Templates require approval before they can be used for bulk messaging
*   For more help contact us through [https://www.titanmind.so/](https://www.titanmind.so/)

## License

MIT License - See LICENSE file