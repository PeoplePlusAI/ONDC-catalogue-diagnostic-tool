# ONDC-catalogue-diagnostic-tool

Different buyer apps have different requirements and format for catalogue. We are building a tool to analyse a seller catalogue and create a report on, to which buyer apps the current catalogue is compatible. 

Requirements for each buyer app are mentioned [here](https://resources.ondc.org/disclosures) under minimum standards for displaying search results to buyers.

On a later stage the tool should generate multiple catalogue versions for each buyer app. 

Say for example if one buyer app requires short and long description about products and if the current catalogue has only long description, use the available information to generate short and long description.

## How to run the POC

1. Clone the repo
2. Install the dependencies using `pip install -r requirements.txt`
3. Create `.env` file inside ops directory and pu the following variables
```
OPENAI_API_KEY=<your openai api key>
```
4. Run the app using `python main.py`
5. Open the browser and go to `http://127.0.0.1:7860`
6. Upload the catalogue file, requirementws and click on `Submit`
7. You will see the results in the browser



