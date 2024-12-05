# Tiny ERP Balance Sheet Transformer
# Author: Rodrigo Brunale
# Created: December 2024
# License: MIT

"""
Tiny ERP Balance Sheet Data Transformation Tool

This script is specifically designed to transform balance sheet ('balancete') data
exported from Tiny ERP (https://tiny.com.br/) into a format optimized for
data visualization in Google Looker Studio.

The tool handles the specific format and peculiarities of Tiny ERP's balance sheet export,
including its date formatting, hierarchical categorization, and Brazilian Portuguese
localization, transforming it into a format that's ideal for creating dashboards
and reports in Google Looker Studio.

Features:
- Specifically handles Tiny ERP balance sheet export format
- Converts wide-format financial data to long format for analytics
- Handles Tiny ERP's date formatting
- Maintains Tiny ERP's categorical hierarchy
- Supports Brazilian Portuguese localization
- Includes error handling and data validation

Requirements:
- pandas
- numpy

Input: Balance sheet CSV export from Tiny ERP
Output: Analytics-ready CSV formatted for Google Looker Studio
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FinancialDataTransformer:
    """
    A class to transform financial balance sheet data from wide to long format.
    Optimized for business intelligence tools like Google Looker Studio.
    """

    def __init__(self):
        """Initialize the transformer with Brazilian Portuguese month mappings."""
        self.month_map = {
            'Jan': 1, 'Fev': 2, 'Mar': 3, 'Abr': 4, 'Mai': 5, 'Jun': 6,
            'Jul': 7, 'Ago': 8, 'Set': 9, 'Out': 10, 'Nov': 11, 'Dez': 12
        }

        self.month_names = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }

    def _validate_input_data(self, df: pd.DataFrame) -> bool:
        """
        Validate input data format and required columns.

        Args:
            df (pd.DataFrame): Input dataframe to validate

        Returns:
            bool: True if validation passes, raises ValueError if not
        """
        required_columns = ['Tipo', 'Grupo', 'Categoria']

        # Check for required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Check for date columns
        date_columns = [col for col in df.columns if '/' in col and col != 'Total']
        if not date_columns:
            raise ValueError("No date columns found in the format 'MMM/YY'")

        return True

    def _parse_date_column(self, col_name: str) -> Tuple[int, int]:
        """
        Parse date column name into month and year.

        Args:
            col_name (str): Column name in format 'MMM/YY'

        Returns:
            Tuple[int, int]: Month number and full year
        """
        month_str, year_str = col_name.strip().split('/')
        month = self.month_map.get(month_str.strip())
        year = 2000 + int(year_str)  # Convert '23' to '2023'
        return month, year

    def transform_data(self, input_file: str, output_file: str) -> pd.DataFrame:
        """
        Transform financial data from wide to long format.

        Args:
            input_file (str): Path to input CSV file
            output_file (str): Path to save transformed CSV

        Returns:
            pd.DataFrame: Transformed dataframe
        """
        try:
            # Read input file
            logger.info(f"Reading input file: {input_file}")
            df = pd.read_csv(input_file)

            # Validate input data
            self._validate_input_data(df)

            # Get date columns
            date_columns = [col for col in df.columns if '/' in col and col != 'Total']

            # Initialize transformed data list
            transformed_data = []

            # Transform data
            logger.info("Transforming data from wide to long format")
            for _, row in df.iterrows():
                for date_col in date_columns:
                    month, year = self._parse_date_column(date_col)

                    # Create date string in YYYY-MM-DD format
                    date_str = f"{year}-{month:02d}-01"

                    # Get value and ensure it's numeric
                    value = pd.to_numeric(str(row[date_col]).replace(',', '.'), errors='coerce')

                    transformed_data.append({
                        'Data': date_str,
                        'Ano': year,
                        'Mes': month,
                        'Mes_Nome': self.month_names[month],
                        'Tipo': row['Tipo'],
                        'Grupo': row['Grupo'],
                        'Categoria': row['Categoria'].strip(),
                        'Valor': round(float(value), 2) if pd.notnull(value) else 0.00
                    })

            # Create transformed dataframe
            transformed_df = pd.DataFrame(transformed_data)

            # Sort data
            transformed_df = transformed_df.sort_values(['Data', 'Tipo', 'Grupo', 'Categoria'])

            # Save to CSV
            logger.info(f"Saving transformed data to: {output_file}")
            transformed_df.to_csv(output_file, index=False, encoding='utf-8-sig')

            return transformed_df

        except Exception as e:
            logger.error(f"Error transforming data: {str(e)}")
            raise

    def generate_summary_stats(self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics from transformed data.

        Args:
            df (pd.DataFrame): Transformed dataframe

        Returns:
            Dict: Summary statistics
        """
        summary = {
            'date_range': {
                'start': df['Data'].min(),
                'end': df['Data'].max()
            },
            'total_entries': len(df),
            'total_income': df[df['Tipo'] == 'Entrada']['Valor'].sum(),
            'total_expenses': df[df['Tipo'] == 'Saída']['Valor'].sum(),
            'unique_groups': df['Grupo'].nunique(),
            'unique_categories': df['Categoria'].nunique()
        }

        return summary

def main():
    """Main function to execute the transformation process."""
    try:
        if len(sys.argv) != 2:
            print("Usage: python optimizer.py input.csv")
            sys.exit(1)

        input_file = sys.argv[1]
        output_file = input_file.replace('.csv', '_optimized.csv')

        transformer = FinancialDataTransformer()
        transformed_df = transformer.transform_data(input_file, output_file)
        summary = transformer.generate_summary_stats(transformed_df)

        logger.info("Transformation completed successfully!")
        logger.info(f"Summary Statistics: {summary}")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
