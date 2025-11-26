from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog


class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        """Generate a title for the blog based on the topic"""
        if "topic" in state and state["topic"]:
            prompt = """You are an expert blog content writer. Use Markdown formatting. Generate a blog title for the {topic}. This title should be creative and SEO friendly."""
            
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content.strip()}}

    def content_generation(self, state: BlogState):
        """Generate detailed blog content based on the topic"""
        if "topic" in state and state["topic"]:
            prompt = """You are an expert blog content writer. Use Markdown formatting. Generate a detailed blog content with detailed breakdown for the {topic}. This content should be creative and SEO friendly."""
            
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {
                "blog": {
                    "title": state['blog']['title'], 
                    "content": response.content.strip()
                }
            }

    def translation(self, state: BlogState):
        """Translate blog content to the target language"""
        blog_content = state["blog"]["content"]
        blog_title = state["blog"]["title"]
        current_language = state["current_language"]
        
        # Language mapping for better prompts
        language_names = {
            "hindi": "Hindi (हिंदी)",
            "french": "French (Français)"
        }
        target_lang = language_names.get(current_language, current_language)

        translation_prompt = f"""You are a professional translator. Translate the following blog post from English to {target_lang}.

STRICT REQUIREMENTS:
1. Translate EVERYTHING including title, headings, content, bullet points
2. Maintain all Markdown formatting (##, ###, *, -)
3. Keep the same structure and tone
4. DO NOT provide alternative titles or suggestions - only translate
5. Output ONLY the translated content

TITLE TO TRANSLATE:
{blog_title}

CONTENT TO TRANSLATE:
{blog_content}

NOW TRANSLATE EVERYTHING TO {target_lang.upper()}:"""

        messages = [HumanMessage(content=translation_prompt)]
        
        # Get raw response without structured output
        response = self.llm.invoke(messages)
        translated_text = response.content.strip()
        
        # Parse the response manually
        lines = translated_text.split('\n', 2)
        if len(lines) >= 3:
            translated_title = lines[0].replace('#', '').strip()
            translated_content = lines[2].strip()
        else:
            # Fallback: use first line as title, rest as content
            translated_title = lines[0].replace('#', '').strip() if lines else blog_title
            translated_content = '\n'.join(lines[1:]).strip() if len(lines) > 1 else translated_text

        return {
            "blog": {
                "title": translated_title,
                "content": translated_content,
            },
            "current_language": current_language,
        }

    def route(self, state: BlogState):
        """Pass through the current language state"""
        return {"current_language": state["current_language"]}

    def route_decision(self, state: BlogState):
        """Route the content to the respective translation function"""
        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            return state["current_language"]
