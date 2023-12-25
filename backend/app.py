from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from src.system_instructions.system_instructions import system_messages

# Config for connecting to LiteLLM running mistral on ollama.
config_list_llm_one = [
    {
        'base_url': 'http://0.0.0.0:8000',
        'api_key': 'null'
    my name is jon le

    }
]

config_list_llm_two = [
    {
        'base_url': 'http://0.0.0.0:26744',
        'api_key': 'null'
    }
]

# Config for AutoGen
llm_config_one = {
    "config_list": config_list_llm_one
}

llm_config_two = {
    "config_list": config_list_llm_two
}

'''
**Roles**:
- **Outliner**: will write an outline of the research paper
- **Drafter**: will write a draft of the research paper from an outline
- **Writer**: will write the final TL;DR
- **Editor**: will edit the final TL;DR. This will be the final copy
- **Group Chat Manager**: keep all assistants under control.
'''

outliner = AssistantAgent(
    name="The Outliner",
    system_message=system_messages["Outliner"],
    llm_config=llm_config_one,
    code_execution_config=False
)

drafter = AssistantAgent(
    name="The Drafter",
    system_message=system_messages["Drafter"],
    llm_config=llm_config_two,
    code_execution_config=False
)

editor = AssistantAgent(
    name="The Editor",
    system_message=system_messages["Editor"],
    llm_config=llm_config_one,
    code_execution_config=False
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config_two,
    system_message="""
       Reply with TERMINATE when your task is finished. Reply with CONTINUE when your task is not completed.
       You will not need to write code. 
    """
)

task = """

Write me a TL;DR of how the internal combustion works


"""

groupchat = GroupChat(agents=[user_proxy, outliner, drafter, editor], messages=[], max_round=12, speaker_selection_method="round_robin")
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config_two)

user_proxy.initiate_chat(manager, message=task)
