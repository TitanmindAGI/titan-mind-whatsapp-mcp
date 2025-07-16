import argparse
import os
from typing import Optional, Dict, Any, Callable, Annotated

from fastmcp import FastMCP

from titan_mind import titan_mind_functions as titan_mind_functions
from titan_mind.titan_mind_functions import Contact
from titan_mind.utils.app_specific.utils import to_run_mcp_in_server_mode_or_std_io, get_script_args

# todo - atm below workflow is attached to every tool description, which is not recommended, but fastmcp and the claude desktop client are not able to share system instructions well. so for now appending the instructions to the tools context also
# todo - give straightforward API or tool to determine if the receiver is in the free form window or not
# todo - LLM are not following the usage instructions so need to update descriptions and check if mcp has other construct for it. the usage instruction given of --> checking if the the receiver have sent a message within the last 24 hours. and after sending the message check if the receiver recieved it or not.
_titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow = \
    """
    TITANMIND WHATSAPP WORKFLOW:
    
    FREE-FORM (24hr window):
       1. Any content allowed
       2. Only after user's have sent a message in the last 24 hours
    
    TEMPLATES (outside 24hr window):
       1. Pre-approved structured content
       2. Required for new conversations
       
    PROCESS:
       1. Check receiver phone number free form messaging window status
       2. A receiver is in the free-form messaging window if a conversation with their phone number already exists and also the receiver have sent a message within the last 24 hours.
       2. Use free-form OR register template
       3. Wait for template approval (if needed)
       4. Send message  
       5. check the conversation, if the receiver received message successfully
    """

_tool_return_object_description: str = \
    """
    Each tool Returns:
            a boolean if the tool was able to perform the api call successfully against the key "status"
            a string containing the message or error if the function ran successfully or not against the key "message"
            a dict containing the response according to the tool functionality or error details if the tool ran into an exception, against the key "result"
    """

_mcp_name = "TitanMind Whatsapp MCP - Handles free-form messages (24hr window) and template workflows automatically"

mcp = FastMCP(
    _mcp_name,
    instructions=_titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow + _tool_return_object_description,
)


@mcp.prompt()
def whatsapp_and_server_workflow() -> str:
    """WhatsApp messaging workflow guide, and server tools return info"""
    return _titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow + _tool_return_object_description


@mcp.prompt()
def send_whatsapp_message() -> str:
    """WhatsApp messaging workflow guide, and server tools return info"""
    return _titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow + _tool_return_object_description


@mcp.resource("resource://workflow")
def whatsapp_and_server_workflow_resource() -> str:
    """WhatsApp messaging workflow guide, and server tools return info"""
    return _titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow + _tool_return_object_description

"""
Guidelines to follow:
1. Keep the tool names char count max to 51. Since some models do not support MCP, and rely on the function calling.
So tool_name + mcp_name needs to be 64, making the mcp_name to have max 13 char count.
"""
@mcp.tool()
def get_conversations_from_the_last_day(
        phone_without_dialer_code: str = "None"
) -> Optional[Dict[str, Any]]:
    ("""
    get all the conversation where there have been the last message sent or received in the last 24 hours.
    
    Args:
        phone_without_dialer_code (str): to filter conversation with a phone number. default is "None" to get all conversations.
    """ + _titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow)

    return titan_mind_functions.get_conversations_from_the_last_day(
        phone_without_dialer_code
    )


@mcp.tool()
def get_the_messages_of_a_conversation_(conversation_id: str) -> Optional[Dict[str, Any]]:
    ("""
    gets the messages in a conversation.

    Args:
        conversation_id (str): alphanumeric id of the whatsapp conversation, to which a message is required to be sent.
        message (str): the message to send.
    """ + _titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow)

    return titan_mind_functions.get_the_conversation_messages(
        conversation_id
    )


@mcp.tool()
def send_whatsapp_message_to_a_conversation(conversation_id: str, message: str) -> Optional[Dict[str, Any]]:
    ("""
    sends a whatsapp message to a Titanmind's whatsapp conversation.

    Args:
        conversation_id (str): id of the whatsapp conversation.
        message (str): the message to send.
    """ + _titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow)

    return titan_mind_functions.send_whatsapp_message_to_a_conversation(
        conversation_id, message
    )


@mcp.tool()
def register_msg_template_for_approval(
        template_name: str,
        message_content_components: list[dict[str, Any]],
        language: str = "en", category: str = "MARKETING",
) -> Optional[Dict[str, Any]]:
    """
    creates and registers a new whatsapp message template for approval.
    Args:
        template_name (str): name of the whatsapp message template, It only accepts a single word without no special characters except underscores
        language (str): language of the whatsapp message template (default is "en")
        category (str): category of the whatsapp message template (default is "MARKETING"), other possible values are "UTILITY", "AUTHENTICATION"
        message_content_components (dict): the message content that needs to be sent. It needs to be structured like the below example, 
        components are required to have BODY component at least, like this: {"type": "BODY", "text": "lorem body text"}, BODY component is for the simple text.
        All other components are optional. 
        HEADER component can have any of the below format, but only one format at a time can be used.: TEXT(the header component with TEXT needs to be like this
        {
        "type": "HEADER",
        "format": "TEXT",
        "text": "lorem header text"
        }
        ), VIDEO(the header component with VIDEO needs to be like this
        {
         "type":"HEADER",
         "format":"VIDEO",
         "example":{
            "header_handle":[
               "https://sample_video_url.jpg"
            ]
         }
        }
        )
        , IMAGE(the header component with IMAGE needs to be like this 
        {
         "type":"HEADER",
         "format":"IMAGE",
         "example":{
            "header_handle":[
               "https://sample_image_url.jpg"
            ]
         }
        }),
       DOCUMENT (the header component with DOCUMENT needs to be like this 
        {
         "type":"HEADER",
         "format":"DOCUMENT",
         "example":{
            "header_handle":[
               "https://sample_document_url"
            ]
         }
      }),
        message_content_components value with all other type of components is mentioned below.
            [
                    {
                        "type": "HEADER",
                        "format": "TEXT",
                        "text": "lorem header text"
                    },
                    {
                        "type": "BODY",
                        "text": "lorem body text"
                    },
                    {
                        "type": "FOOTER",
                        "text": "lorem footer text"
                    },
                    {
                        "type": "BUTTONS",
                        "buttons": [
                            {
                                "type": "QUICK_REPLY",
                                "text": "lorem reply bt"
                            },
                            {
                              "type": "URL",
                              "text": "cta",
                              "url": "https:sample.in"
                            },
                            {
                              "type": "PHONE_NUMBER",
                              "text": "call ",
                              "phone_number": "IN328892398"
                            }
                        ]
                    }
                ]
        Buttons need to follow order of first QUICK_REPLY, then URL, and then PHONE_NUMBER.
    """

    return titan_mind_functions.register_msg_template_for_approval(
        template_name, language, category, message_content_components
    )


@mcp.tool()
def get_the_templates(
        template_name: str = "None",
        page: int = 1,
        page_size: int = 10,
) -> Optional[Dict[str, Any]]:
    ("""
    gets all the created templates with the details like approved/pending status 
    
    Args:
        template_name (str): name of the whatsapp message template, It only accepts a word without no special characters only underscores. Default is "None" to get all the templates
        page (int): page refers to the page in paginated api. default is 1 
        page_size (int): page_size refers to the page_size in paginated api. default is 25 
    """ + _titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow)
    return titan_mind_functions.get_the_templates(
        template_name, page, page_size
    )


@mcp.tool()
def send_msg_to_multiple_num_using_approved_template(
        template_id: int, contacts: list[Contact],
) -> Optional[Dict[str, Any]]:
    ("""
    sends a message to a phone number using an approved whatsapp template.
    
    Args:
        template_id (str): id of the whatsapp message template, it is not the template name.
        contacts (Contact): a contact has three attributes: country_code_alpha(like "IN" for india), country_code(like "91") and phone_without_dialer_code
    """ + _titan_mind_product_whatsapp_channel_messaging_functionality_and_workflow)
    return titan_mind_functions.send_message_to_a_number_using_approved_template(
        template_id, contacts
    )


def main():
    if to_run_mcp_in_server_mode_or_std_io():
        mcp.run(transport="streamable-http", host="0.0.0.0", port=get_script_args().port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
