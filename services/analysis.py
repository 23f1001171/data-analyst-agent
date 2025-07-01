from services.llm import LLMService
from services.visualization import VisualizationService
from utils.web import scrape_table_from_url
from utils.data import execute_duckdb_query
import pandas as pd
import re
import duckdb
from typing import Dict, Any

class AnalysisService:
    def __init__(self):
        self.llm = LLMService()
        self.visualizer = VisualizationService()
    
    async def analyze_task(self, task_description: str) -> Dict[str, Any]:
        # Step 1: Determine task type
        task_type = await self._identify_task_type(task_description)
        
        # Step 2: Process based on type
        if task_type == "web_scraping":
            return await self._process_web_task(task_description)
        elif task_type == "duckdb_query":
            return await self._process_duckdb_task(task_description)
        else:
            return await self._process_general_task(task_description)
    
    async def _identify_task_type(self, task_description: str) -> str:
        response = await self.llm.analyze(
            f"Classify this data analysis task into one of these types: "
            f"'web_scraping', 'duckdb_query', or 'general_analysis'.\n\n"
            f"Task: {task_description}\n\n"
            f"Respond only with the type name."
        )
        return response.strip().lower()
    
    async def _process_web_task(self, task_description: str) -> Dict[str, Any]:
        # Extract URL
        url_match = re.search(r'https?://[^\s]+', task_description)
        if not url_match:
            raise ValueError("No URL found in task description")
        
        url = url_match.group(0)
        df = await scrape_table_from_url(url)
        
        # Get answers to questions
        answers = await self._answer_questions_from_data(task_description, df)
        
        # Generate plots if requested
        plots = await self._generate_requested_plots(task_description, df)
        
        return {**answers, **plots}
    
    async def _process_duckdb_task(self, task_description: str) -> Dict[str, Any]:
        # Extract query if provided
        query_match = re.search(r'```sql\n(.*?)\n```', task_description, re.DOTALL)
        if query_match:
            query = query_match.group(1)
            df = execute_duckdb_query(query)
        else:
            # Let LLM generate the query
            query = await self.llm.analyze(
                f"Generate a DuckDB SQL query to answer this task:\n\n{task_description}"
            )
            df = execute_duckdb_query(query)
        
        answers = await self._answer_questions_from_data(task_description, df)
        plots = await self._generate_requested_plots(task_description, df)
        
        return {**answers, **plots}
    
    async def _process_general_task(self, task_description: str) -> Dict[str, Any]:
        # For tasks that don't fit the other categories
        return {
            "analysis": await self.llm.analyze(
                f"Perform this data analysis task:\n\n{task_description}"
            )
        }
    
    async def _answer_questions_from_data(self, task_description: str, df: pd.DataFrame) -> Dict[str, Any]:
        # Let LLM analyze the data and answer questions
        response = await self.llm.analyze(
            f"Answer these questions based on the provided data:\n\n"
            f"Task: {task_description}\n\n"
            f"Data:\n{df.head().to_markdown()}\n\n"
            f"Provide answers in a JSON-compatible format."
        )
        return self._parse_llm_response(response)
    
    async def _generate_requested_plots(self, task_description: str, df: pd.DataFrame) -> Dict[str, Any]:
        if "plot" not in task_description.lower() and "scatter" not in task_description.lower():
            return {}
        
        # Identify columns to plot
        response = await self.llm.analyze(
            f"Identify which columns to plot from this task description:\n\n"
            f"{task_description}\n\n"
            f"Respond with format: 'x_column,y_column,plot_type'"
        )
        x_col, y_col, plot_type = response.strip().split(',')
        
        plot_data = self.visualizer.create_plot(
            plot_type.strip(),
            df,
            x_col.strip(),
            y_col.strip()
        )
        
        return {"plot": plot_data}
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        # Simple parsing - in practice you'd want more robust parsing
        try:
            if response.startswith('{') and response.endswith('}'):
                return eval(response)
            elif '\n' in response:
                return {f"answer_{i}": line for i, line in enumerate(response.split('\n'))}
            else:
                return {"answer": response}
        except:
            return {"answer": response}

# Singleton instance
analysis_service = AnalysisService()

async def analyze_task(task_description: str) -> Dict[str, Any]:
    return await analysis_service.analyze_task(task_description)