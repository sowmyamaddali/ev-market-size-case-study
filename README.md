# Electric Vehicle Population Data Analysis
This project explores and prepares the **Electric Vehicles Population Data** for a potential end-to-end data science pipeline, including data cleaning, imputation, and future modeling or dashboarding.

---

## Dataset Overview
- **Source:** [Electric Vehicle Population Data](data/Electric_Vehicle_Population_Data.csv)
- **Format:** CSV
- **Total Rows:** 177,866
- **Features:** Vehicle make, model, electric range, city, postal code, legislative district, and more.

---

## Project Goals
- Clean and prepare the dataset for analysis or machine learning.
- Resolve missing values in critical columns such as `legislative_district`.
- Explore EV adoption trends based on vehicle type, geography, and other features.
- Deploy the full pipeline to GitHub as a reproducible data project.

---

## Data Cleaning Summary

The dataset was cleaned using an industry-standard, step-by-step approach:

- **Column names** were standardized (lowercase, underscores) for consistent referencing.
- **Missing values** were handled thoughtfully:
  - `legislative_district` was imputed using ZIP code and city-based fallback logic (only when 1-to-1 mapping was possible).
  - Remaining NaNs in geographic or utility-related columns were dropped (only 9 rows affected).
- **Zero values in `base_msrp`** were identified as placeholders for missing data; about ~98% of entries had `base_msrp = 0`, so this field was used with caution.
- Data types were converted where appropriate (e.g., postal codes and census tracts to strings).
- Duplicate VIN checks were performed to ensure uniqueness where needed.

Cleaned data was saved for downstream exploration and modeling.

---

## Data Exploration & Insights

A thorough univariate and bivariate exploratory data analysis (EDA) was conducted.

### Univariate Insights
- **Model Year**: Rapid growth in EV adoption post-2017, with a spike in 2023.
- **EV Make**: Tesla dominates the dataset, followed by Nissan and Chevrolet.
- **Vehicle Type**: BEVs far outnumber PHEVs (~80% of entries).
- **Electric Range**: Right-skewed distribution; most vehicles < 50 miles (due to PHEVs), with BEVs reaching up to 350 miles.
- **Base MSRP**: Most MSRP values were missing (0), limiting this feature’s usefulness.

### Bivariate Insights
- **Electric Range vs Base MSRP**: Positive trend for BEVs — higher-priced cars offer more range; PHEVs cluster in low-range, low-price segment.
- **Range by Vehicle Type**: BEVs offer much higher and more variable range; PHEVs are tightly grouped under 50 miles.
- **Range by Model Year**: EV range improves significantly post-2016, peaking in 2023.
- **Vehicle Type by County**: BEVs dominate in every top county, especially King County.
- **Vehicle Type Over Time**: Shift from PHEVs (pre-2016) to BEVs (post-2017), with BEVs sharply rising in 2023.

### Regional & Temporal Trends
- **Regional**: Urban counties (like King, Snohomish) show significantly higher BEV adoption.
- **Temporal**: Model years reflect clear technology growth and market preference shifts toward BEVs.

---

## Modeling

The goal was to classify electric vehicles into -
- **Battery Electric Vehicle (BEV)** or
- **Plug-in Hybrid Electric Vehicle (PHEV)**

### Models Used:
- **Logistic Regression** (with class weights to address imbalance)
- **Random Forest Classifier** (with class weights and tuned for interpretability)

### Feature Selection:
Models were trained using a minimal, interpretable feature set:
- `model_year`
- `electric_range`

The `make` and `model` features were excluded to avoid overfitting and ensure the model could generalize beyond brand identity.

### Results:

| Model              | Accuracy | F1 Score (PHEV) | F1 Score (BEV) |
|--------------------|----------|------------------|----------------|
| Logistic Regression| 86.7%    | 0.76             | 0.91           |
| Random Forest      | 99.99%   | 1.00             | 1.00           |

Although the Random Forest model achieved near-perfect performance, this is supported by the feature distribution: a boxplot of `electric_range` shows clear separation between BEVs and PHEVs. The model learned from this strong signal, not from data leakage.

### Final Model:
The Random Forest model was saved and will be used in the Streamlit app for real-time prediction.
