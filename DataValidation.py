import great_expectations as gx
import pandas

context = gx.get_context()

data_source_name = "my_data_source"
data_asset_name = "my_dataframe_data_asset"
batch_definition_name = "my_batch_definition"

my_batch_definition = (
    context.data_sources.get(data_source_name)
    .get_asset(data_asset_name)
    .get_batch_definition(batch_definition_name)
)



csv_path = "./folder_with_data/raw.csv"
dataframe = pandas.read_csv(csv_path)

batch_parameters = {"dataframe": dataframe}

batch = my_batch_definition.get_batch(batch_parameters=batch_parameters)

suite = gx.ExpectationSuite(name = 'churnValidation')

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column='CustomerID')
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column='CustomerID'),
)

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column='Age'),
)

suite.add_expectation(
     gx.expectations.ExpectColumnValuesToBeBetween(
    column="Age", max_value=100, min_value=18
)
)

suite.add_expectation(
     gx.expectations.ExpectColumnValuesToBeInSet(column="Gender",value_set=["Male","Female"])
)

suite.add_expectation(
     gx.expectations.ExpectColumnValuesToBeInSet(column="Churn",value_set=[1,0])
)

validation_results = batch.validate(suite)
print(validation_results)