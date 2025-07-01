import httpx
from bs4 import BeautifulSoup
import pandas as pd
from typing import Optional

async def scrape_table_from_url(url: str, table_index: int = 0) -> pd.DataFrame:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            
            if not tables:
                raise ValueError("No tables found on the page")
            
            if table_index >= len(tables):
                table_index = 0
                
            table = tables[table_index]
            rows = table.find_all('tr')
            
            data = []
            for row in rows:
                cols = row.find_all(['th', 'td'])
                data.append([col.get_text(strip=True) for col in cols])
            
            return pd.DataFrame(data[1:], columns=data[0])
        except Exception as e:
            raise Exception(f"Web scraping failed: {str(e)}")