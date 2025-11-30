from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from backend.core.config import settings
from backend.models.models import TestPlan, TestCase
import json

class RAGService:
    def __init__(self):
        self._embeddings = None
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        
        # Lazy load ChatGroq only when needed? No, ChatGroq is lightweight API wrapper.
        # But let's keep imports clean.
        from langchain_groq import ChatGroq
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY
        )

    @property
    def embeddings(self):
        if self._embeddings is None:
            from langchain_huggingface import HuggingFaceEmbeddings
            self._embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return self._embeddings

    def generate_test_cases(self, feature_request: str) -> TestPlan:
        from langchain_chroma import Chroma
        
        # 1. Retrieve context
        vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(feature_request)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 2. Prompt
        parser = JsonOutputParser(pydantic_object=TestPlan)
        
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert QA Automation Engineer.
            Your task is to generate comprehensive test cases for the following feature request: "{feature_request}"
            
            Base your test cases STRICTLY on the provided context below. Do not hallucinate features not mentioned in the context.
            
            Context:
            {context}
            
            Return the output in the following JSON format:
            {{
                "test_cases": [
                    {{
                        "test_id": "TC-001",
                        "feature": "Feature Name",
                        "test_scenario": "Description of the test",
                        "expected_result": "Expected outcome",
                        "grounded_in": "Source document name (e.g. product_specs.md)"
                    }}
                ]
            }}
            
            {format_instructions}
            """
        )

        chain = prompt | self.llm | parser

        # 3. Generate
        try:
            print(f"DEBUG: Generating test cases for: {feature_request}")
            print(f"DEBUG: Retrieved {len(docs)} documents.")
            # print(f"DEBUG: Context preview: {context[:500]}...") 
            
            result = chain.invoke({
                "feature_request": feature_request,
                "context": context,
                "format_instructions": parser.get_format_instructions()
            })
            print(f"DEBUG: LLM Result: {result}")
            return TestPlan(**result)
        except Exception as e:
            print(f"ERROR generating test cases: {e}")
            import traceback
            traceback.print_exc()
            return TestPlan(test_cases=[])

rag_service = RAGService()
