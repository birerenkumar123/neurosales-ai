import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# NeuroSales AI: Data Analysis\n",
    "This notebook contains Exploratory Data Analysis (EDA) on the `sales_data.csv` to gain insights for the shopkeeper dashboard."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import plotly.express as px\n",
    "\n",
    "# Load the shop dataset\n",
    "df = pd.read_csv('../data/sales_data.csv')\n",
    "print(\"Dataset Shape:\", df.shape)\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Feature Engineering\n",
    "Convert date types and compute the overall transaction revenue based on item `price` & `quantity`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df['revenue'] = df['quantity'] * df['price']\n",
    "df['invoice_date'] = pd.to_datetime(df['invoice_date'], format=\"mixed\", dayfirst=True)\n",
    "display(df.describe())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Top Selling Categories"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "cat_rev = df.groupby(\"category\")[\"revenue\"].sum().reset_index().sort_values(by=\"revenue\", ascending=False)\n",
    "fig = px.bar(cat_rev, x=\"revenue\", y=\"category\", orientation='h', \n",
    "             title=\"Total Revenue by Category\", color=\"category\")\n",
    "fig.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Monthly Revenue Trends"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_trend = df.copy()\n",
    "df_trend['month_year'] = df_trend['invoice_date'].dt.to_period('M').astype(str)\n",
    "monthly_rev = df_trend.groupby(\"month_year\")[\"revenue\"].sum().reset_index()\n",
    "\n",
    "fig2 = px.line(monthly_rev, x=\"month_year\", y=\"revenue\", markers=True, title=\"Monthly Store Revenue\")\n",
    "fig2.show()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open('c:/ts/Neurosales_ai/notebooks/notebook.ipynb', 'w') as f:
    json.dump(notebook_content, f, indent=1)
