# Data Pipeline Project

Use this repository as a **template** for your data pipeline project. You will build a pipeline that takes raw NYC taxi trip records and turns them into a processed result. The project is open-ended: the brief sets the goal, and the structure, tools, and implementation choices are yours to make. Create pull requests in your own copy even if you are working alone, and use them to track your progress.

## Learning Objectives

By the end of this repository, you should be able to:

- Write a script that downloads a public dataset into a local staging directory.
- Build a pipeline that reads staged Parquet files and aggregates them into daily metrics.
- Separate a pipeline into distinct extract, transform, and load stages.
- Explain the difference between ETL and ELT, and justify which one your pipeline uses.
- Orchestrate a pipeline with Prefect (stretch goal).

## Project Brief

In this project you are going to build a data pipeline that processes the `Green Taxi Trips` portion of the [NYC Taxi Trip dataset](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

1. Write a script that downloads the data for the first three months of 2025 and stores it in a local staging directory.
2. Write an ETL or ELT pipeline that reads the locally staged files, processes the data, and calculates revenue per day.

Bonus task, if you have time:

1. Use Prefect for workflow orchestration.

### How to Approach It

**Step 1: Extract** (brief task 1) · Revisit: data ingestion

- List what the download needs: host, file name per month, months, target folder
- Build each file's link from those pieces
- Request each file and save it to your staging directory
- Decide what happens when you run it again

**Step 2: Explore** · Revisit: data quality (optional, prepares Step 3)

- Load one file, optionally in a notebook
- Find the columns you need: when the trip happened and what was paid
- Check them: data types, missing values, value ranges for dates and amounts
- Note what needs cleaning before you can add up revenue per day

**Step 3: Transform and load** (brief task 2) · Revisit: ETL vs. ELT, dbt : dbt is a open source software tool used to transfrom raw data directly inside the cloud data warehoue using simple SQL.

- Choose ETL or ELT: transform in Python before loading, or load raw data and transform in SQL using dbt 
- Read the staged files
- Clean based on what you found in Step 2
- Group by day and sum the revenue
- Write the result to your output location
- Compare row counts before and after cleaning

**Step 4: Orchestrate** (bonus) · Revisit: Prefect

- Get the plain pipeline running end to end first
- Turn each stage into a task and the whole run into a flow
- Add retries where things can fail

### Suggested Folder Structure

```text
<your-repo>/
├── data/
│   ├── raw/                  # Step 1: staged downloads, never edited
│   └── processed/            # Step 3: your daily revenue output
├── exploration/              # Step 2: scripts or notebooks, not part of the pipeline
├── src/
│   └── <package-name>/
│       ├── <stage modules>   # Steps 1 + 3: one per stage, e.g. extract / transform / load
│       ├── <entry point>     # Step 3: runs the stages in order
│       └── <flow>            # Step 4: the Prefect version
├── tests/                    # Step 3: at least one test for your transform
└── README.md                 # how to run it + answers to the review questions
```

(Files in `exploration/` are only for experimenting and exploring the data. The pipeline itself lives in `src/` and runs without them.)

## Learning Path

### Additional Folders and Files

| File / Folder | Description |
|---|---|
| [**solution**](solution/) | A complete local ETL implementation with its own README, scripts, package, and tests. |
| [**pyproject.toml**](pyproject.toml) | Project configuration and dependencies. |
| [**uv.lock**](uv.lock) | Dependency lock file. |

## Setup

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.13.5 or newer
and Python 3.13.17 or a newer 3.13 patch release, as defined in
[`.python-version`](.python-version).

> [!NOTE]
> Throughout these steps, text in angle brackets like `<repo-name>` is a **placeholder**. Replace it, including the `< >` brackets, with your own value. For example, `cd <repo-name>` becomes `cd mle-data-pipeline-project`.

### 1. Create the Repository from the Template

Click **Use this template** on GitHub.

When creating the repository:

- Set yourself as the **Owner**
- Choose a repository name
- Disable **Include all branches**
- Click **Create repository**

> [!IMPORTANT]
> If you are working in pairs or groups, only **one person** should complete this step.

---

### 2. Add Collaborators (Pairs/Groups Only)

If working with teammates:

1. Open the repository on GitHub
2. Go to **Settings → Collaborators**
3. Add your teammates as collaborators
4. Share the repository link with your team

Teammates should accept the invitation before continuing.

---

### 3. Clone the Repository

Copy the SSH URL from the **Code** button on GitHub, then run:

```bash
git clone <copied-ssh-url>
```

The copied SSH URL will look like `git@github.com:<your-username>/<repo-name>.git`.

---

### 4. Move into the Project Folder and Install Dependencies

This installs all dependencies and creates a virtual environment in `.venv/`.

```bash
cd <repo-name>
uv sync
```

---

### 5. Open the Repository in VS Code

> [!NOTE]
> Make sure you open VS Code from the project root so it automatically detects the environment created by `uv sync`.

Launch VS Code in the project root folder:

```bash
code .
```

If you create a notebook to explore the data, select the Python environment created by `uv sync` as the kernel.

## Reference Solution

This repository includes a complete local reference implementation in [solution/](solution/).
Use it to compare implementation choices and expected outputs. It is one way to solve the project, not the required structure for yours.

See [solution/README.md](solution/README.md) for how to run it and how its files fit together.

## Answer the Following Questions

1. What are the steps you took to complete the project?
2. What challenges did you face?
3. What would you do differently if you had more time?

## My Solution

### How to Run

```bash
uv sync                                      # install dependencies + this package
uv run python -m taxi_pipeline.extract       # Step 1: download Jan–Mar 2025 into data/raw/
uv run python exploration/explore.py         # Step 2: inspect the data (optional)
uv run python -m taxi_pipeline.pipeline      # Step 3: full ETL -> data/processed/daily_revenue.{parquet,csv}
uv run pytest                                # tests for the transform
uv run python -m taxi_pipeline.flow          # Step 4: same pipeline as a Prefect flow
```

| File | Stage |
|---|---|
| `src/taxi_pipeline/config.py` | URLs, months, and folder paths |
| `src/taxi_pipeline/extract.py` | **E**: download each month, skip files already present |
| `src/taxi_pipeline/transform.py` | **T**: read, clean, group by day, sum revenue |
| `src/taxi_pipeline/load.py` | **L**: write Parquet + CSV |
| `src/taxi_pipeline/pipeline.py` | runs E → T → L and prints row counts |
| `src/taxi_pipeline/flow.py` | Prefect version with retries on the download |

### ETL or ELT?

This pipeline is **ETL**: the data is transformed in Python (pandas) *before* it is loaded to `data/processed/`.
The dataset is small (~146k rows), fits in memory, and there is no warehouse, so loading raw data
somewhere first and transforming with SQL/dbt (ELT) would add tooling without benefit.

### Cleaning Rules (from exploration)

| Issue found | Rule |
|---|---|
| Pickups outside the window (e.g. 2024-12-25 in the January file) | keep only 2025-01-01 ≤ pickup < 2025-04-01 |
| Negative `total_amount` (refunds/voids, min −$114) | drop rows with amount < 0 |
| Possible missing pickup time or amount | drop those rows |

Result: 146,486 rows read → 145,997 kept (489 dropped, 0.33%) → 90 daily rows, total revenue $3,401,753.17.

## Answers

1. **Steps:** Downloaded the three monthly Parquet files with an idempotent script; explored January to find the
   date and amount columns and their problems; wrote an ETL pipeline split into extract/transform/load modules;
   added unit tests for the cleaning and aggregation; wrapped the stages in a Prefect flow with retries.
2. **Challenges:** Each monthly file contains some trips from other months, so filtering per file would be wrong –
   the filter must use the whole 3-month window. Deciding what counts as "revenue" (negative amounts are refunds).
3. **With more time:** Add data-quality checks that fail the run (e.g. expected number of days), try an ELT version
   with DuckDB + dbt, and schedule the Prefect flow to pick up new months automatically.
