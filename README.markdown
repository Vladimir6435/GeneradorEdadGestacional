# Gestational Age Calculator

## Overview
This Python application calculates the gestational age of a pregnancy and generates key milestone dates based on various input methods. It supports four methods to calculate gestational age and provides a schedule of important pregnancy milestones, including laboratory tests, screenings, and check-ups. The application is built with Streamlit for a user-friendly web interface.

## Features
- Calculate gestational age using one of four methods:
  1. **Last Menstrual Period (LMP)**: Input the date of the last menstrual period.
  2. **Previous Ultrasound**: Input the date and gestational age from a prior ultrasound.
  3. **Estimated Due Date (EDD)**: Input the expected delivery date.
  4. **Manual Entry**: Directly input the current gestational age in weeks and days.
- Generate a chronological list of key pregnancy milestones with specific dates or date ranges, including:
  - Week 11: First trimester labs (PaPP-a, HCG Free, PLGF, TSH, T4L, T3L).
  - Weeks 12 to 13+6: First trimester screening.
  - Weeks 22 to 24+6: Anatomic and congenital heart defect screening.
  - Weeks 34 to 35+6: Fetal growth control.
  - Week 37: Exact date with day of the week.
  - Week 39: Exact date with day of the week.
  - Week 40: Estimated due date with day of the week.
  - Week 41: Exact date.
- Validates inputs to ensure reasonable gestational ages and correct date formats (DD/MM/YYYY).
- Provides error messages for invalid inputs or implausible gestational ages.
- Elegant web interface powered by Streamlit for easy interaction.

## Requirements
- Python 3.8 or higher
- Streamlit (`pip install streamlit`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gestational-age-calculator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd gestational-age-calculator
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Local Execution
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and go to `http://localhost:8501`.
3. Select a calculation method from the dropdown menu and provide the required inputs (dates in DD/MM/YYYY format, weeks/days as integers).
4. Click the "Calcular" button to view the gestational age, estimated due date, and milestone dates.

### Example Output
Upon selecting "Last Menstrual Period" and entering `01/01/2025`:
```
Edad gestacional: 30 semanas y 1 días
Fecha probable de parto: 08/10/2025

Fechas de hitos en orden cronológico:
1. Edad gestacional semana 11: ya se superó esta edad gestacional
2. Edad gestacional semana 12 a semana 13 y 6 días: ya se superó esta edad gestacional
3. Edad gestacional semana 22 a semana 24 y 6 días: ya se superó esta edad gestacional
4. Edad gestacional semana 34 a 35 semanas y 6 días: desde 28/08/2025 hasta 18/09/2025 Control de crecimiento fetal
5. Edad gestacional semana 37: 03/10/2025 que es viernes
6. Edad gestacional semana 39: 17/10/2025 que es viernes
7. Edad gestacional semana 40: 24/10/2025 que es viernes anotar fecha probable de parto
8. Edad gestacional semana 41: 31/10/2025
```

## Deployment on Streamlit Cloud
1. Push the repository to GitHub (see instructions below).
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud) with your GitHub account.
3. Click "New app" and select your repository.
4. Specify `app.py` as the main file and ensure `requirements.txt` is included.
5. Deploy the app. Once deployed, you'll get a public URL to share.

## File Structure
- `app.py`: The main Streamlit application containing the gestational age calculation logic and milestone generation.
- `requirements.txt`: Lists the dependencies (Streamlit).
- `README.md`: This file, providing an overview and usage instructions.

## Notes
- All dates must be entered in the format `DD/MM/YYYY`.
- Weeks and days for gestational age inputs must be integers, with days ranging from 0 to 6.
- The application assumes a standard 40-week (280-day) pregnancy for calculating the estimated due date.
- Milestones are only displayed if they are in the future based on the current gestational age; otherwise, a message indicates that the milestone has been surpassed.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that any new features or modifications include appropriate tests and documentation.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.