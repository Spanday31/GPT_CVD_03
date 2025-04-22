import streamlit as st
import math
from fpdf import FPDF

# ======================
# CVD Risk Calculation
# ======================

@st.cache_data
def calculate_risk(age, sex, sbp, total_chol, hdl, smoker, diabetes):
    sex_val = 1 if sex == "Male" else 0
    smoker_val = 1 if smoker else 0
    diabetes_val = 1 if diabetes else 0
    lp = (0.06 * age + 0.4 * sex_val + 0.02 * sbp + 0.3 * total_chol -
          0.2 * hdl + 0.5 * smoker_val + 0.5 * diabetes_val)
    risk = 1 - 0.9 ** math.exp(lp - 6)
    return round(risk * 100, 1)

# ======================
# PDF Report Generator
# ======================

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'CVD Risk Report', 0, 1, 'C')

def create_pdf(name, age, sex, risk):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Patient Name: {name}", 0, 1)
    pdf.cell(0, 10, f"Age: {age}    Sex: {sex}", 0, 1)
    pdf.cell(0, 10, f"Estimated 10-Year Risk: {risk}%", 0, 1)
    return pdf.output(dest='S').encode('latin1')

# ======================
# Streamlit UI
# ======================

st.set_page_config(page_title="CVD Risk Calculator", layout="centered")

st.title("CVD Risk Calculator")

name = st.text_input("Patient Name")
age = st.number_input("Age", 30, 100, 50)
sex = st.radio("Sex", ["Male", "Female"], horizontal=True)
sbp = st.number_input("Systolic BP (mmHg)", 90, 200, 130)
total_chol = st.number_input("Total Cholesterol (mmol/L)", 2.0, 10.0, 5.0)
hdl = st.number_input("HDL (mmol/L)", 0.5, 3.0, 1.2)
smoker = st.checkbox("Smoker")
diabetes = st.checkbox("Diabetes")

if st.button("Calculate Risk"):
    risk = calculate_risk(age, sex, sbp, total_chol, hdl, smoker, diabetes)
    st.success(f"Estimated 10-Year CVD Risk: {risk}%")

    if st.button("Download PDF Report"):
        pdf_bytes = create_pdf(name or "Unknown", age, sex, risk)
        st.download_button("Download Report", pdf_bytes, file_name=f"{name}_cvd_report.pdf", mime="application/pdf")
