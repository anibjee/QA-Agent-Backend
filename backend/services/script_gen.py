from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.core.config import settings
from backend.models.models import TestCase
import os

class ScriptGenService:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            model_name="llama-3.3-70b-versatile",
            api_key=settings.GROQ_API_KEY
        )

    def generate_script(self, test_case: TestCase) -> str:
        # 1. Load HTML content
        # In a real scenario, we might query the vector DB for the HTML chunk, 
        # but for this assignment, we assume we have the full HTML file available or uploaded.
        # Let's look for checkout.html in the uploads or assets.
        
        html_content = ""
        # Check uploads first
        uploads_path = os.path.join(settings.UPLOAD_DIRECTORY, "checkout.html")
        assets_path = "assets/checkout.html"
        
        if os.path.exists(uploads_path):
            with open(uploads_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        elif os.path.exists(assets_path):
             with open(assets_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        
        # Truncate HTML if too large (naive approach, but necessary for context window)
        # Llama3-70b has 8k context, so we should be fine for this simple file.
        
        # 2. Prompt
        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert Selenium Automation Engineer using Python.
            Your task is to write a complete, runnable Selenium script for the following test case.
            
            Test Case:
            ID: {test_id}
            Feature: {feature}
            Scenario: {scenario}
            Expected Result: {expected_result}
            
            Target HTML Page Source:
            ```html
            {html_content}
            ```
            
            Instructions:
            1. Use `webdriver.Chrome(service=Service(ChromeDriverManager().install()))`. Ensure you import `Service` from `selenium.webdriver.chrome.service` and `ChromeDriverManager` from `webdriver_manager.chrome`.
            2. Open the HTML file. Since this is a local file, assume the user will run it against the local path or a placeholder URL. 
               **IMPORTANT**: Use a placeholder URL `file:///path/to/checkout.html` and add a comment telling the user to update it.
            3. Use precise selectors based on the provided HTML (IDs, Names, CSS Selectors).
            4. Implement assertions to verify the Expected Result.
            5. **IMPORTANT**: When checking style attributes (e.g., color), use substring matching (e.g., `assert "green" in element.get_attribute("style")`).
            6. **IMPORTANT**: When comparing numerical values (prices), convert text to float and round to 2 decimals (e.g., `assert float(element.text.replace('$', '')) == round(expected_val, 2)`).
            7. **IMPORTANT**: Include `import time` at the top. Before `driver.quit()`, add `print("✅ Test Passed!")` and `time.sleep(5)` so the user can see the result.
            8. Return ONLY the Python code. No markdown formatting like ```python ... ```, just the code.
            9. Handle potential race conditions with `WebDriverWait` and `expected_conditions`.
            
            Python Script:
            """
        )

        chain = prompt | self.llm | StrOutputParser()

        # 3. Generate
        try:
            script = chain.invoke({
                "test_id": test_case.test_id,
                "feature": test_case.feature,
                "scenario": test_case.test_scenario,
                "expected_result": test_case.expected_result,
                "html_content": html_content
            })
            
            # Cleanup markdown code blocks if present
            script = script.replace("```python", "").replace("```", "").strip()
            
            return script
        except Exception as e:
            return f"# Error generating script: {e}"

script_gen_service = ScriptGenService()
