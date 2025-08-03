===========================================
MeteoFlow: Weather Data Pipeline
===========================================

An ELT (Extract-Load-Transform) pipeline that retrieves historical daily temperature data from the Open-Meteo API, loads it into a DuckDB database, and optionally exports it to a `.parquet` file for analysis in tools like Power BI.

This project is ideal for climate analysts, researchers, and data scientists investigating weather trends around the world and comparing recent years with past decades.

-------------------
🌟 Project Features
-------------------

- Extracts weather data (min/max temperatures) using city name and year
- Automatically geocodes cities using Open-Meteo's geocoding API
- Loads data into DuckDB
- Exports all collected data as a Parquet file for analysis
- CLI-powered: simple and scriptable
- Minimal setup required

----------------------
📦 Installation & Setup
----------------------

This project uses [`uv`](https://github.com/astral-sh/uv) for managing Python dependencies.

1. **Install `uv` (only once):**

   .. code-block:: bash

      pip install uv

2. **Create a virtual environment:**

   .. code-block:: bash

      uv venv

3. **Activate the virtual environment:**

   .. code-block:: bash

      # On Windows:

      .venv\Scripts\activate

      # On macOS/Linux:

      source .venv/bin/activate

4. **Install dependencies from `pyproject.toml`:**

   .. code-block:: bash

      uv pip install -r pyproject.toml

-------------------------------
🛠 How to Run the Data Pipeline
-------------------------------

Use the CLI to extract weather data for any city and year.

**Extract + Load (to DB):**

.. code-block:: bash

   python . get <city> <year>

Exampl

.. code-block:: bash

   python . get Lisbon 2024

This:

- Geocodes the city
- Extracts daily weather data for all months in that year
- Loads the results into `data/weather.duckdb`

If data for that city/year already exists in the database, it will be skipped.

-------------------------------
📤 Exporting Data to Parquet
-------------------------------

Once you’ve collected data for all the cities and years you want:

.. code-block:: bash

   python . export

This exports all contents of the DuckDB database to:

data/export/weather.parquet


You can now load this file directly into Power BI or any other analysis tool that supports Parquet format.

-------------------
📝 License & Credits
-------------------

- License: MIT
- Created with `Cookiecutter` and the `audreyr/cookiecutter-pypackage` template

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
