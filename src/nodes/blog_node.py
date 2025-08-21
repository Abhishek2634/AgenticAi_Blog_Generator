from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog


class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """Generate a title for the blog based on the topic"""
        if "topic" in state and state["topic"]:
            prompt = """ You are an expert blog content writer. Use Markdown formatting. Generate a blog title for the {topic}. This 
            title should be creative and SEO friendly."""

            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}


    def content_generation(self, state:BlogState):
        if "topic" in state and state["topic"]:
            prompt = """ You are an expert blog content writer. Use Markdown formatting. Generate a detailed blog content with  detailed breakdown for the {topic}. 
            This content should be creative and SEO friendly."""
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title" : state['blog']['title'], "content": response.content}}
        

    def translation(self, state: BlogState):
        blog_content     = state["blog"]["content"]
        current_language = state["current_language"]

        translation_prompt = """
        Translate the following content into {current_language}.
        - Maintain the original tone, style and formatting.
        - Adopt cultural references and idioms appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}
        """

        messages = [
            HumanMessage(
                content=translation_prompt.format(
                    current_language=current_language,
                    blog_content=blog_content,
                )
            )
        ]

        translated: Blog = self.llm.with_structured_output(Blog).invoke(messages)

        return {
            "blog": {
                "title": translated.title,
                "content": translated.content,
            },
            "current_language": current_language,
        }


    def route(self, state: BlogState):
        return {"current_language": state["current_language"]}


    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation funciton.
        """

        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            return state["current_language"]