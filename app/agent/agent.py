import json

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    ToolMessage,
)

from langgraph.prebuilt import create_react_agent


from app.agent.tools import TOOLS
from app.models.llm import get_llm



SYSTEM_PROMPT = (

    "你是企业知识库智能助手。"

    "当用户询问企业制度、政策或知识库相关内容时，"
    "必须调用 knowledge_search 工具。"

    "回答必须基于工具返回的信息。"

    "如果知识库没有相关内容，"
    "明确告诉用户没有找到，不允许编造。"

)



def build_agent():

    return create_react_agent(

        model=get_llm(),

        tools=TOOLS,

        prompt=SYSTEM_PROMPT,

    )




def run_agent(question: str):


    agent = build_agent()


    result = agent.invoke(

        {
            "messages":[
                HumanMessage(
                    content=question
                )
            ]
        }

    )


    messages = result.get(
        "messages",
        []
    )


    answer = ""

    sources = []



    for message in messages:



        # -----------------------
        # Tool返回结果
        # -----------------------

        if isinstance(
            message,
            ToolMessage
        ):

            content = message.content


            try:

                data = json.loads(
                    content
                )


                if "results" in data:

                    sources.extend(
                        data["results"]
                    )


            except Exception:

                pass



        # -----------------------
        # AI最终回答
        # -----------------------

        elif isinstance(
            message,
            AIMessage
        ):


            if message.content:


                if isinstance(
                    message.content,
                    str
                ):

                    answer = message.content


                elif isinstance(
                    message.content,
                    list
                ):

                    texts=[]

                    for part in message.content:

                        if isinstance(
                            part,
                            dict
                        ):

                            texts.append(
                                part.get(
                                    "text",
                                    ""
                                )
                            )

                        else:

                            texts.append(
                                str(part)
                            )


                    answer="".join(texts)




    return {

        "answer": answer,

        "sources": sources

    }