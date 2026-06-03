# Employee Attrition Analysis Dashboard

## Overview

This project analyzes employee attrition patterns using HR workforce data to identify the key factors influencing employee turnover. The objective is to uncover actionable insights that can help organizations improve employee retention, reduce turnover costs, and enhance workforce satisfaction.

The analysis combines exploratory data analysis (EDA), statistical investigation, and interactive visualizations built with Python and Plotly.

---

## Business Problem

Employee attrition is a major challenge for organizations due to its impact on:

* Recruitment and onboarding costs
* Productivity and operational efficiency
* Employee morale and engagement
* Organizational knowledge retention

This project aims to answer the following questions:

* Which employee groups are most likely to leave?
* What factors are associated with higher attrition?
* Which retention strategies should management prioritize?
* How can data-driven decisions improve employee retention?

---

## Dataset Information

The dataset contains **74,498 employee records** and **24 features** describing employee demographics, job characteristics, compensation, workplace experience, and attrition status.

### Target Variable

| Variable  | Description                                              |
| --------- | -------------------------------------------------------- |
| Attrition | Indicates whether an employee stayed or left the company |

### Key Features

* Age
* Gender
* Job Role
* Job Level
* Monthly Income
* Work-Life Balance
* Job Satisfaction
* Performance Rating
* Number of Promotions
* Overtime
* Remote Work
* Leadership Opportunities
* Company Reputation
* Employee Recognition
* Distance from Home
* Marital Status
* Education Level

---

## Data Preparation

The following preprocessing steps were performed:

* Data type validation
* Ordinal feature encoding using ordered categorical variables
* Missing value assessment
* Feature categorization
* Data quality checks
* Exploratory statistical analysis

---

## Exploratory Data Analysis

The EDA focused on identifying relationships between employee attrition and key workforce factors.

### Areas Investigated

* Gender vs Attrition
* Marital Status vs Attrition
* Job Role vs Attrition
* Job Level vs Attrition
* Monthly Income vs Attrition
* Promotions vs Attrition
* Work-Life Balance vs Attrition
* Job Satisfaction vs Attrition
* Overtime vs Attrition
* Remote Work vs Attrition
* Company Reputation vs Attrition
* Employee Recognition vs Attrition
* Leadership Opportunities vs Attrition
* Distance from Home vs Attrition

---

## Key Findings

### 1. Remote Work is the Strongest Retention Factor

Employees with remote work options showed significantly lower attrition rates compared to employees working fully on-site.

**Recommendation:** Expand remote and hybrid work arrangements where operationally feasible.

---

### 2. Job Level Strongly Influences Attrition

Entry-level employees experienced the highest attrition rates, while senior-level employees demonstrated the strongest retention.

**Recommendation:** Improve career progression pathways and mentorship programs.

---

### 3. Work-Life Balance Drives Employee Retention

Employees reporting poor work-life balance were considerably more likely to leave the organization.

**Recommendation:** Reduce burnout, manage workloads effectively, and encourage flexible working arrangements.

---

### 4. Company Reputation Matters

Employees who perceived the company's reputation negatively exhibited higher attrition rates.

**Recommendation:** Strengthen employer branding, transparency, and internal communication.

---

### 5. Overtime Contributes to Employee Turnover

Employees working overtime displayed higher attrition compared to employees without overtime obligations.

**Recommendation:** Monitor workload distribution and implement burnout prevention strategies.

---

## Factors with Limited Impact

The following variables showed relatively weak relationships with attrition:

* Monthly Income
* Job Role
* Employee Recognition
* Education Level (except PhD holders)
* Leadership Opportunities

These variables may contribute indirectly but were not primary drivers of employee turnover in this dataset.

---

## Dashboard Features

The interactive dashboard includes:

* Attrition Overview KPIs
* Attrition by Job Level
* Attrition by Work-Life Balance
* Attrition by Remote Work Status
* Attrition by Marital Status
* Attrition by Company Reputation
* Attrition by Overtime
* Attrition by Promotions
* Employee Demographic Analysis

---

## Tools & Technologies

### Programming Language

* Python

### Libraries

* Pandas
* NumPy
* Plotly Express
* Plotly Graph Objects
* Matplotlib

### Development Environment

* Jupyter Notebook
* Google Colab

---

## Business Recommendations

Based on the analysis, management should prioritize:

1. Expanding Remote and Hybrid Work Policies
2. Improving Work-Life Balance Initiatives
3. Enhancing Career Growth and Promotion Opportunities
4. Reducing Excessive Overtime
5. Strengthening Company Reputation and Employee Engagement

These initiatives are expected to have the greatest impact on reducing employee attrition and improving workforce retention.

---

## Conclusion

The analysis revealed that employee attrition is influenced more by workplace flexibility, career progression, and employee experience than by salary or department. By focusing on the strongest drivers of turnover, organizations can implement targeted retention strategies that improve employee satisfaction and reduce workforce churn.
