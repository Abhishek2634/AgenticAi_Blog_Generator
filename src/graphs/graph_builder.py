from langgraph.graph import StateGraph, START, END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm

    def build_topic_graph(self):
        """Build a graph to generate a blog based on a topic"""
        self.graph = StateGraph(BlogState)
        self.blog_node_obj = BlogNode(self.llm)
        
        # Nodes
        self.graph.add_node("title_creation", self.blog_node_obj.title_creation)
        self.graph.add_node("content_generation", self.blog_node_obj.content_generation)

        # Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)

        return self.graph.compile()

    def setup_graph(self, usecase):
        if usecase == "topic":
            return self.build_topic_graph()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")
