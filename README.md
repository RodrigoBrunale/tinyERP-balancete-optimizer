# TinyERP Balancete Optimizer

## About
This tool is designed to transform balance sheet ('balancete') data exported from Tiny ERP into an optimized format for data visualization in Google Looker Studio. It handles specific formatting and structure requirements of Tiny ERP exports, making it easier to create comprehensive financial dashboards and reports.

## Key Features
- 🔄 Transforms Tiny ERP balance sheet exports from wide to long format
- 📅 Handles Brazilian date formatting (e.g., "Jun/23" to "2023-06-01")
- 📊 Maintains financial data hierarchies (Tipo, Grupo, Categoria)
- 🔢 Preserves financial data precision
- 🌎 Supports Brazilian Portuguese localization
- ✅ Validates input data structure
- 📈 Generates data summary statistics

## Prerequisites
- Python 3.8 or higher
- Required packages: pandas, numpy

## Installation

```bash
# Clone the repository
git clone https://github.com/RodrigoBrunale/tinyERP-balancete-optimizer.git

# Navigate to project directory
cd tinyERP-balancete-optimizer

# Install required packages
pip install pandas numpy
```

## Usage

### Input Format
The tool expects a CSV export from Tiny ERP's balance sheet report with the following structure:
```csv
Tipo,Grupo,Categoria,Jun/23,Jul/23,...,Total
Entrada,Group1,Cat1,100.00,200.00,...,1000.00
Saída,Group2,Cat2,50.00,75.00,...,500.00
```

### Running the Tool
```bash
python optimizer.py input.csv
```
This will generate `input_optimized.csv` in the same directory.

### Output Format
The tool generates a CSV file optimized for Google Looker Studio with the following structure:
```csv
Data,Ano,Mes,Mes_Nome,Tipo,Grupo,Categoria,Valor
2023-06-01,2023,6,Junho,Entrada,Group1,Cat1,100.00
2023-07-01,2023,7,Julho,Entrada,Group1,Cat1,200.00
```

## Google Looker Studio Integration
The transformed data is ready to be imported into Google Looker Studio for:
- Time series analysis
- Category breakdowns
- Financial performance dashboards
- Comparative analysis
- Budget tracking

## Project Structure
```
tinyERP-balancete-optimizer/
├── optimizer.py            # Main transformation script
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
Rodrigo Brunale
- GitHub: [RodrigoBrunale](https://github.com/RodrigoBrunale)
- Email: rodrigo@brunale.com

## Acknowledgments
- [Tiny ERP](https://tiny.com.br/) - Source system for balance sheet data
- Google Looker Studio - Target platform for data visualization
